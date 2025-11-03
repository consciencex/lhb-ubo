#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO System Test Script
สคริปต์ทดสอบระบบตรวจสอบ UBO
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ubo_system import UBOSystem
import json
from datetime import datetime

def test_single_company():
    """ทดสอบการวิเคราะห์บริษัทเดียว"""
    print("=== ทดสอบการวิเคราะห์บริษัทเดียว ===")
    
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    # สร้างระบบ UBO
    ubo_system = UBOSystem(API_KEY)
    
    # ทดสอบกับบริษัทตัวอย่าง
    registration_id = "0105565126796"  # บริษัทจากตัวอย่างที่ให้มา
    
    try:
        print(f"กำลังวิเคราะห์บริษัท: {registration_id}")
        result = ubo_system.analyze_single_company(registration_id)
        
        print(f"\n✅ ผลการวิเคราะห์:")
        print(f"   บริษัท: {result.company_name}")
        print(f"   เลขทะเบียน: {result.company_id}")
        print(f"   จำนวนผู้ถือหุ้นทั้งหมด: {result.total_shareholders}")
        print(f"   จำนวนหุ้นทั้งหมด: {result.total_shares:,}")
        print(f"   ระดับความเสี่ยง: {result.risk_level}")
        print(f"   สถานะการปฏิบัติตามกฎระเบียบ: {result.compliance_status}")
        
        print(f"\n📊 UBO ≥25% ({len(result.ubo_threshold_25)} คน):")
        for sh in result.ubo_threshold_25:
            print(f"   - {sh.name}: {sh.percent:.1f}% ({sh.share_amount:,} หุ้น)")
        
        print(f"\n📊 UBO ≥10% ({len(result.ubo_threshold_10)} คน):")
        for sh in result.ubo_threshold_10:
            print(f"   - {sh.name}: {sh.percent:.1f}% ({sh.share_amount:,} หุ้น)")
        
        print(f"\n👑 ผู้ควบคุม ≥50% ({len(result.control_persons)} คน):")
        for sh in result.control_persons:
            print(f"   - {sh.name}: {sh.percent:.1f}% ({sh.share_amount:,} หุ้น)")
        
        # สร้างรายงาน
        report = ubo_system.generate_report(result)
        
        # บันทึกรายงาน
        filename = f"test_report_{registration_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 รายงานถูกบันทึกเป็น: {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_multiple_companies():
    """ทดสอบการวิเคราะห์หลายบริษัท"""
    print("\n=== ทดสอบการวิเคราะห์หลายบริษัท ===")
    
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    # สร้างระบบ UBO
    ubo_system = UBOSystem(API_KEY)
    
    # รายการบริษัทสำหรับทดสอบ
    test_companies = [
        "0105565126796",  # บริษัทจากตัวอย่าง
        "0107562000386",  # บริษัทจากตัวอย่าง
    ]
    
    try:
        print(f"กำลังวิเคราะห์ {len(test_companies)} บริษัท...")
        results = ubo_system.analyze_multiple_companies(test_companies)
        
        print(f"\n✅ ผลการวิเคราะห์ {len(results)} บริษัท:")
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.company_name} ({result.company_id})")
            print(f"   ระดับความเสี่ยง: {result.risk_level}")
            print(f"   สถานะการปฏิบัติตาม: {result.compliance_status}")
            print(f"   UBO ≥25%: {len(result.ubo_threshold_25)} คน")
            print(f"   UBO ≥10%: {len(result.ubo_threshold_10)} คน")
            print(f"   ผู้ควบคุม: {len(result.control_persons)} คน")
        
        # ส่งออกเป็น Excel
        excel_filename = ubo_system.export_to_excel(results)
        print(f"\n💾 ผลลัพธ์ถูกส่งออกเป็น Excel: {excel_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_api_connection():
    """ทดสอบการเชื่อมต่อ API"""
    print("=== ทดสอบการเชื่อมต่อ API ===")
    
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    try:
        from ubo_system import EnliteAPIClient
        
        # สร้าง API Client
        api_client = EnliteAPIClient(API_KEY)
        
        # ทดสอบการเรียก API
        print("กำลังทดสอบการเชื่อมต่อ API...")
        company_data = api_client.get_company_data("0105565126796")
        
        if company_data:
            print("✅ การเชื่อมต่อ API สำเร็จ")
            print(f"   ได้รับข้อมูลบริษัท: {company_data.get('profile', {}).get('name_th_full', 'ไม่ระบุ')}")
            return True
        else:
            print("❌ ไม่ได้รับข้อมูลจาก API")
            return False
            
    except Exception as e:
        print(f"❌ การเชื่อมต่อ API ล้มเหลว: {e}")
        return False

def main():
    """ฟังก์ชันหลักสำหรับทดสอบ"""
    print("🚀 เริ่มทดสอบระบบ UBO Detection System")
    print("=" * 50)
    
    # ทดสอบการเชื่อมต่อ API
    api_test = test_api_connection()
    if not api_test:
        print("\n❌ การทดสอบหยุดลงเนื่องจากไม่สามารถเชื่อมต่อ API ได้")
        return
    
    # ทดสอบการวิเคราะห์บริษัทเดียว
    single_test = test_single_company()
    
    # ทดสอบการวิเคราะห์หลายบริษัท
    batch_test = test_multiple_companies()
    
    # สรุปผลการทดสอบ
    print("\n" + "=" * 50)
    print("📋 สรุปผลการทดสอบ:")
    print(f"   การเชื่อมต่อ API: {'✅ ผ่าน' if api_test else '❌ ไม่ผ่าน'}")
    print(f"   การวิเคราะห์บริษัทเดียว: {'✅ ผ่าน' if single_test else '❌ ไม่ผ่าน'}")
    print(f"   การวิเคราะห์หลายบริษัท: {'✅ ผ่าน' if batch_test else '❌ ไม่ผ่าน'}")
    
    if all([api_test, single_test, batch_test]):
        print("\n🎉 การทดสอบทั้งหมดผ่าน! ระบบพร้อมใช้งาน")
    else:
        print("\n⚠️  การทดสอบบางส่วนไม่ผ่าน กรุณาตรวจสอบข้อผิดพลาด")

if __name__ == "__main__":
    main()
