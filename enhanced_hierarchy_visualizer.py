#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Hierarchy Tree Visualizer
ระบบสร้างแผนภูมิโครงสร้างการถือหุ้นแบบ Tree Diagram
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

# Set Thai font for matplotlib
plt.rcParams['font.family'] = ['Tahoma', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['font.size'] = 10

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

logger = logging.getLogger(__name__)

@dataclass
class TreeNode:
    """Node สำหรับ Tree Structure"""
    id: str
    name_th: str
    name_en: str
    level: int
    percentage: float
    node_type: str  # 'company', 'individual', 'corporate'
    is_ubo: bool = False
    children: List['TreeNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []

class EnhancedHierarchyVisualizer:
    """ตัวสร้างแผนภูมิโครงสร้างการถือหุ้นแบบ Tree Diagram"""
    
    def __init__(self):
        self.colors = {
            'company': '#FF6B6B',      # Red for main company
            'individual': '#4ECDC4',   # Teal for individuals
            'corporate': '#45B7D1',    # Blue for corporate shareholders
            'ubo': '#FFD93D',         # Yellow for UBOs
            'edge': '#2C3E50'         # Dark blue for edges
        }
        
    def create_hierarchy_tree(self, analysis_result: Dict[str, Any]) -> str:
        """สร้างแผนภูมิ Tree Diagram จากผลการวิเคราะห์"""
        try:
            # สร้าง Tree Structure
            root_node = self._build_tree_structure(analysis_result)
            
            # สร้างแผนภูมิ
            fig, ax = plt.subplots(1, 1, figsize=(20, 14))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # วาด Tree
            self._draw_tree(ax, root_node, x=5, y=9, width=8, height=1.5)
            
            # เพิ่ม Title และ Legend
            self._add_title_and_legend(ax, analysis_result)
            
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
            logger.error(f"Error creating hierarchy tree: {e}")
            return None
    
    def _build_tree_structure(self, analysis_result: Dict[str, Any]) -> TreeNode:
        """สร้าง Tree Structure จากผลการวิเคราะห์"""
        
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
        
        # ข้อมูล UBOs
        ubos = analysis_result.get('ubos', [])
        ubo_names = {ubo.get('name', '') for ubo in ubos}
        
        # ข้อมูล Hierarchy
        hierarchy_data = analysis_result.get('hierarchy_data', {})
        
        # สร้าง Tree จาก hierarchy_data
        self._build_tree_recursive(root_node, hierarchy_data, ubo_names, 0)
        
        return root_node
    
    def _build_tree_recursive(self, parent_node: TreeNode, hierarchy_data: Dict[str, Any], 
                            ubo_names: set, level: int):
        """สร้าง Tree แบบ recursive"""
        
        if level >= 3:  # จำกัดที่ 3 ทอด
            return
        
        # หา children จาก hierarchy_data
        for company_id, company_data in hierarchy_data.items():
            if company_data.get('level', 0) == level + 1:
                shareholders = company_data.get('shareholders', [])
                
                for shareholder in shareholders:
                    # สร้าง child node
                    child_name = shareholder.get('name', 'ไม่ระบุชื่อ')
                    child_percentage = float(shareholder.get('percent', 0))
                    child_type = shareholder.get('shareholder_type', 'personal')
                    
                    # ตรวจสอบว่าเป็น UBO หรือไม่
                    is_ubo = child_name in ubo_names
                    
                    child_node = TreeNode(
                        id=shareholder.get('regis_id', f'child_{len(parent_node.children)}'),
                        name_th=child_name,
                        name_en=child_name,  # ใช้ชื่อเดียวกัน
                        level=level + 1,
                        percentage=child_percentage,
                        node_type='individual' if child_type == 'personal' else 'corporate',
                        is_ubo=is_ubo
                    )
                    
                    parent_node.children.append(child_node)
                    
                    # ถ้าเป็น corporate ให้สร้าง children ต่อ
                    if child_type == 'corporate' and shareholder.get('regis_id'):
                        self._build_tree_recursive(child_node, hierarchy_data, ubo_names, level + 1)
    
    def _draw_tree(self, ax, node: TreeNode, x: float, y: float, width: float, height: float):
        """วาด Tree แบบ recursive"""
        
        # เลือกสีตามประเภทและสถานะ
        if node.is_ubo:
            color = self.colors['ubo']
        else:
            color = self.colors[node.node_type]
        
        # สร้างกล่องสำหรับ node
        box_width = width * 0.8
        box_height = height * 0.6
        
        # วาดกล่อง
        box = FancyBboxPatch(
            (x - box_width/2, y - box_height/2), box_width, box_height,
            boxstyle="round,pad=0.02", 
            facecolor=color, 
            edgecolor='black',
            linewidth=1.5,
            alpha=0.8
        )
        ax.add_patch(box)
        
        # เพิ่มข้อความ
        text_y = y
        if node.is_ubo:
            ax.text(x, text_y + 0.1, f"⭐ UBO", ha='center', va='center', 
                   fontsize=8, fontweight='bold', color='red')
            text_y -= 0.1
        
        # ชื่อบริษัท/บุคคล
        name_text = node.name_th[:20] + "..." if len(node.name_th) > 20 else node.name_th
        ax.text(x, text_y, name_text, ha='center', va='center', 
               fontsize=9, fontweight='bold', wrap=True)
        
        # เปอร์เซ็นต์
        ax.text(x, text_y - 0.15, f"{node.percentage:.2f}%", ha='center', va='center', 
               fontsize=8, fontweight='bold')
        
        # ID (ถ้ามี)
        if node.id and node.id != 'unknown':
            ax.text(x, text_y - 0.25, f"ID: {node.id[:10]}...", ha='center', va='center', 
                   fontsize=7, style='italic')
        
        # วาด children
        if node.children:
            child_count = len(node.children)
            child_width = width / child_count
            child_height = height * 0.8
            
            for i, child in enumerate(node.children):
                child_x = x - width/2 + (i + 0.5) * child_width
                child_y = y - height - 0.5
                
                # วาดเส้นเชื่อม
                ax.plot([x, child_x], [y - box_height/2, child_y + child_height/2], 
                       color=self.colors['edge'], linewidth=2, alpha=0.7)
                
                # วาด child แบบ recursive
                self._draw_tree(ax, child, child_x, child_y, child_width, child_height)
    
    def _add_title_and_legend(self, ax, analysis_result: Dict[str, Any]):
        """เพิ่ม Title และ Legend"""
        
        # Title
        company_info = analysis_result.get('company_info', {})
        company_name = company_info.get('name_th', 'บริษัทไม่ระบุ')
        company_id = company_info.get('regis_id', 'ไม่ระบุ')
        
        ax.text(5, 9.8, f"โครงสร้างการถือหุ้น - {company_name}", 
               ha='center', va='center', fontsize=16, fontweight='bold')
        ax.text(5, 9.6, f"เลขทะเบียน: {company_id}", 
               ha='center', va='center', fontsize=12, style='italic')
        
        # Legend
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['company'], label='บริษัทหลัก'),
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['individual'], label='บุคคลธรรมดา'),
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['corporate'], label='นิติบุคคล'),
            plt.Rectangle((0, 0), 1, 1, facecolor=self.colors['ubo'], label='ผู้ได้รับผลประโยชน์ที่แท้จริง (UBO)')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10, 
                 frameon=True, fancybox=True, shadow=True)
        
        # สถิติ
        ubos = analysis_result.get('ubos', [])
        checklist = analysis_result.get('checklist', {})
        overall_status = checklist.get('overall_status', 'UNKNOWN')
        
        stats_text = f"UBOs พบ: {len(ubos)} คน | สถานะ: {overall_status}"
        ax.text(5, 0.2, stats_text, ha='center', va='center', 
               fontsize=12, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))

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
                    {"name": "บริษัท เอเชีย พรอพเพอร์ตี้ จำกัด", "percent": "20.0", "shareholder_type": "corporate", "regis_id": "0105517006433"},
                    {"name": "นายสมชาย ใจดี", "percent": "15.5", "shareholder_type": "personal", "regis_id": "1234567890123"}
                ]
            },
            "0105517006433": {
                "name_th": "บริษัท เอเชีย พรอพเพอร์ตี้ จำกัด",
                "level": 1,
                "shareholders": [
                    {"name": "นายสมชาย ใจดี", "percent": "40.0", "shareholder_type": "personal", "regis_id": "1234567890123"},
                    {"name": "นางสาวสมหญิง รักดี", "percent": "30.0", "shareholder_type": "personal", "regis_id": "1234567890124"}
                ]
            }
        },
        "checklist": {
            "overall_status": "PASS"
        }
    }
    
    visualizer = EnhancedHierarchyVisualizer()
    result = visualizer.create_hierarchy_tree(sample_data)
    
    if result:
        print("✅ Hierarchy tree created successfully!")
        print(f"Base64 length: {len(result)}")
    else:
        print("❌ Failed to create hierarchy tree")

if __name__ == "__main__":
    main()
