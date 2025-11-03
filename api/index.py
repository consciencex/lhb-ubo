#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vercel entry point for UBO Analysis System."""

import sys
import os

# Add parent directory to path (api/ -> root)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from enhanced_app import app

# Vercel will automatically detect and use the 'app' variable
# No need for custom handler - Vercel Python runtime handles it automatically

