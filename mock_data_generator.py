#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock Data Generator for 6-Tier UBO Analysis Testing
====================================================
Chain Structure (UBO found at Tier 6):
    XXXXXXXX (Level 0) - Main Company - 100%
        └─ HOLD_L1_001 (Level 1) - 100%
            └─ HOLD_L2_001 (Level 2) - 100%
                └─ HOLD_L3_001 (Level 3) - 100%
                    └─ HOLD_L4_001 (Level 4) - 100%
                        └─ HOLD_L5_001 (Level 5) - 100%
                            ├─ MR. DEEP SHAREHOLDER (25%) → UBO
                            ├─ MS. HIDDEN OWNER (20%) → UBO
                            ├─ MR. MINORITY HOLDER (16%) → UBO
                            ├─ MR. THRESHOLD HOLDER (15%) → UBO
                            ├─ MS. BELOW THRESHOLD (14%) → Not UBO
                            └─ MR. SMALL HOLDER (10%) → Not UBO
"""

from datetime import datetime
from typing import Dict, Any


def generate_mock_ubo_data() -> Dict[str, Any]:
    """Generate mock data for 6-Tier UBO scenario."""
    
    mock_data = {
        'company_info': {
            'regis_id': 'XXXXXXXX',
            'name': 'DEMO BANK PUBLIC COMPANY LIMITED',
            'name_en': 'DEMO BANK PUBLIC COMPANY LIMITED',
            'display_name': 'DEMO BANK PUBLIC COMPANY LIMITED',
            'status': 'Active',
            'capital': '50,000,000,000',
            'regis_date': '15 Jan 2010',
            'business_type': 'Banking and Financial Services',
            'business_type_en': 'Banking and Financial Services',
            'address': {'full': '123 Financial District, Bangkok 10500'},
            'check_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'official_signatory': 'นายทดสอบ ระบบหกชั้น และ นางสาวตรวจสอบ ยูบีโอ กรรมการสองคนลงลายมือชื่อร่วมกัน',
            'directors': [
                {'title': 'นาย', 'firstname': 'ทดสอบ', 'lastname': 'ระบบหกชั้น'},
                {'title': 'นางสาว', 'firstname': 'ตรวจสอบ', 'lastname': 'ยูบีโอ'},
                {'title': 'นาย', 'firstname': 'กรรมการ', 'lastname': 'ทดสอบ'}
            ],
            'signatory_names': ['นายทดสอบ ระบบหกชั้น', 'นางสาวตรวจสอบ ยูบีโอ'],
            'directors_signatories': [
                {'name': 'นายทดสอบ ระบบหกชั้น', 'is_signatory': True, 'is_director': True},
                {'name': 'นางสาวตรวจสอบ ยูบีโอ', 'is_signatory': True, 'is_director': True},
                {'name': 'นายกรรมการ ทดสอบ', 'is_signatory': False, 'is_director': True}
            ]
        },
        'analysis_summary': 'Mock 6-Tier Test - UBOs found at Tier 6 (Level 6)',
        'ubos': [
            {
                'name': 'MR. DEEP SHAREHOLDER',
                'total_percentage': 25.0,
                'paths': [['XXXXXXXX', 'HOLD_L1_001', 'HOLD_L2_001', 'HOLD_L3_001', 'HOLD_L4_001', 'HOLD_L5_001']],
                'method': 1,
                'nationality': 'Thai',
                'is_director': False,
                'path_details': [{'factors': [100.0, 100.0, 100.0, 100.0, 100.0, 25.0], 'result': 25.0, 'calculation': '100% × 100% × 100% × 100% × 100% × 25% = 25%'}]
            },
            {
                'name': 'MS. HIDDEN OWNER',
                'total_percentage': 20.0,
                'paths': [['XXXXXXXX', 'HOLD_L1_001', 'HOLD_L2_001', 'HOLD_L3_001', 'HOLD_L4_001', 'HOLD_L5_001']],
                'method': 1,
                'nationality': 'Singaporean',
                'is_director': False,
                'path_details': [{'factors': [100.0, 100.0, 100.0, 100.0, 100.0, 20.0], 'result': 20.0, 'calculation': '100% × 100% × 100% × 100% × 100% × 20% = 20%'}]
            },
            {
                'name': 'MR. MINORITY HOLDER',
                'total_percentage': 16.0,
                'paths': [['XXXXXXXX', 'HOLD_L1_001', 'HOLD_L2_001', 'HOLD_L3_001', 'HOLD_L4_001', 'HOLD_L5_001']],
                'method': 1,
                'nationality': 'Thai',
                'is_director': False,
                'path_details': [{'factors': [100.0, 100.0, 100.0, 100.0, 100.0, 16.0], 'result': 16.0, 'calculation': '100% × 100% × 100% × 100% × 100% × 16% = 16%'}]
            },
            {
                'name': 'MR. THRESHOLD HOLDER',
                'total_percentage': 15.0,
                'paths': [['XXXXXXXX', 'HOLD_L1_001', 'HOLD_L2_001', 'HOLD_L3_001', 'HOLD_L4_001', 'HOLD_L5_001']],
                'method': 1,
                'nationality': 'American',
                'is_director': False,
                'path_details': [{'factors': [100.0, 100.0, 100.0, 100.0, 100.0, 15.0], 'result': 15.0, 'calculation': '100% × 100% × 100% × 100% × 100% × 15% = 15%'}]
            }
        ],
        'hierarchy_data': {
            'XXXXXXXX': {
                'name_en': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'name_th_full': 'บริษัท เดโม แบงค์ จำกัด (มหาชน)',
                'display_name': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'level': 0,
                'company_id': 'XXXXXXXX',
                'status': 'Active',
                'capital': '50,000,000,000',
                'shareholders': [
                    {'display_name': 'HOLDING COMPANY LEVEL 1 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'HOLD_L1_001', 'percent': 100.0, 'effective_percentage': 100.0}
                ]
            },
            'HOLD_L1_001': {
                'name_en': 'HOLDING COMPANY LEVEL 1 CO., LTD.',
                'display_name': 'HOLDING COMPANY LEVEL 1 CO., LTD.',
                'level': 1,
                'company_id': 'HOLD_L1_001',
                'capital': '10,000,000,000',
                'shareholders': [
                    {'display_name': 'HOLDING COMPANY LEVEL 2 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'HOLD_L2_001', 'percent': 100.0, 'effective_percentage': 100.0}
                ]
            },
            'HOLD_L2_001': {
                'name_en': 'HOLDING COMPANY LEVEL 2 CO., LTD.',
                'display_name': 'HOLDING COMPANY LEVEL 2 CO., LTD.',
                'level': 2,
                'company_id': 'HOLD_L2_001',
                'capital': '5,000,000,000',
                'shareholders': [
                    {'display_name': 'HOLDING COMPANY LEVEL 3 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'HOLD_L3_001', 'percent': 100.0, 'effective_percentage': 100.0}
                ]
            },
            'HOLD_L3_001': {
                'name_en': 'HOLDING COMPANY LEVEL 3 CO., LTD.',
                'display_name': 'HOLDING COMPANY LEVEL 3 CO., LTD.',
                'level': 3,
                'company_id': 'HOLD_L3_001',
                'capital': '2,000,000,000',
                'shareholders': [
                    {'display_name': 'HOLDING COMPANY LEVEL 4 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'HOLD_L4_001', 'percent': 100.0, 'effective_percentage': 100.0}
                ]
            },
            'HOLD_L4_001': {
                'name_en': 'HOLDING COMPANY LEVEL 4 CO., LTD.',
                'display_name': 'HOLDING COMPANY LEVEL 4 CO., LTD.',
                'level': 4,
                'company_id': 'HOLD_L4_001',
                'capital': '1,000,000,000',
                'shareholders': [
                    {'display_name': 'HOLDING COMPANY LEVEL 5 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'HOLD_L5_001', 'percent': 100.0, 'effective_percentage': 100.0}
                ]
            },
            'HOLD_L5_001': {
                'name_en': 'HOLDING COMPANY LEVEL 5 CO., LTD.',
                'display_name': 'HOLDING COMPANY LEVEL 5 CO., LTD.',
                'level': 5,
                'company_id': 'HOLD_L5_001',
                'capital': '500,000,000',
                'shareholders': [
                    {'display_name': 'MR. DEEP SHAREHOLDER', 'firstname': 'DEEP', 'lastname': 'SHAREHOLDER', 'shareholder_type': 'personal', 'percent': 25.0, 'effective_percentage': 25.0, 'nationality': 'Thai'},
                    {'display_name': 'MS. HIDDEN OWNER', 'firstname': 'HIDDEN', 'lastname': 'OWNER', 'shareholder_type': 'personal', 'percent': 20.0, 'effective_percentage': 20.0, 'nationality': 'Singaporean'},
                    {'display_name': 'MR. MINORITY HOLDER', 'firstname': 'MINORITY', 'lastname': 'HOLDER', 'shareholder_type': 'personal', 'percent': 16.0, 'effective_percentage': 16.0, 'nationality': 'Thai'},
                    {'display_name': 'MR. THRESHOLD HOLDER', 'firstname': 'THRESHOLD', 'lastname': 'HOLDER', 'shareholder_type': 'personal', 'percent': 15.0, 'effective_percentage': 15.0, 'nationality': 'American'},
                    {'display_name': 'MS. BELOW THRESHOLD', 'firstname': 'BELOW', 'lastname': 'THRESHOLD', 'shareholder_type': 'personal', 'percent': 14.0, 'effective_percentage': 14.0, 'nationality': 'Thai'},
                    {'display_name': 'MR. SMALL HOLDER', 'firstname': 'SMALL', 'lastname': 'HOLDER', 'shareholder_type': 'personal', 'percent': 10.0, 'effective_percentage': 10.0, 'nationality': 'Thai'}
                ]
            }
        },
        'level_summary': {
            'level_1_count': 1,
            'level_2_count': 1,
            'level_3_count': 1,
            'level_4_count': 1,
            'level_5_count': 1,
            'level_6_count': 6,
            'total_personal': 6,
            'total_company': 5
        },
        'checklist': {
            'method_1_check': {'checked': True, 'found_ubo': True, 'companies_checked': 6, 'max_level_reached': 6},
            'method_2_check': {'checked': False, 'required': False},
            'method_3_check': {'checked': False, 'directors_found': 3},
            'exemption_check': {'checked': True, 'is_exempt': False},
            'final_result': {'ubo_identified': True, 'action': 'UBO Identified at Tier 6'}
        },
        'tree_structure': None
    }
    
    # Build network graph
    nodes = []
    edges = []
    ubo_names = {ubo['name'] for ubo in mock_data['ubos']}
    
    for company_id, company_data in mock_data['hierarchy_data'].items():
        node_type = 'main' if company_data['level'] == 0 else 'company'
        nodes.append({'id': company_id, 'name': company_data['display_name'][:30], 'full_name': company_data['display_name'], 'type': node_type, 'level': company_data['level'], 'is_ubo': False})
        
        for sh in company_data.get('shareholders', []):
            sh_name = sh.get('display_name', 'Unknown')
            sh_id = sh.get('regis_id') or sh_name
            sh_type = sh.get('shareholder_type', 'personal')
            is_ubo = sh_name in ubo_names
            
            if sh_type == 'personal':
                nodes.append({'id': sh_id, 'name': sh_name[:30], 'full_name': sh_name, 'type': 'ubo' if is_ubo else 'individual', 'level': company_data['level'] + 1, 'is_ubo': is_ubo, 'nationality': sh.get('nationality', 'Unknown')})
            
            edges.append({'source': sh_id, 'target': company_id, 'percentage': sh.get('percent', 0), 'is_ubo_path': is_ubo})
    
    mock_data['network_graph'] = {'nodes': nodes, 'edges': edges}
    
    return mock_data


if __name__ == '__main__':
    data = generate_mock_ubo_data()
    print("=" * 60)
    print("6-Tier Mock Data Generated")
    print("=" * 60)
    print(f"Main Company: {data['company_info']['name']}")
    print(f"Registration ID: {data['company_info']['regis_id']}")
    print(f"Companies: {len(data['hierarchy_data'])}")
    print(f"UBOs: {len(data['ubos'])}")
    for ubo in data['ubos']:
        print(f"  - {ubo['name']}: {ubo['total_percentage']}%")
