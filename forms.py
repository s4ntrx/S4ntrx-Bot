from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    student_id = StringField(
        "Student ID",
        validators=[DataRequired(), Length(min=2, max=50), Regexp(r"^[A-Za-z0-9\-_/]+$",
                    message="Student ID may only contain letters, numbers, - _ /")],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters.")],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class ChatMessageForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired(), Length(max=2000)])


class PhishingAnalysisForm(FlaskForm):
    content = StringField("Message content", validators=[DataRequired(), Length(max=5000)])
    submit = SubmitField("Analyze")


class UrlAnalysisForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired(), Length(max=500)])
    submit = SubmitField("Analyze")


class IncidentReportForm(FlaskForm):
    incident_type = StringField("Incident Type", validators=[DataRequired(), Length(max=50)])
    description = StringField("Description", validators=[DataRequired(), Length(max=3000)])
    incident_datetime = StringField("Date/Time", validators=[Length(max=50)])
    affected_asset = StringField("Affected Device/Account", validators=[Length(max=200)])
    suspected_threat = StringField("Suspected Threat", validators=[Length(max=200)])
    severity = StringField("Severity", validators=[DataRequired(), Length(max=20)])
    actions_taken = StringField("Actions Already Taken", validators=[Length(max=2000)])
    additional_notes = StringField("Additional Notes", validators=[Length(max=2000)])
    submit = SubmitField("Submit Report")
