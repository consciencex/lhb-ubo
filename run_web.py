#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO Web Interface Launcher
สคริปต์สำหรับเริ่มต้น Web Interface
"""

import subprocess
import sys
import os

def main():
    """เริ่มต้น Web Interface"""
    print("🚀 กำลังเริ่มต้น UBO Web Interface...")
    print("=" * 50)
    
    # ตรวจสอบ dependencies
    try:
        import flask
        import flask_cors
        print("✅ Flask และ Flask-CORS พร้อมใช้งาน")
    except ImportError as e:
        print(f"❌ ไม่พบ dependencies: {e}")
        print("กรุณารัน: pip3 install -r requirements.txt")
        return
    
    # เริ่มต้น Web Application
    print("🌐 กำลังเริ่มต้น Web Application...")
    print("   เข้าถึงระบบได้ที่: http://localhost:5000")
    print("   กด Ctrl+C เพื่อหยุดระบบ")
    print("-" * 50)
    
    try:
        # รัน Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 หยุดการทำงานของระบบ")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
