#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced UBO Detection System
ระบบตรวจสอบผู้ได้รับผลประโยชน์ที่แท้จริงตามเอกสาร NC958 PRO05-2568

Features:
- Loop หาทุกทอด (สูงสุด 3 ทอด)
- เกณฑ์ UBO 15% ตามเอกสาร
- คำนวณสัดส่วนทางอ้อม
- Hierarchy Visualization
- Checklist ตามกระบวนการ
"""

import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import defaultdict, deque
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from io import BytesIO
import base64
import time

# Set Thai font for matplotlib
plt.rcParams['font.family'] = ['Tahoma', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']

# Try to set Thai font specifically
try:
    import matplotlib.font_manager as fm
    # Find Thai fonts
    thai_fonts = [f.name for f in fm.fontManager.ttflist if 'thai' in f.name.lower() or 'tahoma' in f.name.lower()]
    if thai_fonts:
        plt.rcParams['font.family'] = thai_fonts[0]
        print(f"Using Thai font: {thai_fonts[0]}")
except:
    pass

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
    effective_percentage: float = 0.0  # สัดส่วนทางอ้อม
    path: List[str] = None  # เส้นทางการถือหุ้น

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
    level: int = 0  # ระดับทอด
    parent_percentage: float = 0.0  # สัดส่วนจากบริษัทแม่

@dataclass
class UBOCandidate:
    """ผู้สมัคร UBO"""
    name: str
    total_percentage: float
    paths: List[List[str]]  # เส้นทางทั้งหมด
    method: int  # วิธีที่ใช้ระบุ (1, 2, 3)
    is_director: bool = False
    position: str = ""

@dataclass
class UBOAnalysisResult:
    """ผลการวิเคราะห์ UBO"""
    company_id: str
    company_name: str
    check_date: str
    hierarchy: Dict[str, Any]
    ubo_candidates: List[UBOCandidate]
    final_ubos: List[UBOCandidate]
    checklist: Dict[str, Any]
    method_used: int
    max_level_reached: int
    total_companies_checked: int
    risk_level: str
    compliance_status: str

class EnhancedEnliteAPIClient:
    """Enhanced Client สำหรับเรียกใช้ Enlite BOL API พร้อม Cache"""
    
    def __init__(self, api_key: str, base_url: str = "https://xignal-uat.bol.co.th"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': 'HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV',
            'Content-Type': 'text/xml',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Enhanced-UBO-System/1.0'
        })
        self.cache = {}  # Cache สำหรับลดการเรียก API ซ้ำ
        self.rate_limit_delay = 0.5  # Delay ระหว่างการเรียก API
    
    def get_company_data(self, registration_id: str, language: str = "EN") -> Dict[str, Any]:
        """
        ดึงข้อมูลบริษัทจาก Enlite API พร้อม Cache
        """
        # ตรวจสอบ Cache ก่อน
        cache_key = f"{registration_id}_{language}"
        if cache_key in self.cache:
            logger.info(f"Using cached data for {registration_id}")
            return self.cache[cache_key]
        
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
            logger.info(f"Making API request to: {self.base_url}/enlitews/companyData for {registration_id}")
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
            
            response = self.session.post(
                f"{self.base_url}/enlitews/companyData",
                data=soap_body,
                timeout=30
            )
            
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            
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
                    logger.error(f"No return data found for {registration_id}")
                    return None
            
            parsed_data = self._parse_company_data(return_data)
            
            # เก็บใน Cache
            self.cache[cache_key] = parsed_data
            
            return parsed_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {registration_id}: {e}")
            return None
        except ET.ParseError as e:
            logger.error(f"XML parsing failed for {registration_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {registration_id}: {e}")
            return None
    
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
        
        # Parse shareholders from levelHeldBy level 1, 2, 3
        held_by = return_data.find('.//heldBy')
        if held_by is not None:
            data['shareholders'] = []
            data['level_held_by'] = {}
            
            # Parse each level (1, 2, 3)
            for level in ['1', '2', '3']:
                level_held = held_by.find(f'.//levelHeldBy[@level="{level}"]')
                if level_held is not None:
                    level_shareholders = []
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
                            'shareholder_type': 'personal',  # Default
                            'level': int(level)
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
                        
                        level_shareholders.append(shareholder)
                        # เพิ่มใน main list เฉพาะถ้าเป็น level 1 เท่านั้น
                        if level == '1':
                            data['shareholders'].append(shareholder)
                    
                    data['level_held_by'][level] = level_shareholders
        
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

class EnhancedUBOAnalyzer:
    """ตัววิเคราะห์ UBO แบบ Enhanced ตามเอกสาร NC958 PRO05-2568"""
    
    def __init__(self):
        self.threshold_15 = 15.0  # เกณฑ์ 15% ตามเอกสาร
        self.max_levels = 3  # สูงสุด 3 ทอด
        self.ubo_candidates = {}  # Dictionary สำหรับเก็บ UBO candidates
        self.hierarchy = {}  # โครงสร้างการถือหุ้น
        self.processed_companies = set()  # บริษัทที่ตรวจสอบแล้ว
        self.total_companies_checked = 0
    
    def analyze_company_hierarchy(self, api_client: EnhancedEnliteAPIClient, 
                                 start_registration_id: str) -> UBOAnalysisResult:
        """
        วิเคราะห์ UBO แบบ Hierarchy ตามเอกสาร NC958 PRO05-2568
        """
        logger.info(f"Starting UBO analysis for company: {start_registration_id}")
        
        # Reset data structures
        self.ubo_candidates = {}
        self.hierarchy = {}
        self.processed_companies = set()
        self.total_companies_checked = 0
        
        # สร้าง Queue สำหรับการตรวจสอบแบบ BFS
        processing_queue = deque([(start_registration_id, 100.0, 0, [])])
        
        # เริ่มต้นการวิเคราะห์
        while processing_queue:
            current_id, cumulative_percentage, current_level, current_path = processing_queue.popleft()
            
            # ตรวจสอบความลึก - บังคับไป 3 ทอดเสมอ
            if current_level >= self.max_levels:
                logger.info(f"Reached max level {self.max_levels} for {current_id}")
                continue
            
            # ตรวจสอบว่าตรวจสอบบริษัทนี้แล้วหรือไม่
            if current_id in self.processed_companies:
                logger.info(f"Company {current_id} already processed, skipping")
                continue
            
            # เรียก API
            company_data = api_client.get_company_data(current_id)
            if not company_data:
                logger.warning(f"Failed to get data for company {current_id}")
                continue
            
            self.processed_companies.add(current_id)
            self.total_companies_checked += 1
            
            # Parse ข้อมูลบริษัท
            profile = company_data.get('profile', {})
            shareholders_data = company_data.get('shareholders', [])
            directors_data = company_data.get('directors', [])
            
            # บันทึกข้อมูลบริษัทใน Hierarchy
            self.hierarchy[current_id] = {
                'name_th': profile.get('name_th_full', ''),
                'name_en': profile.get('name_en_full', ''),
                'level': current_level,
                'parent_percentage': cumulative_percentage,
                'shareholders': [],
                'directors': directors_data,
                'path': current_path.copy(),
                'company_id': current_id,
                'status': profile.get('company_status', 'Active'),
                'capital': profile.get('capital', ''),
                'regis_date': profile.get('regis_date', ''),
                'address': profile.get('address', {}),
                'business_type': profile.get('business_type_th', '')
            }
            
            # ประมวลผลผู้ถือหุ้น
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
                        path=current_path + [current_id]
                    )
                    
                    # บันทึกใน Hierarchy
                    self.hierarchy[current_id]['shareholders'].append(asdict(shareholder))
                    
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
                        self.ubo_candidates[shareholder_name].paths.append(shareholder.path + [current_id])
                        
                        logger.info(f"Found individual shareholder: {shareholder_name} with {effective_percentage:.2f}%")
                    
                    elif shareholder_type == 'corporate' or regis_id_held_by:
                        # นิติบุคคล - เพิ่มใน Queue สำหรับตรวจสอบต่อ
                        if regis_id_held_by and regis_id_held_by not in self.processed_companies:
                            new_path = current_path + [current_id]
                            processing_queue.append((regis_id_held_by, effective_percentage, current_level + 1, new_path))
                            logger.info(f"Added corporate shareholder {regis_id_held_by} to queue for level {current_level + 1}")
                    
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error parsing shareholder data: {e}")
                    continue
        
        # ระบุ UBO สุดท้าย
        final_ubos = self._identify_final_ubos(company_data)
        
        # สร้าง Checklist
        checklist = self._create_checklist(final_ubos, company_data)
        
        # กำหนดระดับความเสี่ยงและสถานะการปฏิบัติตาม
        risk_level, compliance_status = self._determine_risk_and_compliance(final_ubos)
        
        return UBOAnalysisResult(
            company_id=start_registration_id,
            company_name=profile.get('name_th_full', ''),
            check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            hierarchy=self.hierarchy,
            ubo_candidates=list(self.ubo_candidates.values()),
            final_ubos=final_ubos,
            checklist=checklist,
            method_used=1 if final_ubos else 3,
            max_level_reached=max([company['level'] for company in self.hierarchy.values()]) if self.hierarchy else 0,
            total_companies_checked=self.total_companies_checked,
            risk_level=risk_level,
            compliance_status=compliance_status
        )
    
    def _identify_final_ubos(self, company_data: Dict[str, Any]) -> List[UBOCandidate]:
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
    
    def _create_checklist(self, final_ubos: List[UBOCandidate], company_data: Dict[str, Any]) -> Dict[str, Any]:
        """สร้าง Checklist ตามกระบวนการ"""
        profile = company_data.get('profile', {})
        
        # ตรวจสอบข้อยกเว้น
        is_exempt = False
        exempt_reason = ""
        
        if profile.get('set_symbol'):
            is_exempt = True
            exempt_reason = "บริษัทจดทะเบียนในตลาดหลักทรัพย์"
        
        checklist = {
            'exemption_check': {
                'checked': True,
                'is_exempt': is_exempt,
                'reason': exempt_reason
            },
            'method_1_check': {
                'checked': True,
                'found_ubo': len([ubo for ubo in final_ubos if ubo.method == 1]) > 0,
                'max_level_reached': self.max_levels,
                'companies_checked': self.total_companies_checked
            },
            'method_2_check': {
                'checked': len([ubo for ubo in final_ubos if ubo.method == 1]) == 0,
                'required': len([ubo for ubo in final_ubos if ubo.method == 1]) == 0,
                'note': 'ต้องตรวจสอบผู้มีอำนาจครอบงำกิจการ (Manual)'
            },
            'method_3_check': {
                'checked': len([ubo for ubo in final_ubos if ubo.method == 3]) > 0,
                'directors_found': len(company_data.get('directors', [])),
                'note': 'พิจารณาผู้บริหารสูงสุด (MD/CEO)'
            },
            'final_result': {
                'ubo_identified': len(final_ubos) > 0,
                'action': 'ดำเนินการต่อ' if len(final_ubos) > 0 else 'ปฏิเสธลูกค้า',
                'next_step': 'เก็บข้อมูล UBO เพิ่มเติม + ตรวจสอบ Watchlist' if len(final_ubos) > 0 else 'ปฏิเสธการสร้างความสัมพันธ์'
            }
        }
        
        return checklist
    
    def _determine_risk_and_compliance(self, final_ubos: List[UBOCandidate]) -> Tuple[str, str]:
        """กำหนดระดับความเสี่ยงและสถานะการปฏิบัติตาม"""
        if not final_ubos:
            return 'HIGH', 'NON_COMPLIANT'
        
        method_1_ubos = [ubo for ubo in final_ubos if ubo.method == 1]
        if method_1_ubos:
            max_percentage = max([ubo.total_percentage for ubo in method_1_ubos])
            if max_percentage >= 50:
                return 'HIGH', 'REVIEW_REQUIRED'
            elif max_percentage >= 25:
                return 'MEDIUM', 'COMPLIANT'
            else:
                return 'LOW', 'COMPLIANT'
        
        return 'MEDIUM', 'REVIEW_REQUIRED'

class EnhancedUBOVisualizer:
    """ตัวสร้างภาพการถือหุ้นแบบ Enhanced"""
    
    def __init__(self):
        self.colors = {
            'company': '#2E86AB',
            'ubo_15': '#A23B72',
            'director': '#F18F01',
            'other': '#C73E1D',
            'control': '#8B0000'
        }
    
    def create_hierarchy_chart(self, analysis_result: UBOAnalysisResult) -> str:
        """สร้างแผนภูมิ Hierarchy แบบ Tree"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        
        # สร้าง NetworkX graph
        G = nx.DiGraph()
        
        # เพิ่ม nodes และ edges
        for company_id, company_data in analysis_result.hierarchy.items():
            G.add_node(company_id, 
                      name=company_data['name_th'] or company_data['name_en'],
                      level=company_data['level'],
                      type='company')
            
            for shareholder in company_data['shareholders']:
                shareholder_name = shareholder['name']
                if shareholder['shareholder_type'] == 'personal':
                    G.add_node(shareholder_name, 
                              name=shareholder_name,
                              level=company_data['level'] + 1,
                              type='person',
                              percentage=shareholder['effective_percentage'])
                else:
                    # Corporate shareholder
                    if shareholder['regis_id']:
                        G.add_node(shareholder['regis_id'], 
                                  name=shareholder_name,
                                  level=company_data['level'] + 1,
                                  type='company')
                
                # Add edge
                if shareholder['shareholder_type'] == 'personal':
                    G.add_edge(company_id, shareholder_name, 
                              percentage=shareholder['percent'])
                elif shareholder['regis_id']:
                    G.add_edge(company_id, shareholder['regis_id'], 
                              percentage=shareholder['percent'])
        
        # Layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw nodes
        for node, data in G.nodes(data=True):
            x, y = pos[node]
            
            if data['type'] == 'company':
                color = self.colors['company']
                size = 1000
            elif data['type'] == 'person':
                percentage = data.get('percentage', 0)
                if percentage >= 15:
                    color = self.colors['ubo_15']
                    size = 1500
                else:
                    color = self.colors['other']
                    size = 800
            else:
                color = self.colors['other']
                size = 800
            
            ax.scatter(x, y, c=color, s=size, alpha=0.7, edgecolors='black', linewidth=2)
            
            # Add labels
            label = data['name'][:20] + '...' if len(data['name']) > 20 else data['name']
            ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Draw edges
        for edge in G.edges():
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.5, linewidth=1)
        
        ax.set_title(f'UBO Hierarchy Analysis - {analysis_result.company_name}\n'
                    f'Risk Level: {analysis_result.risk_level} | '
                    f'Method Used: {analysis_result.method_used} | '
                    f'Max Level: {analysis_result.max_level_reached}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Add legend
        legend_elements = [
            patches.Patch(color=self.colors['company'], label='Company'),
            patches.Patch(color=self.colors['ubo_15'], label='UBO ≥15%'),
            patches.Patch(color=self.colors['other'], label='Other Shareholders')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        ax.axis('off')
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_checklist_chart(self, analysis_result: UBOAnalysisResult) -> str:
        """สร้างแผนภูมิ Checklist"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        checklist = analysis_result.checklist
        
        # Checklist items
        checklist_items = [
            ('ตรวจสอบข้อยกเว้น', checklist['exemption_check']['checked'], 
             'ยกเว้น' if checklist['exemption_check']['is_exempt'] else 'ไม่ยกเว้น'),
            ('วิธีที่ 1: ตรวจสอบการถือหุ้น', checklist['method_1_check']['checked'],
             f"ตรวจสอบ {checklist['method_1_check']['companies_checked']} บริษัท"),
            ('พบ UBO ≥15%', checklist['method_1_check']['found_ubo'],
             f"พบ {len([ubo for ubo in analysis_result.final_ubos if ubo.method == 1])} คน"),
            ('วิธีที่ 2: อำนาจครอบงำ', checklist['method_2_check']['checked'],
             'ต้องตรวจสอบเพิ่มเติม' if checklist['method_2_check']['required'] else 'ไม่จำเป็น'),
            ('วิธีที่ 3: ผู้บริหารสูงสุด', checklist['method_3_check']['checked'],
             f"พบ {checklist['method_3_check']['directors_found']} กรรมการ"),
            ('ระบุ UBO ได้', checklist['final_result']['ubo_identified'],
             checklist['final_result']['action'])
        ]
        
        y_positions = range(len(checklist_items))
        
        for i, (item, status, detail) in enumerate(checklist_items):
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
            ax.text(0.5, i * 0.12 + 0.14, f"{symbol} {item}\n{detail}", 
                   ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        ax.set_title(f'UBO Analysis Checklist\n{analysis_result.company_name}\n'
                    f'Method Used: {analysis_result.method_used} | '
                    f'Risk Level: {analysis_result.risk_level}', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64

class EnhancedUBOSystem:
    """ระบบหลักสำหรับตรวจสอบ UBO แบบ Enhanced"""
    
    def __init__(self, api_key: str):
        self.api_client = EnhancedEnliteAPIClient(api_key)
        self.analyzer = EnhancedUBOAnalyzer()
        self.visualizer = EnhancedUBOVisualizer()
        self.results = []
    
    def analyze_company_hierarchy(self, registration_id: str) -> UBOAnalysisResult:
        """วิเคราะห์บริษัทแบบ Hierarchy"""
        try:
            logger.info(f"Starting enhanced UBO analysis for: {registration_id}")
            result = self.analyzer.analyze_company_hierarchy(self.api_client, registration_id)
            self.results.append(result)
            return result
        except Exception as e:
            logger.error(f"Error in enhanced UBO analysis for {registration_id}: {e}")
            raise
    
    def generate_enhanced_report(self, analysis_result: UBOAnalysisResult) -> Dict[str, Any]:
        """สร้างรายงานแบบ Enhanced"""
        hierarchy_chart = self.visualizer.create_hierarchy_chart(analysis_result)
        checklist_chart = self.visualizer.create_checklist_chart(analysis_result)
        
        report = {
            'company_info': {
                'id': analysis_result.company_id,
                'name': analysis_result.company_name,
                'check_date': analysis_result.check_date
            },
            'analysis_summary': {
                'method_used': analysis_result.method_used,
                'max_level_reached': analysis_result.max_level_reached,
                'total_companies_checked': analysis_result.total_companies_checked,
                'risk_level': analysis_result.risk_level,
                'compliance_status': analysis_result.compliance_status
            },
            'ubo_results': {
                'total_candidates': len(analysis_result.ubo_candidates),
                'final_ubos': len(analysis_result.final_ubos),
                'ubo_details': [asdict(ubo) for ubo in analysis_result.final_ubos]
            },
            'hierarchy': analysis_result.hierarchy,
            'checklist': analysis_result.checklist,
            'charts': {
                'hierarchy': hierarchy_chart,
                'checklist': checklist_chart
            }
        }
        
        return report

def main():
    """ตัวอย่างการใช้งาน Enhanced UBO System"""
    # API Key จาก Postman Collection
    API_KEY = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    
    # สร้างระบบ Enhanced UBO
    enhanced_ubo_system = EnhancedUBOSystem(API_KEY)
    
    # วิเคราะห์ LAND AND HOUSES BANK
    registration_id = "0107548000234"
    
    try:
        print(f"🚀 Enhanced UBO Analysis - LAND AND HOUSES BANK")
        print("=" * 60)
        
        result = enhanced_ubo_system.analyze_company_hierarchy(registration_id)
        
        print(f"✅ ผลการวิเคราะห์ Enhanced UBO")
        print(f"   🏢 บริษัท: {result.company_name}")
        print(f"   🆔 เลขทะเบียน: {result.company_id}")
        print(f"   📅 วันที่ตรวจสอบ: {result.check_date}")
        print(f"   🔍 วิธีที่ใช้: {result.method_used}")
        print(f"   📊 ระดับสูงสุดที่ตรวจสอบ: {result.max_level_reached}")
        print(f"   🏢 จำนวนบริษัทที่ตรวจสอบ: {result.total_companies_checked}")
        print(f"   ⚠️  ระดับความเสี่ยง: {result.risk_level}")
        print(f"   ✅ สถานะการปฏิบัติตาม: {result.compliance_status}")
        
        print(f"\n📊 รายละเอียด UBO")
        print("-" * 40)
        
        if result.final_ubos:
            for i, ubo in enumerate(result.final_ubos, 1):
                print(f"   {i}. {ubo.name}")
                print(f"      วิธีที่ใช้: {ubo.method}")
                print(f"      สัดส่วนการถือหุ้น: {ubo.total_percentage:.2f}%")
                print(f"      จำนวนเส้นทาง: {len(ubo.paths)}")
                if ubo.is_director:
                    print(f"      ตำแหน่ง: {ubo.position}")
                print()
        else:
            print("   ไม่พบ UBO")
        
        print(f"\n📋 Checklist การตรวจสอบ")
        print("-" * 40)
        checklist = result.checklist
        print(f"   ✅ ตรวจสอบข้อยกเว้น: {'ยกเว้น' if checklist['exemption_check']['is_exempt'] else 'ไม่ยกเว้น'}")
        print(f"   ✅ วิธีที่ 1: {'พบ UBO' if checklist['method_1_check']['found_ubo'] else 'ไม่พบ UBO'}")
        print(f"   ✅ วิธีที่ 2: {'ต้องตรวจสอบ' if checklist['method_2_check']['required'] else 'ไม่จำเป็น'}")
        print(f"   ✅ วิธีที่ 3: {'พบกรรมการ' if checklist['method_3_check']['checked'] else 'ไม่พบกรรมการ'}")
        print(f"   ✅ ผลลัพธ์สุดท้าย: {checklist['final_result']['action']}")
        
        # สร้างรายงาน
        report = enhanced_ubo_system.generate_enhanced_report(result)
        
        # บันทึกรายงาน
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f"enhanced_ubo_report_{registration_id}_{timestamp}.json"
        
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 รายงานถูกบันทึกเป็น: {report_filename}")
        
        print(f"\n🎉 การวิเคราะห์ Enhanced UBO เสร็จสิ้น!")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        logger.exception("Full error details:")

if __name__ == "__main__":
    main()
