#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LevelHeldBy Tree Visualizer
ระบบสร้างแผนภูมิจาก levelHeldBy level 1,2,3 แยก type personal/company
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from typing import Dict, List, Any, Tuple
import logging
from dataclasses import dataclass
import json

# Set font for matplotlib - use simple fonts to avoid Thai character issues
plt.rcParams['font.family'] = ['Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.size'] = 10

# Disable Thai text in plots to avoid font issues
print("Using simple font: Arial (Thai text disabled in plots)")

logger = logging.getLogger(__name__)

@dataclass
class TreeNode:
    """Node สำหรับ Tree Structure"""
    id: str
    name_th: str
    name_en: str
    level: int
    percentage: float
    node_type: str  # 'personal', 'company'
    is_ubo: bool = False
    children: List['TreeNode'] = None
    shareholder_data: Dict = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.shareholder_data is None:
            self.shareholder_data = {}

class LevelHeldByVisualizer:
    """ตัวสร้างแผนภูมิจาก levelHeldBy level 1,2,3"""
    
    def __init__(self):
        self.colors = {
            'personal': '#4ECDC4',     # Teal for individuals
            'company': '#45B7D1',      # Blue for companies
            'ubo': '#FFD93D',         # Yellow for UBOs
            'edge': '#2C3E50'         # Dark blue for edges
        }
        
    def create_levelheldby_tree(self, analysis_result: Dict[str, Any]) -> str:
        """สร้างแผนภูมิ Tree Diagram จาก levelHeldBy"""
        try:
            # สร้าง Tree Structure จาก levelHeldBy
            root_node = self._build_levelheldby_tree(analysis_result)
            
            # สร้างแผนภูมิ
            fig, ax = plt.subplots(1, 1, figsize=(32, 24))
            ax.set_xlim(0, 16)
            ax.set_ylim(0, 16)
            ax.axis('off')
            
            # วาด Tree
            self._draw_levelheldby_tree(ax, root_node, x=8, y=15, width=14, height=3)
            
            # เพิ่ม Title และ Legend
            self._add_title_and_legend(ax, analysis_result)
            
            # แสดงสถิติการวิเคราะห์
            self._add_analysis_statistics(ax, analysis_result)
            
            # Convert to base64
            import base64
            from io import BytesIO
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
            
        except Exception as e:
            logger.error(f"Error creating levelHeldBy tree: {e}")
            return None
    
    def _build_levelheldby_tree(self, analysis_result: Dict[str, Any]) -> TreeNode:
        """สร้าง Tree Structure จาก levelHeldBy"""
        
        # ข้อมูลบริษัทหลัก
        company_info = analysis_result.get('company_info', {})
        root_id = company_info.get('regis_id', 'unknown')
        root_name_th = company_info.get('name_th', 'บริษัทไม่ระบุ')
        root_name_en = company_info.get('name_en', 'Unknown Company')
        
        root_node = TreeNode(
            id=root_id,
            name_th=root_name_th,
            name_en=root_name_en,
            level=0,
            percentage=100.0,
            node_type='company'
        )
        
        # ข้อมูล UBOs (เฉพาะวิธีที่ 1)
        ubos = analysis_result.get('ubos', [])
        ubo_names = {ubo.get('name', '') for ubo in ubos if ubo.get('total_percentage', 0) >= 15.0}
        
        # ดึงข้อมูลจาก hierarchy_data ที่มี level_held_by
        hierarchy_data = analysis_result.get('hierarchy_data', {})
        
        # สร้าง Tree จาก levelHeldBy
        self._build_levelheldby_recursive(root_node, hierarchy_data, ubo_names, 0)
        
        return root_node
    
    def _build_levelheldby_recursive(self, parent_node: TreeNode, hierarchy_data: Dict[str, Any], 
                                   ubo_names: set, level: int):
        """สร้าง Tree แบบ recursive จาก levelHeldBy"""
        
        if level >= 3:  # จำกัดที่ 3 ทอด
            return
        
        # หา children จาก hierarchy_data
        for company_id, company_data in hierarchy_data.items():
            if company_data.get('level', 0) == level + 1:
                shareholders = company_data.get('shareholders', [])
                
                for shareholder in shareholders:
                    # สร้าง child node
                    child_name = f"{shareholder.get('firstname', '')} {shareholder.get('lastname', '')}".strip()
                    if not child_name:
                        child_name = shareholder.get('name', 'ไม่ระบุชื่อ')
                    
                    child_percentage = float(shareholder.get('percent', 0))
                    child_type = shareholder.get('shareholder_type', 'personal')
                    
                    # ตรวจสอบว่าเป็น UBO หรือไม่ (เฉพาะวิธีที่ 1)
                    is_ubo = child_name in ubo_names and child_percentage >= 15.0
                    
                    child_node = TreeNode(
                        id=shareholder.get('regis_id_held_by', f'child_{len(parent_node.children)}'),
                        name_th=child_name,
                        name_en=child_name,
                        level=level + 1,
                        percentage=child_percentage,
                        node_type=child_type,
                        is_ubo=is_ubo,
                        shareholder_data=shareholder
                    )
                    
                    parent_node.children.append(child_node)
                    
                    # ถ้าเป็น company ให้สร้าง children ต่อ
                    if child_type == 'company' and shareholder.get('regis_id_held_by'):
                        self._build_levelheldby_recursive(child_node, hierarchy_data, ubo_names, level + 1)
    
    def _draw_levelheldby_tree(self, ax, node: TreeNode, x: float, y: float, width: float, height: float):
        """วาด Tree จาก levelHeldBy"""
        
        # เลือกสีตามประเภทและสถานะ
        if node.is_ubo:
            color = self.colors['ubo']
        else:
            color = self.colors[node.node_type]
        
        # สร้างกล่องสำหรับ node
        box_width = width * 0.9
        box_height = height * 0.7
        
        # วาดกล่อง
        box = FancyBboxPatch(
            (x - box_width/2, y - box_height/2), box_width, box_height,
            boxstyle="round,pad=0.02", 
            facecolor=color, 
            edgecolor='black',
            linewidth=2,
            alpha=0.8
        )
        ax.add_patch(box)
        
        # เพิ่มข้อความ
        text_y = y
        
        # UBO Badge (เฉพาะวิธีที่ 1)
        if node.is_ubo:
            ax.text(x, text_y + 0.25, f"⭐ UBO (≥15%)", ha='center', va='center', 
                   fontsize=11, fontweight='bold', color='red')
            text_y -= 0.1
        
        # Level Badge
        ax.text(x - box_width/2 + 0.1, text_y + 0.25, f"L{node.level}", ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='black', alpha=0.7))
        
        # Type Badge
        type_text = "Personal" if node.node_type == 'personal' else "Company"
        ax.text(x + box_width/2 - 0.1, text_y + 0.25, type_text, ha='center', va='center', 
               fontsize=9, fontweight='bold', color='white',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='darkblue', alpha=0.7))
        
        # ชื่อบริษัท/บุคคล - ใช้ชื่อภาษาอังกฤษเพื่อหลีกเลี่ยงปัญหา font
        name_text = node.name_en[:35] + "..." if len(node.name_en) > 35 else node.name_en
        if not name_text.strip():
            name_text = node.name_th[:35] + "..." if len(node.name_th) > 35 else node.name_th
        ax.text(x, text_y, name_text, ha='center', va='center', 
               fontsize=12, fontweight='bold', wrap=True)
        
        # เปอร์เซ็นต์
        ax.text(x, text_y - 0.15, f"{node.percentage:.2f}%", ha='center', va='center', 
               fontsize=11, fontweight='bold')
        
        # ID (ถ้ามี)
        if node.id and node.id != 'unknown':
            ax.text(x, text_y - 0.25, f"ID: {node.id[:15]}...", ha='center', va='center', 
                   fontsize=9, style='italic')
        
        # ข้อมูลเพิ่มเติม - ใช้ภาษาอังกฤษ
        if node.shareholder_data:
            sh_data = node.shareholder_data
            if sh_data.get('nationality'):
                ax.text(x, text_y - 0.35, f"Nationality: {sh_data.get('nationality', 'Unknown')}", 
                       ha='center', va='center', fontsize=8, color='blue')
            if sh_data.get('directorship') == 'YES':
                ax.text(x, text_y - 0.4, f"Director: Yes", ha='center', va='center', 
                       fontsize=8, color='green')
        
        # วาด children
        if node.children:
            child_count = len(node.children)
            child_width = width / child_count
            child_height = height * 0.8
            
            for i, child in enumerate(node.children):
                child_x = x - width/2 + (i + 0.5) * child_width
                child_y = y - height - 1.2
                
                # วาดเส้นเชื่อม
                ax.plot([x, child_x], [y - box_height/2, child_y + child_height/2], 
                       color=self.colors['edge'], linewidth=2, alpha=0.7)
                
                # แสดงเปอร์เซ็นต์บนเส้นเชื่อม
                mid_x = (x + child_x) / 2
                mid_y = (y - box_height/2 + child_y + child_height/2) / 2
                ax.text(mid_x, mid_y, f"{child.percentage:.1f}%", ha='center', va='center', 
                       fontsize=10, fontweight='bold', 
                       bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
                
                # วาด child แบบ recursive
                self._draw_levelheldby_tree(ax, child, child_x, child_y, child_width, child_height)
    
    def _add_title_and_legend(self, ax, analysis_result: Dict[str, Any]):
        """เพิ่ม Title และ Legend"""
        
        # Title - ใช้ภาษาอังกฤษ
        company_info = analysis_result.get('company_info', {})
        company_name = company_info.get('name_en', company_info.get('name_th', 'Unknown Company'))
        company_id = company_info.get('regis_id', 'Unknown')
        
        ax.text(8, 15.8, f"Shareholding Structure from levelHeldBy - {company_name}", 
               ha='center', va='center', fontsize=22, fontweight='bold')
        ax.text(8, 15.6, f"Registration ID: {company_id} | Types: personal/company", 
               ha='center', va='center', fontsize=16, style='italic')
        
        # Legend - ใช้ภาษาอังกฤษ
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['personal'], label='Individual (personal)'),
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['company'], label='Company (corporate)'),
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['ubo'], label='UBO (≥15%)')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', fontsize=14, 
                 frameon=True, fancybox=True, shadow=True)
    
    def _add_analysis_statistics(self, ax, analysis_result: Dict[str, Any]):
        """เพิ่มสถิติการวิเคราะห์"""
        
        # สถิติ
        ubos = analysis_result.get('ubos', [])
        hierarchy_data = analysis_result.get('hierarchy_data', {})
        
        # นับจำนวนในแต่ละระดับและประเภท
        level_counts = {}
        type_counts = {'personal': 0, 'company': 0}
        
        for company_data in hierarchy_data.values():
            level = company_data.get('level', 0)
            level_counts[level] = level_counts.get(level, 0) + 1
            
            shareholders = company_data.get('shareholders', [])
            for sh in shareholders:
                sh_type = sh.get('shareholder_type', 'personal')
                if sh_type in type_counts:
                    type_counts[sh_type] += 1
        
        # นับ UBO ที่ผ่านเกณฑ์ 15%
        ubo_count_15 = len([ubo for ubo in ubos if ubo.get('total_percentage', 0) >= 15.0])
        
        stats_text = f"""
Analysis Statistics from levelHeldBy:
• UBOs with ≥15% threshold: {ubo_count_15} persons
• Companies checked: {len(hierarchy_data)} companies
• Maximum level: 3 tiers (enforced)
• Individuals: {type_counts['personal']} persons
• Companies: {type_counts['company']} companies
• Identification method: Shareholding ≥15% only
        """
        
        ax.text(1, 1, stats_text, ha='left', va='bottom', 
               fontsize=13, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))

def main():
    """ทดสอบระบบ"""
    # สร้างข้อมูลตัวอย่าง
    sample_data = {
        "company_info": {
            "regis_id": "0107548000234",
            "name_th": "ธนาคารแลนด์ แอนด์ เฮาส์ จำกัด (มหาชน)",
            "name_en": "LAND AND HOUSES BANK PUBLIC COMPANY LIMITED"
        },
        "ubos": [
            {"name": "LEOKLVJ PAVOVPVXGCAWJGS", "total_percentage": 15.5},
            {"name": "PVUVLVXVRII RGXVLORELO", "total_percentage": 12.3}
        ],
        "hierarchy_data": {
            "0107548000234": {
                "name_th": "ธนาคารแลนด์ แอนด์ เฮาส์ จำกัด (มหาชน)",
                "level": 0,
                "shareholders": [
                    {"name": "บริษัท เอเชีย พรอพเพอร์ตี้ จำกัด", "percent": "20.0", "shareholder_type": "company", "regis_id_held_by": "0105517006433"},
                    {"name": "นายสมชาย ใจดี", "percent": "15.5", "shareholder_type": "personal", "regis_id_held_by": "1234567890123"}
                ]
            },
            "0105517006433": {
                "name_th": "บริษัท เอเชีย พรอพเพอร์ตี้ จำกัด",
                "level": 1,
                "shareholders": [
                    {"name": "นายสมชาย ใจดี", "percent": "40.0", "shareholder_type": "personal", "regis_id_held_by": "1234567890123"},
                    {"name": "นางสาวสมหญิง รักดี", "percent": "30.0", "shareholder_type": "personal", "regis_id_held_by": "1234567890124"}
                ]
            }
        },
        "checklist": {
            "overall_status": "PASS"
        }
    }
    
    visualizer = LevelHeldByVisualizer()
    result = visualizer.create_levelheldby_tree(sample_data)
    
    if result:
        print("✅ LevelHeldBy tree created successfully!")
        print(f"Base64 length: {len(result)}")
    else:
        print("❌ Failed to create LevelHeldBy tree")

if __name__ == "__main__":
    main()
