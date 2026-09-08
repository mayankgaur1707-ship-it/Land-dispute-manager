# Intelligent Land Record Digitization and Validation System
### *AI-Powered Cadastral Digitization, Spatial Dispute Detection & Tamper-Proof Land Governance*
**Ministry of Rural Development • Government of India Initiative**

![Project Status](https://img.shields.io/badge/Status-Active%20Pilot-emerald)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Shapely%20%7C%20Leaflet.js%20%7C%20SQLite-blue)
![Security](https://img.shields.io/badge/Audit-SHA--256%20Blockchain%20Ledger-purple)

---

## 📌 Executive Summary

India's land governance faces severe challenges due to legacy paper-based records, high manual transcription errors, fraudulent double-sales, and boundary encroachment disputes that clog the judicial system. 

This platform implements the end-to-end blueprint for the **Intelligent Land Record Digitization and Validation System**:
1. **Document Scanning & AI-OCR Extraction**: Ingests Khasra, Khatauni, Sale Deeds, and 7/12 extracts, standardizing ownership, area, and geocoordinates.
2. **GIS Spatial Overlap & Dispute Engine**: Employs computational geometry (`Shapely`) to detect parcel boundary encroachments in real time.
3. **Registry Fraud & Share Validation**: Verifies 100% co-sharer equity closure and prevents duplicate survey number registrations.
4. **Interactive Cadastral GIS Map**: Renders parcels with Leaflet.js, color-coded by legal clearance, with pulse highlights on disputed encroachment zones.
5. **Cryptographic Audit Trail**: Every digitization, mutation, and dispute decree is chained via immutable SHA-256 blocks for verifiable anti-tampering.
6. **Role-Based Portals**: Interfaces for Revenue Officers/Patwaris, Citizens/Farmers, and Banks/Auditors.

---

## 🏛️ System Architecture

```
[ Scanned Deed / Paper Khasra ]
             │
             ▼
[ AI-OCR & Data Extraction Engine ] ──> [ Standardization & GeoJSON Mapping ]
                                                        │
                                                        ▼
                                       [ Intelligent Validation Engine ]
                                       ├── 1. Shapely Spatial Polygon Intersect
                                       ├── 2. Duplicate Khasra Title Check
                                       └── 3. Co-Sharer Equity Summation (100%)
                                                        │
                      ┌─────────────────────────────────┴─────────────────────────────────┐
                      ▼                                                                   ▼
          [ If Dispute Detected ]                                              [ If Validation Passes ]
   • Flag Encroachment Area (m²)                                           • Mark Parcel Status: CLEAR
   • Generate Overlap Polygon GeoJSON                                      • Issue Encumbrance-Free Badge
   • Route to Officer Resolution Console                                   • Register in Bhulekh Ledger
                      │                                                                   │
                      └───────────────────────────────┬───────────────────────────────────┘
                                                      │
                                                      ▼
                                       [ SHA-256 Blockchain Audit Trail ]
                                       • Prev Hash + Current Hash Linkage
                                       • 100% Tamper Verification
                                                      │
                                                      ▼
                                    [ Interactive GIS Cadastral Map (Leaflet) ]
                                    • Green: Clear Title
                                    • Red: Disputed Overlap
                                    • Orange: Share Warning
```

---

## 🚀 Quickstart & Running Locally

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.14)
- Web browser (Chrome, Edge, Firefox)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python main.py
```
*The server will automatically initialize the database, seed cadastral parcels for Rampur Village, and start the web portal at:*
👉 **`http://localhost:8000`**

---

## 🧪 Automated Testing

Run the test suite to verify the validation engine, spatial overlap detection, and cryptographic audit hashing:
```bash
python -m unittest discover tests
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status |
| `GET` | `/api/analytics` | High-level KPI metrics (clear %, dispute counts, hectares) |
| `GET` | `/api/records/` | List land records (supports search, village, status filters) |
| `GET` | `/api/records/{id}` | Detailed parcel view with linked dispute history |
| `POST` | `/api/records/digitize` | AI-OCR extraction, automated validation & dispute detection |
| `GET` | `/api/gis/parcels` | GeoJSON FeatureCollection formatted for GIS maps |
| `GET` | `/api/disputes/` | List all active/resolved land disputes |
| `POST` | `/api/disputes/{id}/resolve`| Revenue Officer demarcation and settlement action |
| `GET` | `/api/audit/ledger` | Complete cryptographic block ledger |
| `GET` | `/api/audit/verify` | Validates entire SHA-256 hash chain for tampering |
| `GET` | `/api/templates` | Pre-loaded official revenue deed templates |

---

## 👥 Use-Case Personas

- **Revenue Officer / Tehsildar**: Inspect flagged boundary overlaps, compare claimed boundary coordinates, and issue mutation or demarcation orders.
- **Farmer / Citizen**: Search land titles by Khasra number or name, verify unencumbered ownership, and view geo-tagged parcel boundaries.
- **Bank / Lending Officer**: Instantly check land collateral for active disputes, legal encumbrances, or double mortgages before sanctioning loans.
