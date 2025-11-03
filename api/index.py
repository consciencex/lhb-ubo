#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vercel entry point for UBO Analysis System."""

import sys
import os

# Add parent directory to path if needed
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

from enhanced_app import app

# Vercel will automatically detect and use the 'app' variable
# No need for custom handler - Vercel Python runtime handles it automatically

