#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO Web Application
เว็บแอปพลิเคชันสำหรับตรวจสอบ UBO

Features:
- Web Interface สำหรับตรวจสอบ UBO
- Batch Processing สำหรับหลายบริษัท
- Interactive Charts และ Visualizations
- Export Results to Excel/PDF
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import tempfile
from datetime import datetime
import pandas as pd
from ubo_system import UBOSystem, UBOCheckResult
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global UBO System instance
ubo_system = None

def initialize_ubo_system():
    """Initialize UBO System with API key"""
    global ubo_system
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    ubo_system = UBOSystem(API_KEY)
    logger.info("UBO System initialized successfully")

@app.route('/')
def index():
    """หน้าแรกของแอปพลิเคชัน"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_company():
    """API endpoint สำหรับวิเคราะห์บริษัท"""
    try:
        data = request.get_json()
        registration_id = data.get('registration_id')
        
        if not registration_id:
            return jsonify({'error': 'Registration ID is required'}), 400
        
        if not ubo_system:
            initialize_ubo_system()
        
        # Analyze company
        result = ubo_system.analyze_single_company(registration_id)
        
        # Generate report
        report = ubo_system.generate_report(result)
        
        return jsonify({
            'success': True,
            'data': report
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_company: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze_batch', methods=['POST'])
def analyze_batch():
    """API endpoint สำหรับวิเคราะห์หลายบริษัท"""
    try:
        data = request.get_json()
        registration_ids = data.get('registration_ids', [])
        
        if not registration_ids:
            return jsonify({'error': 'Registration IDs are required'}), 400
        
        if not ubo_system:
            initialize_ubo_system()
        
        # Analyze multiple companies
        results = ubo_system.analyze_multiple_companies(registration_ids)
        
        # Generate reports for all companies
        reports = []
        for result in results:
            report = ubo_system.generate_report(result)
            reports.append(report)
        
        return jsonify({
            'success': True,
            'data': reports,
            'total_analyzed': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_batch: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export_excel', methods=['POST'])
def export_excel():
    """API endpoint สำหรับส่งออกผลลัพธ์เป็น Excel"""
    try:
        data = request.get_json()
        results_data = data.get('results', [])
        
        if not results_data:
            return jsonify({'error': 'No results data provided'}), 400
        
        # Convert JSON data back to UBOCheckResult objects
        results = []
        for result_data in results_data:
            # This is a simplified conversion - in production, you'd want more robust handling
            result = UBOCheckResult(
                company_id=result_data['company_info']['id'],
                company_name=result_data['company_info']['name'],
                check_date=result_data['company_info']['check_date'],
                ubo_threshold_25=[],  # Simplified for demo
                ubo_threshold_10=[],
                control_persons=[],
                total_shares=result_data['ubo_analysis']['total_shares'],
                total_shareholders=result_data['ubo_analysis']['total_shareholders'],
                hierarchy_levels=1,
                risk_level=result_data['ubo_analysis']['risk_level'],
                compliance_status=result_data['ubo_analysis']['compliance_status']
            )
            results.append(result)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_file.close()
        
        # Export to Excel
        filename = ubo_system.export_to_excel(results, temp_file.name)
        
        return jsonify({
            'success': True,
            'filename': os.path.basename(filename),
            'download_url': f'/download/{os.path.basename(filename)}'
        })
        
    except Exception as e:
        logger.error(f"Error in export_excel: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download exported files"""
    try:
        # In production, you'd want to secure this path
        file_path = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ubo_system_initialized': ubo_system is not None
    })

if __name__ == '__main__':
    # Initialize UBO system on startup
    initialize_ubo_system()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
