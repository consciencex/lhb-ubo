#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vercel Serverless Function wrapper for UBO Analysis API."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from final_ubo_system import analyze_company_ubo
import logging
from typing import Any, Dict, Optional, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


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
            return f"{label} ({regis})" if regis not in label else label
        return regis
    return label or 'Unknown'


def build_tree_structure(root_id: str, hierarchy: Dict, ubo_names: Set) -> Dict:
    """Build hierarchical tree structure for D3 visualization."""
    root_data = hierarchy.get(root_id, {})
    root_name = root_data.get('display_name') or root_data.get('name_en') or root_id
    
    def _build_node(node_id: str, level: int = 0) -> Dict:
        node_data = hierarchy.get(node_id, {})
        if not node_data:
            return None
        
        node_name = node_data.get('display_name') or node_data.get('name_en') or node_id
        shareholders = node_data.get('shareholders', [])
        
        node = {
            'id': node_id,
            'name': _format_display_label(node_name, node_id),
            'type': 'company',
            'level': level,
            'percentage': 100.0 if level == 0 else 0.0,
            'isUbo': node_name in ubo_names or node_id in ubo_names,
            'children': []
        }
        
        for sh in shareholders:
            child_id = sh.get('regis_id') or sh.get('name', '')
            if not child_id:
                continue
            
            child_name = sh.get('display_name') or sh.get('name', 'Unknown')
            child_type = 'company' if sh.get('shareholder_type') == 'company' else 'personal'
            direct_percent = float(sh.get('percent', 0) or 0)
            
            child_node = {
                'id': child_id,
                'name': _format_display_label(child_name, sh.get('regis_id')),
                'type': child_type,
                'level': level + 1,
                'percentage': round(direct_percent, 4),
                'isUbo': child_name in ubo_names or child_id in ubo_names,
                'children': []
            }
            
            if child_type == 'company' and child_id in hierarchy:
                child_node['children'] = [_build_node(child_id, level + 1)]
            
            node['children'].append(child_node)
        
        return node
    
    return _build_node(root_id, 0)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze company UBO."""
    try:
        data = request.get_json()
        registration_id = data.get('registration_id', '').strip()
        
        if not registration_id:
            return jsonify({
                'success': False,
                'error': 'Registration ID is required'
            }), 400
        
        logger.info(f"Analyzing company: {registration_id}")
        
        # Analyze company
        result = analyze_company_ubo(registration_id)
        
        if not result or not result.hierarchy:
            return jsonify({
                'success': False,
                'error': 'No data found for this company'
            }), 404
        
        # Prepare response data
        root_company = result.hierarchy.get(registration_id, {})
        hierarchy_data = result.hierarchy
        
        # Extract UBO names
        ubo_name_set = _extract_ubo_name_set(result.ubos)
        
        # Build tree structure
        try:
            tree_structure = build_tree_structure(
                registration_id,
                hierarchy_data,
                ubo_name_set
            )
        except Exception as e:
            logger.warning(f"Failed to prepare hierarchy tree data: {e}")
            tree_structure = None
        
        # Format company info
        company_info = {
            'regis_id': registration_id,
            'name_en': root_company.get('name_en', ''),
            'name_th': root_company.get('name_th', ''),
            'display_name': root_company.get('display_name') or root_company.get('name_en') or registration_id,
            'business_type': root_company.get('business_type_en') or root_company.get('business_type', 'Unknown'),
            'status': root_company.get('status', 'Unknown'),
            'capital': root_company.get('capital', 'Unknown'),
            'regis_date': root_company.get('regis_date', 'Unknown'),
            'check_date': root_company.get('check_date', 'Unknown')
        }
        
        # Format UBOs
        ubos_list = []
        for ubo in result.ubos:
            if ubo.total_percentage >= 15.0:
                ubos_list.append({
                    'name': ubo.name,
                    'total_percentage': round(ubo.total_percentage, 4),
                    'identification_method': f"Method {ubo.method}",
                    'nationality': getattr(ubo, 'nationality', 'Unknown'),
                    'is_director': getattr(ubo, 'is_director', False)
                })
        
        return jsonify({
            'success': True,
            'data': {
                'company_info': company_info,
                'hierarchy_data': hierarchy_data,
                'ubos': ubos_list,
                'tree_structure': tree_structure
            }
        })
        
    except Exception as e:
        logger.error(f"Error analyzing company: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Vercel serverless handler
# Vercel will automatically detect and use this handler
def handler(request):
    """Vercel serverless handler."""
    from werkzeug.wrappers import Response
    
    with app.request_context(request.environ):
        try:
            rv = app.full_dispatch_request()
        except Exception as e:
            rv = app.handle_exception(e)
        return Response(
            rv.get_data(),
            status=rv.status_code,
            headers=dict(rv.headers)
        )

