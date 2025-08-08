from flask import Blueprint, jsonify, request, send_file
from src.auth import require_api_key
from src.db import db
from src.services.medical_records import MedicalRecordService

service = MedicalRecordService(db)

medical_records_bp = Blueprint("medical_records", __name__)


@medical_records_bp.route("/medical-records", methods=["POST"])
@require_api_key
def create_record():
    data = request.json or {}
    if "user_id" not in data or "age" not in data:
        return (
            jsonify({"status": "error", "message": "user_id and age are required"}),
            400,
        )
    record = service.add_record(data)
    return jsonify({"status": "success", "data": record}), 201


@medical_records_bp.route("/medical-records/<user_id>", methods=["GET"])
@require_api_key
def list_records(user_id):
    records = service.get_records_by_user(user_id)
    return jsonify({"status": "success", "data": records}), 200


@medical_records_bp.route("/medical-records/<user_id>/pdf", methods=["GET"])
@require_api_key
def export_records_pdf(user_id):
    try:
        pdf_io = service.export_user_pdf(user_id)
    except RuntimeError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500
    return send_file(
        pdf_io,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{user_id}_medication_history.pdf",
    )
