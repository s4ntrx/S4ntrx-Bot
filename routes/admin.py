from functools import wraps
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from models.user import User
from models.chat import ChatSession
from models.incident import IncidentReport
from models.analysis import PhishingAnalysis, UrlAnalysis

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)
    return wrapped


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "total_students": User.query.filter_by(role="student").count(),
        "total_conversations": ChatSession.query.count(),
        "security_reports": IncidentReport.query.count(),
        "phishing_analyses": PhishingAnalysis.query.count(),
        "url_analyses": UrlAnalysis.query.count(),
        "high_risk_events": (
            PhishingAnalysis.query.filter(PhishingAnalysis.risk_level.in_(["HIGH", "CRITICAL"])).count()
            + UrlAnalysis.query.filter(UrlAnalysis.risk_level.in_(["HIGH", "CRITICAL"])).count()
        ),
    }
    recent_reports = IncidentReport.query.order_by(IncidentReport.created_at.desc()).limit(10).all()
    return render_template("admin.html", stats=stats, recent_reports=recent_reports)
