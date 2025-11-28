#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6-Tier UBO Scenario Test
=========================

This script tests the 6-Tier shareholding analysis by creating a mock scenario
where UBO is found at Tier 6 (Level 6).

Chain Structure:
    Main Company (Level 0) - 100%
        └─ Holding L1 (Level 1) - 100%
            └─ Holding L2 (Level 2) - 100%
                └─ Holding L3 (Level 3) - 100%
                    └─ Holding L4 (Level 4) - 100%
                        └─ Holding L5 (Level 5) - 100%
                            ├─ MR. DEEP SHAREHOLDER (25%) → UBO ✅
                            ├─ MS. HIDDEN OWNER (20%) → UBO ✅
                            ├─ MR. THRESHOLD HOLDER (15%) → UBO ✅
                            ├─ MS. BELOW THRESHOLD (14%) → Not UBO
                            ├─ MR. SMALL HOLDER (10%) → Not UBO
                            └─ MR. MINORITY (16%) → UBO ✅

Effective % Calculation:
    100% × 100% × 100% × 100% × 100% × Direct% = Direct%

Expected UBOs (≥15%):
    1. MR. DEEP SHAREHOLDER: 25%
    2. MS. HIDDEN OWNER: 20%
    3. MR. MINORITY: 16%
    4. MR. THRESHOLD HOLDER: 15%

Usage:
    python3 test_6tier_scenario.py
"""

import json
import sys
import os
from datetime import datetime
from collections import deque
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==============================================================================
# MOCK DATA - 6-Tier Scenario (UBO at Tier 6)
# ==============================================================================

MOCK_COMPANIES = {
    # Level 0 - Main Company
    "DEMO_MAIN_001": {
        "display_name": "DEMO BANK PUBLIC COMPANY LIMITED",
        "name_th_full": "บริษัท เดโม แบงค์ จำกัด (มหาชน)",
        "name_en": "DEMO BANK PUBLIC COMPANY LIMITED",
        "business_type": "Banking",
        "capital": "50,000,000,000",
        "regis_date": "01 Jan 2000",
        "status": "Active",
        "level": 0,
        "official_signatory": "นายทดสอบ ระบบหกชั้น และ นางสาวตรวจสอบ ยูบีโอ กรรมการสองคนลงลายมือชื่อร่วมกัน",
        "directors": [
            {"title": "นาย", "firstname": "ทดสอบ", "lastname": "ระบบหกชั้น"},
            {"title": "นางสาว", "firstname": "ตรวจสอบ", "lastname": "ยูบีโอ"},
            {"title": "นาย", "firstname": "กรรมการ", "lastname": "ทดสอบ"}
        ],
        "shareholders": [
            {
                "display_name": "HOLDING COMPANY LEVEL 1 CO., LTD.",
                "firstname": "",
                "lastname": "",
                "nationality": "Thai",
                "share_amount": 50000000,
                "percent": 100.0,
                "shareholder_type": "company",
                "regis_id": "HOLD_L1_001"
            }
        ]
    },
    
    # Level 1 - Holding L1
    "HOLD_L1_001": {
        "display_name": "HOLDING COMPANY LEVEL 1 CO., LTD.",
        "name_th_full": "บริษัท โฮลดิ้ง ระดับ 1 จำกัด",
        "name_en": "HOLDING COMPANY LEVEL 1 CO., LTD.",
        "business_type": "Holding Company",
        "capital": "10,000,000,000",
        "regis_date": "15 Mar 2005",
        "status": "Active",
        "level": 1,
        "directors": [],
        "shareholders": [
            {
                "display_name": "HOLDING COMPANY LEVEL 2 CO., LTD.",
                "firstname": "",
                "lastname": "",
                "nationality": "Thai",
                "share_amount": 10000000,
                "percent": 100.0,
                "shareholder_type": "company",
                "regis_id": "HOLD_L2_001"
            }
        ]
    },
    
    # Level 2 - Holding L2
    "HOLD_L2_001": {
        "display_name": "HOLDING COMPANY LEVEL 2 CO., LTD.",
        "name_th_full": "บริษัท โฮลดิ้ง ระดับ 2 จำกัด",
        "name_en": "HOLDING COMPANY LEVEL 2 CO., LTD.",
        "business_type": "Holding Company",
        "capital": "5,000,000,000",
        "regis_date": "20 Jun 2008",
        "status": "Active",
        "level": 2,
        "directors": [],
        "shareholders": [
            {
                "display_name": "HOLDING COMPANY LEVEL 3 CO., LTD.",
                "firstname": "",
                "lastname": "",
                "nationality": "Thai",
                "share_amount": 5000000,
                "percent": 100.0,
                "shareholder_type": "company",
                "regis_id": "HOLD_L3_001"
            }
        ]
    },
    
    # Level 3 - Holding L3
    "HOLD_L3_001": {
        "display_name": "HOLDING COMPANY LEVEL 3 CO., LTD.",
        "name_th_full": "บริษัท โฮลดิ้ง ระดับ 3 จำกัด",
        "name_en": "HOLDING COMPANY LEVEL 3 CO., LTD.",
        "business_type": "Holding Company",
        "capital": "2,000,000,000",
        "regis_date": "10 Sep 2010",
        "status": "Active",
        "level": 3,
        "directors": [],
        "shareholders": [
            {
                "display_name": "HOLDING COMPANY LEVEL 4 CO., LTD.",
                "firstname": "",
                "lastname": "",
                "nationality": "Thai",
                "share_amount": 2000000,
                "percent": 100.0,
                "shareholder_type": "company",
                "regis_id": "HOLD_L4_001"
            }
        ]
    },
    
    # Level 4 - Holding L4
    "HOLD_L4_001": {
        "display_name": "HOLDING COMPANY LEVEL 4 CO., LTD.",
        "name_th_full": "บริษัท โฮลดิ้ง ระดับ 4 จำกัด",
        "name_en": "HOLDING COMPANY LEVEL 4 CO., LTD.",
        "business_type": "Holding Company",
        "capital": "1,000,000,000",
        "regis_date": "05 Dec 2012",
        "status": "Active",
        "level": 4,
        "directors": [],
        "shareholders": [
            {
                "display_name": "HOLDING COMPANY LEVEL 5 CO., LTD.",
                "firstname": "",
                "lastname": "",
                "nationality": "Thai",
                "share_amount": 1000000,
                "percent": 100.0,
                "shareholder_type": "company",
                "regis_id": "HOLD_L5_001"
            }
        ]
    },
    
    # Level 5 - Holding L5 (contains Tier 6 shareholders = UBOs)
    "HOLD_L5_001": {
        "display_name": "HOLDING COMPANY LEVEL 5 CO., LTD.",
        "name_th_full": "บริษัท โฮลดิ้ง ระดับ 5 จำกัด",
        "name_en": "HOLDING COMPANY LEVEL 5 CO., LTD.",
        "business_type": "Holding Company",
        "capital": "500,000,000",
        "regis_date": "15 Feb 2015",
        "status": "Active",
        "level": 5,
        "directors": [],
        "shareholders": [
            # Tier 6 - Personal Shareholders (UBOs)
            {
                "display_name": "MR. DEEP SHAREHOLDER",
                "firstname": "DEEP",
                "lastname": "SHAREHOLDER",
                "nationality": "Thai",
                "share_amount": 125000,
                "percent": 25.0,  # UBO ≥15% ✅
                "shareholder_type": "personal",
                "regis_id": ""
            },
            {
                "display_name": "MS. HIDDEN OWNER",
                "firstname": "HIDDEN",
                "lastname": "OWNER",
                "nationality": "Singaporean",
                "share_amount": 100000,
                "percent": 20.0,  # UBO ≥15% ✅
                "shareholder_type": "personal",
                "regis_id": ""
            },
            {
                "display_name": "MR. MINORITY",
                "firstname": "MINORITY",
                "lastname": "HOLDER",
                "nationality": "Thai",
                "share_amount": 80000,
                "percent": 16.0,  # UBO ≥15% ✅
                "shareholder_type": "personal",
                "regis_id": ""
            },
            {
                "display_name": "MR. THRESHOLD HOLDER",
                "firstname": "THRESHOLD",
                "lastname": "HOLDER",
                "nationality": "American",
                "share_amount": 75000,
                "percent": 15.0,  # UBO exactly at threshold ✅
                "shareholder_type": "personal",
                "regis_id": ""
            },
            {
                "display_name": "MS. BELOW THRESHOLD",
                "firstname": "BELOW",
                "lastname": "THRESHOLD",
                "nationality": "Thai",
                "share_amount": 70000,
                "percent": 14.0,  # Not UBO (< 15%)
                "shareholder_type": "personal",
                "regis_id": ""
            },
            {
                "display_name": "MR. SMALL HOLDER",
                "firstname": "SMALL",
                "lastname": "HOLDER",
                "nationality": "Thai",
                "share_amount": 50000,
                "percent": 10.0,  # Not UBO (< 15%)
                "shareholder_type": "personal",
                "regis_id": ""
            }
        ]
    }
}


# ==============================================================================
# 6-Tier UBO Analyzer (Simplified for Testing)
# ==============================================================================

class SixTierUBOAnalyzer:
    """Simplified 6-Tier UBO Analyzer for testing mock data."""
    
    def __init__(self, mock_data: Dict[str, Any]):
        self.mock_data = mock_data
        self.max_levels = 7  # Level 0-6 (6 Tiers)
        self.threshold = 15.0
        
    def get_company_data(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get company data from mock."""
        return self.mock_data.get(company_id)
    
    def analyze(self, main_company_id: str) -> Dict[str, Any]:
        """Run 6-Tier BFS analysis."""
        
        ubo_candidates = {}  # name -> {total_percentage, paths, nationality, ...}
        hierarchy = {}
        
        # BFS Queue: (company_id, effective_percentage, level, path_chain)
        processing_queue = deque([(main_company_id, 100.0, 0, [])])
        visited = set()
        
        print(f"\n{'='*60}")
        print(f"🔍 Starting 6-Tier BFS Analysis")
        print(f"{'='*60}")
        print(f"Main Company: {main_company_id}")
        print(f"Max Levels: {self.max_levels} (Level 0-6)")
        print(f"UBO Threshold: {self.threshold}%")
        print(f"{'='*60}\n")
        
        while processing_queue:
            company_id, effective_pct, level, path_chain = processing_queue.popleft()
            
            # Check max level
            if level >= self.max_levels:
                print(f"  ⛔ Max level reached for {company_id}")
                continue
            
            # Check visited
            if company_id in visited:
                print(f"  ⚠️ Already visited: {company_id}")
                continue
            visited.add(company_id)
            
            # Get company data
            company_data = self.get_company_data(company_id)
            if not company_data:
                print(f"  ❌ No data for: {company_id}")
                continue
            
            # Store in hierarchy
            hierarchy[company_id] = {
                **company_data,
                'effective_percentage': effective_pct
            }
            
            company_name = company_data.get('display_name', company_id)
            shareholders = company_data.get('shareholders', [])
            
            print(f"📦 Level {level}: {company_name}")
            print(f"   Effective: {effective_pct:.4f}%")
            print(f"   Shareholders: {len(shareholders)}")
            
            # Process shareholders
            for sh in shareholders:
                sh_name = sh.get('display_name', 'Unknown')
                sh_type = sh.get('shareholder_type', 'personal')
                direct_pct = sh.get('percent', 0)
                sh_effective = effective_pct * (direct_pct / 100.0)
                
                if sh_type == 'personal':
                    # Personal shareholder - check UBO
                    tier = level + 1
                    print(f"   👤 [Tier {tier}] {sh_name}: {direct_pct}% direct, {sh_effective:.4f}% effective")
                    
                    if sh_name not in ubo_candidates:
                        ubo_candidates[sh_name] = {
                            'name': sh_name,
                            'total_percentage': 0,
                            'paths': [],
                            'nationality': sh.get('nationality', 'Unknown'),
                            'is_director': False
                        }
                    
                    ubo_candidates[sh_name]['total_percentage'] += sh_effective
                    ubo_candidates[sh_name]['paths'].append({
                        'chain': path_chain + [company_name, sh_name],
                        'direct': direct_pct,
                        'effective': sh_effective,
                        'tier': tier
                    })
                    
                    if sh_effective >= self.threshold:
                        print(f"      ✅ UBO FOUND! ({sh_effective:.2f}% ≥ {self.threshold}%)")
                    
                elif sh_type == 'company':
                    # Company shareholder - add to queue
                    sh_regis = sh.get('regis_id', '')
                    if sh_regis and level + 1 < self.max_levels:
                        print(f"   🏢 {sh_name}: {direct_pct}% → Queue (Level {level + 1})")
                        processing_queue.append((
                            sh_regis,
                            sh_effective,
                            level + 1,
                            path_chain + [company_name]
                        ))
            
            print()
        
        # Filter UBOs (≥15%)
        ubos = [
            ubo for ubo in ubo_candidates.values()
            if ubo['total_percentage'] >= self.threshold
        ]
        ubos.sort(key=lambda x: x['total_percentage'], reverse=True)
        
        return {
            'ubos': ubos,
            'hierarchy': hierarchy,
            'all_candidates': ubo_candidates
        }


# ==============================================================================
# Main Test Runner
# ==============================================================================

def run_test():
    """Run 6-Tier scenario test."""
    
    print("\n" + "="*70)
    print("🧪 6-TIER UBO SCENARIO TEST")
    print("="*70)
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Initialize analyzer
    analyzer = SixTierUBOAnalyzer(MOCK_COMPANIES)
    
    # Run analysis
    result = analyzer.analyze("DEMO_MAIN_001")
    
    # Display results
    print("\n" + "="*70)
    print("📊 ANALYSIS RESULTS")
    print("="*70)
    
    ubos = result['ubos']
    print(f"\n✅ UBOs Found (≥15%): {len(ubos)}")
    print("-" * 50)
    
    for i, ubo in enumerate(ubos, 1):
        print(f"\n{i}. {ubo['name']}")
        print(f"   Total Effective: {ubo['total_percentage']:.2f}%")
        print(f"   Nationality: {ubo['nationality']}")
        print(f"   Paths: {len(ubo['paths'])}")
        for path in ubo['paths']:
            print(f"      • Tier {path['tier']}: {' → '.join(path['chain'])}")
            print(f"        Direct: {path['direct']}%, Effective: {path['effective']:.4f}%")
    
    # Verify expected results
    print("\n" + "="*70)
    print("✅ VERIFICATION")
    print("="*70)
    
    expected_ubos = {
        "MR. DEEP SHAREHOLDER": 25.0,
        "MS. HIDDEN OWNER": 20.0,
        "MR. MINORITY": 16.0,
        "MR. THRESHOLD HOLDER": 15.0
    }
    
    found_ubos = {ubo['name']: ubo['total_percentage'] for ubo in ubos}
    
    all_pass = True
    for name, expected_pct in expected_ubos.items():
        actual_pct = found_ubos.get(name, 0)
        status = "✅ PASS" if abs(actual_pct - expected_pct) < 0.01 else "❌ FAIL"
        if status == "❌ FAIL":
            all_pass = False
        print(f"{status}: {name} - Expected: {expected_pct}%, Got: {actual_pct:.2f}%")
    
    # Check that below-threshold holders are NOT in UBO list
    below_threshold = ["MS. BELOW THRESHOLD", "MR. SMALL HOLDER"]
    for name in below_threshold:
        if name in found_ubos:
            print(f"❌ FAIL: {name} should NOT be UBO (below threshold)")
            all_pass = False
        else:
            print(f"✅ PASS: {name} correctly excluded (below threshold)")
    
    print("\n" + "="*70)
    if all_pass:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️ SOME TESTS FAILED!")
    print("="*70)
    
    # Summary statistics
    print("\n📈 SUMMARY STATISTICS")
    print("-" * 50)
    print(f"Total Companies Traversed: {len(result['hierarchy'])}")
    print(f"Total Personal Shareholders Found: {len(result['all_candidates'])}")
    print(f"UBOs (≥15%): {len(ubos)}")
    print(f"Below Threshold: {len(result['all_candidates']) - len(ubos)}")
    
    # Level breakdown
    level_counts = {}
    for company_id, company_data in result['hierarchy'].items():
        level = company_data.get('level', 0)
        level_counts[level] = level_counts.get(level, 0) + 1
    
    print("\n📊 COMPANIES BY LEVEL:")
    for level in sorted(level_counts.keys()):
        print(f"   Level {level}: {level_counts[level]} companies")
    
    print("\n" + "="*70)
    print(f"Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    return all_pass


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)

