import requests
import os

# Configuration from user request
API_URL = "https://enlite.lhb.co.th/enlitews/companyData"
API_KEY = "fVldOOnGL48NHuUYclP5kLKtZXoCZOr49DFtDqR5vLleuQJ1wQdMyLpY8P7g2ZtQ"
REGISTRATION_ID = "0107562000386"

# SOAP Body exactly as provided by user
SOAP_BODY = f"""<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:eh="http://eh.actimize.com"
                  xmlns:view="http://view.bol.com/">
   <soapenv:Header/>
   <soapenv:Body>
      <view:getDataEnlite>
            <registrationId>{REGISTRATION_ID}</registrationId>
            <language>TH</language>
      </view:getDataEnlite>
   </soapenv:Body>
</soapenv:Envelope>"""

headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'text/xml'
}

print(f"🚀 Starting API Smoke Test")
print(f"URL: {API_URL}")
print(f"Registration ID: {REGISTRATION_ID}")
print("-" * 50)

try:
    response = requests.post(API_URL, data=SOAP_BODY, headers=headers, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print("-" * 50)
    print("Response Body Preview (first 500 chars):")
    print(response.text[:500])
    print("-" * 50)
    
    if response.status_code == 200 and "return" in response.text:
        print("✅ SUCCESS: API returned valid response")
    else:
        print("❌ FAILURE: API returned error or unexpected response")

except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")
