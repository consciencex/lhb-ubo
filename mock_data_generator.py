#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mock Data Generator for UBO Analysis Testing"""

from datetime import datetime
from typing import Dict, Any

def generate_mock_ubo_data() -> Dict[str, Any]:
    """Generate realistic mock data for UBO network visualization testing.
    
    Scenario: DEMO BANK PUBLIC COMPANY LIMITED
    - 3 Tiers of shareholding
    - Mix of companies and individuals
    - Multiple UBO candidates (≥15%)
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
            'total_companies_checked': 12,
            'risk_level': 'Low',
            'compliance_status': 'Compliant'
        },
        'ubo_results': {
            'total_candidates': 8,
            'final_ubos': 3,
            'ubo_details': [
                {
                    'name': 'WILLIAM ANDERSON',
                    'method': 'Method 1',
                    'total_percentage': 28.50,
                    'paths': 2,
                    'nationality': 'American',
                    'is_director': True,
                    'ubo_status': 'YES'
                },
                {
                    'name': 'SOPHIA CHEN',
                    'method': 'Method 1',
                    'total_percentage': 18.75,
                    'paths': 3,
                    'nationality': 'Singaporean',
                    'is_director': False,
                    'ubo_status': 'YES'
                },
                {
                    'name': 'JAMES TANAKA',
                    'method': 'Method 1',
                    'total_percentage': 15.20,
                    'paths': 1,
                    'nationality': 'Japanese',
                    'is_director': True,
                    'ubo_status': 'YES'
                }
            ]
        },
        'ubos': [
            {
                'name': 'WILLIAM ANDERSON',
                'total_percentage': 28.50,
                'paths': [['XXXXXXXX', 'COMP_A'], ['XXXXXXXX', 'COMP_B', 'COMP_D']],
                'method': 1,
                'nationality': 'American',
                'is_director': True,
                'identification_method': 'Method 1',
                'ubo_status': 'YES'
            },
            {
                'name': 'SOPHIA CHEN',
                'total_percentage': 18.75,
                'paths': [['XXXXXXXX', 'COMP_A'], ['XXXXXXXX', 'COMP_C'], ['XXXXXXXX', 'COMP_E']],
                'method': 1,
                'nationality': 'Singaporean',
                'is_director': False,
                'identification_method': 'Method 1',
                'ubo_status': 'YES'
            },
            {
                'name': 'JAMES TANAKA',
                'total_percentage': 15.20,
                'paths': [['XXXXXXXX', 'COMP_B']],
                'method': 1,
                'nationality': 'Japanese',
                'is_director': True,
                'identification_method': 'Method 1',
                'ubo_status': 'YES'
            },
            {
                'name': 'EMILY RODRIGUEZ',
                'total_percentage': 8.50,
                'paths': [['XXXXXXXX', 'COMP_C', 'COMP_F']],
                'method': 1,
                'nationality': 'Spanish',
                'is_director': False,
                'identification_method': 'Method 1',
                'ubo_status': 'NO'
            },
            {
                'name': 'DAVID KIM',
                'total_percentage': 6.30,
                'paths': [['XXXXXXXX', 'COMP_D']],
                'method': 1,
                'nationality': 'Korean',
                'is_director': False,
                'identification_method': 'Method 1',
                'ubo_status': 'NO'
            }
        ],
        'hierarchy_data': {
            'XXXXXXXX': {
                'name_en': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'name_th': '',
                'display_name': 'DEMO BANK PUBLIC COMPANY LIMITED',
                'level': 0,
                'parent_percentage': 100.0,
                'shareholders': [
                    {
                        'name': 'GLOBAL INVESTMENT CORPORATION',
                        'display_name': 'GLOBAL INVESTMENT CORPORATION',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_A',
                        'regis_id_held_by': 'COMP_A',
                        'percent': 35.50,
                        'direct_percent': 35.50,
                        'effective_percentage': 35.50,
                        'type_label': 'Company',
                        'ubo_path': [{'entity_id': 'COMP_A', 'entity_name': 'GLOBAL INVESTMENT CORPORATION', 'share_percent': 35.50}],
                        'ubo_factors': [35.50],
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'ASIA PACIFIC HOLDINGS LTD',
                        'display_name': 'ASIA PACIFIC HOLDINGS LTD',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_B',
                        'regis_id_held_by': 'COMP_B',
                        'percent': 28.75,
                        'direct_percent': 28.75,
                        'effective_percentage': 28.75,
                        'type_label': 'Company',
                        'ubo_path': [{'entity_id': 'COMP_B', 'entity_name': 'ASIA PACIFIC HOLDINGS LTD', 'share_percent': 28.75}],
                        'ubo_factors': [28.75],
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'EUROPEAN FINANCIAL GROUP',
                        'display_name': 'EUROPEAN FINANCIAL GROUP',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_C',
                        'regis_id_held_by': 'COMP_C',
                        'percent': 18.20,
                        'direct_percent': 18.20,
                        'effective_percentage': 18.20,
                        'type_label': 'Company',
                        'ubo_path': [{'entity_id': 'COMP_C', 'entity_name': 'EUROPEAN FINANCIAL GROUP', 'share_percent': 18.20}],
                        'ubo_factors': [18.20],
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'MICHAEL BROWN',
                        'display_name': 'MICHAEL BROWN',
                        'firstname': 'MICHAEL',
                        'lastname': 'BROWN',
                        'shareholder_type': 'personal',
                        'regis_id': '',
                        'percent': 12.50,
                        'direct_percent': 12.50,
                        'effective_percentage': 12.50,
                        'nationality': 'British',
                        'directorship': 'YES',
                        'type_label': 'Individual',
                        'ubo_path': [{'entity_id': 'MICHAEL BROWN', 'entity_name': 'MICHAEL BROWN', 'share_percent': 12.50}],
                        'ubo_factors': [12.50],
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'EMMA WILSON',
                        'display_name': 'EMMA WILSON',
                        'firstname': 'EMMA',
                        'lastname': 'WILSON',
                        'shareholder_type': 'personal',
                        'regis_id': '',
                        'percent': 3.80,
                        'direct_percent': 3.80,
                        'effective_percentage': 3.80,
                        'nationality': 'Australian',
                        'directorship': 'NO',
                        'type_label': 'Individual',
                        'ubo_path': [{'entity_id': 'EMMA WILSON', 'entity_name': 'EMMA WILSON', 'share_percent': 3.80}],
                        'ubo_factors': [3.80],
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    },
                    {
                        'name': 'OLIVIA MARTIN',
                        'display_name': 'OLIVIA MARTIN',
                        'firstname': 'OLIVIA',
                        'lastname': 'MARTIN',
                        'shareholder_type': 'personal',
                        'regis_id': '',
                        'percent': 1.25,
                        'direct_percent': 1.25,
                        'effective_percentage': 1.25,
                        'nationality': 'Canadian',
                        'directorship': 'NO',
                        'type_label': 'Individual',
                        'ubo_path': [{'entity_id': 'OLIVIA MARTIN', 'entity_name': 'OLIVIA MARTIN', 'share_percent': 1.25}],
                        'ubo_factors': [1.25],
                        'company_name': 'DEMO BANK PUBLIC COMPANY LIMITED'
                    }
                ],
                'company_id': 'XXXXXXXX',
                'status': 'Active',
                'capital': '50,000,000,000',
                'business_type': 'Banking and Financial Services',
                'business_type_en': 'Banking and Financial Services'
            },
            'COMP_A': {
                'name_en': 'GLOBAL INVESTMENT CORPORATION',
                'display_name': 'GLOBAL INVESTMENT CORPORATION',
                'level': 1,
                'parent_percentage': 35.50,
                'shareholders': [
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 45.00,
                        'direct_percent': 45.00,
                        'effective_percentage': 15.975,
                        'nationality': 'American',
                        'directorship': 'YES',
                        'type_label': 'Individual',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    },
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 32.00,
                        'direct_percent': 32.00,
                        'effective_percentage': 11.36,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    },
                    {
                        'name': 'VENTURE CAPITAL PARTNERS',
                        'display_name': 'VENTURE CAPITAL PARTNERS',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_E',
                        'regis_id_held_by': 'COMP_E',
                        'percent': 23.00,
                        'direct_percent': 23.00,
                        'effective_percentage': 8.165,
                        'type_label': 'Company',
                        'company_name': 'GLOBAL INVESTMENT CORPORATION'
                    }
                ],
                'company_id': 'COMP_A',
                'capital': '8,500,000,000',
                'business_type_en': 'Investment and Holdings'
            },
            'COMP_B': {
                'name_en': 'ASIA PACIFIC HOLDINGS LTD',
                'display_name': 'ASIA PACIFIC HOLDINGS LTD',
                'level': 1,
                'parent_percentage': 28.75,
                'shareholders': [
                    {
                        'name': 'JAMES TANAKA',
                        'display_name': 'JAMES TANAKA',
                        'shareholder_type': 'personal',
                        'percent': 52.87,
                        'direct_percent': 52.87,
                        'effective_percentage': 15.20,
                        'nationality': 'Japanese',
                        'directorship': 'YES',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 35.00,
                        'direct_percent': 35.00,
                        'effective_percentage': 10.0625,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    },
                    {
                        'name': 'STRATEGIC INVESTMENTS INC',
                        'display_name': 'STRATEGIC INVESTMENTS INC',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_D',
                        'regis_id_held_by': 'COMP_D',
                        'percent': 12.13,
                        'direct_percent': 12.13,
                        'effective_percentage': 3.487,
                        'type_label': 'Company',
                        'company_name': 'ASIA PACIFIC HOLDINGS LTD'
                    }
                ],
                'company_id': 'COMP_B',
                'capital': '12,000,000,000',
                'business_type_en': 'Investment and Holdings'
            },
            'COMP_C': {
                'name_en': 'EUROPEAN FINANCIAL GROUP',
                'display_name': 'EUROPEAN FINANCIAL GROUP',
                'level': 1,
                'parent_percentage': 18.20,
                'shareholders': [
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 40.66,
                        'direct_percent': 40.66,
                        'effective_percentage': 7.40,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    },
                    {
                        'name': 'INTERNATIONAL EQUITY FUND',
                        'display_name': 'INTERNATIONAL EQUITY FUND',
                        'shareholder_type': 'company',
                        'regis_id': 'COMP_F',
                        'regis_id_held_by': 'COMP_F',
                        'percent': 46.70,
                        'direct_percent': 46.70,
                        'effective_percentage': 8.50,
                        'type_label': 'Company',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    },
                    {
                        'name': 'LUCAS BERGMANN',
                        'display_name': 'LUCAS BERGMANN',
                        'shareholder_type': 'personal',
                        'percent': 12.64,
                        'direct_percent': 12.64,
                        'effective_percentage': 2.30,
                        'nationality': 'German',
                        'type_label': 'Individual',
                        'company_name': 'EUROPEAN FINANCIAL GROUP'
                    }
                ],
                'company_id': 'COMP_C',
                'capital': '6,750,000,000',
                'business_type_en': 'Financial Services'
            },
            'COMP_D': {
                'name_en': 'STRATEGIC INVESTMENTS INC',
                'display_name': 'STRATEGIC INVESTMENTS INC',
                'level': 2,
                'parent_percentage': 3.487,
                'shareholders': [
                    {
                        'name': 'WILLIAM ANDERSON',
                        'display_name': 'WILLIAM ANDERSON',
                        'shareholder_type': 'personal',
                        'percent': 72.00,
                        'direct_percent': 72.00,
                        'effective_percentage': 2.51,
                        'nationality': 'American',
                        'type_label': 'Individual',
                        'company_name': 'STRATEGIC INVESTMENTS INC'
                    },
                    {
                        'name': 'DAVID KIM',
                        'display_name': 'DAVID KIM',
                        'shareholder_type': 'personal',
                        'percent': 28.00,
                        'direct_percent': 28.00,
                        'effective_percentage': 0.98,
                        'nationality': 'Korean',
                        'type_label': 'Individual',
                        'company_name': 'STRATEGIC INVESTMENTS INC'
                    }
                ],
                'company_id': 'COMP_D',
                'capital': '2,100,000,000',
                'business_type_en': 'Investment Services'
            },
            'COMP_E': {
                'name_en': 'VENTURE CAPITAL PARTNERS',
                'display_name': 'VENTURE CAPITAL PARTNERS',
                'level': 2,
                'parent_percentage': 8.165,
                'shareholders': [
                    {
                        'name': 'SOPHIA CHEN',
                        'display_name': 'SOPHIA CHEN',
                        'shareholder_type': 'personal',
                        'percent': 85.00,
                        'direct_percent': 85.00,
                        'effective_percentage': 6.94,
                        'nationality': 'Singaporean',
                        'type_label': 'Individual',
                        'company_name': 'VENTURE CAPITAL PARTNERS'
                    },
                    {
                        'name': 'ALEXANDER NOVAK',
                        'display_name': 'ALEXANDER NOVAK',
                        'shareholder_type': 'personal',
                        'percent': 15.00,
                        'direct_percent': 15.00,
                        'effective_percentage': 1.22,
                        'nationality': 'Russian',
                        'type_label': 'Individual',
                        'company_name': 'VENTURE CAPITAL PARTNERS'
                    }
                ],
                'company_id': 'COMP_E',
                'capital': '3,200,000,000',
                'business_type_en': 'Venture Capital'
            },
            'COMP_F': {
                'name_en': 'INTERNATIONAL EQUITY FUND',
                'display_name': 'INTERNATIONAL EQUITY FUND',
                'level': 2,
                'parent_percentage': 8.50,
                'shareholders': [
                    {
                        'name': 'EMILY RODRIGUEZ',
                        'display_name': 'EMILY RODRIGUEZ',
                        'shareholder_type': 'personal',
                        'percent': 100.00,
                        'direct_percent': 100.00,
                        'effective_percentage': 8.50,
                        'nationality': 'Spanish',
                        'type_label': 'Individual',
                        'company_name': 'INTERNATIONAL EQUITY FUND'
                    }
                ],
                'company_id': 'COMP_F',
                'capital': '4,500,000,000',
                'business_type_en': 'Investment Fund'
            }
        },
        'checklist': {
            'method_1_check': {
                'checked': True,
                'found_ubo': True,
                'companies_checked': 12,
                'max_level_reached': 3
            },
            'method_2_check': {
                'checked': True,
                'required': False
            }
        }
    }
    
    return mock_data

