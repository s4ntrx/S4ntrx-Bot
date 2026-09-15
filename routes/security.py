from flask import Blueprint, render_template
from flask_login import login_required, current_user

from extensions import db
from forms import PhishingAnalysisForm, UrlAnalysisForm
from models.analysis import PhishingAnalysis, UrlAnalysis
from services.phishing_detector import analyze_message
from services.url_analyzer import analyze_url

security_bp = Blueprint("security", __name__)


@security_bp.route("/phishing", methods=["GET", "POST"])
@login_required
def phishing():
    form = PhishingAnalysisForm()
    result = None
    if form.validate_on_submit():
        result = analyze_message(form.content.data)
        db.session.add(PhishingAnalysis(
            user_id=current_user.id,
            risk_level=result["risk_level"],
            indicator_count=result["indicator_count"],
        ))
        db.session.commit()
    return render_template("phishing.html", form=form, result=result)


@security_bp.route("/url-analyzer", methods=["GET", "POST"])
@login_required
def url_analyzer():
    form = UrlAnalysisForm()
    result = None
    if form.validate_on_submit():
        result = analyze_url(form.url.data)
        db.session.add(UrlAnalysis(
            user_id=current_user.id,
            url=result["url"][:500],
            risk_level=result["risk_level"],
            indicator_count=result["indicator_count"],
        ))
        db.session.commit()
    return render_template("url_analyzer.html", form=form, result=result)


@security_bp.route("/password-security")
@login_required
def password_security():
    # Entirely client-side — see static/js/password_checker.js.
    # The password itself is never sent to the server.
    return render_template("password.html")
