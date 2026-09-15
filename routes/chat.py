from flask import Blueprint, render_template, request, jsonify, abort, current_app
from flask_login import login_required, current_user

from extensions import db
from models.chat import ChatSession, ChatMessage
from services.ai_service import get_ai_provider

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


def _get_owned_session(session_id: int) -> ChatSession:
    """Fetch a chat session and verify it belongs to the current user.
    Never trust a session id alone — always filter by owner too, to
    prevent one student reading another's chat (IDOR)."""
    session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
    if session is None:
        abort(404)
    return session


@chat_bp.route("/")
@login_required
def index():
    sessions = (
        ChatSession.query.filter_by(user_id=current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )
    active_session = sessions[0] if sessions else None
    return render_template("chat.html", sessions=sessions, active_session=active_session)


@chat_bp.route("/<int:session_id>")
@login_required
def view_session(session_id):
    sessions = (
        ChatSession.query.filter_by(user_id=current_user.id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )
    active_session = _get_owned_session(session_id)
    return render_template("chat.html", sessions=sessions, active_session=active_session)


@chat_bp.route("/new", methods=["POST"])
@login_required
def new_session():
    session = ChatSession(user_id=current_user.id, title="New Conversation")
    db.session.add(session)
    db.session.commit()
    return jsonify({"session_id": session.id})


@chat_bp.route("/<int:session_id>/message", methods=["POST"])
@login_required
def send_message(session_id):
    session = _get_owned_session(session_id)

    data = request.get_json(silent=True) or {}
    text = (data.get("message") or "").strip()
    if not text:
        return jsonify({"error": "Message cannot be empty."}), 400
    if len(text) > 2000:
        return jsonify({"error": "Message is too long (max 2000 characters)."}), 400

    user_msg = ChatMessage(session_id=session.id, sender="user", message=text)
    db.session.add(user_msg)

    if session.title == "New Conversation":
        session.title = text[:60]

    history = [{"sender": m.sender, "message": m.message} for m in session.messages]

    provider = get_ai_provider(current_app.config)
    try:
        reply_text = provider.generate_reply(text, history)
    except Exception:
        current_app.logger.exception("AI provider failed to generate a reply")
        reply_text = (
            "Sorry — I couldn't generate a response just now. Please try "
            "again in a moment."
        )

    bot_msg = ChatMessage(session_id=session.id, sender="bot", message=reply_text)
    db.session.add(bot_msg)
    db.session.commit()

    return jsonify({
        "user_message": {"sender": "user", "message": user_msg.message, "created_at": user_msg.created_at.isoformat()},
        "bot_message": {"sender": "bot", "message": bot_msg.message, "created_at": bot_msg.created_at.isoformat()},
        "session_title": session.title,
    })


@chat_bp.route("/<int:session_id>/delete", methods=["POST"])
@login_required
def delete_session(session_id):
    session = _get_owned_session(session_id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({"deleted": True})
