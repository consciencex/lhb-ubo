#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple UBO Test Script
ทดสอบระบบ UBO แบบง่าย
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_ubo_system import EnhancedUBOSystem
import json

def test_ubo_system():
    """ทดสอบระบบ UBO"""
    
    # Initialize system
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    try:
        print("🚀 Initializing Enhanced UBO System...")
        ubo_system = EnhancedUBOSystem(API_KEY)
        print("✅ UBO System initialized successfully")
        
        # Test with LH Bank
        company_id = "0107548000234"
        print(f"\n🔍 Analyzing company: {company_id}")
        
        result = ubo_system.analyze_company_hierarchy(company_id)
        
        # Convert dataclass to dict for easier handling
        if hasattr(result, '__dict__'):
            result_dict = result.__dict__
        else:
            result_dict = result
        
        if "error" in result_dict:
            print(f"❌ Error: {result_dict['error']}")
            return False
        
        print("✅ Analysis completed successfully!")
        
        # Display results
        company_info = result_dict.get("company_info", {})
        print(f"\n📊 Company Information:")
        print(f"  Name (TH): {company_info.get('name_th', 'N/A')}")
        print(f"  Name (EN): {company_info.get('name_en', 'N/A')}")
        print(f"  Status: {company_info.get('status', 'N/A')}")
        
        ubos = result_dict.get("ubos", [])
        print(f"\n👥 UBOs Found: {len(ubos)}")
        
        for i, ubo in enumerate(ubos, 1):
            print(f"  {i}. {ubo.get('name', 'N/A')} - {ubo.get('total_percentage', 0):.2f}%")
            print(f"     Method: {ubo.get('identification_method', 'N/A')}")
        
        checklist = result_dict.get("checklist", {})
        overall_status = checklist.get("overall_status", "UNKNOWN")
        print(f"\n📋 Overall Status: {overall_status}")
        
        # Save result (convert dataclasses to dicts)
        def convert_to_dict(obj):
            if hasattr(obj, '__dict__'):
                return {k: convert_to_dict(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            else:
                return obj
        
        result_json = convert_to_dict(result_dict)
        
        with open('test_result.json', 'w', encoding='utf-8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Result saved to test_result.json")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ubo_system()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
        sys.exit(1)
