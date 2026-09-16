from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models.user import User
from forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter(
            (User.email == form.email.data.lower()) | (User.student_id == form.student_id.data)
        ).first()
        if existing:
            flash("An account with that email or student ID already exists.", "error")
            return render_template("register.html", form=form)

        user = User(
            name=form.name.data.strip(),
            student_id=form.student_id.data.strip(),
            email=form.email.data.lower().strip(),
            role="student",
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        # Same generic error for "no user" and "wrong password" — do not
        # reveal which one failed, that leaks account existence.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.", "error")
            return render_template("login.html", form=form)

        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
