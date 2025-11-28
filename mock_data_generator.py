#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mock Data Generator for UBO Analysis Testing"""

from datetime import datetime
from typing import Dict, Any

def generate_mock_ubo_data() -> Dict[str, Any]:
    """Generate realistic mock data for UBO network visualization testing.
    
    Enhanced Scenario: DEMO BANK PUBLIC COMPANY LIMITED
    - 3 Tiers of shareholding with MORE nodes per layer
    - Mix of companies and individuals
    - Only 2 UBO candidates (≥15%): William Anderson and Sophia Chen
    - Various capital sizes for node visualization
    - Various shareholding percentages for edge visualization
    """
    
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
            'address': {
                'full': '123 Financial District, Bangkok 10500'
            },
            'check_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'analysis_summary': {
            'method_used': 'Method 1 (Shareholding ≥15%)',
            'max_level_reached': 3,
            'total_companies_checked': 20,
            'risk_level': 'Low',
            'compliance_status': 'Compliant'
        },
        'ubo_results': {
            'total_candidates': 12,
            'final_ubos': 2,  # Only 2 UBOs
            'ubo_details': [
                {
                    'name': 'WILLIAM ANDERSON',
                    'method': 'Method 1',
                    'total_percentage': 32.45,
                    'paths': 4,
                    'nationality': 'American',
                    'is_director': True,
                    'ubo_status': 'YES'
                },
                {
                    'name': 'SOPHIA CHEN',
                    'method': 'Method 1',
                    'total_percentage': 22.18,
                    'paths': 5,
                    'nationality': 'Singaporean',
                    'is_director': False,
                    'ubo_status': 'YES'
                }
            ]
        },
        'ubos': [
            {
                'name': 'WILLIAM ANDERSON',
                'total_percentage': 28.099,
                'paths': [['XXXXXXXX', 'COMP_A'], ['XXXXXXXX', 'COMP_B'], ['XXXXXXXX', 'COMP_C'], ['XXXXXXXX', 'COMP_D', 'COMP_J'], ['XXXXXXXX', 'COMP_G']],
                'method': 1,
                'nationality': 'American',
                'is_director': True,
                'identification_method': 'Method 1',
                'ubo_status': 'YES',
                'paths_count': 5,
                'path_details': [
                    {
                        'factors': [18.5, 22.5, 76.2],
                        'names': ['VENTURE CAPITAL PARTNERS', 'GLOBAL INVESTMENT CORPORATION', 'WILLIAM ANDERSON'],
                        'result': 3.171,
                        'calculation': '76.2% × 18.5% × 22.5% = 3.171%'
                    },
                    {
                        'factors': [22.5, 38.2],
                        'names': ['GLOBAL INVESTMENT CORPORATION', 'WILLIAM ANDERSON'],
                        'result': 8.595,
                        'calculation': '38.2% × 22.5% = 8.595%'
                    },
                    {
                        'factors': [18.8, 42.1],
                        'names': ['ASIA PACIFIC HOLDINGS LTD', 'WILLIAM ANDERSON'],
                        'result': 7.914,
                        'calculation': '42.1% × 18.8% = 7.914%'
                    },
                    {
                        'factors': [31.2, 14.6, 82.5],
                        'names': ['PRIVATE EQUITY VENTURES', 'NORTH AMERICAN FUND', 'WILLIAM ANDERSON'],
                        'result': 3.758,
                        'calculation': '82.5% × 31.2% × 14.6% = 3.758%'
                    },
                    {
                        'factors': [16.3, 28.6],
                        'names': ['EUROPEAN FINANCIAL GROUP', 'WILLIAM ANDERSON'],
                        'result': 4.661,
                        'calculation': '28.6% × 16.3% = 4.661%'
                    }
                ]
            },
            {
                'name': 'SOPHIA CHEN',
                'total_percentage': 22.18,
                'paths': [['XXXXXXXX', 'COMP_A'], ['XXXXXXXX', 'COMP_B', 'COMP_H'], ['XXXXXXXX', 'COMP_C'], ['XXXXXXXX', 'COMP_E', 'COMP_K'], ['XXXXXXXX', 'COMP_F', 'COMP_L']],
                'method': 1,
                'nationality': 'Singaporean',
                'is_director': False,
                'identification_method': 'Method 1',
                'ubo_status': 'YES',
                'paths_count': 5,
                'path_details': [
                    {
                        'factors': [22.5, 28.4],
                        'names': ['GLOBAL INVESTMENT CORPORATION', 'SOPHIA CHEN'],
                        'result': 6.39,
                        'calculation': '28.4% × 22.5% = 6.390%'
                    },
                    {
                        'factors': [18.75, 14.2, 68.4],
                        'names': ['ASIA PACIFIC HOLDINGS LTD', 'STRATEGIC HOLDINGS INC', 'SOPHIA CHEN'],
                        'result': 1.819,
                        'calculation': '68.4% × 14.2% × 18.75% = 1.819%'
                    },
                    {
                        'factors': [16.3, 35.8],
                        'names': ['EUROPEAN FINANCIAL GROUP', 'SOPHIA CHEN'],
                        'result': 5.835,
                        'calculation': '35.8% × 16.3% = 5.835%'
                    },
                    {
                        'factors': [12.8, 52.3, 58.7],
                        'names': ['SOUTHEAST ASIA CAPITAL', 'EMERGING MARKETS FUND', 'SOPHIA CHEN'],
                        'result': 3.929,
                        'calculation': '58.7% × 52.3% × 12.8% = 3.929%'
                    },
                    {
                        'factors': [6.35, 64.2, 92.1],
                        'names': ['MIDDLE EAST INVESTMENT GROUP', 'INTERNATIONAL EQUITY FUND', 'SOPHIA CHEN'],
                        'result': 3.755,
                        'calculation': '92.1% × 64.2% × 6.35% = 3.755%'
                    }
                ]
            },
            # Non-UBOs (< 15%)
            {
                'name': 'JAMES TANAKA',
                'total_percentage': 11.80,
                'paths': [['XXXXXXXX', 'COMP_B'], ['XXXXXXXX', 'COMP_D']],
                'method': 1,
                'nationality': 'Japanese',
                'is_director': True,
                'identification_method': 'Method 1',
                'ubo_status': 'NO'
            },
            {
                'name': 'EMILY RODRIGUEZ',
                'total_percentage': 9.35,
                'paths': [['XXXXXXXX', 'COMP_E', 'COMP_K']],
                'method': 1,
                'nationality': 'Spanish',
                'is_director': False,
                'identification_method': 'Method 1',
                'ubo_status': 'NO'
            },
            {
                'name': 'MICHAEL BROWN',
                'total_percentage': 8.70,
                'paths': [['XXXXXXXX']],
                'method': 1,
                'nationality': 'British',
                'is_director': False,
                'identification_method': 'Method 1',
                'ubo_status': 'NO'
            }
        ],
        'hierarchy_data': {
            # Level 0: Main Company
            'XXXXXXXX': {
                'name_en': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'name_th': '',
                'display_name': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'level': 0,
                'parent_percentage': 100.0,
                'shareholders': [
                    # Layer 1 - 6 shareholders (mix of companies and individuals)
                    {
                        'name': 'GLOBAL INVESTMENT CORPORATION',
                        'display_name': 'GLOBAL INVESTMENT CORPORATION',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_A',
                        'regis_id_held_by': 'COMP_A',
                        'percent': 22.50,
                        'direct_percent': 22.50,
                        'effective_percentage': 22.50,
                        'type_label': 'Company',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'ASIA PACIFIC HOLDINGS LTD',
                        'display_name': 'ASIA PACIFIC HOLDINGS LTD',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_B',
                        'regis_id_held_by': 'COMP_B',
                        'percent': 18.75,
                        'direct_percent': 18.75,
                        'effective_percentage': 18.75,
                        'type_label': 'Company',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'EUROPEAN FINANCIAL GROUP',
                        'display_name': 'EUROPEAN FINANCIAL GROUP',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_C',
                        'regis_id_held_by': 'COMP_C',
                        'percent': 16.30,
                        'direct_percent': 16.30,
                        'effective_percentage': 16.30,
                        'type_label': 'Company',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'NORTH AMERICAN FUND',
                        'display_name': 'NORTH AMERICAN FUND',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_D',
                        'regis_id_held_by': 'COMP_D',
                        'percent': 14.60,
                        'direct_percent': 14.60,
                        'effective_percentage': 14.60,
                        'type_label': 'Company',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'SOUTHEAST ASIA CAPITAL',
                        'display_name': 'SOUTHEAST ASIA CAPITAL',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_E',
                        'regis_id_held_by': 'COMP_E',
                        'percent': 12.80,
                        'direct_percent': 12.80,
                        'effective_percentage': 12.80,
                        'type_label': 'Company',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'MIDDLE EAST INVESTMENT GROUP',
                        'display_name': 'MIDDLE EAST INVESTMENT GROUP',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_F',
                        'regis_id_held_by': 'COMP_F',
                        'percent': 6.35,
                        'direct_percent': 6.35,
                        'effective_percentage': 6.35,
                        'type_label': 'Company',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'MICHAEL BROWN',
                        'display_name': 'MICHAEL BROWN',
                        'firstname': 'MICHAEL',
                        'lastname': 'BROWN',
                        'shareholder_type': 'personal',
                        'regis_id': '',
                        'percent': 8.70,
                        'direct_percent': 8.70,
                        'effective_percentage': 8.70,
                        'nationality': 'British',
                        'directorship': 'NO',
                        'type_label': 'Individual',
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    }
                ],
                'company_id': 'XXXXXXXX',
                'status': 'Active',
                'capital': '50,000,000,000',
                'business_type': 'Banking and Financial Services',
                'business_type_en': 'Banking and Financial Services'
            },
            
            # Level 1: COMP_A - 5 shareholders
            'COMP_A': {
                'name_en': 'GLOBAL INVESTMENT CORPORATION',
                'display_name': 'GLOBAL INVESTMENT CORPORATION',
                'level': 1,
                'parent_percentage': 22.50,
                'shareholders': [
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 38.20,
                        'direct_percent': 38.20,
                        'effective_percentage': 8.595,
                        'nationality': 'American',
                        'directorship': 'YES',
                        'type_label': 'Individual',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    },
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 28.40,
                        'direct_percent': 28.40,
                        'effective_percentage': 6.39,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    },
                    {
                        'name': 'VENTURE CAPITAL PARTNERS',
                        'display_name': 'VENTURE CAPITAL PARTNERS',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_G',
                        'regis_id_held_by': 'COMP_G',
                        'percent': 18.50,
                        'direct_percent': 18.50,
                        'effective_percentage': 4.16,
                        'type_label': 'Company',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    },
                    {
                        'name': 'DAVID LEE',
                        'display_name': 'DAVID LEE',
                        'shareholder_type': 'personal',
                        'percent': 9.90,
                        'direct_percent': 9.90,
                        'effective_percentage': 2.23,
                        'nationality': 'Australian',
                        'type_label': 'Individual',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    },
                    {
                        'name': 'OLIVIA MARTIN',
                        'display_name': 'OLIVIA MARTIN',
                        'shareholder_type': 'personal',
                        'percent': 5.00,
                        'direct_percent': 5.00,
                        'effective_percentage': 1.125,
                        'nationality': 'Canadian',
                        'type_label': 'Individual',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    }
                ],
                'company_id': 'COMP_A',
                'capital': '8,500,000,000',
                'business_type_en': 'Investment and Holdings'
            },
            
            # Level 1: COMP_B - 6 shareholders
            'COMP_B': {
                'name_en': 'ASIA PACIFIC HOLDINGS LTD',
                'display_name': 'ASIA PACIFIC HOLDINGS LTD',
                'level': 1,
                'parent_percentage': 18.75,
                'shareholders': [
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 42.10,
                        'direct_percent': 42.10,
                        'effective_percentage': 7.894,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'JAMES TANAKA',
                        'display_name': 'JAMES TANAKA',
                        'shareholder_type': 'personal',
                        'percent': 32.50,
                        'direct_percent': 32.50,
                        'effective_percentage': 6.094,
                        'nationality': 'Japanese',
                        'directorship': 'YES',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'STRATEGIC HOLDINGS INC',
                        'display_name': 'STRATEGIC HOLDINGS INC',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_H',
                        'regis_id_held_by': 'COMP_H',
                        'percent': 14.20,
                        'direct_percent': 14.20,
                        'effective_percentage': 2.66,
                        'type_label': 'Company',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'LUCAS BERGMANN',
                        'display_name': 'LUCAS BERGMANN',
                        'shareholder_type': 'personal',
                        'percent': 6.80,
                        'direct_percent': 6.80,
                        'effective_percentage': 1.275,
                        'nationality': 'German',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'EMMA WILSON',
                        'display_name': 'EMMA WILSON',
                        'shareholder_type': 'personal',
                        'percent': 2.90,
                        'direct_percent': 2.90,
                        'effective_percentage': 0.544,
                        'nationality': 'Australian',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'CHEN WEI',
                        'display_name': 'CHEN WEI',
                        'shareholder_type': 'personal',
                        'percent': 1.50,
                        'direct_percent': 1.50,
                        'effective_percentage': 0.281,
                        'nationality': 'Chinese',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    }
                ],
                'company_id': 'COMP_B',
                'capital': '12,000,000,000',
                'business_type_en': 'Investment and Holdings'
            },
            
            # Level 1: COMP_C - 5 shareholders
            'COMP_C': {
                'name_en': 'EUROPEAN FINANCIAL GROUP',
                'display_name': 'EUROPEAN FINANCIAL GROUP',
                'level': 1,
                'parent_percentage': 16.30,
                'shareholders': [
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 35.80,
                        'direct_percent': 35.80,
                        'effective_percentage': 5.835,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    },
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 28.60,
                        'direct_percent': 28.60,
                        'effective_percentage': 4.662,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    },
                    {
                        'name': 'PIERRE DUBOIS',
                        'display_name': 'PIERRE DUBOIS',
                        'shareholder_type': 'personal',
                        'percent': 22.40,
                        'direct_percent': 22.40,
                        'effective_percentage': 3.651,
                        'nationality': 'French',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    },
                    {
                        'name': 'MARIA GARCIA',
                        'display_name': 'MARIA GARCIA',
                        'shareholder_type': 'personal',
                        'percent': 8.70,
                        'direct_percent': 8.70,
                        'effective_percentage': 1.418,
                        'nationality': 'Spanish',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    },
                    {
                        'name': 'ALEXANDER PETROV',
                        'display_name': 'ALEXANDER PETROV',
                        'shareholder_type': 'personal',
                        'percent': 4.50,
                        'direct_percent': 4.50,
                        'effective_percentage': 0.734,
                        'nationality': 'Russian',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    }
                ],
                'company_id': 'COMP_C',
                'capital': '6,750,000,000',
                'business_type_en': 'Financial Services'
            },
            
            # Level 1: COMP_D - 4 shareholders
            'COMP_D': {
                'name_en': 'NORTH AMERICAN FUND',
                'display_name': 'NORTH AMERICAN FUND',
                'level': 1,
                'parent_percentage': 14.60,
                'shareholders': [
                    {
                        'name': 'JAMES TANAKA',
                        'display_name': 'JAMES TANAKA',
                        'shareholder_type': 'personal',
                        'percent': 39.10,
                        'direct_percent': 39.10,
                        'effective_percentage': 5.709,
                        'nationality': 'Japanese',
                        'type_label': 'Individual',
                        'company_name': 'NORTH AMERICAN FUND'
                    },
                    {
                        'name': 'PRIVATE EQUITY VENTURES',
                        'display_name': 'PRIVATE EQUITY VENTURES',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_J',
                        'regis_id_held_by': 'COMP_J',
                        'percent': 31.20,
                        'direct_percent': 31.20,
                        'effective_percentage': 4.555,
                        'type_label': 'Company',
                        'company_name': 'NORTH AMERICAN FUND'
                    },
                    {
                        'name': 'SARAH JOHNSON',
                        'display_name': 'SARAH JOHNSON',
                        'shareholder_type': 'personal',
                        'percent': 19.70,
                        'direct_percent': 19.70,
                        'effective_percentage': 2.876,
                        'nationality': 'Canadian',
                        'type_label': 'Individual',
                        'company_name': 'NORTH AMERICAN FUND'
                    },
                    {
                        'name': 'ROBERT MILLER',
                        'display_name': 'ROBERT MILLER',
                        'shareholder_type': 'personal',
                        'percent': 10.00,
                        'direct_percent': 10.00,
                        'effective_percentage': 1.46,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'NORTH AMERICAN FUND'
                    }
                ],
                'company_id': 'COMP_D',
                'capital': '9,200,000,000',
                'business_type_en': 'Investment Fund'
            },
            
            # Level 1: COMP_E - 4 shareholders
            'COMP_E': {
                'name_en': 'SOUTHEAST ASIA CAPITAL',
                'display_name': 'SOUTHEAST ASIA CAPITAL',
                'level': 1,
                'parent_percentage': 12.80,
                'shareholders': [
                    {
                        'name': 'EMERGING MARKETS FUND',
                        'display_name': 'EMERGING MARKETS FUND',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_K',
                        'regis_id_held_by': 'COMP_K',
                        'percent': 52.30,
                        'direct_percent': 52.30,
                        'effective_percentage': 6.694,
                        'type_label': 'Company',
                        'company_name': 'SOUTHEAST ASIA CAPITAL'
                    },
                    {
                        'name': 'MUHAMMAD RAHMAN',
                        'display_name': 'MUHAMMAD RAHMAN',
                        'shareholder_type': 'personal',
                        'percent': 28.10,
                        'direct_percent': 28.10,
                        'effective_percentage': 3.597,
                        'nationality': 'Malaysian',
                        'type_label': 'Individual',
                        'company_name': 'SOUTHEAST ASIA CAPITAL'
                    },
                    {
                        'name': 'NGUYEN VAN THANH',
                        'display_name': 'NGUYEN VAN THANH',
                        'shareholder_type': 'personal',
                        'percent': 12.40,
                        'direct_percent': 12.40,
                        'effective_percentage': 1.587,
                        'nationality': 'Vietnamese',
                        'type_label': 'Individual',
                        'company_name': 'SOUTHEAST ASIA CAPITAL'
                    },
                    {
                        'name': 'ARJUN PATEL',
                        'display_name': 'ARJUN PATEL',
                        'shareholder_type': 'personal',
                        'percent': 7.20,
                        'direct_percent': 7.20,
                        'effective_percentage': 0.922,
                        'nationality': 'Indian',
                        'type_label': 'Individual',
                        'company_name': 'SOUTHEAST ASIA CAPITAL'
                    }
                ],
                'company_id': 'COMP_E',
                'capital': '7,100,000,000',
                'business_type_en': 'Investment and Holdings'
            },
            
            # Level 1: COMP_F - 3 shareholders
            'COMP_F': {
                'name_en': 'MIDDLE EAST INVESTMENT GROUP',
                'display_name': 'MIDDLE EAST INVESTMENT GROUP',
                'level': 1,
                'parent_percentage': 6.35,
                'shareholders': [
                    {
                        'name': 'INTERNATIONAL EQUITY FUND',
                        'display_name': 'INTERNATIONAL EQUITY FUND',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_L',
                        'regis_id_held_by': 'COMP_L',
                        'percent': 64.20,
                        'direct_percent': 64.20,
                        'effective_percentage': 4.077,
                        'type_label': 'Company',
                        'company_name': 'MIDDLE EAST INVESTMENT GROUP'
                    },
                    {
                        'name': 'AHMED AL-SAYED',
                        'display_name': 'AHMED AL-SAYED',
                        'shareholder_type': 'personal',
                        'percent': 23.50,
                        'direct_percent': 23.50,
                        'effective_percentage': 1.492,
                        'nationality': 'UAE',
                        'type_label': 'Individual',
                        'company_name': 'MIDDLE EAST INVESTMENT GROUP'
                    },
                    {
                        'name': 'FATIMA HASSAN',
                        'display_name': 'FATIMA HASSAN',
                        'shareholder_type': 'personal',
                        'percent': 12.30,
                        'direct_percent': 12.30,
                        'effective_percentage': 0.781,
                        'nationality': 'Saudi Arabian',
                        'type_label': 'Individual',
                        'company_name': 'MIDDLE EAST INVESTMENT GROUP'
                    }
                ],
                'company_id': 'COMP_F',
                'capital': '4,800,000,000',
                'business_type_en': 'Investment Services'
            },
            
            # Level 2: COMP_G - 4 shareholders
            'COMP_G': {
                'name_en': 'VENTURE CAPITAL PARTNERS',
                'display_name': 'VENTURE CAPITAL PARTNERS',
                'level': 2,
                'parent_percentage': 4.16,
                'shareholders': [
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 76.20,
                        'direct_percent': 76.20,
                        'effective_percentage': 3.170,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'VENTURE CAPITAL PARTNERS'
                    },
                    {
                        'name': 'ALEXANDER NOVAK',
                        'display_name': 'ALEXANDER NOVAK',
                        'shareholder_type': 'personal',
                        'percent': 15.30,
                        'direct_percent': 15.30,
                        'effective_percentage': 0.636,
                        'nationality': 'Russian',
                        'type_label': 'Individual',
                        'company_name': 'VENTURE CAPITAL PARTNERS'
                    },
                    {
                        'name': 'THOMAS ANDERSON',
                        'display_name': 'THOMAS ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 5.90,
                        'direct_percent': 5.90,
                        'effective_percentage': 0.245,
                        'nationality': 'Swedish',
                        'type_label': 'Individual',
                        'company_name': 'VENTURE CAPITAL PARTNERS'
                    },
                    {
                        'name': 'LISA MULLER',
                        'display_name': 'LISA MULLER',
                        'shareholder_type': 'personal',
                        'percent': 2.60,
                        'direct_percent': 2.60,
                        'effective_percentage': 0.108,
                        'nationality': 'German',
                        'type_label': 'Individual',
                        'company_name': 'VENTURE CAPITAL PARTNERS'
                    }
                ],
                'company_id': 'COMP_G',
                'capital': '3,200,000,000',
                'business_type_en': 'Venture Capital'
            },
            
            # Level 2: COMP_H - 3 shareholders
            'COMP_H': {
                'name_en': 'STRATEGIC HOLDINGS INC',
                'display_name': 'STRATEGIC HOLDINGS INC',
                'level': 2,
                'parent_percentage': 2.66,
                'shareholders': [
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 68.40,
                        'direct_percent': 68.40,
                        'effective_percentage': 1.819,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'STRATEGIC HOLDINGS INC'
                    },
                    {
                        'name': 'KEVIN WONG',
                        'display_name': 'KEVIN WONG',
                        'shareholder_type': 'personal',
                        'percent': 21.30,
                        'direct_percent': 21.30,
                        'effective_percentage': 0.567,
                        'nationality': 'Hong Kong',
                        'type_label': 'Individual',
                        'company_name': 'STRATEGIC HOLDINGS INC'
                    },
                    {
                        'name': 'YUKI YAMAMOTO',
                        'display_name': 'YUKI YAMAMOTO',
                        'shareholder_type': 'personal',
                        'percent': 10.30,
                        'direct_percent': 10.30,
                        'effective_percentage': 0.274,
                        'nationality': 'Japanese',
                        'type_label': 'Individual',
                        'company_name': 'STRATEGIC HOLDINGS INC'
                    }
                ],
                'company_id': 'COMP_H',
                'capital': '2,600,000,000',
                'business_type_en': 'Investment Holdings'
            },
            
            # Level 2: COMP_J - 3 shareholders
            'COMP_J': {
                'name_en': 'PRIVATE EQUITY VENTURES',
                'display_name': 'PRIVATE EQUITY VENTURES',
                'level': 2,
                'parent_percentage': 4.555,
                'shareholders': [
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 82.50,
                        'direct_percent': 82.50,
                        'effective_percentage': 3.758,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'PRIVATE EQUITY VENTURES'
                    },
                    {
                        'name': 'JENNIFER SMITH',
                        'display_name': 'JENNIFER SMITH',
                        'shareholder_type': 'personal',
                        'percent': 12.10,
                        'direct_percent': 12.10,
                        'effective_percentage': 0.551,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'PRIVATE EQUITY VENTURES'
                    },
                    {
                        'name': 'DANIEL PARK',
                        'display_name': 'DANIEL PARK',
                        'shareholder_type': 'personal',
                        'percent': 5.40,
                        'direct_percent': 5.40,
                        'effective_percentage': 0.246,
                        'nationality': 'Korean',
                        'type_label': 'Individual',
                        'company_name': 'PRIVATE EQUITY VENTURES'
                    }
                ],
                'company_id': 'COMP_J',
                'capital': '5,400,000,000',
                'business_type_en': 'Private Equity'
            },
            
            # Level 2: COMP_K - 4 shareholders
            'COMP_K': {
                'name_en': 'EMERGING MARKETS FUND',
                'display_name': 'EMERGING MARKETS FUND',
                'level': 2,
                'parent_percentage': 6.694,
                'shareholders': [
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 58.70,
                        'direct_percent': 58.70,
                        'effective_percentage': 3.929,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'EMERGING MARKETS FUND'
                    },
                    {
                        'name': 'EMILY RODRIGUEZ',
                        'display_name': 'EMILY RODRIGUEZ',
                        'shareholder_type': 'personal',
                        'percent': 25.80,
                        'direct_percent': 25.80,
                        'effective_percentage': 1.727,
                        'nationality': 'Spanish',
                        'type_label': 'Individual',
                        'company_name': 'EMERGING MARKETS FUND'
                    },
                    {
                        'name': 'RAJESH KUMAR',
                        'display_name': 'RAJESH KUMAR',
                        'shareholder_type': 'personal',
                        'percent': 10.20,
                        'direct_percent': 10.20,
                        'effective_percentage': 0.683,
                        'nationality': 'Indian',
                        'type_label': 'Individual',
                        'company_name': 'EMERGING MARKETS FUND'
                    },
                    {
                        'name': 'CARLOS SILVA',
                        'display_name': 'CARLOS SILVA',
                        'shareholder_type': 'personal',
                        'percent': 5.30,
                        'direct_percent': 5.30,
                        'effective_percentage': 0.355,
                        'nationality': 'Brazilian',
                        'type_label': 'Individual',
                        'company_name': 'EMERGING MARKETS FUND'
                    }
                ],
                'company_id': 'COMP_K',
                'capital': '4,200,000,000',
                'business_type_en': 'Investment Fund'
            },
            
            # Level 2: COMP_L - 4 shareholders
            'COMP_L': {
                'name_en': 'INTERNATIONAL EQUITY FUND',
                'display_name': 'INTERNATIONAL EQUITY FUND',
                'level': 2,
                'parent_percentage': 4.077,
                'shareholders': [
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 92.10,
                        'direct_percent': 92.10,
                        'effective_percentage': 3.755,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'INTERNATIONAL EQUITY FUND'
                    },
                    {
                        'name': 'GIOVANNI ROSSI',
                        'display_name': 'GIOVANNI ROSSI',
                        'shareholder_type': 'personal',
                        'percent': 4.60,
                        'direct_percent': 4.60,
                        'effective_percentage': 0.188,
                        'nationality': 'Italian',
                        'type_label': 'Individual',
                        'company_name': 'INTERNATIONAL EQUITY FUND'
                    },
                    {
                        'name': 'ANNA KOWALSKI',
                        'display_name': 'ANNA KOWALSKI',
                        'shareholder_type': 'personal',
                        'percent': 2.10,
                        'direct_percent': 2.10,
                        'effective_percentage': 0.086,
                        'nationality': 'Polish',
                        'type_label': 'Individual',
                        'company_name': 'INTERNATIONAL EQUITY FUND'
                    },
                    {
                        'name': 'LARS NIELSEN',
                        'display_name': 'LARS NIELSEN',
                        'shareholder_type': 'personal',
                        'percent': 1.20,
                        'direct_percent': 1.20,
                        'effective_percentage': 0.049,
                        'nationality': 'Danish',
                        'type_label': 'Individual',
                        'company_name': 'INTERNATIONAL EQUITY FUND'
                    }
                ],
                'company_id': 'COMP_L',
                'capital': '3,900,000,000',
                'business_type_en': 'Investment Fund'
            }
        },
        'checklist': {
            'method_1_check': {
                'checked': True,
                'found_ubo': True,
                'companies_checked': 20,
                'max_level_reached': 3
            },
            'method_2_check': {
                'checked': True,
                'required': False
            }
        }
    }
    
    return mock_data
