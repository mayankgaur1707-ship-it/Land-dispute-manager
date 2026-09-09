import unittest
import asyncio
from backend.ocr_service import scan_registry_document, extract_land_record_from_text
from backend.database import init_db, get_record_by_id
from backend.routes import scan_document_endpoint, get_scanned_documents

class TestRegistryScanner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_scan_registry_document_extraction(self):
        sample_text = """
        REGISTRATION DEED & KHASRA RECORD (SUB-REGISTRAR OFFICE VARANASI)
        Deed No: REG-2026-UP-44912
        Village: Rampur, Tehsil: Sadar, District: Varanasi, State: Uttar Pradesh
        Khasra Number: 108/A
        Khata Number: 52
        Land Area: 2,500.00 Sq. Meters (0.2500 Hectares)
        Classification: Agricultural Land (कृषि भूमि)
        PURCHASER / OWNER:
        1. Anand Kumar Mishra s/o K.N. Mishra - Share: 100.0% [Aadhaar: XXXX-XXXX-9912]
        """
        res = scan_registry_document(raw_text=sample_text, filename="test_deed_108.pdf")
        self.assertTrue(res["success"])
        record = res["scanned_record"]
        self.assertEqual(record["khasra_no"], "108/A")
        self.assertEqual(record["khata_no"], "52")
        self.assertEqual(record["village"], "Rampur")
        self.assertEqual(record["area_sq_meters"], 2500.0)
        self.assertTrue(len(record["owners"]) >= 1)
        self.assertIn("Anand", record["owners"][0]["name"])

        # Check accuracy metrics
        self.assertTrue(res["overall_accuracy"] >= 85.0)
        hud = res["corner_hud_data"]
        self.assertIn("overall_accuracy", hud)
        self.assertIn("field_accuracies", hud)
        self.assertIn("Parties / Names", hud["field_accuracies"])
        self.assertIn("Registry & Khasra ID", hud["field_accuracies"])
        self.assertIn("Land Area (Sq.M)", hud["field_accuracies"])

    def test_scan_document_endpoint_async(self):
        payload = {
            "filename": "deed_sample_khasra_105.pdf",
            "sample_id": "sample_clear_105"
        }
        res = asyncio.run(scan_document_endpoint(file=None, payload=payload))
        self.assertTrue(res["success"])
        self.assertIn("record", res)
        self.assertIn("corner_hud_data", res)
        self.assertIn("overall_accuracy", res["accuracy_report"])
        self.assertGreater(res["accuracy_report"]["overall_accuracy"], 90.0)
        
        # Verify saved record exists in DB
        saved = get_record_by_id(res["record"]["id"])
        self.assertIsNotNone(saved)
        self.assertEqual(saved["khasra_no"], "105")

    def test_get_scanned_documents_endpoint(self):
        res = get_scanned_documents()
        self.assertIn("records", res)
        self.assertGreater(res["count"], 0)

if __name__ == "__main__":
    unittest.main()
