#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enhanced UBO Web Application (English output only)."""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import sys
import re
from datetime import datetime
import logging
from typing import Any, Dict, List, Optional, Set
import networkx as nx

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables

# Import Final UBO System
from final_ubo_system import analyze_company_ubo

# Import Mock Data Generator
from mock_data_generator import generate_mock_ubo_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global UBO System instance placeholder (not required for new system)
ubo_system = None


def _extract_ubo_name_set(ubo_entries):
    """Collect name strings for identified UBOs (>=15%)."""
    names = set()
    if not ubo_entries:
        return names
    for entry in ubo_entries:
        if hasattr(entry, '__dict__'):
            total = getattr(entry, 'total_percentage', 0) or 0
            name = getattr(entry, 'name', '')
            if total >= 15.0 and name:
                names.add(str(name))
        elif isinstance(entry, dict):
            name = entry.get('name')
            status = entry.get('ubo_status')
            total = entry.get('total_percentage', 0) or 0
            if name and (status == 'YES' or total >= 15.0):
                names.add(str(name))
    return names


def _format_display_label(name: Optional[str], regis_id: Optional[str]) -> str:
    label = (name or '').strip()
    regis = (regis_id or '').strip()
    if regis:
        if label:
            return label if regis in label else f"{label} ({regis})"
        return regis
    return label or 'Unknown'


def extract_names_from_signatory(signatory_text: str) -> List[str]:
    """Extract person names from officialSignatory text.
    
    Example inputs: 
    "นายปราโมทย์ ปาทาน ลงลายมือชื่อร่วมกับนายชลากรณ์ ปัญญาโฉม หรือ นายสุรการ ศิริโมทย์..."
    "พลเอกสมชาย ธนะรัชต์นายสมพร สืบถวิลกุล นางสาวจรูญศรี วันเกิดผล..." - titles stuck together
    "นายชุมพล ณ ลำเลียง" - names with "ณ" prefix in surname
    
    Returns: List of names like ["นายปราโมทย์ ปาทาน", "นายชลากรณ์ ปัญญาโฉม", ...]
    """
    if not signatory_text:
        return []
    
    names = []
    text = signatory_text.strip()
    
    # ========== COMPREHENSIVE TITLE PATTERNS ==========
    # Thai military ranks and honorific titles
    military_titles = r'(?:พลเอก|พลโท|พลตรี|พลตำรวจ(?:เอก|โท|ตรี)?|พล\.?(?:อ\.?|ท\.?|ต\.?)?)'
    academic_titles = r'(?:ดร\.?|ศ\.?(?:ดร\.?)?|รศ\.?(?:ดร\.?)?|ผศ\.?(?:ดร\.?)?)'
    noble_titles = r'(?:ม\.ล\.?|ม\.ร\.ว\.?|หม่อม(?:ราชวงศ์|หลวง)?)'
    common_titles = r'(?:นาย|นาง(?:สาว)?|คุณ)'
    
    # Combined title pattern - military first (longer), then academic, noble, common
    title_pattern = rf'(?:{military_titles}|{academic_titles}|{noble_titles}|{common_titles})'
    
    # ========== PREPROCESSING: Insert spaces before titles ==========
    # This handles cases like "ธนะรัชต์นายสมพร" -> "ธนะรัชต์ นายสมพร"
    processed_text = text
    # Insert space before any title that's stuck to preceding Thai text
    processed_text = re.sub(rf'([\u0E00-\u0E7F])({title_pattern})', r'\1 \2', processed_text)
    
    # ========== KEYWORDS AND VALIDATION ==========
    # Keywords that indicate text is NOT a name
    invalid_keywords = ['ลงลายมือ', 'ร่วมกัน', 'ข้อจำกัด', 'กรรมการ', 'ประทับ', 'ตรา', 'สำคัญ', 
                       'ของบริษัท', 'อำนาจ', 'ไม่มี', 'รวมเป็น', 'คน', 'หนึ่ง', 'สอง', 'สาม', 
                       'สี่', 'ห้า', 'หก', 'เจ็ด', 'แปด', 'เก้า', 'สิบ']
    
    # Trailing keywords that should be removed from lastname
    trailing_keywords = ['ลงลายมือ', 'ร่วมกัน', 'ข้อจำกัด', 'กรรมการ', 'ประทับ', 'รวมเป็น',
                        'หนึ่ง', 'สอง', 'สาม', 'สี่', 'ห้า', 'หก', 'ใน']
    
    def is_valid_name(name: str) -> bool:
        """Check if extracted name is valid."""
        if not name or len(name) < 5:
            return False
        for keyword in invalid_keywords:
            if keyword in name:
                return False
        return True
    
    def clean_lastname(lastname: str) -> str:
        """Remove trailing keywords from lastname."""
        result = lastname
        for keyword in trailing_keywords:
            idx = result.find(keyword)
            if idx > 0:
                result = result[:idx].strip()
        return result
    
    # ========== EXTRACT NAMES FROM PREPROCESSED TEXT ==========
    
    # Pattern for names with "ณ" in surname (e.g., นายชุมพล ณ ลำเลียง)
    pattern_na = rf'({title_pattern})([\u0E00-\u0E7F\-]+)\s+(ณ\s+[\u0E00-\u0E7F\-]+)'
    for match in re.finditer(pattern_na, processed_text):
        title = match.group(1)
        firstname = match.group(2)
        lastname = clean_lastname(match.group(3))
        full_name = f"{title}{firstname} {lastname}".strip()
        if is_valid_name(full_name):
            names.append(full_name)
    
    # Pattern for standard names (title + firstname + lastname)
    pattern_std = rf'({title_pattern})([\u0E00-\u0E7F]+)\s+([\u0E00-\u0E7F]+)'
    for match in re.finditer(pattern_std, processed_text):
        title = match.group(1)
        firstname = match.group(2)
        lastname = match.group(3)
        
        # Skip if lastname starts with ณ (already captured above)
        if lastname.startswith('ณ'):
            continue
        
        # Clean lastname - remove trailing keywords
        lastname = clean_lastname(lastname)
        
        # Skip very short lastnames (probably captured wrong)
        if len(lastname) < 2:
            continue
        
        # Skip if firstname contains another title (indicates wrong parsing)
        if re.search(title_pattern, firstname):
            continue
            
        full_name = f"{title}{firstname} {lastname}".strip()
        if is_valid_name(full_name):
            names.append(full_name)
    
    # ========== Remove duplicates while preserving order ==========
    seen = set()
    unique_names = []
    for name in names:
        # Normalize: remove spaces and Thai tone marks for comparison
        normalized = re.sub(r'[\s\u0E31\u0E34-\u0E3A\u0E47-\u0E4E]', '', name).lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_names.append(name)
    
    return unique_names


def normalize_name_for_matching(name: str) -> str:
    """Remove title and normalize name for matching."""
    titles = ['นาย', 'นาง', 'นางสาว', 'ดร.', 'ดร', 'ศ.', 'รศ.', 'ผศ.', 'Mr.', 'Mrs.', 'Ms.', 'Dr.']
    normalized = name.strip()
    for title in titles:
        if normalized.startswith(title):
            normalized = normalized[len(title):].strip()
            break
    return normalized.replace(' ', '').lower()


def build_directors_signatories_table(directors: List[Dict], signatory_names: List[str]) -> List[Dict]:
    """Build a combined table of directors and signatories with role classification.
    
    Directors: title + firstname + lastname (e.g., "นายพิชัย จิราธิวัฒน์")
    Signatory: Already has title (e.g., "นายพิชัย จิราธิวัฒน์")
    
    Returns list of dicts with: name, is_signatory, is_director
    """
    # Build director data with TITLE included
    director_data = []
    for d in directors:
        title = d.get('title', '').strip()
        firstname = d.get('firstname', '').strip()
        lastname = d.get('lastname', '').strip()
        full_name = f"{title}{firstname} {lastname}".strip()
        if full_name:
            director_data.append({
                'full_name': full_name,
                'normalized': normalize_name_for_matching(full_name)
            })
    
    # Build signatory data
    signatory_data = []
    for name in signatory_names:
        signatory_data.append({
            'full_name': name,
            'normalized': normalize_name_for_matching(name)
        })
    
    # Combined results
    combined = {}
    matched_directors = set()
    matched_signatories = set()
    
    # First pass: Exact normalized match
    for sig_idx, sig in enumerate(signatory_data):
        for dir_idx, dir_d in enumerate(director_data):
            if sig['normalized'] == dir_d['normalized']:
                combined[dir_d['full_name']] = {
                    'name': dir_d['full_name'],
                    'is_signatory': True,
                    'is_director': True
                }
                matched_directors.add(dir_idx)
                matched_signatories.add(sig_idx)
                break
    
    # Second pass: Fuzzy match (partial name match)
    for sig_idx, sig in enumerate(signatory_data):
        if sig_idx in matched_signatories:
            continue
        sig_norm = sig['normalized']
        for dir_idx, dir_d in enumerate(director_data):
            if dir_idx in matched_directors:
                continue
            dir_norm = dir_d['normalized']
            if len(sig_norm) > 3 and len(dir_norm) > 3:
                if sig_norm in dir_norm or dir_norm in sig_norm:
                    combined[dir_d['full_name']] = {
                        'name': dir_d['full_name'],
                        'is_signatory': True,
                        'is_director': True
                    }
                    matched_directors.add(dir_idx)
                    matched_signatories.add(sig_idx)
                    break
    
    # Add unmatched signatories
    for sig_idx, sig in enumerate(signatory_data):
        if sig_idx not in matched_signatories:
            combined[sig['full_name']] = {
                'name': sig['full_name'],
                'is_signatory': True,
                'is_director': False
            }
    
    # Add unmatched directors
    for dir_idx, dir_d in enumerate(director_data):
        if dir_idx not in matched_directors:
            combined[dir_d['full_name']] = {
                'name': dir_d['full_name'],
                'is_signatory': False,
                'is_director': True
            }
    
    # Sort: both roles first, then signatories, then directors, then by name
    result = list(combined.values())
    result.sort(key=lambda x: (
        -int(x['is_signatory'] and x['is_director']),
        -x['is_signatory'],
        -x['is_director'],
        x['name']
    ))
    
    return result


def build_network_graph(root_id: str, hierarchy: Dict[str, Any], ubo_names: set) -> Dict[str, Any]:
    """Build NetworkX graph structure for interactive spider-web visualization.
    
    Returns:
        Dict with 'nodes' and 'edges' for D3.js force-directed graph
    """
    if not hierarchy or root_id not in hierarchy:
        return {'nodes': [], 'edges': []}
    
    G = nx.DiGraph()
    visited = set()
    
    def add_nodes_edges(node_id: str, level: int = 0):
        if node_id in visited or node_id not in hierarchy:
            return
        visited.add(node_id)
        
        node_data = hierarchy[node_id]
        name = node_data.get('display_name') or node_data.get('name_en') or node_id
        node_type = 'company' if level == 0 else 'company'
        
        # Parse capital (ทุนจดทะเบียน) for node size
        capital_str = str(node_data.get('capital', '0'))
        try:
            capital = float(capital_str.replace(',', '').replace('฿', '').replace('THB', '').strip())
        except:
            capital = 0
        
        # Add node
        G.add_node(node_id, 
                   name=name[:30],  # Truncate for display
                   full_name=name,
                   type=node_type,
                   level=level,
                   capital=capital,
                   is_ubo=name in ubo_names,
                   regis_id=node_data.get('company_id', node_id))
        
        # Add edges for shareholders
        shareholders = node_data.get('shareholders', [])
        for sh in shareholders:
            sh_type = sh.get('shareholder_type', 'personal')
            sh_name = sh.get('display_name', '')
            sh_regis_id = sh.get('regis_id', '') or sh.get('regis_id_held_by', '')
            direct_percent = float(sh.get('direct_percent', 0) or sh.get('percent', 0))
            
            # Create unique child_id
            if sh_type == 'company' and sh_regis_id:
                child_id = sh_regis_id
                child_node_type = 'company'
            else:
                child_id = f"person_{sh_name}_{node_id}"
                child_node_type = 'personal'
            
            # Add child node if not exists
            if not G.has_node(child_id):
                G.add_node(child_id,
                          name=sh_name[:30],
                          full_name=sh_name,
                          type=child_node_type,
                          level=level + 1,
                          capital=0,
                          is_ubo=sh_name in ubo_names,
                          regis_id=sh_regis_id or '')
            
            # Add edge (direction: parent -> child, แสดงว่า parent ถือหุ้นใน child)
            # แต่ตามความหมายจริง คือ child ถือหุ้นใน parent
            # ให้ใช้ child -> parent เพื่อแสดงทิศทางการถือหุ้น
            G.add_edge(child_id, node_id, weight=direct_percent, percent=direct_percent)
            
            # Recursively add corporate shareholders
            if sh_type == 'company' and sh_regis_id and sh_regis_id in hierarchy:
                add_nodes_edges(sh_regis_id, level + 1)
    
    add_nodes_edges(root_id, 0)
    
    # Convert to JSON format for D3.js
    nodes = []
    for node_id, attrs in G.nodes(data=True):
        nodes.append({
            'id': node_id,
            'name': attrs['name'],
            'full_name': attrs['full_name'],
            'type': attrs['type'],
            'level': attrs['level'],
            'capital': attrs['capital'],
            'is_ubo': attrs['is_ubo'],
            'regis_id': attrs['regis_id']
        })
    
    edges = []
    for source, target, attrs in G.edges(data=True):
        edges.append({
            'source': source,
            'target': target,
            'percent': attrs['percent']
        })
    
    return {'nodes': nodes, 'edges': edges}

def build_tree_structure(root_id: str, hierarchy: Dict[str, Any], ubo_names: set) -> Optional[Dict[str, Any]]:
    """Build a hierarchy tree suitable for D3 rendering."""
    if not hierarchy or root_id not in hierarchy:
        return None

    visited = set()

    def _build_node(node_id: str, level: int = 0, effective: float = 100.0, direct: float = 100.0) -> Optional[Dict[str, Any]]:
        node_data = hierarchy.get(node_id, {})
        name = node_data.get('display_name') or node_data.get('name_en') or node_id
        company_id = node_data.get('company_id')
        try:
            effective_value = float(effective if effective is not None else node_data.get('parent_percentage', 0) or 0)
        except (TypeError, ValueError):
            effective_value = 0.0
        try:
            direct_value = float(direct if direct is not None else node_data.get('direct_percent', effective_value) or 0)
        except (TypeError, ValueError):
            direct_value = effective_value

        node = {
            'id': node_id,
            'name': _format_display_label(name, company_id),
            'type': 'company',
            'level': level,
            'effective_percent': round(effective_value, 4),
            'direct_percent': round(direct_value, 4),
            'isUbo': name in ubo_names or node_id in ubo_names,
            'children': []
        }

        if node_id in visited:
            node['name'] = f"{name} (already shown)"
            node['effective_percent'] = round(effective_value, 4)
            node['direct_percent'] = round(direct_value, 4)
            return node

        visited.add(node_id)
        shareholders = node_data.get('shareholders', [])
        for sh in shareholders:
            child_name = sh.get('display_name') or sh.get('regis_id') or 'Unknown'
            child_type = 'company' if sh.get('shareholder_type') == 'company' else 'personal'
            child_id = sh.get('regis_id') or f"{node_id}:{child_name}"
            try:
                child_effective = float(sh.get('effective_percentage', sh.get('percent', 0)) or 0)
            except (TypeError, ValueError):
                child_effective = 0.0
            try:
                child_direct = float(sh.get('direct_percent', sh.get('percent', 0)) or 0)
            except (TypeError, ValueError):
                child_direct = child_effective

            child_node = {
                'id': child_id,
                'name': _format_display_label(child_name, sh.get('regis_id')),
                'type': child_type,
                'level': level + 1,
                'effective_percent': round(child_effective, 4),
                'direct_percent': round(child_direct, 4),
                'isUbo': child_name in ubo_names or child_id in ubo_names,
                'children': []
            }

            if child_type == 'company' and sh.get('regis_id'):
                if sh['regis_id'] in visited:
                    child_node['name'] = f"{child_name} (already shown)"
                else:
                    subtree = _build_node(sh['regis_id'], level + 1, child_effective, child_direct)
                    if subtree:
                        subtree['effective_percent'] = round(child_effective, 4)
                        subtree['direct_percent'] = round(child_direct, 4)
                        subtree['level'] = level + 1
                        subtree['isUbo'] = subtree.get('name') in ubo_names or subtree.get('id') in ubo_names
                        child_node = subtree

            node['children'].append(child_node)

        visited.remove(node_id)
        return node

    return _build_node(root_id, level=0, effective=100.0, direct=100.0)

def initialize_ubo_system():
    """Initialize UBO System with API Key"""
    try:
        logger.info("Correct UBO System initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize UBO System: {e}")
        return False

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_file(os.path.join(app.root_path, 'static', 'icon', 'LHB_Logo.png'), mimetype='image/png')

@app.route('/')
def index():
    """Main page"""
    return render_template('enhanced_index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_company():
    """Analyze company and return structured UBO report."""
    try:
        data = request.get_json()
        registration_id = data.get('registration_id', '').strip()
        
        if not registration_id:
            return jsonify({'error': 'Please provide a company registration ID'}), 400
        
        # ✅ Mock Data Mode: If registration_id == "XXXXXXXX", use mock data
        if registration_id == "XXXXXXXX":
            logger.info("🎭 Using MOCK DATA for demonstration")
            mock_report = generate_mock_ubo_data()
            
            # Build network graph from mock data
            try:
                ubo_name_set = _extract_ubo_name_set(mock_report.get('ubos', []))
                mock_report['network_graph'] = build_network_graph(
                    registration_id,
                    mock_report.get('hierarchy_data', {}),
                    ubo_name_set
                )
            except Exception as e:
                logger.warning(f"Failed to build mock network graph: {e}")
                mock_report['network_graph'] = {'nodes': [], 'edges': []}
            
            # Build tree structure from mock data
            try:
                mock_report['tree_structure'] = build_tree_structure(
                    registration_id,
                    mock_report.get('hierarchy_data', {}),
                    ubo_name_set
                )
            except Exception as e:
                logger.warning(f"Failed to build mock tree structure: {e}")
                mock_report['tree_structure'] = None
            
            return jsonify({
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'data': mock_report,
                'is_mock': True
            })
        
        # ✅ Real Data Mode: Normal API call
        
        # New implementation does not rely on a persistent UBO system instance
        
        logger.info(f"Starting analysis for company: {registration_id}")
        
        # Perform UBO analysis
        result = analyze_company_ubo(registration_id)
        
        # Convert dataclass response to dictionary if needed
        if hasattr(result, '__dict__'):
            result_dict = result.__dict__
        else:
            result_dict = result
        
        # Extract main company data from hierarchy
        hierarchy = result_dict.get('hierarchy', {})
        main_company_data = hierarchy.get(registration_id, {})
        
        # Create report from analyzed data (English only)
        display_name = (
            main_company_data.get('display_name')
            or main_company_data.get('name_en')
            or main_company_data.get('name_th')
            or registration_id
        )
        business_type = (
            main_company_data.get('business_type_en')
            or main_company_data.get('business_type')
            or 'Unknown'
        )

        # Extract officialSignatory and directors
        official_signatory_text = main_company_data.get('official_signatory', '')
        signatory_names = extract_names_from_signatory(official_signatory_text)
        directors_list = main_company_data.get('directors', [])
        directors_signatories = build_directors_signatories_table(directors_list, signatory_names)
        
        report = {
            'company_info': {
                'regis_id': registration_id,
                'name': display_name,
                'name_en': display_name,
                'display_name': display_name,
                'status': main_company_data.get('status', 'Active'),
                'capital': main_company_data.get('capital', 'Unknown'),
                'regis_date': main_company_data.get('regis_date', 'Unknown'),
                'business_type': business_type,
                'business_type_en': business_type,
                'address': main_company_data.get('address', {}),
                'check_date': result_dict.get('check_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'official_signatory': official_signatory_text,
                'signatory_names': signatory_names,
                'directors': directors_list,
                'directors_signatories': directors_signatories
            },
            'ubos': [],
            'checklist': result_dict.get('checklist', {}),
            'hierarchy_data': hierarchy,
            'analysis_summary': f"Analysis completed - Checked {result_dict.get('total_companies_checked', 0)} companies, Max level {result_dict.get('max_level_reached', 0)} tiers",
            'level_summary': {
                'level_1_count': len([c for c in hierarchy.values() if c.get('level') == 1]),
                'level_2_count': len([c for c in hierarchy.values() if c.get('level') == 2]),
                'level_3_count': len([c for c in hierarchy.values() if c.get('level') == 3]),
                'level_4_count': len([c for c in hierarchy.values() if c.get('level') == 4]),
                'level_5_count': len([c for c in hierarchy.values() if c.get('level') == 5]),
                'level_6_count': len([c for c in hierarchy.values() if c.get('level') == 6]),
                'total_personal': sum(len([s for s in c.get('shareholders', []) if s.get('shareholder_type') == 'personal']) for c in hierarchy.values()),
                'total_company': sum(len([s for s in c.get('shareholders', []) if s.get('shareholder_type') == 'company']) for c in hierarchy.values())
            }
        }
        
        # Convert UBO candidates into serialisable dictionaries
        ubo_candidates = result_dict.get('ubo_candidates', [])
        for candidate in ubo_candidates:
            if hasattr(candidate, '__dict__'):
                candidate_dict = candidate.__dict__
            else:
                candidate_dict = candidate
            nationality = candidate_dict.get('nationality') or 'Unknown'
            
            # Include path details for calculation transparency
            path_details = candidate_dict.get('path_details', [])
            if hasattr(path_details, '__iter__') and not isinstance(path_details, (str, bytes)):
                path_details_list = list(path_details)
            else:
                path_details_list = []
                
            report['ubos'].append({
                'name': candidate_dict.get('name', 'Unknown'),
                'total_percentage': candidate_dict.get('total_percentage', 0),
                'identification_method': f"Method {candidate_dict.get('method', 1)}",
                'nationality': nationality,
                'is_director': candidate_dict.get('is_director', False),
                'ubo_status': 'YES' if candidate_dict.get('total_percentage', 0) >= 15.0 else 'NO',
                'path_details': path_details_list,
                'paths_count': len(path_details_list)
            })
        
        # Build network graph (NetworkX-based spider web visualization)
        try:
            ubo_name_set = _extract_ubo_name_set(report['ubos'])
            report['network_graph'] = build_network_graph(
                registration_id,
                hierarchy,
                ubo_name_set
            )
        except Exception as e:
            logger.warning(f"Failed to prepare network graph: {e}")
            report['network_graph'] = {'nodes': [], 'edges': []}
        
        # Build hierarchical tree structure for D3 visualisation (keep for compatibility)
        try:
            report['tree_structure'] = build_tree_structure(
                registration_id,
                hierarchy,
                ubo_name_set
            )
        except Exception as e:
            logger.warning(f"Failed to prepare hierarchy tree data: {e}")
            report['tree_structure'] = None
        
        # Return report directly (no file writing for Vercel serverless)
        logger.info(f"Analysis completed for {registration_id}")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'data': report
        })
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/export_excel', methods=['POST'])
def export_excel():
    """Export analysis results to CSV (Excel-compatible format)."""
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({'error': 'No data available for export'}), 400
        
        # Build CSV data (no pandas needed)
        import csv
        import io
        
        csv_data = []
        headers = ['Company ID', 'Company Name', 'Check Date', 'Method Used', 'Max Level', 
                   'Companies Checked', 'Risk Level', 'Compliance Status', 'Total UBO Candidates', 
                   'Final UBOs', 'UBO Name', 'UBO Method', 'UBO Percentage', 'UBO Paths', 
                   'Is Director', 'Position']
        
        for result in results:
            if 'error' in result:
                continue
                
            company_info = result.get('company_info', {})
            analysis_summary = result.get('analysis_summary', {})
            ubo_results = result.get('ubo_results', {})
            
            # Base row
            base_row = [
                company_info.get('id', ''),
                company_info.get('name', ''),
                company_info.get('check_date', ''),
                analysis_summary.get('method_used', ''),
                analysis_summary.get('max_level_reached', ''),
                analysis_summary.get('total_companies_checked', ''),
                analysis_summary.get('risk_level', ''),
                analysis_summary.get('compliance_status', ''),
                ubo_results.get('total_candidates', ''),
                ubo_results.get('final_ubos', '')
            ]
            
            # UBO details
            ubo_details = ubo_results.get('ubo_details', [])
            if ubo_details:
                for ubo in ubo_details:
                    row = base_row + [
                        ubo.get('name', ''),
                        ubo.get('method', ''),
                        ubo.get('total_percentage', ''),
                        len(ubo.get('paths', [])),
                        ubo.get('is_director', False),
                        ubo.get('position', '')
                    ]
                    csv_data.append(row)
            else:
                csv_data.append(base_row + ['', '', '', '', '', ''])
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(csv_data)
        
        # Return CSV data directly (no file writing for Vercel)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"ubo_analysis_{timestamp}.csv"
        csv_content = output.getvalue()
        
        # Return as downloadable response
        from io import BytesIO
        from flask import make_response
        
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
        response.headers['Content-Disposition'] = f'attachment; filename={csv_filename}'
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        return jsonify({'error': f'Failed to export: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download endpoint (disabled for serverless - use direct export instead)."""
    return jsonify({
        'error': 'File download not available in serverless environment',
        'message': 'Use CSV export button to download data directly'
    }), 501

@app.route('/api/status')
def system_status():
    """Return system status."""
    return jsonify({
        'status': 'running',
        'ubo_system_initialized': ubo_system is not None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Launch the web application."""
    print("🚀 Enhanced UBO Web Application")
    print("=" * 50)

    if not initialize_ubo_system():
        print("❌ Unable to initialize the UBO system")
        return

    print("✅ UBO system initialized successfully")
    print("🌐 Starting web server...")
    print("   Access the UI at: http://localhost:4444")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        app.run(host='0.0.0.0', port=4444, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")

if __name__ == '__main__':
    main()
