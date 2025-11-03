#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced UBO System - Correct API Loop Implementation
ระบบวิเคราะห์ UBO ที่ทำงานถูกต้องตาม API Response Structure
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import deque

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
    shareholder_type: str  # 'personal' or 'company'
    regis_id: str
    business_status: Optional[str] = None
    directorship: Optional[str] = None
    director_update_date: Optional[str] = None
    effective_percentage: float = 0.0  # สัดส่วนทางอ้อม
    path: List[str] = None  # เส้นทางการถือหุ้น
    
    def __post_init__(self):
        if self.path is None:
            self.path = []

@dataclass
class UBOCandidate:
    """ข้อมูล UBO Candidate"""
    name: str
    total_percentage: float
    paths: List[List[str]]
    method: int  # 1 = shareholding, 2 = control, 3 = management

@dataclass
class UBOAnalysisResult:
    """ผลลัพธ์การวิเคราะห์ UBO"""
    registration_id: str
    company_name: str
    ubo_candidates: List[UBOCandidate]
    final_ubos: List[UBOCandidate]
    hierarchy: Dict[str, Any]
    checklist: Dict[str, Any]
    risk_level: str
    compliance_status: str
    total_companies_checked: int
    max_level_reached: int
    check_date: str

class CorrectEnliteAPIClient:
    """API Client ที่ทำงานถูกต้องตาม API Response Structure"""
    
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
            'User-Agent': 'Correct-UBO-System/1.0'
        })
        self.cache = {}
        self.rate_limit_delay = 0.5
    
    def get_company_data(self, registration_id: str) -> Optional[Dict[str, Any]]:
        """ดึงข้อมูลบริษัทจาก API"""
        if registration_id in self.cache:
            logger.info(f"Using cached data for {registration_id}")
            return self.cache[registration_id]
        
        try:
            # สร้าง SOAP Request
            soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:eh="http://eh.actimize.com" xmlns:view="http://view.bol.com/">
    <soapenv:Header/>
    <soapenv:Body>
        <view:getDataEnlite>
            <registrationId>{registration_id}</registrationId>
            <language>EN</language>
        </view:getDataEnlite>
    </soapenv:Body>
</soapenv:Envelope>"""
            
            url = f"{self.base_url}/enlitews/companyData"
            logger.info(f"Making API request to: {url} for {registration_id}")
            
            response = self.session.post(url, data=soap_body, timeout=30)
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = self._parse_company_data(response.text)
                self.cache[registration_id] = data
                return data
            else:
                logger.error(f"API request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error for {registration_id}: {e}")
            return None
    
    def _parse_company_data(self, xml_response: str) -> Dict[str, Any]:
        """Parse XML response to structured format"""
        try:
            root = ET.fromstring(xml_response)
            return_data = root.find('.//return')
            
            if return_data is None:
                logger.error("No return data found in response")
                return {}
            
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
                    'set_symbol': self._get_text(profile, 'setSymbol'),
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
            
            # Parse shareholders - เฉพาะ Level 1 เท่านั้น
            held_by = return_data.find('.//heldBy')
            if held_by is not None:
                data['shareholders'] = []
                
                # ดึงเฉพาะ levelHeldBy level="1" เท่านั้น
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
                        
                        # ถ้าเป็นนิติบุคคลและไม่มีชื่อ ให้ใช้ regis_id_held_by
                        if shareholder.get('shareholder_type') == 'company' and not shareholder.get('firstname'):
                            regis_id = shareholder.get('regis_id_held_by', '')
                            if regis_id:
                                shareholder['firstname'] = f"บริษัท {regis_id}"
                                shareholder['lastname'] = ""
                        
                        data['shareholders'].append(shareholder)
            
            return data
            
        except Exception as e:
            logger.error(f"Error parsing XML response: {e}")
            return {}
    
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

class CorrectUBOAnalyzer:
    """ตัววิเคราะห์ UBO ที่ทำงานถูกต้องตาม API Structure"""
    
    def __init__(self):
        self.threshold_15 = 15.0  # เกณฑ์ 15% ตามเอกสาร
        self.max_levels = 3  # สูงสุด 3 ทอด
        self.ubo_candidates = {}  # Dictionary สำหรับเก็บ UBO candidates
        self.hierarchy = {}  # โครงสร้างการถือหุ้น
        self.processed_companies = set()  # บริษัทที่ตรวจสอบแล้ว
        self.total_companies_checked = 0
        self.max_level_reached = 0
    
    def analyze_company_hierarchy(self, api_client: CorrectEnliteAPIClient, 
                                 start_registration_id: str) -> UBOAnalysisResult:
        """
        วิเคราะห์ UBO แบบ Hierarchy ที่ถูกต้องตาม API Structure
        """
        logger.info(f"Starting CORRECT UBO analysis for company: {start_registration_id}")
        
        # Reset data structures
        self.ubo_candidates = {}
        self.hierarchy = {}
        self.processed_companies = set()
        self.total_companies_checked = 0
        self.max_level_reached = 0
        
        # เริ่มต้นการวิเคราะห์แบบ Recursive
        self._analyze_level_recursive(api_client, start_registration_id, 100.0, 0, [])
        
        # ระบุ UBO สุดท้าย
        final_ubos = self._identify_final_ubos()
        
        # สร้าง Checklist
        checklist = self._create_checklist(final_ubos)
        
        # กำหนดระดับความเสี่ยงและสถานะการปฏิบัติตาม
        risk_level, compliance_status = self._determine_risk_and_compliance(final_ubos)
        
        return UBOAnalysisResult(
            registration_id=start_registration_id,
            company_name=self.hierarchy.get(start_registration_id, {}).get('name_th', ''),
            ubo_candidates=list(self.ubo_candidates.values()),
            final_ubos=final_ubos,
            hierarchy=self.hierarchy,
            checklist=checklist,
            risk_level=risk_level,
            compliance_status=compliance_status,
            total_companies_checked=self.total_companies_checked,
            max_level_reached=self.max_level_reached,
            check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def _analyze_level_recursive(self, api_client: CorrectEnliteAPIClient, 
                                company_id: str, cumulative_percentage: float, 
                                current_level: int, current_path: list):
        """วิเคราะห์แต่ละ Level แบบ recursive"""
        
        # ตรวจสอบระดับสูงสุด
        if current_level >= self.max_levels:
            logger.info(f"Reached max level {self.max_levels} for {company_id}")
            return
        
        # ตรวจสอบว่าเคยประมวลผลแล้วหรือไม่
        if company_id in self.processed_companies:
            logger.info(f"Using cached data for {company_id}")
            return
        
        # เรียก API สำหรับบริษัทนี้
        company_data = api_client.get_company_data(company_id)
        if not company_data:
            logger.warning(f"Failed to get data for company {company_id}")
            return
        
        self.processed_companies.add(company_id)
        self.total_companies_checked += 1
        self.max_level_reached = max(self.max_level_reached, current_level)
        
        # Parse ข้อมูลบริษัท
        profile = company_data.get('profile', {})
        shareholders_data = company_data.get('shareholders', [])
        directors_data = company_data.get('directors', [])
        
        # บันทึกข้อมูลบริษัทใน Hierarchy
        self.hierarchy[company_id] = {
            'name_th': profile.get('name_th_full', ''),
            'name_en': profile.get('name_en_full', ''),
            'level': current_level,
            'parent_percentage': cumulative_percentage,
            'shareholders': [],
            'directors': directors_data,
            'path': current_path.copy(),
            'company_id': company_id,
            'status': profile.get('company_status', 'Active'),
            'capital': profile.get('capital', ''),
            'regis_date': profile.get('regis_date', ''),
            'address': profile.get('address', {}),
            'business_type': profile.get('business_type_th', '')
        }
        
        # ประมวลผลผู้ถือหุ้น Level 1 ของบริษัทนี้
        corporate_shareholders = []  # เก็บนิติบุคคลเพื่อเรียก API ต่อ
        
        for sh_data in shareholders_data:
            try:
                share_amount = int(sh_data.get('share_amount', '0').replace(',', ''))
                percent = float(sh_data.get('percent', '0'))
                
                # คำนวณสัดส่วนทางอ้อม
                effective_percentage = (cumulative_percentage * percent) / 100.0
                
                shareholder_name = f"{sh_data.get('firstname', '')} {sh_data.get('lastname', '')}".strip()
                shareholder_type = sh_data.get('shareholder_type', 'personal')
                regis_id_held_by = sh_data.get('regis_id_held_by', '')
                
                # สร้าง Shareholder object
                shareholder = Shareholder(
                    name=shareholder_name,
                    firstname=sh_data.get('firstname', ''),
                    lastname=sh_data.get('lastname', ''),
                    nationality=sh_data.get('nationality', ''),
                    share_amount=share_amount,
                    percent=percent,
                    shareholder_type=shareholder_type,
                    regis_id=regis_id_held_by,
                    business_status=sh_data.get('business_status'),
                    directorship=sh_data.get('directorship'),
                    director_update_date=sh_data.get('director_upd_date'),
                    effective_percentage=effective_percentage,
                    path=current_path + [company_id]
                )
                
                # บันทึกใน Hierarchy
                self.hierarchy[company_id]['shareholders'].append(asdict(shareholder))
                
                # ตรวจสอบประเภทผู้ถือหุ้น
                if shareholder_type == 'personal' and shareholder_name:
                    # บุคคลธรรมดา - เพิ่มใน UBO candidates
                    if shareholder_name not in self.ubo_candidates:
                        self.ubo_candidates[shareholder_name] = UBOCandidate(
                            name=shareholder_name,
                            total_percentage=0.0,
                            paths=[],
                            method=1
                        )
                    
                    self.ubo_candidates[shareholder_name].total_percentage += effective_percentage
                    self.ubo_candidates[shareholder_name].paths.append(shareholder.path + [company_id])
                    
                    logger.info(f"Found individual shareholder: {shareholder_name} with {effective_percentage:.2f}%")
                
                elif shareholder_type == 'company' or regis_id_held_by:
                    # นิติบุคคล - เก็บไว้เพื่อเรียก API ต่อ
                    if regis_id_held_by and regis_id_held_by not in self.processed_companies:
                        corporate_shareholders.append((regis_id_held_by, effective_percentage))
                        logger.info(f"Found corporate shareholder: {shareholder_name} ({regis_id_held_by}) with {effective_percentage:.2f}%")
                
            except (ValueError, TypeError) as e:
                logger.warning(f"Error parsing shareholder data: {e}")
                continue
        
        # เรียก API สำหรับนิติบุคคลที่พบ (Level ถัดไป)
        for corp_id, corp_percentage in corporate_shareholders:
            new_path = current_path + [company_id]
            self._analyze_level_recursive(api_client, corp_id, corp_percentage, current_level + 1, new_path)
    
    def _identify_final_ubos(self) -> List[UBOCandidate]:
        """ระบุ UBO สุดท้ายตามเกณฑ์ 15% - ใช้เฉพาะวิธีที่ 1"""
        final_ubos = []
        
        # วิธีที่ 1: ตรวจสอบการถือหุ้น >= 15% เท่านั้น
        for candidate in self.ubo_candidates.values():
            if candidate.total_percentage >= self.threshold_15:
                final_ubos.append(candidate)
                logger.info(f"UBO identified (Method 1): {candidate.name} with {candidate.total_percentage:.2f}%")
        
        # ไม่ใช้วิธีที่ 3 (กรรมการ) ตามที่ผู้ใช้ต้องการ
        logger.info(f"Method 1 only - Found {len(final_ubos)} UBOs with >=15% shareholding")
        
        return final_ubos
    
    def _create_checklist(self, final_ubos: List[UBOCandidate]) -> Dict[str, Any]:
        """สร้าง Checklist การปฏิบัติตาม"""
        return {
            'method_1_check': {
                'checked': True,
                'found_ubo': len(final_ubos) > 0,
                'companies_checked': self.total_companies_checked,
                'max_level_reached': self.max_level_reached
            },
            'method_2_check': {
                'checked': True,
                'required': len(final_ubos) == 0,
                'note': 'ต้องตรวจสอบผู้มีอำนาจครอบงำกิจการ (Manual)'
            },
            'method_3_check': {
                'checked': False,
                'directors_found': sum(len(company.get('directors', [])) for company in self.hierarchy.values()),
                'note': 'พิจารณาผู้บริหารสูงสุด (MD/CEO)'
            },
            'exemption_check': {
                'checked': True,
                'is_exempt': False,
                'reason': ''
            },
            'final_result': {
                'ubo_identified': len(final_ubos) > 0,
                'action': 'ปฏิเสธลูกค้า' if len(final_ubos) == 0 else 'ดำเนินการต่อ',
                'next_step': 'ปฏิเสธการสร้างความสัมพันธ์' if len(final_ubos) == 0 else 'ตรวจสอบ AMLO Watchlist'
            }
        }
    
    def _determine_risk_and_compliance(self, final_ubos: List[UBOCandidate]) -> tuple:
        """กำหนดระดับความเสี่ยงและสถานะการปฏิบัติตาม"""
        if len(final_ubos) > 0:
            return 'HIGH', 'COMPLIANT'
        else:
            return 'HIGH', 'NON_COMPLIANT'

# Global instances
api_client = CorrectEnliteAPIClient("HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV")
ubo_analyzer = CorrectUBOAnalyzer()

def analyze_company_ubo(registration_id: str) -> UBOAnalysisResult:
    """ฟังก์ชันหลักสำหรับวิเคราะห์ UBO"""
    return ubo_analyzer.analyze_company_hierarchy(api_client, registration_id)

if __name__ == "__main__":
    # ทดสอบระบบ
    test_company_id = "0107548000234"  # LH Bank
    result = analyze_company_ubo(test_company_id)
    
    print(f"Analysis completed for {test_company_id}")
    print(f"Total companies checked: {result.total_companies_checked}")
    print(f"Max level reached: {result.max_level_reached}")
    print(f"UBOs found: {len(result.final_ubos)}")
    
    for ubo in result.final_ubos:
        print(f"UBO: {ubo.name} - {ubo.total_percentage:.2f}%")
