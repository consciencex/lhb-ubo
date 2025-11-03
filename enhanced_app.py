#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enhanced UBO Web Application (English output only)."""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime
import logging
from typing import Any, Dict, Optional, Set

# Import Final UBO System
from final_ubo_system import analyze_company_ubo

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
                'check_date': result_dict.get('check_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            },
            'ubos': [],
            'checklist': result_dict.get('checklist', {}),
            'hierarchy_data': hierarchy,
            'analysis_summary': f"Analysis completed - Checked {result_dict.get('total_companies_checked', 0)} companies, Max level {result_dict.get('max_level_reached', 0)} tiers",
            'level_summary': {
                'level_1_count': len([c for c in hierarchy.values() if c.get('level') == 1]),
                'level_2_count': len([c for c in hierarchy.values() if c.get('level') == 2]),
                'level_3_count': len([c for c in hierarchy.values() if c.get('level') == 3]),
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
                
            report['ubos'].append({
                'name': candidate_dict.get('name', 'Unknown'),
                'total_percentage': candidate_dict.get('total_percentage', 0),
                'identification_method': f"Method {candidate_dict.get('method', 1)}",
                'nationality': nationality,
                'is_director': candidate_dict.get('is_director', False),
                'ubo_status': 'YES' if candidate_dict.get('total_percentage', 0) >= 15.0 else 'NO'
            })
        
        # Build hierarchical tree structure for D3 visualisation
        try:
            ubo_name_set = _extract_ubo_name_set(report['ubos'])
            report['tree_structure'] = build_tree_structure(
                registration_id,
                hierarchy,
                ubo_name_set
            )
        except Exception as e:
            logger.warning(f"Failed to prepare hierarchy tree data: {e}")
            report['tree_structure'] = None
        
        # Persist a snapshot of the report for auditing/debugging
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"enhanced_ubo_report_{registration_id}_{timestamp}.json"
        
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Analysis completed for {registration_id}")
        
        return jsonify({
            'success': True,
            'data': report,
            'report_file': report_filename
        })
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/export_excel', methods=['POST'])
def export_excel():
    """Export analysis results to Excel (disabled - use JSON export instead)."""
    # Excel export disabled to reduce deployment size
    # pandas and openpyxl dependencies are too large (>250MB)
    return jsonify({
        'error': 'Excel export is disabled to reduce deployment size. Please use JSON export endpoint instead.',
        'message': 'Use /api/analyze endpoint to get JSON data'
    }), 501

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated files."""
    try:
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {e}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

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
