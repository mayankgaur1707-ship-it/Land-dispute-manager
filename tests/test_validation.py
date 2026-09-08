import unittest
from backend.models import LandClassification, DisputeStatus, DisputeType
from backend.validation_engine import validate_land_record
from backend.blockchain_audit import calculate_sha256, GENESIS_HASH

class TestLandValidationEngine(unittest.TestCase):

    def test_share_equity_mismatch(self):
        candidate = {
            "id": "TEST-1",
            "khasra_no": "999",
            "khata_no": "1",
            "village": "Rampur",
            "area_sq_meters": 1000.0,
            "owners": [
                {"name": "Owner A", "share_percentage": 50.0},
                {"name": "Owner B", "share_percentage": 60.0}  # 110% total
            ],
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[[82.90, 25.30], [82.91, 25.30], [82.91, 25.31], [82.90, 25.31], [82.90, 25.30]]]
            }
        }
        status, tags, disputes, conf = validate_land_record(candidate, [])
        self.assertEqual(status, DisputeStatus.WARNING.value)
        self.assertTrue(any("Share mismatch" in t for t in tags))
        self.assertEqual(len(disputes), 1)
        self.assertEqual(disputes[0]["dispute_type"], DisputeType.OWNERSHIP_SHARE_MISMATCH.value)

    def test_duplicate_survey_detection(self):
        existing = [{
            "id": "EXIST-1",
            "khasra_no": "400",
            "village": "Rampur",
            "owners": [{"name": "Original Owner", "share_percentage": 100.0}],
            "boundary_geojson": None
        }]
        candidate = {
            "id": "NEW-1",
            "khasra_no": "400",
            "khata_no": "22",
            "village": "Rampur",
            "area_sq_meters": 1500.0,
            "owners": [{"name": "Conflicting Claimant", "share_percentage": 100.0}],
            "boundary_geojson": None
        }
        status, tags, disputes, conf = validate_land_record(candidate, existing)
        self.assertEqual(status, DisputeStatus.DISPUTED.value)
        self.assertTrue(any("Duplicate Khasra" in t for t in tags))
        self.assertEqual(disputes[0]["dispute_type"], DisputeType.DUPLICATE_SURVEY_NO.value)

    def test_spatial_boundary_encroachment(self):
        # Existing plot from lon 82.980 to 82.982, lat 25.310 to 25.312
        existing = [{
            "id": "PARCEL-A",
            "khasra_no": "101",
            "village": "Rampur",
            "owners": [{"name": "Ramesh", "share_percentage": 100.0}],
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[[82.980, 25.310], [82.982, 25.310], [82.982, 25.312], [82.980, 25.312], [82.980, 25.310]]]
            }
        }]
        # Overlapping plot from lon 82.981 to 82.983 (overlaps 50% horizontally)
        candidate = {
            "id": "PARCEL-B",
            "khasra_no": "102",
            "khata_no": "5",
            "village": "Rampur",
            "area_sq_meters": 2000.0,
            "owners": [{"name": "Suresh", "share_percentage": 100.0}],
            "boundary_geojson": {
                "type": "Polygon",
                "coordinates": [[[82.981, 25.310], [82.983, 25.310], [82.983, 25.312], [82.981, 25.312], [82.981, 25.310]]]
            }
        }
        status, tags, disputes, conf = validate_land_record(candidate, existing)
        self.assertEqual(status, DisputeStatus.DISPUTED.value)
        self.assertTrue(any("Spatial Encroachment" in t for t in tags))
        self.assertEqual(disputes[0]["dispute_type"], DisputeType.BOUNDARY_OVERLAP.value)
        self.assertIsNotNone(disputes[0]["overlap_geojson"])
        self.assertGreater(disputes[0]["overlap_area_sq_meters"], 10.0)

    def test_sha256_hash_immutability(self):
        data1 = {"khasra_no": "101", "owner": "Rajesh"}
        data2 = {"khasra_no": "101", "owner": "Rajesh"}
        data3 = {"khasra_no": "101", "owner": "Altered Owner"}

        hash1 = calculate_sha256(data1)
        hash2 = calculate_sha256(data2)
        hash3 = calculate_sha256(data3)

        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)
        self.assertEqual(len(hash1), 64)

if __name__ == '__main__':
    unittest.main()
