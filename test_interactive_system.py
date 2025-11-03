#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Interactive UBO System
ทดสอบระบบ UBO แบบ Interactive
"""

import requests
import json
import time

def test_ubo_analysis():
    """ทดสอบการวิเคราะห์ UBO"""
    
    print("🔍 ทดสอบระบบ UBO แบบ Interactive")
    print("=" * 50)
    
    # Test data
    company_id = "0107548000234"
    api_url = "http://localhost:4444/api/analyze"
    
    print(f"📊 วิเคราะห์บริษัท: {company_id}")
    
    # Make API request
    try:
        response = requests.post(api_url, 
                               json={"registration_id": company_id},
                               timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result = data.get('data', {})
                
                print("\n✅ การวิเคราะห์สำเร็จ!")
                print(f"📋 สรุป: {result.get('analysis_summary', 'ไม่ระบุ')}")
                
                # Company info
                company_info = result.get('company_info', {})
                print(f"\n🏢 ข้อมูลบริษัท:")
                print(f"  ชื่อไทย: {company_info.get('name_th', 'ไม่ระบุ')}")
                print(f"  ชื่ออังกฤษ: {company_info.get('name_en', 'ไม่ระบุ')}")
                print(f"  เลขทะเบียน: {company_info.get('regis_id', 'ไม่ระบุ')}")
                print(f"  สถานะ: {company_info.get('status', 'ไม่ระบุ')}")
                
                # UBOs
                ubos = result.get('ubos', [])
                print(f"\n👥 UBOs ที่พบ: {len(ubos)} คน")
                for i, ubo in enumerate(ubos):
                    print(f"  {i+1}. {ubo.get('name', 'ไม่ระบุ')} - {ubo.get('total_percentage', 0)}%")
                    print(f"     วิธี: {ubo.get('identification_method', 'ไม่ระบุ')}")
                    print(f"     เป็นกรรมการ: {ubo.get('is_director', False)}")
                
                # Hierarchy data
                hierarchy_data = result.get('hierarchy_data', {})
                print(f"\n🏗️ โครงสร้างการถือหุ้น:")
                print(f"  จำนวนบริษัทที่ตรวจสอบ: {len(hierarchy_data)} บริษัท")
                
                # จัดกลุ่มตาม level
                levels = {}
                for company_id, company_data in hierarchy_data.items():
                    level = company_data.get('level', 0)
                    if level not in levels:
                        levels[level] = []
                    levels[level].append(company_data)
                
                for level in sorted(levels.keys()):
                    companies = levels[level]
                    print(f"\n  Level {level}: {len(companies)} บริษัท")
                    
                    for company in companies:
                        name = company.get('name_th', 'ไม่ระบุชื่อ')
                        shareholders = company.get('shareholders', [])
                        print(f"    - {name}")
                        print(f"      ผู้ถือหุ้น: {len(shareholders)} คน")
                        
                        # แสดงผู้ถือหุ้นที่สำคัญ
                        for sh in shareholders[:5]:  # แสดงแค่ 5 คนแรก
                            sh_name = sh.get('name', 'ไม่ระบุ')
                            sh_percent = sh.get('percent', 0)
                            sh_effective = sh.get('effective_percentage', 0)
                            sh_type = sh.get('shareholder_type', 'personal')
                            print(f"        • {sh_name}: {sh_percent}% (Effective: {sh_effective}%) [{sh_type}]")
                        
                        if len(shareholders) > 5:
                            print(f"        ... และอีก {len(shareholders) - 5} คน")
                
                # Checklist
                checklist = result.get('checklist', {})
                print(f"\n📋 Checklist:")
                print(f"  Method 1 (Shareholding ≥15%): {checklist.get('method_1_check', {}).get('found_ubo', False)}")
                print(f"  Method 3 (Directors): {checklist.get('method_3_check', {}).get('directors_found', 0)} คน")
                print(f"  Final Result: {checklist.get('final_result', {}).get('action', 'ไม่ระบุ')}")
                
                # Tree image
                tree_image = result.get('hierarchy_tree_image')
                if tree_image:
                    print(f"\n🌳 แผนภูมิ Tree: มีข้อมูล (ขนาด: {len(tree_image)} ตัวอักษร)")
                else:
                    print(f"\n🌳 แผนภูมิ Tree: ไม่มีข้อมูล")
                
                # Save detailed result
                with open('test_interactive_result.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print(f"\n💾 ผลการทดสอบบันทึกใน test_interactive_result.json")
                
                return True
                
            else:
                print(f"❌ การวิเคราะห์ล้มเหลว: {data.get('error', 'ไม่ระบุสาเหตุ')}")
                return False
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - การวิเคราะห์ใช้เวลานานเกินไป")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ได้")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 เริ่มทดสอบระบบ UBO แบบ Interactive")
    
    # Wait for server to be ready
    print("⏳ รอให้เซิร์ฟเวอร์พร้อม...")
    time.sleep(2)
    
    success = test_ubo_analysis()
    
    if success:
        print("\n✅ การทดสอบเสร็จสิ้น - ระบบทำงานได้ปกติ!")
        print("🌐 เปิดเบราว์เซอร์ไปที่: http://localhost:4444")
    else:
        print("\n❌ การทดสอบล้มเหลว - มีปัญหากับระบบ")

if __name__ == "__main__":
    main()
