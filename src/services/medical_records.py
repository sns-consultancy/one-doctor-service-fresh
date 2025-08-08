import json
from datetime import datetime
from io import BytesIO

try:
    from fpdf import FPDF
except ImportError:  # pragma: no cover - optional dependency
    FPDF = None


class MedicalRecordService:
    """Service to manage medication records with age categorization."""

    def __init__(self, db):
        self.db = db

    def categorize_age(self, age):
        if age < 1:
            return "infant"
        if age < 3:
            return "toddler"
        if age < 18:
            return "young"
        return "adult"

    def add_record(self, data):
        entry = {
            "user_id": data["user_id"],
            "age": data["age"],
            "medication": data.get("medication"),
            "notes": data.get("notes", ""),
            "entered_by": data.get("entered_by"),
            "entered_by_role": data.get("entered_by_role", "patient"),
            "category": self.categorize_age(data["age"]),
            "date": datetime.utcnow().isoformat(),
        }
        self.db.collection("medical_records").add(entry)
        return entry

    def get_records_by_user(self, user_id):
        records = []
        docs = (
            self.db.collection("medical_records")
            .where("user_id", "==", user_id)
            .stream()
        )
        for doc in docs:
            records.append(doc.to_dict())
        return records

    def to_json(self, records):
        return json.dumps(records, indent=2)

    def export_user_pdf(self, user_id):
        if FPDF is None:  # pragma: no cover
            raise RuntimeError("fpdf package is required for PDF export")
        records = self.get_records_by_user(user_id)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Medication History for {user_id}", ln=True)
        for r in records:
            line = f"{r.get('date', '')}: {r.get('medication', 'N/A')} ({r.get('category', '')})"
            pdf.multi_cell(0, 10, line)
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        return BytesIO(pdf_bytes)
