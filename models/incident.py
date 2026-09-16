from datetime import datetime
from extensions import db


class IncidentReport(db.Model):
    __tablename__ = "incident_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    incident_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_datetime = db.Column(db.String(50), nullable=True)
    affected_asset = db.Column(db.String(200), nullable=True)
    suspected_threat = db.Column(db.String(200), nullable=True)
    severity = db.Column(db.String(20), nullable=False, default="medium")  # low|medium|high|critical
    actions_taken = db.Column(db.Text, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="open")  # open|reviewing|closed

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref="incident_reports")
