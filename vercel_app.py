#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vercel entry point for UBO Analysis System."""

import sys
import os

# Add parent directory to path if needed
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

from enhanced_app import app

# Export app for Vercel
# Vercel will use this as the WSGI application
def handler(request):
    """Vercel serverless handler (WSGI-compatible)."""
    from werkzeug.wrappers import Request, Response
    
    @Request.application
    def wsgi_handler(req):
        with app.request_context(req.environ):
            try:
                rv = app.full_dispatch_request()
            except Exception as e:
                rv = app.handle_exception(e)
            return Response(rv.get_data(), status=rv.status_code, headers=dict(rv.headers))
    
    return wsgi_handler(request.environ, lambda status, headers: None)

# For Vercel Python runtime
# If running on Vercel, app will be used directly
if __name__ == '__main__':
    app.run()

