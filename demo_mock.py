#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO System Demo with Mock Data
สาธิตระบบตรวจสอบ UBO ด้วยข้อมูลจำลอง
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ubo_system import UBOSystem, Shareholder, UBOCheckResult
import json
from datetime import datetime

def create_mock_data():
    """สร้างข้อมูลจำลองสำหรับทดสอบ"""
    # สร้างข้อมูลผู้ถือหุ้นจำลอง
    mock_shareholders = [
        Shareholder(
            name="นายสมชาย ใจดี",
            firstname="สมชาย",
            lastname="ใจดี",
            nationality="Thai",
            share_amount=300000,
            percent=30.0,
            shareholder_type="personal",
            regis_id="1234567890123",
            business_status="Active",
            directorship="YES",
            director_update_date="01 Jan 2024"
        ),
        Shareholder(
            name="นางสมหญิง รักดี",
            firstname="สมหญิง",
            lastname="รักดี",
            nationality="Thai",
            share_amount=250000,
            percent=25.0,
            shareholder_type="personal",
            regis_id="1234567890124",
            business_status="Active",
            directorship="YES",
            director_update_date="01 Jan 2024"
        ),
        Shareholder(
            name="บริษัท เทคโนโลยี จำกัด",
            firstname="",
            lastname="",
            nationality="Thai",
            share_amount=200000,
            percent=20.0,
            shareholder_type="corporate",
            regis_id="0101234567890",
            business_status="Active",
            directorship="NO",
            director_update_date=""
        ),
        Shareholder(
            name="นายสมศักดิ์ เก่งมาก",
            firstname="สมศักดิ์",
            lastname="เก่งมาก",
            nationality="Thai",
            share_amount=150000,
            percent=15.0,
            shareholder_type="personal",
            regis_id="1234567890125",
            business_status="Active",
            directorship="NO",
            director_update_date=""
        ),
        Shareholder(
            name="นางสมพร สวยงาม",
            firstname="สมพร",
            lastname="สวยงาม",
            nationality="Thai",
            share_amount=100000,
            percent=10.0,
            shareholder_type="personal",
            regis_id="1234567890126",
            business_status="Active",
            directorship="NO",
            director_update_date=""
        )
    ]
    
    return mock_shareholders

def demo_with_mock_data():
    """สาธิตระบบด้วยข้อมูลจำลอง"""
    print("🚀 UBO Detection System - Demo with Mock Data")
    print("=" * 60)
    
    # สร้างระบบ UBO
    print("📋 กำลังสร้างระบบ UBO...")
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    ubo_system = UBOSystem(API_KEY)
    
    # สร้างข้อมูลจำลอง
    mock_shareholders = create_mock_data()
    
    # สร้างผลลัพธ์ UBO จำลอง
    mock_result = UBOCheckResult(
        company_id="0107548000234",
        company_name="บริษัท ตัวอย่าง จำกัด",
        check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ubo_threshold_25=[sh for sh in mock_shareholders if sh.percent >= 25.0],
        ubo_threshold_10=[sh for sh in mock_shareholders if sh.percent >= 10.0],
        control_persons=[sh for sh in mock_shareholders if sh.percent >= 50.0],
        total_shares=1000000,
        total_shareholders=len(mock_shareholders),
        hierarchy_levels=1,
        risk_level="MEDIUM",
        compliance_status="COMPLIANT"
    )
    
    try:
        print(f"🔍 กำลังวิเคราะห์บริษัท: {mock_result.company_id}")
        print("-" * 40)
        
        # แสดงผลการวิเคราะห์
        print(f"✅ ผลการวิเคราะห์ UBO")
        print(f"   🏢 บริษัท: {mock_result.company_name}")
        print(f"   🆔 เลขทะเบียน: {mock_result.company_id}")
        print(f"   📅 วันที่ตรวจสอบ: {mock_result.check_date}")
        print(f"   👥 จำนวนผู้ถือหุ้นทั้งหมด: {mock_result.total_shareholders}")
        print(f"   📊 จำนวนหุ้นทั้งหมด: {mock_result.total_shares:,}")
        print(f"   ⚠️  ระดับความเสี่ยง: {mock_result.risk_level}")
        print(f"   ✅ สถานะการปฏิบัติตามกฎระเบียบ: {mock_result.compliance_status}")
        
        # แสดงรายละเอียด UBO
        print(f"\n📊 รายละเอียดผู้ถือหุ้น")
        print("-" * 40)
        
        if mock_result.ubo_threshold_25:
            print(f"🔴 UBO ≥25% ({len(mock_result.ubo_threshold_25)} คน):")
            for i, sh in enumerate(mock_result.ubo_threshold_25, 1):
                print(f"   {i}. {sh.name}")
                print(f"      สัญชาติ: {sh.nationality}")
                print(f"      หุ้น: {sh.share_amount:,} ({sh.percent:.1f}%)")
                print(f"      ประเภท: {sh.shareholder_type}")
                if sh.directorship:
                    print(f"      เป็นกรรมการ: {sh.directorship}")
                print()
        else:
            print("🔴 UBO ≥25%: ไม่พบ")
        
        if mock_result.ubo_threshold_10:
            print(f"🟡 UBO ≥10% ({len(mock_result.ubo_threshold_10)} คน):")
            for i, sh in enumerate(mock_result.ubo_threshold_10, 1):
                print(f"   {i}. {sh.name}")
                print(f"      สัญชาติ: {sh.nationality}")
                print(f"      หุ้น: {sh.share_amount:,} ({sh.percent:.1f}%)")
                print(f"      ประเภท: {sh.shareholder_type}")
                if sh.directorship:
                    print(f"      เป็นกรรมการ: {sh.directorship}")
                print()
        else:
            print("🟡 UBO ≥10%: ไม่พบ")
        
        if mock_result.control_persons:
            print(f"👑 ผู้ควบคุม ≥50% ({len(mock_result.control_persons)} คน):")
            for i, sh in enumerate(mock_result.control_persons, 1):
                print(f"   {i}. {sh.name}")
                print(f"      สัญชาติ: {sh.nationality}")
                print(f"      หุ้น: {sh.share_amount:,} ({sh.percent:.1f}%)")
                print(f"      ประเภท: {sh.shareholder_type}")
                if sh.directorship:
                    print(f"      เป็นกรรมการ: {sh.directorship}")
                print()
        else:
            print("👑 ผู้ควบคุม ≥50%: ไม่พบ")
        
        # สร้างรายงาน
        print("📄 กำลังสร้างรายงาน...")
        report = ubo_system.generate_report(mock_result)
        
        # บันทึกรายงาน
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"mock_ubo_report_{mock_result.company_id}_{timestamp}.json"
        
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 รายงานถูกบันทึกเป็น: {report_filename}")
        
        # ส่งออกเป็น Excel
        print("📊 กำลังส่งออกเป็น Excel...")
        excel_filename = ubo_system.export_to_excel([mock_result])
        print(f"📈 ไฟล์ Excel: {excel_filename}")
        
        # แสดงสรุปการตรวจสอบ
        print(f"\n📋 สรุปการตรวจสอบ UBO")
        print("=" * 60)
        
        # Checklist การตรวจสอบ
        checklist_items = [
            ("สถานะบริษัท", mock_result.company_name != ""),
            ("จำนวนผู้ถือหุ้น", mock_result.total_shareholders > 0),
            ("UBO ≥25%", len(mock_result.ubo_threshold_25) > 0),
            ("UBO ≥10%", len(mock_result.ubo_threshold_10) > 0),
            ("ผู้ควบคุม ≥50%", len(mock_result.control_persons) > 0),
            ("การประเมินความเสี่ยง", mock_result.risk_level != ""),
            ("สถานะการปฏิบัติตาม", mock_result.compliance_status != "")
        ]
        
        for item, status in checklist_items:
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {item}")
        
        # คำแนะนำ
        print(f"\n💡 คำแนะนำ:")
        if mock_result.risk_level == "HIGH":
            print("   ⚠️  ระดับความเสี่ยงสูง - ควรตรวจสอบเพิ่มเติม")
        elif mock_result.risk_level == "MEDIUM":
            print("   ⚠️  ระดับความเสี่ยงปานกลาง - ควรติดตาม")
        else:
            print("   ✅ ระดับความเสี่ยงต่ำ - ปกติ")
        
        if mock_result.compliance_status == "REVIEW_REQUIRED":
            print("   🔍 ต้องตรวจสอบเพิ่มเติม")
        elif mock_result.compliance_status == "NON_COMPLIANT":
            print("   ❌ ไม่ปฏิบัติตามกฎระเบียบ")
        else:
            print("   ✅ ปฏิบัติตามกฎระเบียบ")
        
        print(f"\n🎉 การวิเคราะห์เสร็จสิ้น!")
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        print(f"   ประเภทข้อผิดพลาด: {type(e).__name__}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    success = demo_with_mock_data()
    
    if success:
        print(f"\n✅ การสาธิตสำเร็จ! ระบบพร้อมใช้งาน")
        print(f"🌐 สำหรับ Web Interface ให้รัน: python app.py")
        print(f"📝 หมายเหตุ: ข้อมูลนี้เป็นข้อมูลจำลองสำหรับการสาธิต")
    else:
        print(f"\n❌ การสาธิตล้มเหลว กรุณาตรวจสอบข้อผิดพลาด")

if __name__ == "__main__":
    main()
