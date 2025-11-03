#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UBO (Ultimate Beneficial Owner) Detection System
ระบบตรวจสอบผู้ได้รับผลประโยชน์ที่แท้จริง

Features:
- API Integration with Enlite BOL
- Hierarchical Shareholding Analysis
- UBO Criteria Checking (25%, 10%, Control)
- Multi-company Batch Processing
- Visual Checklist Results
"""

import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

# Set Thai font for matplotlib
plt.rcParams['font.family'] = ['Tahoma', 'DejaVu Sans', 'Arial Unicode MS']
from io import BytesIO
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Shareholder:
    """ข้อมูลผู้ถือหุ้น"""
    name: str
    firstname: str
    lastname: str
    nationality: str
    share_amount: int
    percent: float
    shareholder_type: str  # 'personal' or 'corporate'
    regis_id: Optional[str] = None
    business_status: Optional[str] = None
    directorship: Optional[str] = None
    director_update_date: Optional[str] = None

@dataclass
class Company:
    """ข้อมูลบริษัท"""
    regis_id: str
    name_th: str
    name_en: str
    business_type: str
    company_status: str
    capital: str
    regis_date: str
    address: Dict[str, str]
    shareholders: List[Shareholder]
    directors: List[Dict[str, str]]

@dataclass
class UBOCheckResult:
    """ผลการตรวจสอบ UBO"""
    company_id: str
    company_name: str
    check_date: str
    ubo_threshold_25: List[Shareholder]  # ผู้ถือหุ้น >= 25%
    ubo_threshold_10: List[Shareholder]  # ผู้ถือหุ้น >= 10%
    control_persons: List[Shareholder]   # ผู้ควบคุม
    total_shares: int
    total_shareholders: int
    hierarchy_levels: int
    risk_level: str  # 'LOW', 'MEDIUM', 'HIGH'
    compliance_status: str  # 'COMPLIANT', 'NON_COMPLIANT', 'REVIEW_REQUIRED'

class EnliteAPIClient:
    """Client สำหรับเรียกใช้ Enlite BOL API"""
    
    def __init__(self, api_key: str, base_url: str = "https://xignal-uat.bol.co.th"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': api_key,
            'Content-Type': 'text/xml',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'User-Agent': 'UBO-System/1.0'
        })
    
    def get_company_data(self, registration_id: str, language: str = "EN") -> Dict[str, Any]:
        """
        ดึงข้อมูลบริษัทจาก Enlite API
        
        Args:
            registration_id: เลขทะเบียนบริษัท
            language: ภาษา (EN/TH)
        
        Returns:
            ข้อมูลบริษัทในรูปแบบ Dictionary
        """
        soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:eh="http://eh.actimize.com"
                  xmlns:view="http://view.bol.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <view:getDataEnlite>
            <registrationId>{registration_id}</registrationId>
            <language>{language}</language>
      </view:getDataEnlite>
   </soapenv:Body>
</soapenv:Envelope>"""
        
        try:
            logger.info(f"Making API request to: {self.base_url}/enlitews/companyData")
            logger.info(f"Request body: {soap_body}")
            
            response = self.session.post(
                f"{self.base_url}/enlitews/companyData",
                data=soap_body,
                timeout=30
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            # Log response content for debugging
            logger.info(f"Response content (first 1000 chars): {response.text[:1000]}...")
            
            # Parse XML response
            root = ET.fromstring(response.text)
            
            # Extract data using namespace
            ns = {
                'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                'view': 'http://view.bol.com/'
            }
            
            return_data = root.find('.//view:return', ns)
            if return_data is None:
                # Try alternative namespace or structure
                return_data = root.find('.//return')
                if return_data is None:
                    # Log the full response for debugging
                    logger.error(f"Full API Response: {response.text}")
                    raise ValueError("No return data found in response")
            
            return self._parse_company_data(return_data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except ET.ParseError as e:
            logger.error(f"XML parsing failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def _parse_company_data(self, return_data) -> Dict[str, Any]:
        """Parse XML data to structured format"""
        data = {}
        
        # Parse profile summary
        profile = return_data.find('.//profileSummary')
        if profile is not None:
            data['profile'] = {
                'name_th_full': self._get_text(profile, 'nameThFull'),
                'name_th': self._get_text(profile, 'nameTh'),
                'business_type_th': self._get_text(profile, 'businessTypeTh'),
                'name_en_full': self._get_text(profile, 'nameEnFull'),
                'name_en': self._get_text(profile, 'nameEn'),
                'business_type_en': self._get_text(profile, 'businessTypeEn'),
                'regis_id': self._get_text(profile, 'regisId'),
                'company_status': self._get_text(profile, 'companyStatus'),
                'capital': self._get_text(profile, 'capital'),
                'regis_date': self._get_text(profile, 'regisDate'),
                'address': self._parse_address(profile.find('.//address'))
            }
        
        # Parse directors
        directors = return_data.find('.//director')
        if directors is not None:
            data['directors'] = []
            for director in directors.findall('.//list'):
                data['directors'].append({
                    'title': self._get_text(director, 'title'),
                    'firstname': self._get_text(director, 'firstname'),
                    'lastname': self._get_text(director, 'lastname')
                })
        
        # Parse shareholders
        held_by = return_data.find('.//heldBy')
        if held_by is not None:
            data['shareholders'] = []
            level_held = held_by.find('.//levelHeldBy[@level="1"]')
            if level_held is not None:
                for shareholder_data in level_held.findall('.//data'):
                    shareholder = {
                        'regis_id_held_by': self._get_text(shareholder_data, 'regisIdHeldBy'),
                        'business_status': self._get_text(shareholder_data, 'businessStatus'),
                        'num_of_sh': self._get_text(shareholder_data, 'numOfSH'),
                        'share_amount': self._get_text(shareholder_data, 'shareAmount'),
                        'percent': self._get_text(shareholder_data, 'percent'),
                        'nationality': self._get_text(shareholder_data, 'nationality'),
                        'directorship': self._get_text(shareholder_data, 'directorShip'),
                        'director_upd_date': self._get_text(shareholder_data, 'directorUpdDate'),
                        'shareholder_type': 'personal'  # Default
                    }
                    
                    # Parse shareholder details
                    shareholder_elem = shareholder_data.find('.//shareholder')
                    if shareholder_elem is not None:
                        shareholder.update({
                            'title': self._get_text(shareholder_elem, 'title'),
                            'firstname': self._get_text(shareholder_elem, 'firstname'),
                            'lastname': self._get_text(shareholder_elem, 'lastname'),
                            'business_type': self._get_text(shareholder_elem, 'businessType'),
                            'shareholder_type': shareholder_elem.get('type', 'personal')
                        })
                    
                    data['shareholders'].append(shareholder)
        
        return data
    
    def _get_text(self, element, tag: str) -> str:
        """Helper method to get text from XML element"""
        if element is None:
            return ""
        elem = element.find(tag)
        return elem.text if elem is not None and elem.text else ""
    
    def _parse_address(self, address_elem) -> Dict[str, str]:
        """Parse address information"""
        if address_elem is None:
            return {}
        
        return {
            'address_no': self._get_text(address_elem, 'addressNo'),
            'moo': self._get_text(address_elem, 'moo'),
            'building_en': self._get_text(address_elem, 'buildingEn'),
            'building_th': self._get_text(address_elem, 'buildingTh'),
            'floor': self._get_text(address_elem, 'floor'),
            'soi_en': self._get_text(address_elem, 'soiEn'),
            'soi_th': self._get_text(address_elem, 'soiTh'),
            'road_en': self._get_text(address_elem, 'roadEn'),
            'road_th': self._get_text(address_elem, 'roadTh'),
            'moo_ban_en': self._get_text(address_elem, 'mooBanEn'),
            'moo_ban_th': self._get_text(address_elem, 'mooBanTh'),
            'sub_district': self._get_text(address_elem, 'subDistrict'),
            'district': self._get_text(address_elem, 'district'),
            'province': self._get_text(address_elem, 'province'),
            'postcode': self._get_text(address_elem, 'postcode'),
            'room': self._get_text(address_elem, 'room'),
            'room_en': self._get_text(address_elem, 'roomEn')
        }

class UBOAnalyzer:
    """ตัววิเคราะห์ UBO"""
    
    def __init__(self):
        self.threshold_25 = 25.0  # เกณฑ์ 25%
        self.threshold_10 = 10.0  # เกณฑ์ 10%
        self.control_threshold = 50.0  # เกณฑ์การควบคุม 50%
    
    def analyze_company(self, company_data: Dict[str, Any]) -> UBOCheckResult:
        """
        วิเคราะห์ข้อมูลบริษัทเพื่อหา UBO
        
        Args:
            company_data: ข้อมูลบริษัทจาก API
        
        Returns:
            ผลการตรวจสอบ UBO
        """
        profile = company_data.get('profile', {})
        shareholders_data = company_data.get('shareholders', [])
        
        # Convert to Shareholder objects
        shareholders = []
        total_shares = 0
        
        for sh_data in shareholders_data:
            try:
                share_amount = int(sh_data.get('share_amount', '0').replace(',', ''))
                percent = float(sh_data.get('percent', '0'))
                total_shares += share_amount
                
                shareholder = Shareholder(
                    name=f"{sh_data.get('firstname', '')} {sh_data.get('lastname', '')}".strip(),
                    firstname=sh_data.get('firstname', ''),
                    lastname=sh_data.get('lastname', ''),
                    nationality=sh_data.get('nationality', ''),
                    share_amount=share_amount,
                    percent=percent,
                    shareholder_type=sh_data.get('shareholder_type', 'personal'),
                    regis_id=sh_data.get('regis_id_held_by'),
                    business_status=sh_data.get('business_status'),
                    directorship=sh_data.get('directorship'),
                    director_update_date=sh_data.get('director_upd_date')
                )
                shareholders.append(shareholder)
            except (ValueError, TypeError) as e:
                logger.warning(f"Error parsing shareholder data: {e}")
                continue
        
        # Analyze UBO criteria
        ubo_25 = [sh for sh in shareholders if sh.percent >= self.threshold_25]
        ubo_10 = [sh for sh in shareholders if sh.percent >= self.threshold_10]
        control_persons = [sh for sh in shareholders if sh.percent >= self.control_threshold]
        
        # Determine risk level
        risk_level = self._calculate_risk_level(ubo_25, ubo_10, control_persons, shareholders)
        
        # Determine compliance status
        compliance_status = self._determine_compliance_status(ubo_25, ubo_10, control_persons)
        
        return UBOCheckResult(
            company_id=profile.get('regis_id', ''),
            company_name=profile.get('name_th_full', ''),
            check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ubo_threshold_25=ubo_25,
            ubo_threshold_10=ubo_10,
            control_persons=control_persons,
            total_shares=total_shares,
            total_shareholders=len(shareholders),
            hierarchy_levels=1,  # Level 1 only from API
            risk_level=risk_level,
            compliance_status=compliance_status
        )
    
    def _calculate_risk_level(self, ubo_25: List[Shareholder], ubo_10: List[Shareholder], 
                            control_persons: List[Shareholder], all_shareholders: List[Shareholder]) -> str:
        """คำนวณระดับความเสี่ยง"""
        if len(control_persons) > 0:
            return 'HIGH'
        elif len(ubo_25) > 0:
            return 'MEDIUM'
        elif len(ubo_10) > 0:
            return 'LOW'
        else:
            return 'LOW'
    
    def _determine_compliance_status(self, ubo_25: List[Shareholder], ubo_10: List[Shareholder], 
                                   control_persons: List[Shareholder]) -> str:
        """กำหนดสถานะการปฏิบัติตามกฎระเบียบ"""
        if len(control_persons) > 0:
            return 'REVIEW_REQUIRED'
        elif len(ubo_25) > 0:
            return 'COMPLIANT'
        elif len(ubo_10) > 0:
            return 'COMPLIANT'
        else:
            return 'COMPLIANT'

class UBOVisualizer:
    """ตัวสร้างภาพการถือหุ้นแบบ Hierarchical"""
    
    def __init__(self):
        self.colors = {
            'company': '#2E86AB',
            'ubo_25': '#A23B72',
            'ubo_10': '#F18F01',
            'other': '#C73E1D',
            'control': '#8B0000'
        }
    
    def create_hierarchy_chart(self, ubo_result: UBOCheckResult) -> str:
        """
        สร้างแผนภูมิการถือหุ้นแบบ Hierarchical
        
        Returns:
            Base64 encoded image string
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Create company node
        company_rect = FancyBboxPatch(
            (0.4, 0.8), 0.2, 0.15,
            boxstyle="round,pad=0.01",
            facecolor=self.colors['company'],
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(company_rect)
        ax.text(0.5, 0.875, f"{ubo_result.company_name}\n({ubo_result.company_id})", 
                ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Create shareholder nodes
        y_positions = [0.6, 0.4, 0.2]
        categories = [
            ('UBO ≥25%', ubo_result.ubo_threshold_25, self.colors['ubo_25']),
            ('UBO ≥10%', ubo_result.ubo_threshold_10, self.colors['ubo_10']),
            ('Control ≥50%', ubo_result.control_persons, self.colors['control'])
        ]
        
        for i, (category, shareholders, color) in enumerate(categories):
            if not shareholders:
                continue
                
            y_pos = y_positions[i]
            x_start = 0.1
            x_width = 0.8 / len(shareholders) if len(shareholders) > 0 else 0.8
            
            for j, shareholder in enumerate(shareholders):
                x_pos = x_start + j * x_width
                
                # Create shareholder rectangle
                rect = FancyBboxPatch(
                    (x_pos, y_pos), x_width - 0.02, 0.1,
                    boxstyle="round,pad=0.005",
                    facecolor=color,
                    edgecolor='black',
                    linewidth=1
                )
                ax.add_patch(rect)
                
                # Add shareholder text
                ax.text(x_pos + x_width/2, y_pos + 0.05, 
                       f"{shareholder.name}\n{shareholder.percent:.1f}%", 
                       ha='center', va='center', fontsize=8, fontweight='bold', color='white')
                
                # Draw connection line
                ax.plot([0.5, x_pos + x_width/2], [0.8, y_pos + 0.1], 
                       'k-', linewidth=1, alpha=0.7)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add legend
        legend_elements = [
            patches.Patch(color=self.colors['company'], label='Company'),
            patches.Patch(color=self.colors['control'], label='Control ≥50%'),
            patches.Patch(color=self.colors['ubo_25'], label='UBO ≥25%'),
            patches.Patch(color=self.colors['ubo_10'], label='UBO ≥10%')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        # Add title
        ax.set_title(f'UBO Analysis - {ubo_result.company_name}\nRisk Level: {ubo_result.risk_level}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_checklist_chart(self, ubo_result: UBOCheckResult) -> str:
        """สร้างแผนภูมิ Checklist การตรวจสอบ"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        # Checklist items
        checklist_items = [
            ('Company Status Active', ubo_result.company_name != ''),
            ('Total Shareholders Identified', ubo_result.total_shareholders > 0),
            ('UBO ≥25% Identified', len(ubo_result.ubo_threshold_25) > 0),
            ('UBO ≥10% Identified', len(ubo_result.ubo_threshold_10) > 0),
            ('Control Persons ≥50%', len(ubo_result.control_persons) > 0),
            ('Risk Assessment Complete', ubo_result.risk_level != ''),
            ('Compliance Status Determined', ubo_result.compliance_status != '')
        ]
        
        y_positions = range(len(checklist_items))
        
        for i, (item, status) in enumerate(checklist_items):
            color = '#4CAF50' if status else '#F44336'
            symbol = '✓' if status else '✗'
            
            # Create rectangle
            rect = FancyBboxPatch(
                (0.1, i * 0.12 + 0.1), 0.8, 0.08,
                boxstyle="round,pad=0.01",
                facecolor=color,
                edgecolor='black',
                linewidth=1
            )
            ax.add_patch(rect)
            
            # Add text
            ax.text(0.5, i * 0.12 + 0.14, f"{symbol} {item}", 
                   ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        ax.set_title(f'UBO Compliance Checklist\n{ubo_result.company_name}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64

class UBOSystem:
    """ระบบหลักสำหรับตรวจสอบ UBO"""
    
    def __init__(self, api_key: str):
        self.api_client = EnliteAPIClient(api_key)
        self.analyzer = UBOAnalyzer()
        self.visualizer = UBOVisualizer()
        self.results = []
    
    def analyze_single_company(self, registration_id: str) -> UBOCheckResult:
        """วิเคราะห์บริษัทเดียว"""
        try:
            logger.info(f"Analyzing company: {registration_id}")
            company_data = self.api_client.get_company_data(registration_id)
            ubo_result = self.analyzer.analyze_company(company_data)
            self.results.append(ubo_result)
            return ubo_result
        except Exception as e:
            logger.error(f"Error analyzing company {registration_id}: {e}")
            raise
    
    def analyze_multiple_companies(self, registration_ids: List[str]) -> List[UBOCheckResult]:
        """วิเคราะห์หลายบริษัท"""
        results = []
        for reg_id in registration_ids:
            try:
                result = self.analyze_single_company(reg_id)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze {reg_id}: {e}")
                continue
        return results
    
    def generate_report(self, ubo_result: UBOCheckResult) -> Dict[str, Any]:
        """สร้างรายงานการตรวจสอบ"""
        hierarchy_chart = self.visualizer.create_hierarchy_chart(ubo_result)
        checklist_chart = self.visualizer.create_checklist_chart(ubo_result)
        
        report = {
            'company_info': {
                'id': ubo_result.company_id,
                'name': ubo_result.company_name,
                'check_date': ubo_result.check_date
            },
            'ubo_analysis': {
                'total_shares': ubo_result.total_shares,
                'total_shareholders': ubo_result.total_shareholders,
                'ubo_25_count': len(ubo_result.ubo_threshold_25),
                'ubo_10_count': len(ubo_result.ubo_threshold_10),
                'control_persons_count': len(ubo_result.control_persons),
                'risk_level': ubo_result.risk_level,
                'compliance_status': ubo_result.compliance_status
            },
            'ubo_details': {
                'ubo_25': [asdict(sh) for sh in ubo_result.ubo_threshold_25],
                'ubo_10': [asdict(sh) for sh in ubo_result.ubo_threshold_10],
                'control_persons': [asdict(sh) for sh in ubo_result.control_persons]
            },
            'charts': {
                'hierarchy': hierarchy_chart,
                'checklist': checklist_chart
            }
        }
        
        return report
    
    def export_to_excel(self, results: List[UBOCheckResult], filename: str = None) -> str:
        """ส่งออกผลลัพธ์เป็น Excel"""
        if filename is None:
            filename = f"ubo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = []
            for result in results:
                summary_data.append({
                    'Company ID': result.company_id,
                    'Company Name': result.company_name,
                    'Check Date': result.check_date,
                    'Total Shares': result.total_shares,
                    'Total Shareholders': result.total_shareholders,
                    'UBO ≥25% Count': len(result.ubo_threshold_25),
                    'UBO ≥10% Count': len(result.ubo_threshold_10),
                    'Control Persons Count': len(result.control_persons),
                    'Risk Level': result.risk_level,
                    'Compliance Status': result.compliance_status
                })
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Detailed UBO sheet
            ubo_details = []
            for result in results:
                for sh in result.ubo_threshold_25 + result.ubo_threshold_10 + result.control_persons:
                    ubo_details.append({
                        'Company ID': result.company_id,
                        'Company Name': result.company_name,
                        'Shareholder Name': sh.name,
                        'First Name': sh.firstname,
                        'Last Name': sh.lastname,
                        'Nationality': sh.nationality,
                        'Share Amount': sh.share_amount,
                        'Percentage': sh.percent,
                        'Shareholder Type': sh.shareholder_type,
                        'UBO Category': '≥25%' if sh.percent >= 25 else '≥10%' if sh.percent >= 10 else 'Control' if sh.percent >= 50 else 'Other'
                    })
            
            if ubo_details:
                df_ubo = pd.DataFrame(ubo_details)
                df_ubo.to_excel(writer, sheet_name='UBO Details', index=False)
        
        return filename

def main():
    """ตัวอย่างการใช้งาน"""
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    # สร้างระบบ UBO
    ubo_system = UBOSystem(API_KEY)
    
    # ตัวอย่างการวิเคราะห์บริษัทเดียว
    registration_id = "0105565126796"  # จากตัวอย่างที่ให้มา
    
    try:
        print(f"กำลังวิเคราะห์บริษัท: {registration_id}")
        result = ubo_system.analyze_single_company(registration_id)
        
        print(f"\n=== ผลการวิเคราะห์ UBO ===")
        print(f"บริษัท: {result.company_name}")
        print(f"เลขทะเบียน: {result.company_id}")
        print(f"จำนวนผู้ถือหุ้นทั้งหมด: {result.total_shareholders}")
        print(f"จำนวนหุ้นทั้งหมด: {result.total_shares:,}")
        print(f"ระดับความเสี่ยง: {result.risk_level}")
        print(f"สถานะการปฏิบัติตามกฎระเบียบ: {result.compliance_status}")
        
        print(f"\n=== UBO ≥25% ===")
        for sh in result.ubo_threshold_25:
            print(f"- {sh.name}: {sh.percent:.1f}% ({sh.share_amount:,} หุ้น)")
        
        print(f"\n=== UBO ≥10% ===")
        for sh in result.ubo_threshold_10:
            print(f"- {sh.name}: {sh.percent:.1f}% ({sh.share_amount:,} หุ้น)")
        
        print(f"\n=== ผู้ควบคุม ≥50% ===")
        for sh in result.control_persons:
            print(f"- {sh.name}: {sh.percent:.1f}% ({sh.share_amount:,} หุ้น)")
        
        # สร้างรายงาน
        report = ubo_system.generate_report(result)
        
        # บันทึกรายงานเป็น JSON
        with open(f"ubo_report_{registration_id}.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\nรายงานถูกบันทึกเป็น: ubo_report_{registration_id}.json")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
