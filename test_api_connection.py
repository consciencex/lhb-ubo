#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test API Connection Script
ทดสอบการเชื่อมต่อ API แยกต่างหาก
"""

import requests
import xml.etree.ElementTree as ET
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api_connection():
    """ทดสอบการเชื่อมต่อ API"""
    
    # API Configuration
    api_key = "HHaUz9c32FK9IYSP8uOKpKoT4csC2HvSkzG3EQ0JM6pMmf0VGYAxcJPjrsY9lHsV"
    base_url = "https://xignal-uat.bol.co.th"
    test_company_id = "0107548000234"  # LH Bank
    
    # Headers
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'text/xml',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Enhanced-UBO-System/1.0'
    }
    
    # SOAP Body
    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:eh="http://eh.actimize.com"
                  xmlns:view="http://view.bol.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <view:getDataEnlite>
            <registrationId>{test_company_id}</registrationId>
            <language>EN</language>
      </view:getDataEnlite>
   </soapenv:Body>
</soapenv:Envelope>"""
    
    try:
        logger.info(f"Testing API connection for company: {test_company_id}")
        logger.info(f"URL: {base_url}/enlitews/companyData")
        
        # Make request
        response = requests.post(
            f"{base_url}/enlitews/companyData",
            data=soap_body,
            headers=headers,
            timeout=30
        )
        
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            logger.info("✅ API Connection Successful!")
            
            # Parse XML
            try:
                root = ET.fromstring(response.text)
                
                # Check for return data
                ns = {
                    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                    'view': 'http://view.bol.com/'
                }
                
                return_data = root.find('.//view:return', ns)
                if return_data is None:
                    return_data = root.find('.//return')
                
                if return_data is not None:
                    logger.info("✅ XML Parsing Successful!")
                    
                    # Extract basic info
                    profile = return_data.find('.//profileSummary')
                    if profile is not None:
                        name_th = profile.find('nameThFull')
                        name_en = profile.find('nameEnFull')
                        status = profile.find('companyStatus')
                        
                        logger.info(f"Company Name (TH): {name_th.text if name_th is not None else 'N/A'}")
                        logger.info(f"Company Name (EN): {name_en.text if name_en is not None else 'N/A'}")
                        logger.info(f"Company Status: {status.text if status is not None else 'N/A'}")
                    
                    # Check shareholders
                    held_by = return_data.find('.//heldBy')
                    if held_by is not None:
                        level_held = held_by.find('.//levelHeldBy[@level="1"]')
                        if level_held is not None:
                            shareholders = level_held.findall('.//data')
                            logger.info(f"✅ Found {len(shareholders)} shareholders")
                            
                            for i, sh in enumerate(shareholders[:3]):  # Show first 3
                                percent = sh.find('percent')
                                firstname = sh.find('.//shareholder/firstname')
                                lastname = sh.find('.//shareholder/lastname')
                                logger.info(f"  Shareholder {i+1}: {firstname.text if firstname is not None else 'N/A'} {lastname.text if lastname is not None else 'N/A'} - {percent.text if percent is not None else 'N/A'}%")
                        else:
                            logger.warning("⚠️ No shareholders found")
                    else:
                        logger.warning("⚠️ No heldBy section found")
                    
                    # Check directors
                    directors = return_data.find('.//director')
                    if directors is not None:
                        director_list = directors.findall('.//list')
                        logger.info(f"✅ Found {len(director_list)} directors")
                        
                        for i, director in enumerate(director_list[:3]):  # Show first 3
                            firstname = director.find('firstname')
                            lastname = director.find('lastname')
                            logger.info(f"  Director {i+1}: {firstname.text if firstname is not None else 'N/A'} {lastname.text if lastname is not None else 'N/A'}")
                    else:
                        logger.warning("⚠️ No directors found")
                    
                else:
                    logger.error("❌ No return data found in XML response")
                    logger.info(f"Raw XML Response (first 500 chars): {response.text[:500]}")
                
            except ET.ParseError as e:
                logger.error(f"❌ XML Parsing Error: {e}")
                logger.info(f"Raw Response (first 500 chars): {response.text[:500]}")
            
        else:
            logger.error(f"❌ API Request Failed with status {response.status_code}")
            logger.info(f"Response Text: {response.text}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request Exception: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_api_connection()
