#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Correct UBO System
"""

from correct_ubo_system import analyze_company_ubo
import json

def test_correct_ubo_system():
    """ทดสอบระบบ UBO ใหม่"""
    print("🧪 ทดสอบระบบ UBO ใหม่")
    print("=" * 50)
    
    # ทดสอบกับ LH Bank
    company_id = "0107548000234"
    print(f"📊 วิเคราะห์บริษัท: {company_id}")
    
    # วิเคราะห์ UBO
    result = analyze_company_ubo(company_id)
    
    # แสดงผลลัพธ์
    print(f"\n✅ ผลการวิเคราะห์:")
    print(f"   - ชื่อบริษัท: {result.company_name}")
    print(f"   - ตรวจสอบบริษัท: {result.total_companies_checked} บริษัท")
    print(f"   - ระดับสูงสุด: {result.max_level_reached}")
    print(f"   - UBO ที่พบ: {len(result.final_ubos)} คน")
    
    # แสดงข้อมูล Level
    print(f"\n📈 สรุปข้อมูล Level:")
    level_counts = {}
    for company_id, company_data in result.hierarchy.items():
        level = company_data.get('level', 0)
        level_counts[level] = level_counts.get(level, 0) + 1
    
    for level in sorted(level_counts.keys()):
        print(f"   - Level {level}: {level_counts[level]} บริษัท")
    
    # แสดงผู้ถือหุ้นแต่ละ Level
    print(f"\n👥 ผู้ถือหุ้นแต่ละ Level:")
    for level in sorted(level_counts.keys()):
        print(f"\n   Level {level}:")
        for company_id, company_data in result.hierarchy.items():
            if company_data.get('level') == level:
                shareholders = company_data.get('shareholders', [])
                print(f"     📍 {company_data.get('name_th', 'ไม่ระบุ')} ({company_id})")
                for sh in shareholders[:5]:  # แสดงแค่ 5 คนแรก
                    name = f"{sh.get('firstname', '')} {sh.get('lastname', '')}".strip()
                    percent = sh.get('effective_percentage', 0)
                    sh_type = sh.get('shareholder_type', 'personal')
                    print(f"       - {name}: {percent:.2f}% ({sh_type})")
                if len(shareholders) > 5:
                    print(f"       ... และอีก {len(shareholders) - 5} คน")
    
    # แสดง UBO
    print(f"\n👑 UBO ที่พบ:")
    if result.final_ubos:
        for i, ubo in enumerate(result.final_ubos, 1):
            print(f"   {i}. {ubo.name}: {ubo.total_percentage:.2f}%")
    else:
        print("   ไม่พบ UBO ที่ผ่านเกณฑ์ ≥15%")
    
    # บันทึกผลลัพธ์
    result_dict = {
        'registration_id': result.registration_id,
        'company_name': result.company_name,
        'total_companies_checked': result.total_companies_checked,
        'max_level_reached': result.max_level_reached,
        'ubos_found': len(result.final_ubos),
        'level_summary': level_counts,
        'hierarchy': result.hierarchy,
        'final_ubos': [ubo.__dict__ for ubo in result.final_ubos]
    }
    
    with open('correct_ubo_test_result.json', 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกผลลัพธ์ใน: correct_ubo_test_result.json")
    print("=" * 50)

if __name__ == "__main__":
    test_correct_ubo_system()
