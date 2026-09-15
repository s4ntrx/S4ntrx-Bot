import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()  # reads .env in local development; in production, set real env vars

from extensions import db, login_manager, csrf
from config import config_by_name


def create_app(env_name=None):
    env_name = env_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[env_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access S4ntrx Bot."
    login_manager.login_message_category = "error"

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.chat import chat_bp
    from routes.security import security_bp
    from routes.incidents import incidents_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.cli.command("seed-admin")
    def seed_admin():
        """Promote or create an admin account: flask seed-admin"""
        import getpass

        with app.app_context():
            email = input("Admin email: ").strip().lower()
            user = User.query.filter_by(email=email).first()
            if user:
                user.role = "admin"
                db.session.commit()
                print(f"Existing user {email} promoted to admin.")
                return

            name = input("Full name: ").strip()
            student_id = input("Admin ID (any unique value): ").strip()
            password = getpass.getpass("Password: ")
            user = User(name=name, student_id=student_id, email=email, role="admin")
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Admin account created for {email}.")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))
