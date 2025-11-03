#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock UBO System for Testing
ระบบ UBO แบบ Mock สำหรับทดสอบเมื่อ API ไม่พร้อมใช้งาน
"""

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
plt.rcParams['font.family'] = ['Tahoma', 'DejaVu Sans', 'Arial Unicode MS']

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
    is_director: bool = False

@dataclass
class Company:
    """ข้อมูลบริษัท"""
    regis_id: str
    name_th: str
    name_en: str
    status: str
    shareholders: List[Shareholder]
    directors: List[Dict[str, str]]

@dataclass
class UBOCandidate:
    """ข้อมูลผู้สมัคร UBO"""
    name: str
    firstname: str
    lastname: str
    nationality: str
    total_percentage: float
    direct_percentage: float
    indirect_percentage: float
    ownership_paths: List[List[str]]
    is_director: bool = False
    identification_method: str = "Method 1"  # Method 1, 2, or 3

class MockUBOSystem:
    """ระบบ UBO แบบ Mock สำหรับทดสอบ"""
    
    def __init__(self):
        self.threshold_15 = 15.0
        self.max_levels = 3
        self.ubo_candidates = {}
        self.hierarchy = {}
        self.processed_companies = set()
        
        # Mock data for testing
        self.mock_data = self._create_mock_data()
    
    def _create_mock_data(self) -> Dict[str, Company]:
        """สร้าง Mock Data สำหรับทดสอบ"""
        
        # LH Bank Mock Data
        lh_bank_shareholders = [
            Shareholder(
                name="นายสมชาย ใจดี",
                firstname="สมชาย",
                lastname="ใจดี",
                nationality="Thai",
                share_amount=15000000,
                percent=15.0,
                shareholder_type="personal",
                regis_id="1234567890123",
                is_director=True
            ),
            Shareholder(
                name="บริษัท เอเชีย พรอพเพอร์ตี้ จำกัด",
                firstname="",
                lastname="",
                nationality="Thai",
                share_amount=20000000,
                percent=20.0,
                shareholder_type="corporate",
                regis_id="0105517006433",
                is_director=False
            ),
            Shareholder(
                name="นางสาวสมหญิง รักดี",
                firstname="สมหญิง",
                lastname="รักดี",
                nationality="Thai",
                share_amount=12000000,
                percent=12.0,
                shareholder_type="personal",
                regis_id="1234567890124",
                is_director=True
            ),
            Shareholder(
                name="นายสมศักดิ์ เก่งดี",
                firstname="สมศักดิ์",
                lastname="เก่งดี",
                nationality="Thai",
                share_amount=8000000,
                percent=8.0,
                shareholder_type="personal",
                regis_id="1234567890125",
                is_director=False
            ),
            Shareholder(
                name="บริษัท ไทยแลนด์ โฮลดิ้ง จำกัด",
                firstname="",
                lastname="",
                nationality="Thai",
                share_amount=25000000,
                percent=25.0,
                shareholder_type="corporate",
                regis_id="0105547107432",
                is_director=False
            ),
            Shareholder(
                name="นางสมพร ดีมาก",
                firstname="สมพร",
                lastname="ดีมาก",
                nationality="Thai",
                share_amount=10000000,
                percent=10.0,
                shareholder_type="personal",
                regis_id="1234567890126",
                is_director=True
            ),
            Shareholder(
                name="นายสมบูรณ์ เก่งมาก",
                firstname="สมบูรณ์",
                lastname="เก่งมาก",
                nationality="Thai",
                share_amount=9000000,
                percent=9.0,
                shareholder_type="personal",
                regis_id="1234567890127",
                is_director=False
            )
        ]
        
        lh_bank_directors = [
            {"title": "นาย", "firstname": "สมชาย", "lastname": "ใจดี"},
            {"title": "นางสาว", "firstname": "สมหญิง", "lastname": "รักดี"},
            {"title": "นาง", "firstname": "สมพร", "lastname": "ดีมาก"},
            {"title": "นาย", "firstname": "สมศักดิ์", "lastname": "เก่งดี"}
        ]
        
        lh_bank = Company(
            regis_id="0107548000234",
            name_th="ธนาคารแลนด์ แอนด์ เฮาส์ จำกัด (มหาชน)",
            name_en="LAND AND HOUSES BANK PUBLIC COMPANY LIMITED",
            status="Active",
            shareholders=lh_bank_shareholders,
            directors=lh_bank_directors
        )
        
        # Asia Property Mock Data (Level 2)
        asia_property_shareholders = [
            Shareholder(
                name="นายสมชาย ใจดี",
                firstname="สมชาย",
                lastname="ใจดี",
                nationality="Thai",
                share_amount=8000000,
                percent=40.0,
                shareholder_type="personal",
                regis_id="1234567890123",
                is_director=True
            ),
            Shareholder(
                name="นางสาวสมหญิง รักดี",
                firstname="สมหญิง",
                lastname="รักดี",
                nationality="Thai",
                share_amount=6000000,
                percent=30.0,
                shareholder_type="personal",
                regis_id="1234567890124",
                is_director=True
            ),
            Shareholder(
                name="นายสมศักดิ์ เก่งดี",
                firstname="สมศักดิ์",
                lastname="เก่งดี",
                nationality="Thai",
                share_amount=6000000,
                percent=30.0,
                shareholder_type="personal",
                regis_id="1234567890125",
                is_director=False
            )
        ]
        
        asia_property_directors = [
            {"title": "นาย", "firstname": "สมชาย", "lastname": "ใจดี"},
            {"title": "นางสาว", "firstname": "สมหญิง", "lastname": "รักดี"}
        ]
        
        asia_property = Company(
            regis_id="0105517006433",
            name_th="บริษัท เอเชีย พรอพเพอร์ตี้ จำกัด",
            name_en="ASIA PROPERTY COMPANY LIMITED",
            status="Active",
            shareholders=asia_property_shareholders,
            directors=asia_property_directors
        )
        
        # Thailand Holding Mock Data (Level 2)
        thailand_holding_shareholders = [
            Shareholder(
                name="นายสมบูรณ์ เก่งมาก",
                firstname="สมบูรณ์",
                lastname="เก่งมาก",
                nationality="Thai",
                share_amount=10000000,
                percent=50.0,
                shareholder_type="personal",
                regis_id="1234567890127",
                is_director=True
            ),
            Shareholder(
                name="นางสมพร ดีมาก",
                firstname="สมพร",
                lastname="ดีมาก",
                nationality="Thai",
                share_amount=10000000,
                percent=50.0,
                shareholder_type="personal",
                regis_id="1234567890126",
                is_director=True
            )
        ]
        
        thailand_holding_directors = [
            {"title": "นาย", "firstname": "สมบูรณ์", "lastname": "เก่งมาก"},
            {"title": "นาง", "firstname": "สมพร", "lastname": "ดีมาก"}
        ]
        
        thailand_holding = Company(
            regis_id="0105547107432",
            name_th="บริษัท ไทยแลนด์ โฮลดิ้ง จำกัด",
            name_en="THAILAND HOLDING COMPANY LIMITED",
            status="Active",
            shareholders=thailand_holding_shareholders,
            directors=thailand_holding_directors
        )
        
        return {
            "0107548000234": lh_bank,
            "0105517006433": asia_property,
            "0105547107432": thailand_holding
        }
    
    def get_company_data(self, registration_id: str) -> Optional[Company]:
        """ดึงข้อมูลบริษัทจาก Mock Data"""
        logger.info(f"Getting mock data for company: {registration_id}")
        return self.mock_data.get(registration_id)
    
    def analyze_ubo(self, company_id: str) -> Dict[str, Any]:
        """วิเคราะห์ UBO ตามเอกสาร NC958 PRO05-2568"""
        logger.info(f"Starting UBO analysis for company: {company_id}")
        
        # Reset for new analysis
        self.ubo_candidates = {}
        self.hierarchy = {}
        self.processed_companies = set()
        
        # Get company data
        company = self.get_company_data(company_id)
        if not company:
            return {
                "error": f"Company {company_id} not found in mock data",
                "company_info": None,
                "ubos": [],
                "checklist": {},
                "hierarchy_graph": None,
                "analysis_summary": "Analysis failed - company not found"
            }
        
        # Build hierarchy using BFS
        queue = deque([(company_id, 0, 1.0, [company_id])])  # (company_id, level, effective_percentage, path)
        
        while queue:
            current_id, level, effective_percent, path = queue.popleft()
            
            if current_id in self.processed_companies or level >= self.max_levels:
                continue
            
            self.processed_companies.add(current_id)
            current_company = self.get_company_data(current_id)
            
            if not current_company:
                continue
            
            # Store in hierarchy
            self.hierarchy[current_id] = {
                "name_th": current_company.name_th,
                "name_en": current_company.name_en,
                "level": level,
                "shareholders": []
            }
            
            # Process shareholders
            for shareholder in current_company.shareholders:
                shareholder_info = {
                    "name": shareholder.name,
                    "firstname": shareholder.firstname,
                    "lastname": shareholder.lastname,
                    "nationality": shareholder.nationality,
                    "percent": shareholder.percent,
                    "share_amount": shareholder.share_amount,
                    "shareholder_type": shareholder.shareholder_type,
                    "regis_id": shareholder.regis_id,
                    "is_director": shareholder.is_director
                }
                
                self.hierarchy[current_id]["shareholders"].append(shareholder_info)
                
                # Calculate effective percentage
                effective_percentage = effective_percent * (shareholder.percent / 100.0)
                
                if shareholder.shareholder_type == "personal":
                    # Natural person - potential UBO
                    full_name = f"{shareholder.firstname} {shareholder.lastname}".strip()
                    
                    if full_name not in self.ubo_candidates:
                        self.ubo_candidates[full_name] = UBOCandidate(
                            name=full_name,
                            firstname=shareholder.firstname,
                            lastname=shareholder.lastname,
                            nationality=shareholder.nationality,
                            total_percentage=0.0,
                            direct_percentage=0.0,
                            indirect_percentage=0.0,
                            ownership_paths=[],
                            is_director=shareholder.is_director
                        )
                    
                    # Add ownership path
                    ownership_path = path + [current_id]
                    self.ubo_candidates[full_name].ownership_paths.append(ownership_path)
                    
                    if level == 0:
                        self.ubo_candidates[full_name].direct_percentage += effective_percentage
                    else:
                        self.ubo_candidates[full_name].indirect_percentage += effective_percentage
                    
                    self.ubo_candidates[full_name].total_percentage += effective_percentage
                    
                elif shareholder.shareholder_type == "corporate" and shareholder.regis_id:
                    # Corporate shareholder - continue traversal
                    if shareholder.regis_id in self.mock_data:
                        new_path = path + [shareholder.regis_id]
                        queue.append((shareholder.regis_id, level + 1, effective_percentage, new_path))
        
        # Identify UBOs based on 15% threshold
        identified_ubos = []
        for name, candidate in self.ubo_candidates.items():
            if candidate.total_percentage >= self.threshold_15:
                candidate.identification_method = "Method 1 (Shareholding ≥15%)"
                identified_ubos.append(asdict(candidate))
        
        # If no UBOs found via Method 1, use Method 3 (Directors)
        if not identified_ubos:
            logger.info("No UBOs found via Method 1, trying Method 3 (Directors)")
            for name, candidate in self.ubo_candidates.items():
                if candidate.is_director:
                    candidate.identification_method = "Method 3 (Director)"
                    identified_ubos.append(asdict(candidate))
        
        # Generate checklist
        checklist = self._generate_checklist(company, identified_ubos)
        
        # Generate hierarchy graph
        graph_base64 = self._generate_shareholding_graph(company_id)
        
        # Analysis summary
        analysis_summary = self._generate_analysis_summary(company, identified_ubos)
        
        return {
            "company_info": {
                "regis_id": company.regis_id,
                "name_th": company.name_th,
                "name_en": company.name_en,
                "status": company.status,
                "total_shareholders": len(company.shareholders),
                "total_directors": len(company.directors)
            },
            "ubos": identified_ubos,
            "checklist": checklist,
            "hierarchy_graph": graph_base64,
            "analysis_summary": analysis_summary,
            "hierarchy_data": self.hierarchy,
            "ubo_candidates": {name: asdict(candidate) for name, candidate in self.ubo_candidates.items()}
        }
    
    def _generate_checklist(self, company: Company, ubos: List[Dict]) -> Dict[str, Any]:
        """สร้าง Checklist ตามกระบวนการ NC958 PRO05-2568"""
        
        checklist = {
            "company_identification": {
                "company_registered": True,
                "company_active": company.status == "Active",
                "company_data_available": True
            },
            "ubo_identification_methods": {
                "method_1_shareholding": {
                    "applied": True,
                    "threshold_15_percent": self.threshold_15,
                    "max_levels_traversed": self.max_levels,
                    "natural_persons_found": len([u for u in ubos if u.get("identification_method", "").startswith("Method 1")]),
                    "passed": len([u for u in ubos if u.get("identification_method", "").startswith("Method 1")]) > 0
                },
                "method_2_dominant_control": {
                    "applied": False,
                    "passed": False,
                    "reason": "Method 1 successful"
                },
                "method_3_executive_authority": {
                    "applied": len([u for u in ubos if u.get("identification_method", "").startswith("Method 3")]) > 0,
                    "directors_identified": len([u for u in ubos if u.get("identification_method", "").startswith("Method 3")]),
                    "passed": len([u for u in ubos if u.get("identification_method", "").startswith("Method 3")]) > 0
                }
            },
            "ubo_data_collection": {
                "full_name_collected": len(ubos) > 0,
                "id_document_available": False,  # Mock data doesn't have ID numbers
                "address_available": False,
                "nationality_collected": len([u for u in ubos if u.get("nationality")]) > 0,
                "dob_available": False,
                "occupation_available": False
            },
            "compliance_status": {
                "ubo_identified": len(ubos) > 0,
                "ubo_threshold_met": len([u for u in ubos if u.get("total_percentage", 0) >= self.threshold_15]) > 0,
                "watchlist_check_required": len(ubos) > 0,
                "watchlist_check_completed": False,  # Would need external service
                "relationship_approved": len(ubos) > 0
            },
            "overall_status": "PASS" if len(ubos) > 0 else "FAIL"
        }
        
        return checklist
    
    def _generate_shareholding_graph(self, company_id: str) -> str:
        """สร้างแผนภูมิโครงสร้างการถือหุ้น"""
        try:
            # Create networkx graph
            G = nx.DiGraph()
            
            # Add nodes and edges
            for comp_id, comp_data in self.hierarchy.items():
                G.add_node(comp_id, 
                          name_th=comp_data["name_th"],
                          name_en=comp_data["name_en"],
                          level=comp_data["level"])
                
                for shareholder in comp_data["shareholders"]:
                    if shareholder["shareholder_type"] == "corporate" and shareholder["regis_id"]:
                        # Add edge to corporate shareholder
                        G.add_edge(comp_id, shareholder["regis_id"], 
                                 percent=shareholder["percent"],
                                 share_amount=shareholder["share_amount"])
            
            # Create matplotlib figure
            fig, ax = plt.subplots(1, 1, figsize=(16, 12))
            
            # Use hierarchical layout
            pos = nx.spring_layout(G, k=3, iterations=50)
            
            # Draw nodes
            node_colors = []
            node_sizes = []
            
            for node in G.nodes():
                level = G.nodes[node].get("level", 0)
                if level == 0:
                    node_colors.append("#FF6B6B")  # Red for root
                    node_sizes.append(3000)
                elif level == 1:
                    node_colors.append("#4ECDC4")  # Teal for level 1
                    node_sizes.append(2000)
                else:
                    node_colors.append("#45B7D1")  # Blue for level 2+
                    node_sizes.append(1500)
            
            nx.draw_networkx_nodes(G, pos, 
                                 node_color=node_colors,
                                 node_size=node_sizes,
                                 alpha=0.8)
            
            # Draw edges with labels
            edge_labels = {}
            for edge in G.edges():
                percent = G.edges[edge]["percent"]
                edge_labels[edge] = f"{percent:.1f}%"
            
            nx.draw_networkx_edges(G, pos, 
                                 edge_color="gray",
                                 arrows=True,
                                 arrowsize=20,
                                 alpha=0.6)
            
            nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
            
            # Draw node labels
            node_labels = {}
            for node in G.nodes():
                name = G.nodes[node]["name_th"]
                if len(name) > 30:
                    name = name[:27] + "..."
                node_labels[node] = name
            
            nx.draw_networkx_labels(G, pos, node_labels, font_size=8, font_weight="bold")
            
            ax.set_title("โครงสร้างการถือหุ้น (Shareholding Structure)", 
                        fontsize=16, fontweight="bold", pad=20)
            ax.axis("off")
            
            # Add legend
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF6B6B', markersize=15, label='บริษัทหลัก (Level 0)'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4ECDC4', markersize=15, label='ผู้ถือหุ้นระดับ 1 (Level 1)'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#45B7D1', markersize=15, label='ผู้ถือหุ้นระดับ 2+ (Level 2+)')
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Error generating graph: {e}")
            return None
    
    def _generate_analysis_summary(self, company: Company, ubos: List[Dict]) -> str:
        """สร้างสรุปการวิเคราะห์"""
        
        summary_parts = []
        
        # Company info
        summary_parts.append(f"บริษัท: {company.name_th}")
        summary_parts.append(f"เลขทะเบียน: {company.regis_id}")
        summary_parts.append(f"สถานะ: {company.status}")
        
        # UBO analysis
        if ubos:
            summary_parts.append(f"\n✅ พบผู้ได้รับผลประโยชน์ที่แท้จริง (UBO) {len(ubos)} คน:")
            for i, ubo in enumerate(ubos, 1):
                summary_parts.append(f"  {i}. {ubo['name']} - {ubo['total_percentage']:.2f}% ({ubo['identification_method']})")
        else:
            summary_parts.append("\n❌ ไม่พบผู้ได้รับผลประโยชน์ที่แท้จริง (UBO)")
        
        # Method used
        methods_used = set([ubo.get("identification_method", "") for ubo in ubos])
        if methods_used:
            summary_parts.append(f"\nวิธีการระบุ UBO: {', '.join(methods_used)}")
        
        # Compliance status
        if ubos:
            summary_parts.append("\n✅ สถานะการปฏิบัติตามกฎหมาย: ผ่าน")
            summary_parts.append("📋 ต้องตรวจสอบรายชื่อผู้ต้องสงสัย (Watchlist)")
        else:
            summary_parts.append("\n❌ สถานะการปฏิบัติตามกฎหมาย: ไม่ผ่าน")
            summary_parts.append("⚠️ ต้องปฏิเสธความสัมพันธ์ทางธุรกิจ")
        
        return "\n".join(summary_parts)

def main():
    """ทดสอบระบบ Mock UBO"""
    system = MockUBOSystem()
    
    # Test with LH Bank
    result = system.analyze_ubo("0107548000234")
    
    print("=== UBO Analysis Result ===")
    print(f"Company: {result['company_info']['name_th']}")
    print(f"UBOs Found: {len(result['ubos'])}")
    
    for i, ubo in enumerate(result['ubos'], 1):
        print(f"  {i}. {ubo['name']} - {ubo['total_percentage']:.2f}%")
    
    print(f"\nOverall Status: {result['checklist']['overall_status']}")
    
    # Save result to JSON
    with open('mock_ubo_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Result saved to mock_ubo_result.json")

if __name__ == "__main__":
    main()
