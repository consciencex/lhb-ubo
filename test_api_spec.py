#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO API Test Script
สคริปต์ทดสอบ API ตาม Spec ที่ถูกต้อง
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ubo_system import EnliteAPIClient
import logging

# Configure logging to see detailed API calls
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api_connection():
    """ทดสอบการเชื่อมต่อ API ตาม Spec"""
    print("🧪 ทดสอบ API Connection ตาม Spec")
    print("=" * 50)
    
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    # สร้าง API Client
    api_client = EnliteAPIClient(API_KEY)
    
    # ทดสอบกับบริษัทที่คุณระบุ
    test_companies = [
        "0107548000234",  # บริษัทที่คุณต้องการทดสอบ
        "0105565126796",  # บริษัทจากตัวอย่าง
        "0107562000386"   # บริษัทจากตัวอย่าง
    ]
    
    for company_id in test_companies:
        try:
            print(f"\n🔍 ทดสอบบริษัท: {company_id}")
            print("-" * 30)
            
            # เรียก API
            company_data = api_client.get_company_data(company_id, "EN")
            
            if company_data:
                print(f"✅ สำเร็จ! ได้รับข้อมูลบริษัท")
                
                # แสดงข้อมูลพื้นฐาน
                profile = company_data.get('profile', {})
                if profile:
                    print(f"   ชื่อบริษัท: {profile.get('name_th_full', 'ไม่ระบุ')}")
                    print(f"   เลขทะเบียน: {profile.get('regis_id', 'ไม่ระบุ')}")
                    print(f"   สถานะ: {profile.get('company_status', 'ไม่ระบุ')}")
                    print(f"   ทุนจดทะเบียน: {profile.get('capital', 'ไม่ระบุ')}")
                
                # แสดงข้อมูลผู้ถือหุ้น
                shareholders = company_data.get('shareholders', [])
                print(f"   จำนวนผู้ถือหุ้น: {len(shareholders)}")
                
                if shareholders:
                    print("   รายชื่อผู้ถือหุ้น:")
                    for i, sh in enumerate(shareholders[:3], 1):  # แสดงแค่ 3 คนแรก
                        name = f"{sh.get('firstname', '')} {sh.get('lastname', '')}".strip()
                        percent = sh.get('percent', '0')
                        print(f"     {i}. {name}: {percent}%")
                
                # แสดงข้อมูลกรรมการ
                directors = company_data.get('directors', [])
                print(f"   จำนวนกรรมการ: {len(directors)}")
                
            else:
                print("❌ ไม่ได้รับข้อมูลจาก API")
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            print(f"   ประเภทข้อผิดพลาด: {type(e).__name__}")
    
    print(f"\n🎯 การทดสอบ API เสร็จสิ้น")

def test_specific_company():
    """ทดสอบบริษัทเฉพาะที่คุณระบุ"""
    print("\n🎯 ทดสอบบริษัทเฉพาะ: 0107548000234")
    print("=" * 50)
    
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    api_client = EnliteAPIClient(API_KEY)
    
    try:
        print("📡 กำลังเรียก API...")
        company_data = api_client.get_company_data("0107548000234", "EN")
        
        if company_data:
            print("✅ ได้รับข้อมูลสำเร็จ!")
            
            # แสดงข้อมูลทั้งหมด
            print("\n📊 ข้อมูลบริษัท:")
            profile = company_data.get('profile', {})
            for key, value in profile.items():
                if value:
                    print(f"   {key}: {value}")
            
            print("\n👥 ข้อมูลผู้ถือหุ้น:")
            shareholders = company_data.get('shareholders', [])
            for i, sh in enumerate(shareholders, 1):
                name = f"{sh.get('firstname', '')} {sh.get('lastname', '')}".strip()
                print(f"   {i}. {name}")
                print(f"      หุ้น: {sh.get('share_amount', '0')} ({sh.get('percent', '0')}%)")
                print(f"      สัญชาติ: {sh.get('nationality', 'ไม่ระบุ')}")
                print(f"      ประเภท: {sh.get('shareholder_type', 'ไม่ระบุ')}")
                print()
            
            print("\n👨‍💼 ข้อมูลกรรมการ:")
            directors = company_data.get('directors', [])
            for i, director in enumerate(directors, 1):
                name = f"{director.get('firstname', '')} {director.get('lastname', '')}".strip()
                print(f"   {i}. {name}")
            
        else:
            print("❌ ไม่ได้รับข้อมูลจาก API")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        logger.exception("Full error details:")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 UBO API Test Script")
    print("ทดสอบ API ตาม Spec ที่ถูกต้อง")
    print("=" * 60)
    
    # ทดสอบการเชื่อมต่อ API
    test_api_connection()
    
    # ทดสอบบริษัทเฉพาะ
    test_specific_company()
    
    print(f"\n✅ การทดสอบเสร็จสิ้น!")

if __name__ == "__main__":
    main()
