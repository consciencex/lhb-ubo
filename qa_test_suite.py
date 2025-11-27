import unittest
import requests
import json
import csv
import io

BASE_URL = "http://localhost:4444"

class TestUBOSystem(unittest.TestCase):

    def test_status_endpoint(self):
        """Test the /api/status endpoint."""
        print("\nTesting /api/status...")
        try:
            response = requests.get(f"{BASE_URL}/api/status")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "running")
            print("✅ /api/status passed")
        except Exception as e:
            self.fail(f"Failed to connect to {BASE_URL}/api/status: {e}")

    def test_analyze_mock_data(self):
        """Test /api/analyze with mock data ID 'XXXXXXXX'."""
        print("\nTesting /api/analyze with mock data...")
        payload = {"registration_id": "XXXXXXXX"}
        response = requests.post(f"{BASE_URL}/api/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check basic structure
        self.assertTrue(data.get("success"))
        self.assertTrue(data.get("is_mock"))
        self.assertIn("data", data)
        
        report = data["data"]
        self.assertIn("company_info", report)
        self.assertIn("ubos", report)
        self.assertIn("hierarchy_data", report)
        self.assertIn("network_graph", report)
        
        # Check UBOs content
        ubos = report["ubos"]
        self.assertIsInstance(ubos, list)
        if len(ubos) > 0:
            first_ubo = ubos[0]
            self.assertIn("name", first_ubo)
            self.assertIn("total_percentage", first_ubo)
            self.assertIn("ubo_status", first_ubo)
            
        print("✅ /api/analyze (mock) passed")

    def test_analyze_missing_id(self):
        """Test /api/analyze with missing ID."""
        print("\nTesting /api/analyze with missing ID...")
        payload = {}
        response = requests.post(f"{BASE_URL}/api/analyze", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)
        print("✅ /api/analyze (missing ID) passed")

    def test_export_excel(self):
        """Test /api/export_excel endpoint."""
        print("\nTesting /api/export_excel...")
        # Create dummy result data similar to what the frontend sends
        dummy_results = [{
            "company_info": {"id": "123", "name": "Test Corp", "check_date": "2023-01-01"},
            "analysis_summary": {"risk_level": "HIGH", "compliance_status": "COMPLIANT"},
            "ubo_results": {
                "total_candidates": 1,
                "final_ubos": 1,
                "ubo_details": [{
                    "name": "John Doe",
                    "method": "1",
                    "total_percentage": "25.00",
                    "paths": [],
                    "is_director": True,
                    "position": "Director"
                }]
            }
        }]
        
        payload = {"results": dummy_results}
        response = requests.post(f"{BASE_URL}/api/export_excel", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "text/csv; charset=utf-8-sig")
        
        # Verify CSV content
        content = response.content.decode('utf-8-sig')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        self.assertTrue(len(rows) > 1) # Header + Data
        self.assertEqual(rows[0][0], "Company ID")
        self.assertEqual(rows[1][0], "123")
        self.assertEqual(rows[1][10], "John Doe")
        
        print("✅ /api/export_excel passed")

if __name__ == '__main__':
    unittest.main()
