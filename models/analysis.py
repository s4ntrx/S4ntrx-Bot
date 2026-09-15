from datetime import datetime
from extensions import db


class PhishingAnalysis(db.Model):
    __tablename__ = "phishing_analyses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    risk_level = db.Column(db.String(20), nullable=False)  # LOW|MEDIUM|HIGH|CRITICAL
    indicator_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class UrlAnalysis(db.Model):
    __tablename__ = "url_analyses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    indicator_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
