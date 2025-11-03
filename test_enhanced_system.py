#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced UBO System - Complete Test Suite
ชุดทดสอบระบบ Enhanced UBO ที่สมบูรณ์
"""

import sys
import os
import json
import time
from datetime import datetime

# Import Enhanced UBO System
from enhanced_ubo_system import EnhancedUBOSystem

def test_api_connection():
    """ทดสอบการเชื่อมต่อ API"""
    print("🔌 ทดสอบการเชื่อมต่อ API")
    print("-" * 40)
    
    try:
        API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
        ubo_system = EnhancedUBOSystem(API_KEY)
        
        # ทดสอบกับบริษัทที่รู้จัก
        test_company = "0107548000234"  # LAND AND HOUSES BANK
        
        print(f"📡 กำลังทดสอบ API กับบริษัท: {test_company}")
        
        # เรียก API โดยตรง
        company_data = ubo_system.api_client.get_company_data(test_company)
        
        if company_data:
            print("✅ API Connection สำเร็จ!")
            profile = company_data.get('profile', {})
            print(f"   ชื่อบริษัท: {profile.get('name_th_full', 'ไม่ระบุ')}")
            print(f"   เลขทะเบียน: {profile.get('regis_id', 'ไม่ระบุ')}")
            print(f"   สถานะ: {profile.get('company_status', 'ไม่ระบุ')}")
            return True
        else:
            print("❌ API Connection ล้มเหลว")
            return False
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_enhanced_analysis():
    """ทดสอบการวิเคราะห์แบบ Enhanced"""
    print("\n🔍 ทดสอบการวิเคราะห์แบบ Enhanced")
    print("-" * 40)
    
    try:
        API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
        ubo_system = EnhancedUBOSystem(API_KEY)
        
        # ทดสอบกับ LAND AND HOUSES BANK
        test_company = "0107548000234"
        
        print(f"📊 กำลังวิเคราะห์บริษัท: {test_company}")
        
        # วิเคราะห์บริษัท
        result = ubo_system.analyze_company_hierarchy(test_company)
        
        print("✅ การวิเคราะห์สำเร็จ!")
        print(f"   บริษัท: {result.company_name}")
        print(f"   วิธีที่ใช้: {result.method_used}")
        print(f"   ระดับสูงสุด: {result.max_level_reached}")
        print(f"   บริษัทที่ตรวจสอบ: {result.total_companies_checked}")
        print(f"   ระดับความเสี่ยง: {result.risk_level}")
        print(f"   สถานะการปฏิบัติตาม: {result.compliance_status}")
        print(f"   จำนวน UBO: {len(result.final_ubos)}")
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_report_generation():
    """ทดสอบการสร้างรายงาน"""
    print("\n📄 ทดสอบการสร้างรายงาน")
    print("-" * 40)
    
    try:
        API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
        ubo_system = EnhancedUBOSystem(API_KEY)
        
        # วิเคราะห์บริษัท
        test_company = "0107548000234"
        result = ubo_system.analyze_company_hierarchy(test_company)
        
        # สร้างรายงาน
        report = ubo_system.generate_enhanced_report(result)
        
        print("✅ การสร้างรายงานสำเร็จ!")
        print(f"   ข้อมูลบริษัท: {report['company_info']['name']}")
        print(f"   สรุปการวิเคราะห์: {report['analysis_summary']['method_used']}")
        print(f"   ผล UBO: {report['ubo_results']['final_ubos']} คน")
        print(f"   มีแผนภูมิ: {'ใช่' if report['charts']['hierarchy'] else 'ไม่'}")
        print(f"   มี Checklist: {'ใช่' if report['charts']['checklist'] else 'ไม่'}")
        
        # บันทึกรายงาน
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"test_report_{test_company}_{timestamp}.json"
        
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 รายงานถูกบันทึกเป็น: {report_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_multiple_companies():
    """ทดสอบการวิเคราะห์หลายบริษัท"""
    print("\n🏢 ทดสอบการวิเคราะห์หลายบริษัท")
    print("-" * 40)
    
    try:
        API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
        ubo_system = EnhancedUBOSystem(API_KEY)
        
        # ทดสอบกับหลายบริษัท
        test_companies = [
            "0107548000234",  # LAND AND HOUSES BANK
            "0105565126796",  # CONSCIENCE X
            "0107562000386"   # CENTRAL RETAIL
        ]
        
        print(f"📊 กำลังวิเคราะห์ {len(test_companies)} บริษัท")
        
        results = []
        for company_id in test_companies:
            try:
                print(f"   🔍 วิเคราะห์: {company_id}")
                result = ubo_system.analyze_company_hierarchy(company_id)
                results.append(result)
                print(f"      ✅ สำเร็จ - UBO: {len(result.final_ubos)} คน")
            except Exception as e:
                print(f"      ❌ ล้มเหลว: {e}")
        
        print(f"✅ การวิเคราะห์หลายบริษัทสำเร็จ!")
        print(f"   บริษัทที่วิเคราะห์ได้: {len(results)}/{len(test_companies)}")
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_web_app():
    """ทดสอบ Web Application"""
    print("\n🌐 ทดสอบ Web Application")
    print("-" * 40)
    
    try:
        # ตรวจสอบไฟล์ Web App
        required_files = [
            "enhanced_app.py",
            "templates/enhanced_index.html"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ พบไฟล์: {file}")
            else:
                print(f"❌ ไม่พบไฟล์: {file}")
                return False
        
        print("✅ Web Application files พร้อมใช้งาน")
        print("   เริ่มต้นได้ด้วย: python3 enhanced_app.py")
        print("   เข้าถึงได้ที่: http://localhost:4444")
        
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return False

def run_complete_test():
    """รันการทดสอบทั้งหมด"""
    print("🧪 Enhanced UBO System - Complete Test Suite")
    print("=" * 60)
    print(f"📅 วันที่ทดสอบ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    tests = [
        ("API Connection", test_api_connection),
        ("Enhanced Analysis", test_enhanced_analysis),
        ("Report Generation", test_report_generation),
        ("Multiple Companies", test_multiple_companies),
        ("Web Application", test_web_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔍 กำลังทดสอบ: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: ผ่าน")
            else:
                print(f"❌ {test_name}: ไม่ผ่าน")
        except Exception as e:
            print(f"❌ {test_name}: เกิดข้อผิดพลาด - {e}")
            results.append((test_name, False))
        
        print("")
        time.sleep(1)  # หน่วงเวลาเล็กน้อย
    
    # สรุปผลการทดสอบ
    print("📊 สรุปผลการทดสอบ")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ผ่าน" if result else "❌ ไม่ผ่าน"
        print(f"   {test_name}: {status}")
    
    print("")
    print(f"🎯 ผลการทดสอบ: {passed}/{total} ผ่าน")
    
    if passed == total:
        print("🎉 การทดสอบทั้งหมดผ่าน! ระบบพร้อมใช้งาน")
        print("")
        print("🚀 วิธีเริ่มต้นใช้งาน:")
        print("   1. รัน Web App: python3 enhanced_app.py")
        print("   2. เปิดเบราว์เซอร์: http://localhost:4444")
        print("   3. ใส่เลขทะเบียนบริษัทและคลิกวิเคราะห์")
        print("")
        print("📚 เอกสารเพิ่มเติม:")
        print("   - README.md: คู่มือการใช้งาน")
        print("   - USAGE.md: คำแนะนำการใช้งาน")
        print("   - PROJECT_SUMMARY.md: สรุปโปรเจค")
    else:
        print("⚠️  การทดสอบบางส่วนไม่ผ่าน กรุณาตรวจสอบข้อผิดพลาด")
    
    return passed == total

def main():
    """ฟังก์ชันหลัก"""
    try:
        success = run_complete_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 หยุดการทดสอบ")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดในการทดสอบ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
