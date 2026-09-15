from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from extensions import db
from forms import IncidentReportForm
from models.incident import IncidentReport

incidents_bp = Blueprint("incidents", __name__, url_prefix="/incidents")

VALID_SEVERITIES = {"low", "medium", "high", "critical"}


@incidents_bp.route("/")
@login_required
def list_reports():
    reports = (
        IncidentReport.query.filter_by(user_id=current_user.id)
        .order_by(IncidentReport.created_at.desc())
        .all()
    )
    return render_template("incident_list.html", reports=reports)


@incidents_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_report():
    form = IncidentReportForm()
    if form.validate_on_submit():
        severity = (form.severity.data or "medium").strip().lower()
        if severity not in VALID_SEVERITIES:
            severity = "medium"

        report = IncidentReport(
            user_id=current_user.id,
            incident_type=(form.incident_type.data or "").strip(),
            description=(form.description.data or "").strip(),
            incident_datetime=(form.incident_datetime.data or "").strip() or None,
            affected_asset=(form.affected_asset.data or "").strip() or None,
            suspected_threat=(form.suspected_threat.data or "").strip() or None,
            severity=severity,
            actions_taken=(form.actions_taken.data or "").strip() or None,
            additional_notes=(form.additional_notes.data or "").strip() or None,
        )
        db.session.add(report)
        db.session.commit()
        flash("Incident report submitted.", "success")
        return redirect(url_for("incidents.list_reports"))

    return render_template("incident_report.html", form=form)


@incidents_bp.route("/<int:report_id>")
@login_required
def view_report(report_id):
    report = IncidentReport.query.filter_by(id=report_id, user_id=current_user.id).first()
    if report is None:
        abort(404)
    return render_template("incident_detail.html", report=report)
