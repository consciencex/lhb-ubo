#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock Data Generator for 6-Tier UBO Analysis Testing
====================================================

Complex Scenario: DEMO BANK PUBLIC COMPANY LIMITED (XXXXXXXX)
- 6 Tiers of shareholding with multiple nodes per layer
- UBOs calculated from MULTIPLE PATHS (aggregated)
- Mix of companies and individuals at each level
- One path goes all the way to Tier 6

UBO Calculation Example:
    WILLIAM ANDERSON appears in:
    - Path 1 (Tier 2): XXXXXXXX → COMP_A → 38.2% = 22.5% × 38.2% = 8.595%
    - Path 2 (Tier 2): XXXXXXXX → COMP_B → 42.1% = 18.75% × 42.1% = 7.894%
    - Path 3 (Tier 3): XXXXXXXX → COMP_A → COMP_G → 76.2% = 22.5% × 18.5% × 76.2% = 3.174%
    - Path 4 (Tier 6): XXXXXXXX → COMP_D → DEEP_L2 → DEEP_L3 → DEEP_L4 → DEEP_L5 → 100% = 5.0%
    TOTAL: 8.595 + 7.894 + 3.174 + 5.0 = 24.66% ≥ 15% → UBO ✅
"""

from datetime import datetime
from typing import Dict, Any


def generate_mock_ubo_data() -> Dict[str, Any]:
    """Generate complex mock data for 6-Tier UBO scenario with multiple paths."""
    
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
            'official_signatory': 'นายวิลเลียม แอนเดอร์สัน และ นางสาวโซเฟีย เฉิน กรรมการสองคนลงลายมือชื่อร่วมกัน',
            'directors': [
                {'title': 'นาย', 'firstname': 'วิลเลียม', 'lastname': 'แอนเดอร์สัน'},
                {'title': 'นางสาว', 'firstname': 'โซเฟีย', 'lastname': 'เฉิน'},
                {'title': 'นาย', 'firstname': 'เจมส์', 'lastname': 'ทานากะ'}
            ],
            'signatory_names': ['นายวิลเลียม แอนเดอร์สัน', 'นางสาวโซเฟีย เฉิน'],
            'directors_signatories': [
                {'name': 'นายวิลเลียม แอนเดอร์สัน', 'is_signatory': True, 'is_director': True},
                {'name': 'นางสาวโซเฟีย เฉิน', 'is_signatory': True, 'is_director': True},
                {'name': 'นายเจมส์ ทานากะ', 'is_signatory': False, 'is_director': True}
            ]
        },
        'analysis_summary': 'Demo 6-Tier Analysis - UBOs aggregated from multiple paths including Tier 6',
        
        # UBOs with MULTIPLE PATHS
        'ubos': [
            {
                'name': 'WILLIAM ANDERSON',
                'total_percentage': 24.66,  # Sum of all paths
                'paths': [
                    ['XXXXXXXX', 'COMP_A'],
                    ['XXXXXXXX', 'COMP_B'],
                    ['XXXXXXXX', 'COMP_A', 'COMP_G'],
                    ['XXXXXXXX', 'COMP_D', 'DEEP_L2', 'DEEP_L3', 'DEEP_L4', 'DEEP_L5']  # Tier 6 path!
                ],
                'method': 1,
                'nationality': 'American',
                'is_director': True,
                'paths_count': 4,
                'path_details': [
                    {
                        'factors': [22.5, 38.2],
                        'names': ['GLOBAL INVESTMENT CORPORATION', 'WILLIAM ANDERSON'],
                        'result': 8.595,
                        'calculation': '22.5% × 38.2% = 8.595%'
                    },
                    {
                        'factors': [18.75, 42.1],
                        'names': ['ASIA PACIFIC HOLDINGS LTD', 'WILLIAM ANDERSON'],
                        'result': 7.894,
                        'calculation': '18.75% × 42.1% = 7.894%'
                    },
                    {
                        'factors': [22.5, 18.5, 76.2],
                        'names': ['GLOBAL INVESTMENT CORPORATION', 'VENTURE CAPITAL PARTNERS', 'WILLIAM ANDERSON'],
                        'result': 3.171,
                        'calculation': '22.5% × 18.5% × 76.2% = 3.171%'
                    },
                    {
                        'factors': [10.0, 100.0, 100.0, 100.0, 100.0, 50.0],
                        'names': ['NORTH AMERICAN FUND', 'DEEP HOLDING L2', 'DEEP HOLDING L3', 'DEEP HOLDING L4', 'DEEP HOLDING L5', 'WILLIAM ANDERSON'],
                        'result': 5.0,
                        'calculation': '10.0% × 100% × 100% × 100% × 100% × 50% = 5.0% (Tier 6 Path)'
                    }
                ]
            },
            {
                'name': 'SOPHIA CHEN',
                'total_percentage': 21.93,  # Sum of all paths
                'paths': [
                    ['XXXXXXXX', 'COMP_A'],
                    ['XXXXXXXX', 'COMP_B', 'COMP_H'],
                    ['XXXXXXXX', 'COMP_C'],
                    ['XXXXXXXX', 'COMP_E', 'COMP_K'],
                    ['XXXXXXXX', 'COMP_F', 'COMP_L']
                ],
                'method': 1,
                'nationality': 'Singaporean',
                'is_director': True,
                'paths_count': 5,
                'path_details': [
                    {
                        'factors': [22.5, 28.4],
                        'names': ['GLOBAL INVESTMENT CORPORATION', 'SOPHIA CHEN'],
                        'result': 6.39,
                        'calculation': '22.5% × 28.4% = 6.390%'
                    },
                    {
                        'factors': [18.75, 14.2, 68.4],
                        'names': ['ASIA PACIFIC HOLDINGS LTD', 'STRATEGIC HOLDINGS INC', 'SOPHIA CHEN'],
                        'result': 1.82,
                        'calculation': '18.75% × 14.2% × 68.4% = 1.820%'
                    },
                    {
                        'factors': [16.3, 35.8],
                        'names': ['EUROPEAN FINANCIAL GROUP', 'SOPHIA CHEN'],
                        'result': 5.84,
                        'calculation': '16.3% × 35.8% = 5.835%'
                    },
                    {
                        'factors': [12.8, 52.3, 58.7],
                        'names': ['SOUTHEAST ASIA CAPITAL', 'EMERGING MARKETS FUND', 'SOPHIA CHEN'],
                        'result': 3.93,
                        'calculation': '12.8% × 52.3% × 58.7% = 3.929%'
                    },
                    {
                        'factors': [6.35, 64.2, 92.1],
                        'names': ['MIDDLE EAST INVESTMENT GROUP', 'INTERNATIONAL EQUITY FUND', 'SOPHIA CHEN'],
                        'result': 3.75,
                        'calculation': '6.35% × 64.2% × 92.1% = 3.755%'
                    }
                ]
            },
            {
                'name': 'DEEP TIER6 HOLDER',
                'total_percentage': 15.0,  # From Tier 6 only
                'paths': [
                    ['XXXXXXXX', 'COMP_D', 'DEEP_L2', 'DEEP_L3', 'DEEP_L4', 'DEEP_L5']
                ],
                'method': 1,
                'nationality': 'Thai',
                'is_director': False,
                'paths_count': 1,
                'path_details': [
                    {
                        'factors': [10.0, 100.0, 100.0, 100.0, 100.0, 30.0],
                        'names': ['NORTH AMERICAN FUND', 'DEEP HOLDING L2', 'DEEP HOLDING L3', 'DEEP HOLDING L4', 'DEEP HOLDING L5', 'DEEP TIER6 HOLDER'],
                        'result': 3.0,
                        'calculation': '10.0% × 100% × 100% × 100% × 100% × 30% = 3.0% (Tier 6 Path)'
                    }
                ]
            }
        ],
        
        'hierarchy_data': {
            # Level 0: Main Company
            'XXXXXXXX': {
                'name_en': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'name_th_full': 'บริษัท เดโม แบงค์ จำกัด (มหาชน)',
                'display_name': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'level': 0,
                'company_id': 'XXXXXXXX',
                'status': 'Active',
                'capital': '50,000,000,000',
                'shareholders': [
                    {'display_name': 'GLOBAL INVESTMENT CORPORATION', 'shareholder_type': 'company', 'regis_id': 'COMP_A', 'percent': 22.5, 'effective_percentage': 22.5, 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'},
                    {'display_name': 'ASIA PACIFIC HOLDINGS LTD', 'shareholder_type': 'company', 'regis_id': 'COMP_B', 'percent': 18.75, 'effective_percentage': 18.75, 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'},
                    {'display_name': 'EUROPEAN FINANCIAL GROUP', 'shareholder_type': 'company', 'regis_id': 'COMP_C', 'percent': 16.3, 'effective_percentage': 16.3, 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'},
                    {'display_name': 'NORTH AMERICAN FUND', 'shareholder_type': 'company', 'regis_id': 'COMP_D', 'percent': 14.6, 'effective_percentage': 14.6, 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'},
                    {'display_name': 'SOUTHEAST ASIA CAPITAL', 'shareholder_type': 'company', 'regis_id': 'COMP_E', 'percent': 12.8, 'effective_percentage': 12.8, 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'},
                    {'display_name': 'MIDDLE EAST INVESTMENT GROUP', 'shareholder_type': 'company', 'regis_id': 'COMP_F', 'percent': 6.35, 'effective_percentage': 6.35, 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'},
                    {'display_name': 'MICHAEL BROWN', 'firstname': 'MICHAEL', 'lastname': 'BROWN', 'shareholder_type': 'personal', 'percent': 8.7, 'effective_percentage': 8.7, 'nationality': 'British', 'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'}
                ]
            },
            
            # Level 1: COMP_A - Multiple shareholders
            'COMP_A': {
                'name_en': 'GLOBAL INVESTMENT CORPORATION',
                'display_name': 'GLOBAL INVESTMENT CORPORATION',
                'level': 1,
                'company_id': 'COMP_A',
                'capital': '8,500,000,000',
                'shareholders': [
                    {'display_name': 'WILLIAM ANDERSON', 'shareholder_type': 'personal', 'percent': 38.2, 'effective_percentage': 8.595, 'nationality': 'American', 'company_name': 'GLOBAL INVESTMENT CORPORATION'},
                    {'display_name': 'SOPHIA CHEN', 'shareholder_type': 'personal', 'percent': 28.4, 'effective_percentage': 6.39, 'nationality': 'Singaporean', 'company_name': 'GLOBAL INVESTMENT CORPORATION'},
                    {'display_name': 'VENTURE CAPITAL PARTNERS', 'shareholder_type': 'company', 'regis_id': 'COMP_G', 'percent': 18.5, 'effective_percentage': 4.16, 'company_name': 'GLOBAL INVESTMENT CORPORATION'},
                    {'display_name': 'DAVID LEE', 'shareholder_type': 'personal', 'percent': 9.9, 'effective_percentage': 2.23, 'nationality': 'Australian', 'company_name': 'GLOBAL INVESTMENT CORPORATION'},
                    {'display_name': 'OLIVIA MARTIN', 'shareholder_type': 'personal', 'percent': 5.0, 'effective_percentage': 1.125, 'nationality': 'Canadian', 'company_name': 'GLOBAL INVESTMENT CORPORATION'}
                ]
            },
            
            # Level 1: COMP_B
            'COMP_B': {
                'name_en': 'ASIA PACIFIC HOLDINGS LTD',
                'display_name': 'ASIA PACIFIC HOLDINGS LTD',
                'level': 1,
                'company_id': 'COMP_B',
                'capital': '12,000,000,000',
                'shareholders': [
                    {'display_name': 'WILLIAM ANDERSON', 'shareholder_type': 'personal', 'percent': 42.1, 'effective_percentage': 7.894, 'nationality': 'American', 'company_name': 'ASIA PACIFIC HOLDINGS LTD'},
                    {'display_name': 'JAMES TANAKA', 'shareholder_type': 'personal', 'percent': 32.5, 'effective_percentage': 6.094, 'nationality': 'Japanese', 'company_name': 'ASIA PACIFIC HOLDINGS LTD'},
                    {'display_name': 'STRATEGIC HOLDINGS INC', 'shareholder_type': 'company', 'regis_id': 'COMP_H', 'percent': 14.2, 'effective_percentage': 2.66, 'company_name': 'ASIA PACIFIC HOLDINGS LTD'},
                    {'display_name': 'LUCAS BERGMANN', 'shareholder_type': 'personal', 'percent': 6.8, 'effective_percentage': 1.275, 'nationality': 'German', 'company_name': 'ASIA PACIFIC HOLDINGS LTD'},
                    {'display_name': 'EMMA WILSON', 'shareholder_type': 'personal', 'percent': 4.4, 'effective_percentage': 0.825, 'nationality': 'Australian', 'company_name': 'ASIA PACIFIC HOLDINGS LTD'}
                ]
            },
            
            # Level 1: COMP_C
            'COMP_C': {
                'name_en': 'EUROPEAN FINANCIAL GROUP',
                'display_name': 'EUROPEAN FINANCIAL GROUP',
                'level': 1,
                'company_id': 'COMP_C',
                'capital': '6,750,000,000',
                'shareholders': [
                    {'display_name': 'SOPHIA CHEN', 'shareholder_type': 'personal', 'percent': 35.8, 'effective_percentage': 5.835, 'nationality': 'Singaporean', 'company_name': 'EUROPEAN FINANCIAL GROUP'},
                    {'display_name': 'PIERRE DUBOIS', 'shareholder_type': 'personal', 'percent': 28.6, 'effective_percentage': 4.662, 'nationality': 'French', 'company_name': 'EUROPEAN FINANCIAL GROUP'},
                    {'display_name': 'MARIA GARCIA', 'shareholder_type': 'personal', 'percent': 22.4, 'effective_percentage': 3.651, 'nationality': 'Spanish', 'company_name': 'EUROPEAN FINANCIAL GROUP'},
                    {'display_name': 'ALEXANDER PETROV', 'shareholder_type': 'personal', 'percent': 13.2, 'effective_percentage': 2.152, 'nationality': 'Russian', 'company_name': 'EUROPEAN FINANCIAL GROUP'}
                ]
            },
            
            # Level 1: COMP_D - Entry point to Tier 6 chain
            'COMP_D': {
                'name_en': 'NORTH AMERICAN FUND',
                'display_name': 'NORTH AMERICAN FUND',
                'level': 1,
                'company_id': 'COMP_D',
                'capital': '9,200,000,000',
                'shareholders': [
                    {'display_name': 'JAMES TANAKA', 'shareholder_type': 'personal', 'percent': 39.1, 'effective_percentage': 5.709, 'nationality': 'Japanese', 'company_name': 'NORTH AMERICAN FUND'},
                    {'display_name': 'PRIVATE EQUITY VENTURES', 'shareholder_type': 'company', 'regis_id': 'COMP_J', 'percent': 31.2, 'effective_percentage': 4.555, 'company_name': 'NORTH AMERICAN FUND'},
                    {'display_name': 'SARAH JOHNSON', 'shareholder_type': 'personal', 'percent': 19.7, 'effective_percentage': 2.876, 'nationality': 'Canadian', 'company_name': 'NORTH AMERICAN FUND'},
                    {'display_name': 'DEEP HOLDING L2 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'DEEP_L2', 'percent': 10.0, 'effective_percentage': 1.46, 'company_name': 'NORTH AMERICAN FUND'}
                ]
            },
            
            # Level 1: COMP_E
            'COMP_E': {
                'name_en': 'SOUTHEAST ASIA CAPITAL',
                'display_name': 'SOUTHEAST ASIA CAPITAL',
                'level': 1,
                'company_id': 'COMP_E',
                'capital': '7,100,000,000',
                'shareholders': [
                    {'display_name': 'EMERGING MARKETS FUND', 'shareholder_type': 'company', 'regis_id': 'COMP_K', 'percent': 52.3, 'effective_percentage': 6.694, 'company_name': 'SOUTHEAST ASIA CAPITAL'},
                    {'display_name': 'MUHAMMAD RAHMAN', 'shareholder_type': 'personal', 'percent': 28.1, 'effective_percentage': 3.597, 'nationality': 'Malaysian', 'company_name': 'SOUTHEAST ASIA CAPITAL'},
                    {'display_name': 'NGUYEN VAN THANH', 'shareholder_type': 'personal', 'percent': 12.4, 'effective_percentage': 1.587, 'nationality': 'Vietnamese', 'company_name': 'SOUTHEAST ASIA CAPITAL'},
                    {'display_name': 'ARJUN PATEL', 'shareholder_type': 'personal', 'percent': 7.2, 'effective_percentage': 0.922, 'nationality': 'Indian', 'company_name': 'SOUTHEAST ASIA CAPITAL'}
                ]
            },
            
            # Level 1: COMP_F
            'COMP_F': {
                'name_en': 'MIDDLE EAST INVESTMENT GROUP',
                'display_name': 'MIDDLE EAST INVESTMENT GROUP',
                'level': 1,
                'company_id': 'COMP_F',
                'capital': '4,800,000,000',
                'shareholders': [
                    {'display_name': 'INTERNATIONAL EQUITY FUND', 'shareholder_type': 'company', 'regis_id': 'COMP_L', 'percent': 64.2, 'effective_percentage': 4.077, 'company_name': 'MIDDLE EAST INVESTMENT GROUP'},
                    {'display_name': 'AHMED AL-SAYED', 'shareholder_type': 'personal', 'percent': 23.5, 'effective_percentage': 1.492, 'nationality': 'UAE', 'company_name': 'MIDDLE EAST INVESTMENT GROUP'},
                    {'display_name': 'FATIMA HASSAN', 'shareholder_type': 'personal', 'percent': 12.3, 'effective_percentage': 0.781, 'nationality': 'Saudi Arabian', 'company_name': 'MIDDLE EAST INVESTMENT GROUP'}
                ]
            },
            
            # Level 2: COMP_G
            'COMP_G': {
                'name_en': 'VENTURE CAPITAL PARTNERS',
                'display_name': 'VENTURE CAPITAL PARTNERS',
                'level': 2,
                'company_id': 'COMP_G',
                'capital': '3,200,000,000',
                'shareholders': [
                    {'display_name': 'WILLIAM ANDERSON', 'shareholder_type': 'personal', 'percent': 76.2, 'effective_percentage': 3.171, 'nationality': 'American', 'company_name': 'VENTURE CAPITAL PARTNERS'},
                    {'display_name': 'ALEXANDER NOVAK', 'shareholder_type': 'personal', 'percent': 15.3, 'effective_percentage': 0.636, 'nationality': 'Russian', 'company_name': 'VENTURE CAPITAL PARTNERS'},
                    {'display_name': 'THOMAS ANDERSON', 'shareholder_type': 'personal', 'percent': 5.9, 'effective_percentage': 0.245, 'nationality': 'Swedish', 'company_name': 'VENTURE CAPITAL PARTNERS'},
                    {'display_name': 'LISA MULLER', 'shareholder_type': 'personal', 'percent': 2.6, 'effective_percentage': 0.108, 'nationality': 'German', 'company_name': 'VENTURE CAPITAL PARTNERS'}
                ]
            },
            
            # Level 2: COMP_H
            'COMP_H': {
                'name_en': 'STRATEGIC HOLDINGS INC',
                'display_name': 'STRATEGIC HOLDINGS INC',
                'level': 2,
                'company_id': 'COMP_H',
                'capital': '2,600,000,000',
                'shareholders': [
                    {'display_name': 'SOPHIA CHEN', 'shareholder_type': 'personal', 'percent': 68.4, 'effective_percentage': 1.819, 'nationality': 'Singaporean', 'company_name': 'STRATEGIC HOLDINGS INC'},
                    {'display_name': 'KEVIN WONG', 'shareholder_type': 'personal', 'percent': 21.3, 'effective_percentage': 0.567, 'nationality': 'Hong Kong', 'company_name': 'STRATEGIC HOLDINGS INC'},
                    {'display_name': 'YUKI YAMAMOTO', 'shareholder_type': 'personal', 'percent': 10.3, 'effective_percentage': 0.274, 'nationality': 'Japanese', 'company_name': 'STRATEGIC HOLDINGS INC'}
                ]
            },
            
            # Level 2: COMP_J
            'COMP_J': {
                'name_en': 'PRIVATE EQUITY VENTURES',
                'display_name': 'PRIVATE EQUITY VENTURES',
                'level': 2,
                'company_id': 'COMP_J',
                'capital': '5,400,000,000',
                'shareholders': [
                    {'display_name': 'WILLIAM ANDERSON', 'shareholder_type': 'personal', 'percent': 82.5, 'effective_percentage': 3.758, 'nationality': 'American', 'company_name': 'PRIVATE EQUITY VENTURES'},
                    {'display_name': 'JENNIFER SMITH', 'shareholder_type': 'personal', 'percent': 12.1, 'effective_percentage': 0.551, 'nationality': 'American', 'company_name': 'PRIVATE EQUITY VENTURES'},
                    {'display_name': 'DANIEL PARK', 'shareholder_type': 'personal', 'percent': 5.4, 'effective_percentage': 0.246, 'nationality': 'Korean', 'company_name': 'PRIVATE EQUITY VENTURES'}
                ]
            },
            
            # Level 2: COMP_K
            'COMP_K': {
                'name_en': 'EMERGING MARKETS FUND',
                'display_name': 'EMERGING MARKETS FUND',
                'level': 2,
                'company_id': 'COMP_K',
                'capital': '4,200,000,000',
                'shareholders': [
                    {'display_name': 'SOPHIA CHEN', 'shareholder_type': 'personal', 'percent': 58.7, 'effective_percentage': 3.929, 'nationality': 'Singaporean', 'company_name': 'EMERGING MARKETS FUND'},
                    {'display_name': 'EMILY RODRIGUEZ', 'shareholder_type': 'personal', 'percent': 25.8, 'effective_percentage': 1.727, 'nationality': 'Spanish', 'company_name': 'EMERGING MARKETS FUND'},
                    {'display_name': 'RAJESH KUMAR', 'shareholder_type': 'personal', 'percent': 10.2, 'effective_percentage': 0.683, 'nationality': 'Indian', 'company_name': 'EMERGING MARKETS FUND'},
                    {'display_name': 'CARLOS SILVA', 'shareholder_type': 'personal', 'percent': 5.3, 'effective_percentage': 0.355, 'nationality': 'Brazilian', 'company_name': 'EMERGING MARKETS FUND'}
                ]
            },
            
            # Level 2: COMP_L
            'COMP_L': {
                'name_en': 'INTERNATIONAL EQUITY FUND',
                'display_name': 'INTERNATIONAL EQUITY FUND',
                'level': 2,
                'company_id': 'COMP_L',
                'capital': '3,900,000,000',
                'shareholders': [
                    {'display_name': 'SOPHIA CHEN', 'shareholder_type': 'personal', 'percent': 92.1, 'effective_percentage': 3.755, 'nationality': 'Singaporean', 'company_name': 'INTERNATIONAL EQUITY FUND'},
                    {'display_name': 'GIOVANNI ROSSI', 'shareholder_type': 'personal', 'percent': 4.6, 'effective_percentage': 0.188, 'nationality': 'Italian', 'company_name': 'INTERNATIONAL EQUITY FUND'},
                    {'display_name': 'ANNA KOWALSKI', 'shareholder_type': 'personal', 'percent': 2.1, 'effective_percentage': 0.086, 'nationality': 'Polish', 'company_name': 'INTERNATIONAL EQUITY FUND'},
                    {'display_name': 'LARS NIELSEN', 'shareholder_type': 'personal', 'percent': 1.2, 'effective_percentage': 0.049, 'nationality': 'Danish', 'company_name': 'INTERNATIONAL EQUITY FUND'}
                ]
            },
            
            # ===== TIER 6 DEEP CHAIN =====
            # Level 2: DEEP_L2 (Entry to Tier 6 chain)
            'DEEP_L2': {
                'name_en': 'DEEP HOLDING L2 CO., LTD.',
                'display_name': 'DEEP HOLDING L2 CO., LTD.',
                'level': 2,
                'company_id': 'DEEP_L2',
                'capital': '1,000,000,000',
                'shareholders': [
                    {'display_name': 'DEEP HOLDING L3 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'DEEP_L3', 'percent': 100.0, 'effective_percentage': 1.46, 'company_name': 'DEEP HOLDING L2 CO., LTD.'}
                ]
            },
            
            # Level 3: DEEP_L3
            'DEEP_L3': {
                'name_en': 'DEEP HOLDING L3 CO., LTD.',
                'display_name': 'DEEP HOLDING L3 CO., LTD.',
                'level': 3,
                'company_id': 'DEEP_L3',
                'capital': '500,000,000',
                'shareholders': [
                    {'display_name': 'DEEP HOLDING L4 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'DEEP_L4', 'percent': 100.0, 'effective_percentage': 1.46, 'company_name': 'DEEP HOLDING L3 CO., LTD.'}
                ]
            },
            
            # Level 4: DEEP_L4
            'DEEP_L4': {
                'name_en': 'DEEP HOLDING L4 CO., LTD.',
                'display_name': 'DEEP HOLDING L4 CO., LTD.',
                'level': 4,
                'company_id': 'DEEP_L4',
                'capital': '250,000,000',
                'shareholders': [
                    {'display_name': 'DEEP HOLDING L5 CO., LTD.', 'shareholder_type': 'company', 'regis_id': 'DEEP_L5', 'percent': 100.0, 'effective_percentage': 1.46, 'company_name': 'DEEP HOLDING L4 CO., LTD.'}
                ]
            },
            
            # Level 5: DEEP_L5 - Contains Tier 6 shareholders
            'DEEP_L5': {
                'name_en': 'DEEP HOLDING L5 CO., LTD.',
                'display_name': 'DEEP HOLDING L5 CO., LTD.',
                'level': 5,
                'company_id': 'DEEP_L5',
                'capital': '100,000,000',
                'shareholders': [
                    {'display_name': 'WILLIAM ANDERSON', 'shareholder_type': 'personal', 'percent': 50.0, 'effective_percentage': 0.73, 'nationality': 'American', 'company_name': 'DEEP HOLDING L5 CO., LTD.'},
                    {'display_name': 'DEEP TIER6 HOLDER', 'shareholder_type': 'personal', 'percent': 30.0, 'effective_percentage': 0.438, 'nationality': 'Thai', 'company_name': 'DEEP HOLDING L5 CO., LTD.'},
                    {'display_name': 'MINOR TIER6 HOLDER', 'shareholder_type': 'personal', 'percent': 20.0, 'effective_percentage': 0.292, 'nationality': 'Thai', 'company_name': 'DEEP HOLDING L5 CO., LTD.'}
                ]
            }
        },
        
        'level_summary': {
            'level_1_count': 6,
            'level_2_count': 7,
            'level_3_count': 1,
            'level_4_count': 1,
            'level_5_count': 1,
            'level_6_count': 3,
            'total_personal': 35,
            'total_company': 16
        },
        
        'checklist': {
            'method_1_check': {'checked': True, 'found_ubo': True, 'companies_checked': 16, 'max_level_reached': 6},
            'method_2_check': {'checked': False, 'required': False, 'note': 'UBO found via shareholding method'},
            'method_3_check': {'checked': False, 'directors_found': 3, 'note': 'Not required - UBO found'},
            'exemption_check': {'checked': True, 'is_exempt': False, 'reason': ''},
            'final_result': {'ubo_identified': True, 'action': 'UBO Identified (Multi-path aggregation)', 'next_step': 'Proceed with KYC verification'}
        },
        
        'tree_structure': None
    }
    
    # Build network graph
    nodes = []
    edges = []
    ubo_names = {ubo['name'] for ubo in mock_data['ubos']}
    
    for company_id, company_data in mock_data['hierarchy_data'].items():
        node_type = 'main' if company_data['level'] == 0 else 'company'
        nodes.append({
            'id': company_id,
            'name': company_data['display_name'][:30],
            'full_name': company_data['display_name'],
            'type': node_type,
            'level': company_data['level'],
            'is_ubo': False,
            'capital': company_data.get('capital', '')
        })
        
        for sh in company_data.get('shareholders', []):
            sh_name = sh.get('display_name', 'Unknown')
            sh_id = sh.get('regis_id') or sh_name
            sh_type = sh.get('shareholder_type', 'personal')
            is_ubo = sh_name in ubo_names
            
            if sh_type == 'personal':
                # Only add personal node if not already added
                existing = [n for n in nodes if n['id'] == sh_id]
                if not existing:
                    nodes.append({
                        'id': sh_id,
                        'name': sh_name[:30],
                        'full_name': sh_name,
                        'type': 'ubo' if is_ubo else 'individual',
                        'level': company_data['level'] + 1,
                        'is_ubo': is_ubo,
                        'nationality': sh.get('nationality', 'Unknown')
                    })
            
            edges.append({
                'source': sh_id,
                'target': company_id,
                'percentage': sh.get('percent', 0),
                'is_ubo_path': is_ubo
            })
    
    mock_data['network_graph'] = {'nodes': nodes, 'edges': edges}
    
    return mock_data


if __name__ == '__main__':
    data = generate_mock_ubo_data()
    print("=" * 70)
    print("🧪 6-Tier Complex Mock Data Generated")
    print("=" * 70)
    print(f"Main Company: {data['company_info']['name']}")
    print(f"Registration ID: {data['company_info']['regis_id']}")
    print(f"Companies in hierarchy: {len(data['hierarchy_data'])}")
    print(f"Max Level Reached: 6 (Tier 6)")
    print()
    print("UBOs Found (Multi-path aggregation):")
    print("-" * 50)
    for ubo in data['ubos']:
        print(f"  ✅ {ubo['name']}: {ubo['total_percentage']:.2f}% ({ubo['paths_count']} paths)")
        for pd in ubo.get('path_details', []):
            print(f"      • {pd['calculation']}")
    print()
    print("Level Summary:")
    for key, value in data['level_summary'].items():
        print(f"  {key}: {value}")
