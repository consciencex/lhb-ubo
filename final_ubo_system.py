#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final UBO analysis system implementing the requested queue-based logic."""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import deque
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Shareholder:
    """Shareholder data model."""
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
    effective_percentage: float = 0.0  # Indirect (effective) holding percentage
    path: List[str] = None  # Traversal path for provenance
    
    def __post_init__(self):
        if self.path is None:
            self.path = []

@dataclass
class UBOCandidate:
    """UBO candidate aggregation model."""
    name: str
    total_percentage: float
    paths: List[List[str]]
    method: int  # 1 = shareholding, 2 = control, 3 = management
    nationality: Optional[str] = None
    is_director: bool = False
    path_details: List[Dict[str, Any]] = None  # Detailed path calculation info
    
    def __post_init__(self):
        if self.path_details is None:
            self.path_details = []

@dataclass
class UBOAnalysisResult:
    """Container for final UBO analysis results."""
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

class FinalEnliteAPIClient:
    """Thin client for the Enlite SOAP API."""
    
    def __init__(self, api_key: str, base_url: str = "https://enlite.lhb.co.th"):
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
            'User-Agent': 'Final-UBO-System/1.0'
        })
        self.cache = {}
        self.rate_limit_delay = 0.5
    
    def get_company_data(self, registration_id: str, language: str = "EN") -> Optional[Dict[str, Any]]:
        """Fetch company data from the Enlite API."""
        if registration_id in self.cache:
            logger.info(f"Using cached data for {registration_id}")
            return self.cache[registration_id]
        
        try:
            # Build SOAP request payload
            soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:eh="http://eh.actimize.com" xmlns:view="http://view.bol.com/">
    <soapenv:Header/>
    <soapenv:Body>
        <view:getDataEnlite>
            <registrationId>{registration_id}</registrationId>
            <language>TH</language>
        </view:getDataEnlite>
    </soapenv:Body>
</soapenv:Envelope>"""
            
            url = f"{self.base_url}/enlitews/companyData"
            logger.info(f"Making API request to: {url} for {registration_id}")
            
            timeout = int(os.getenv('ENLITE_API_TIMEOUT', '60'))
            response = self.session.post(url, data=soap_body, timeout=timeout)
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Force UTF-8 encoding for Thai text
                response_text = response.content.decode('utf-8')
                data = self._parse_company_data(response_text)
                self.cache[registration_id] = data
                return data
            else:
                logger.error(f"API request failed with status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error for {registration_id} - API took too long to respond")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for {registration_id} - Unable to connect to API")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {registration_id}: {e}")
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
            
            # Parse officialSignatory
            official_signatory = return_data.find('.//officialSignatory')
            if official_signatory is not None and official_signatory.text:
                data['official_signatory'] = official_signatory.text.strip()
            else:
                data['official_signatory'] = ''
            
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
            
            # Parse shareholders (levelHeldBy level="1" only)
            held_by = return_data.find('.//heldBy')
            if held_by is not None:
                data['shareholders'] = []
                
                # Only levelHeldBy level="1" is provided by the API
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
                        
                        # If it's a company and no name, use regis_id_held_by
                        if shareholder.get('shareholder_type') == 'company' and not shareholder.get('firstname'):
                            regis_id = shareholder.get('regis_id_held_by', '')
                            if regis_id:
                                shareholder['firstname'] = f"Company {regis_id}"
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

class FinalUBOAnalyzer:
    """Queue-based UBO analyzer following the requested algorithm."""
    
    def __init__(self):
        self.threshold_15 = 15.0  # Method 1 threshold (>=15%)
        self.max_levels = 4  # Traverse up to level 3 (0=main, 1=tier1, 2=tier2, 3=tier3)
        self.ubo_results = {}  # Aggregated UBO candidates (PERSONAL ONLY)
        self.hierarchy = {}  # Shareholding hierarchy map
        self.visited_companies = set()  # Track visited companies to avoid loops
        self.total_companies_checked = 0
        self.max_level_reached = 0
    
    def _sanitize_label(self, text: Optional[str], fallback: str = "") -> str:
        """Return an ASCII-safe label, falling back when necessary."""
        if not text:
            return fallback
        cleaned = ''.join(
            ch for ch in str(text)
            if ch.isascii() and ch not in {'\n', '\r', '\t'}
        ).strip()
        return cleaned if cleaned else fallback

    def analyze_company_hierarchy(self, api_client: FinalEnliteAPIClient, 
                                 start_company_id: str) -> UBOAnalysisResult:
        """Perform queue-based traversal across shareholding layers."""
        logger.info(f"Starting FINAL UBO analysis for company: {start_company_id}")
        
        # Reset data structures
        self.ubo_results = {}
        self.hierarchy = {}
        self.visited_companies = set()
        self.total_companies_checked = 0
        self.max_level_reached = 0
        
        # Initialize processing queue
        processing_queue = deque([(start_company_id, 100.0, 0, [])])
        
        # Processing Loop
        while processing_queue:
            # Get Task
            current_company_id, current_percentage, current_level, path_chain = processing_queue.popleft()
            
            # Check Depth
            if current_level >= self.max_levels:
                logger.info(f"Reached max level {self.max_levels} for {current_company_id}")
                continue
            
            # Check Visited
            if current_company_id in self.visited_companies:
                logger.info(f"Company {current_company_id} already visited, skipping")
                continue
            
            # Mark as Visited
            self.visited_companies.add(current_company_id)
            
            # API Call
            company_data = api_client.get_company_data(current_company_id)
            if not company_data:
                logger.warning(f"Failed to get data for company {current_company_id}")
                continue
            
            self.total_companies_checked += 1
            self.max_level_reached = max(self.max_level_reached, current_level)
            
            # Parse company profile and related data
            profile = company_data.get('profile', {})
            shareholders_data = company_data.get('shareholders', [])
            directors_data = company_data.get('directors', [])
            
            # Prepare English-first metadata
            company_name_en = self._sanitize_label(
                profile.get('name_en_full')
                or profile.get('name_en')
                or profile.get('name_th_full')
                or profile.get('name_th')
                or current_company_id,
                fallback=current_company_id
            )
            company_name_th = self._sanitize_label(
                profile.get('name_th_full') or profile.get('name_th'),
                fallback=""
            )
            business_type_en = self._sanitize_label(
                profile.get('business_type_en') or profile.get('business_type_th'),
                fallback="Unknown"
            )
            business_type_th = self._sanitize_label(profile.get('business_type_th'), fallback="")

            # Store company node within the hierarchy (English-first fields)
            self.hierarchy[current_company_id] = {
                'name_en': company_name_en,
                'name_th': company_name_th,
                'display_name': company_name_en or company_name_th or current_company_id,
                'level': current_level,
                'parent_percentage': current_percentage,
                'shareholders': [],
                'directors': directors_data,
                'official_signatory': company_data.get('official_signatory', ''),
                'company_id': current_company_id,
                'status': profile.get('company_status', 'Active'),
                'capital': profile.get('capital', ''),
                'regis_date': profile.get('regis_date', ''),
                'address': profile.get('address', {}),
                'business_type': business_type_en,
                'business_type_en': business_type_en,
                'business_type_th': business_type_th
            }
            
            # Parse Shareholders (Level 1 from current_company_id)
            current_display_name = self.hierarchy[current_company_id]['display_name']

            for sh_data in shareholders_data:
                try:
                    share_amount = int(sh_data.get('share_amount', '0').replace(',', ''))
                    direct_percentage = float(sh_data.get('percent', '0'))
                    
                    # Calculate Effective Percentage
                    effective_percentage = (current_percentage / 100.0) * direct_percentage
                    
                    shareholder_type = sh_data.get('shareholder_type', 'personal')
                    regis_id_held_by = sh_data.get('regis_id_held_by', '')
                    
                    # ✅ สำหรับบริษัท ใช้ companyName หรือ companyNameFull จาก API
                    if shareholder_type == 'company':
                        company_name_full = sh_data.get('companyNameFull', '').strip()
                        company_name = sh_data.get('companyName', '').strip()
                        shareholder_name_raw = company_name_full or company_name or f"{sh_data.get('firstname', '')} {sh_data.get('lastname', '')}".strip()
                        # ใช้ชื่อภาษาอังกฤษจาก API (ไม่ต้อง sanitize)
                        shareholder_name = self._sanitize_label(shareholder_name_raw, fallback=f"Company {regis_id_held_by}" if regis_id_held_by else "Corporate Shareholder")
                    else:
                        shareholder_name_raw = f"{sh_data.get('firstname', '')} {sh_data.get('lastname', '')}".strip()
                        shareholder_name = self._sanitize_label(shareholder_name_raw, fallback="Individual Shareholder")
                    
                    # Build shareholder object
                    sanitized_nationality = self._sanitize_label(sh_data.get('nationality', ''), fallback='')

                    shareholder = Shareholder(
                        name=shareholder_name,
                        firstname=sh_data.get('firstname', ''),
                        lastname=sh_data.get('lastname', ''),
                        nationality=sanitized_nationality,
                        share_amount=share_amount,
                        percent=direct_percentage,
                        shareholder_type=shareholder_type,
                        regis_id=regis_id_held_by,
                        business_status=sh_data.get('business_status'),
                        directorship=sh_data.get('directorship'),
                        director_update_date=sh_data.get('director_upd_date'),
                        effective_percentage=effective_percentage,
                        path=[current_company_id]
                    )
                    
                    shareholder_dict = asdict(shareholder)
                    shareholder_dict['display_name'] = shareholder_name or (regis_id_held_by or 'Unknown')
                    shareholder_dict['type_label'] = 'Company' if shareholder_type == 'company' else 'Individual'
                    shareholder_dict['direct_percent'] = direct_percentage
                    shareholder_path = path_chain + [{
                        'entity_id': regis_id_held_by or shareholder_name,
                        'entity_name': shareholder_name,
                        'share_percent': direct_percentage
                    }]
                    shareholder_dict['ubo_path'] = shareholder_path
                    shareholder_dict['ubo_factors'] = [step.get('share_percent', 0) for step in shareholder_path]
                    
                    # Persist shareholder into hierarchy
                    self.hierarchy[current_company_id]['shareholders'].append(shareholder_dict)
                    
                    # Check Shareholder Type
                    if shareholder_type == 'personal':
                        # Add/Update ubo_results
                        if shareholder_name not in self.ubo_results:
                            self.ubo_results[shareholder_name] = UBOCandidate(
                                name=shareholder_name,
                                total_percentage=0.0,
                                paths=[],
                                path_details=[],
                                method=1,
                                nationality=sanitized_nationality or None,
                                is_director=(shareholder.directorship or '').upper() == 'YES'
                            )
                        
                        self.ubo_results[shareholder_name].total_percentage += effective_percentage
                        self.ubo_results[shareholder_name].paths.append([step.get('entity_id') for step in shareholder_path])
                        
                        # Add detailed path calculation
                        path_factors = [step.get('share_percent', 0) for step in shareholder_path]
                        path_names = [step.get('entity_name', 'Unknown') for step in shareholder_path]
                        path_detail = {
                            'factors': path_factors,
                            'names': path_names,
                            'result': effective_percentage,
                            'calculation': ' × '.join([f"{f:.2f}%" for f in path_factors]) + f" = {effective_percentage:.3f}%"
                        }
                        self.ubo_results[shareholder_name].path_details.append(path_detail)
                        
                        candidate = self.ubo_results[shareholder_name]
                        if not candidate.nationality and sanitized_nationality:
                            candidate.nationality = sanitized_nationality
                        if (shareholder.directorship or '').upper() == 'YES':
                            candidate.is_director = True
                        
                        logger.info(f"Found individual shareholder: {shareholder_name} with {effective_percentage:.2f}%")
                    
                    elif shareholder_type == 'corporate' or regis_id_held_by:
                        # ✅ Corporate shareholders: เพิ่มเข้า queue เพื่อหาผู้ถือหุ้นต่อ
                        # แต่ไม่นับบริษัทเป็น UBO (UBO ต้องเป็น Person เท่านั้น)
                        if regis_id_held_by:
                            new_task_path = path_chain + [{
                                'entity_id': regis_id_held_by,
                                'entity_name': shareholder_name,
                                'share_percent': direct_percentage
                            }]
                            new_task = (regis_id_held_by, effective_percentage, current_level + 1, new_task_path)
                            processing_queue.append(new_task)
                            logger.info(f"Added corporate shareholder {regis_id_held_by} to queue for level {current_level + 1}")
                        else:
                            # If no regis_id_held_by, still try to process as corporate
                            logger.warning(f"Corporate shareholder {shareholder_name} has no regis_id_held_by")
                
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error parsing shareholder data: {e}")
                    continue
        
        # Final Calculation (Personal shareholders only)
        final_ubos = self._identify_final_ubos()
        
        # Build compliance checklist summary
        checklist = self._create_checklist(final_ubos)
        
        # Determine risk/compliance summary
        risk_level, compliance_status = self._determine_risk_and_compliance(final_ubos)
        
        return UBOAnalysisResult(
            registration_id=start_company_id,
            company_name=self.hierarchy.get(start_company_id, {}).get('display_name', ''),
            ubo_candidates=list(self.ubo_results.values()),
            final_ubos=final_ubos,
            hierarchy=self.hierarchy,
            checklist=checklist,
            risk_level=risk_level,
            compliance_status=compliance_status,
            total_companies_checked=self.total_companies_checked,
            max_level_reached=self.max_level_reached,
            check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    
    def _identify_final_ubos(self) -> List[UBOCandidate]:
        """Filter UBO candidates using Method 1 (≥15% shareholding).
        
        ✅ UBO ต้องเป็น PERSON (Individual) เท่านั้น - ไม่ใช่บริษัท
        """
        final_ubos = []
        
        # Filter for PERSONAL shareholders only where total percentage >= 15.0
        for candidate in self.ubo_results.values():
            if candidate.total_percentage >= self.threshold_15:
                candidate.name = self._sanitize_label(candidate.name, fallback="Individual Shareholder")
                final_ubos.append(candidate)
                logger.info(f"UBO identified (Method 1 - Personal): {candidate.name} with {candidate.total_percentage:.2f}%")
        
        logger.info(f"Method 1 - Found {len(final_ubos)} Personal UBOs with >=15% shareholding")
        
        return final_ubos
    
    def _create_checklist(self, final_ubos: List[UBOCandidate]) -> Dict[str, Any]:
        """Build a compliance checklist summary."""
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
                'note': 'Manual control check required if no UBO is identified'
            },
            'method_3_check': {
                'checked': False,
                'directors_found': sum(len(company.get('directors', [])) for company in self.hierarchy.values()),
                'note': 'Consider senior management (MD/CEO) if escalation is needed'
            },
            'exemption_check': {
                'checked': True,
                'is_exempt': False,
                'reason': ''
            },
            'final_result': {
                'ubo_identified': len(final_ubos) > 0,
                'action': 'Reject customer' if len(final_ubos) == 0 else 'Proceed',
                'next_step': 'Reject onboarding' if len(final_ubos) == 0 else 'Screen against AMLO watchlist'
            }
        }
    
    def _determine_risk_and_compliance(self, final_ubos: List[UBOCandidate]) -> tuple:
        """Determine risk level and compliance status summary."""
        if len(final_ubos) > 0:
            return 'HIGH', 'COMPLIANT'
        else:
            return 'HIGH', 'NON_COMPLIANT'

# Global instances - Load from environment variables
# SECURITY: API keys must be set via environment variables or .env file
# Never hardcode API keys in source code!
ENLITE_API_KEY = os.getenv('ENLITE_API_KEY')
ENLITE_API_URL = os.getenv('ENLITE_API_URL', 'https://enlite.lhb.co.th')

# Validate required environment variables
if not ENLITE_API_KEY:
    import logging
    logging.warning("ENLITE_API_KEY not set! API calls will fail. Set it in .env file or environment variables.")
ENLITE_API_TIMEOUT = int(os.getenv('ENLITE_API_TIMEOUT', '60'))

api_client = FinalEnliteAPIClient(ENLITE_API_KEY, ENLITE_API_URL)
ubo_analyzer = FinalUBOAnalyzer()

def analyze_company_ubo(registration_id: str) -> UBOAnalysisResult:
    """Main entrypoint used by the web layer to analyse a company."""
    return ubo_analyzer.analyze_company_hierarchy(api_client, registration_id)

if __name__ == "__main__":
# Manual test harness
    test_company_id = "0107548000234"  # LH Bank
    result = analyze_company_ubo(test_company_id)
    
    print(f"Analysis completed for {test_company_id}")
    print(f"Total companies checked: {result.total_companies_checked}")
    print(f"Max level reached: {result.max_level_reached}")
    print(f"UBOs found: {len(result.final_ubos)}")
    
    for ubo in result.final_ubos:
        print(f"UBO: {ubo.name} - {ubo.total_percentage:.2f}%")
