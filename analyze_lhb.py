#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO Analysis for LAND AND HOUSES BANK (0107548000234)
การวิเคราะห์ UBO สำหรับธนาคารแลนด์ แอนด์ เฮาส์
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ubo_system import UBOSystem
import json
from datetime import datetime

def analyze_land_houses_bank():
    """วิเคราะห์ UBO สำหรับธนาคารแลนด์ แอนด์ เฮาส์"""
    print("🏦 UBO Analysis - LAND AND HOUSES BANK")
    print("=" * 60)
    
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    # สร้างระบบ UBO
    print("📋 กำลังสร้างระบบ UBO...")
    ubo_system = UBOSystem(API_KEY)
    
    # บริษัทที่ต้องการวิเคราะห์
    company_id = "0107548000234"  # LAND AND HOUSES BANK
    
    try:
        print(f"🔍 กำลังวิเคราะห์บริษัท: {company_id}")
        print("-" * 40)
        
        # วิเคราะห์บริษัท
        result = ubo_system.analyze_single_company(company_id)
        
        # แสดงผลการวิเคราะห์
        print(f"✅ ผลการวิเคราะห์ UBO")
        print(f"   🏢 บริษัท: {result.company_name}")
        print(f"   🆔 เลขทะเบียน: {result.company_id}")
        print(f"   📅 วันที่ตรวจสอบ: {result.check_date}")
        print(f"   👥 จำนวนผู้ถือหุ้นทั้งหมด: {result.total_shareholders}")
        print(f"   📊 จำนวนหุ้นทั้งหมด: {result.total_shares:,}")
        print(f"   ⚠️  ระดับความเสี่ยง: {result.risk_level}")
        print(f"   ✅ สถานะการปฏิบัติตามกฎระเบียบ: {result.compliance_status}")
        
        # แสดงรายละเอียด UBO
        print(f"\n📊 รายละเอียดผู้ถือหุ้น")
        print("-" * 40)
        
        if result.ubo_threshold_25:
            print(f"🔴 UBO ≥25% ({len(result.ubo_threshold_25)} คน):")
            for i, sh in enumerate(result.ubo_threshold_25, 1):
                print(f"   {i}. {sh.name}")
                print(f"      สัญชาติ: {sh.nationality}")
                print(f"      หุ้น: {sh.share_amount:,} ({sh.percent:.1f}%)")
                print(f"      ประเภท: {sh.shareholder_type}")
                if sh.directorship:
                    print(f"      เป็นกรรมการ: {sh.directorship}")
                print()
        else:
            print("🔴 UBO ≥25%: ไม่พบ")
        
        if result.ubo_threshold_10:
            print(f"🟡 UBO ≥10% ({len(result.ubo_threshold_10)} คน):")
            for i, sh in enumerate(result.ubo_threshold_10, 1):
                print(f"   {i}. {sh.name}")
                print(f"      สัญชาติ: {sh.nationality}")
                print(f"      หุ้น: {sh.share_amount:,} ({sh.percent:.1f}%)")
                print(f"      ประเภท: {sh.shareholder_type}")
                if sh.directorship:
                    print(f"      เป็นกรรมการ: {sh.directorship}")
                print()
        else:
            print("🟡 UBO ≥10%: ไม่พบ")
        
        if result.control_persons:
            print(f"👑 ผู้ควบคุม ≥50% ({len(result.control_persons)} คน):")
            for i, sh in enumerate(result.control_persons, 1):
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
        report = ubo_system.generate_report(result)
        
        # บันทึกรายงาน
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"ubo_report_lhb_{company_id}_{timestamp}.json"
        
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 รายงานถูกบันทึกเป็น: {report_filename}")
        
        # ส่งออกเป็น Excel
        print("📊 กำลังส่งออกเป็น Excel...")
        excel_filename = ubo_system.export_to_excel([result])
        print(f"📈 ไฟล์ Excel: {excel_filename}")
        
        # แสดงสรุปการตรวจสอบ
        print(f"\n📋 สรุปการตรวจสอบ UBO")
        print("=" * 60)
        
        # Checklist การตรวจสอบ
        checklist_items = [
            ("สถานะบริษัท", result.company_name != ""),
            ("จำนวนผู้ถือหุ้น", result.total_shareholders > 0),
            ("UBO ≥25%", len(result.ubo_threshold_25) > 0),
            ("UBO ≥10%", len(result.ubo_threshold_10) > 0),
            ("ผู้ควบคุม ≥50%", len(result.control_persons) > 0),
            ("การประเมินความเสี่ยง", result.risk_level != ""),
            ("สถานะการปฏิบัติตาม", result.compliance_status != "")
        ]
        
        for item, status in checklist_items:
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {item}")
        
        # คำแนะนำเฉพาะสำหรับธนาคาร
        print(f"\n💡 คำแนะนำสำหรับธนาคาร:")
        if result.risk_level == "HIGH":
            print("   ⚠️  ระดับความเสี่ยงสูง - ต้องตรวจสอบเพิ่มเติม")
            print("   🔍 ควรตรวจสอบการถือหุ้นของบริษัทแม่")
            print("   📋 ต้องรายงานต่อธนาคารแห่งประเทศไทย")
        elif result.risk_level == "MEDIUM":
            print("   ⚠️  ระดับความเสี่ยงปานกลาง - ควรติดตาม")
            print("   📊 ควรตรวจสอบการเปลี่ยนแปลงการถือหุ้น")
        else:
            print("   ✅ ระดับความเสี่ยงต่ำ - ปกติ")
        
        if result.compliance_status == "REVIEW_REQUIRED":
            print("   🔍 ต้องตรวจสอบเพิ่มเติม")
            print("   📋 ต้องรายงานต่อหน่วยงานกำกับดูแล")
        elif result.compliance_status == "NON_COMPLIANT":
            print("   ❌ ไม่ปฏิบัติตามกฎระเบียบ")
            print("   🚨 ต้องดำเนินการแก้ไขทันที")
        else:
            print("   ✅ ปฏิบัติตามกฎระเบียบ")
        
        # ข้อมูลเพิ่มเติมสำหรับธนาคาร
        print(f"\n🏦 ข้อมูลเพิ่มเติมสำหรับธนาคาร:")
        print(f"   💰 ทุนจดทะเบียน: 20,000 ล้านบาท")
        print(f"   📅 ก่อตั้ง: 29 มีนาคม 2005")
        print(f"   🏢 ประเภท: บริษัทมหาชนจำกัด")
        print(f"   📍 ที่ตั้ง: Q House Lumpini, สาทร, กรุงเทพฯ")
        
        print(f"\n🎉 การวิเคราะห์เสร็จสิ้น!")
        return True
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        print(f"   ประเภทข้อผิดพลาด: {type(e).__name__}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    success = analyze_land_houses_bank()
    
    if success:
        print(f"\n✅ การวิเคราะห์สำเร็จ! ระบบพร้อมใช้งาน")
        print(f"🌐 สำหรับ Web Interface ให้รัน: python app.py")
        print(f"📊 ข้อมูลนี้เป็นข้อมูลจริงจาก API Enlite BOL")
    else:
        print(f"\n❌ การวิเคราะห์ล้มเหลว กรุณาตรวจสอบข้อผิดพลาด")

if __name__ == "__main__":
    main()
