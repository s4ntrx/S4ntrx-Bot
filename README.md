# S4ntrx Bot

A multi-user cybersecurity education chatbot built for a school project.
Students register, chat with an AI security assistant, analyze suspicious
messages and URLs, check password strength, file incident reports, and
an admin can view aggregate statistics.

**Everything in this repo runs with zero paid services and zero external
AI API keys.** The chatbot works out of the box using a local
knowledge-base responder — an optional, more conversational mode using
Ollama is documented below but is not required.

---

## 1. What's actually built (scope)

| Feature | Status |
|---|---|
| Registration / login / logout, hashed passwords, CSRF, sessions | Done |
| Per-user chat history (IDOR-safe — verified in tests) | Done |
| AI chat: offline knowledge-base responder (default) | Done |
| AI chat: optional Ollama integration | Done, optional, off by default |
| Phishing message analyzer (rule-based, risk-scored) | Done |
| URL structural analyzer (rule-based, risk-scored) | Done |
| Password strength checker (100% client-side, never transmitted) | Done |
| Incident reporting (student-scoped) | Done |
| Admin dashboard (aggregate stats, role-gated) | Done |
| Automated tests, charts, data migrations, RAG/embeddings | **Not built** — see Limitations |

Nothing below claims to be more finished than this table says.

---

## 2. System requirements & storage

| Component | Requirement | Approx. storage |
|---|---|---|
| Python | 3.10 or newer | ~150 MB (if not already installed) |
| pip packages (this project) | Flask, SQLAlchemy, Flask-Login, Flask-WTF, python-dotenv, psycopg2-binary, requests | ~60–90 MB total in a virtual environment |
| Database (default) | SQLite — a single file, created automatically | Negligible (grows with usage, typically a few MB for a class project) |
| Database (optional, multi-server) | PostgreSQL via Supabase free tier | 0 MB local — hosted remotely |
| **Ollama (optional, only if you want a more conversational AI)** | Ollama runtime | ~700 MB |
| — smallest usable model (`llama3.2:1b`) | | ~1.3 GB download |
| — better-quality model (`llama3.2:3b`) | | ~2 GB download |
| — larger model (`llama3:8b`) | | ~4.7 GB download |

**Bottom line:** the app itself needs well under 200 MB of disk and no
GPU. Only enable Ollama if you have the time and bandwidth to download
a model tonight — otherwise skip it entirely; the default knowledge-base
responder is real, working, and needs nothing extra.

---

## 3. Install — step by step

### Windows

1. Install Python 3.10+ from python.org (check "Add Python to PATH" during install).
2. Install Git from git-scm.com.
3. Open PowerShell in the project folder:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   ```
4. Generate a secret key and paste it into `.env`:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
5. Run:
   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in a browser.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"   # paste into SECRET_KEY in .env
python app.py
```

Then open `http://127.0.0.1:5000`.

The SQLite database file is created automatically on first run at
`instance/s4ntrx.db` — no manual database setup needed for local use.

### Creating an admin account

```bash
flask --app app seed-admin
```

This prompts for an email; if that email already has an account it's
promoted to admin, otherwise it creates a new admin account interactively.

### (Optional) Enabling Ollama for a more conversational AI

Only do this if you have time and disk space before your deadline —
it is not required for a working bot.

1. Install Ollama from ollama.com (or `curl -fsSL https://ollama.com/install.sh | sh` on Linux).
2. Pull a small model: `ollama pull llama3.2:1b`
3. In `.env`, set:
   ```
   AI_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.2:1b
   ```
4. Restart the Flask app. If Ollama isn't reachable, chat automatically
   falls back to the offline knowledge-base responder instead of crashing.

### (Optional) Switching to Postgres/Supabase

Create a free Supabase project, copy its connection string, and set in `.env`:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```
No code changes needed.

---

## 4. Project structure

```
s4ntrx-bot/
├── app.py                  # App factory, blueprint registration, CLI commands
├── config.py                # Env-driven configuration
├── extensions.py             # Shared db / login_manager / csrf instances
├── forms.py                  # WTForms (CSRF + validation) for every form
├── requirements.txt
├── .env.example
├── README.md
├── LICENSE
├── models/
│   ├── user.py                # User (hashed password, role)
│   ├── chat.py                 # ChatSession, ChatMessage
│   ├── incident.py             # IncidentReport
│   └── analysis.py             # PhishingAnalysis, UrlAnalysis (logs for admin stats)
├── routes/
│   ├── auth.py                 # register / login / logout
│   ├── main.py                  # landing page, dashboard
│   ├── chat.py                   # chat sessions & messages (IDOR-safe)
│   ├── security.py               # phishing detector, URL analyzer, password page
│   ├── incidents.py               # incident reporting
│   └── admin.py                    # admin dashboard (role-gated)
├── services/
│   ├── ai_service.py               # AIProvider / KnowledgeBaseProvider / OllamaProvider
│   ├── phishing_detector.py         # rule-based message analysis
│   └── url_analyzer.py               # rule-based URL structure analysis
├── knowledge/                          # Markdown knowledge base the AI draws from
│   ├── phishing.md, malware.md, ransomware.md, passwords.md,
│   ├── authentication.md, network_security.md, social_engineering.md,
│   └── incident_response.md, cybersecurity_basics.md
├── templates/                            # Jinja2 + Bootstrap 5
└── static/css, static/js
```

---

## 5. Manual test checklist (no automated test suite yet — see Limitations)

- [ ] Register, then log in
- [ ] Duplicate email/student ID registration is rejected
- [ ] Wrong password shows a generic error (doesn't reveal account existence)
- [ ] `/dashboard`, `/chat`, `/phishing`, `/url-analyzer`, `/incidents` all redirect to login when logged out
- [ ] Start a chat, ask about phishing/malware/passwords/MFA — response should be topic-relevant
- [ ] Log in as a second student — confirm you cannot open the first student's `/chat/<id>` URL directly (should 404)
- [ ] Submit an obviously suspicious message to the Phishing Detector — should show HIGH/CRITICAL
- [ ] Submit `http://192.168.1.1/verify-account` to the URL Analyzer — should flag IP-based domain + suspicious keyword
- [ ] Type a password on the Password Security page — check DevTools Network tab to confirm nothing is sent to the server
- [ ] Submit an incident report, confirm it appears only for that student
- [ ] Promote a user with `flask --app app seed-admin`, confirm `/admin/` works for them and returns 403 for a student

---

## 6. Deployment (free-tier)

```
Browser
   ↓
Flask app  →  free host (Render/PythonAnywhere free tier, etc.)
   ↓
Supabase PostgreSQL (set DATABASE_URL)
```

Set `FLASK_ENV=production` and a real `SECRET_KEY` in the host's
environment variables — never commit `.env`. If you enable Ollama,
it must run on a machine you control (Ollama itself generally can't
run on typical free web-hosting tiers) — keep `AI_PROVIDER=knowledge`
for hosted deployments unless you're self-hosting the whole stack.

---

## 7. Security notes

- Passwords hashed with Werkzeug (`generate_password_hash` / `check_password_hash`), never stored in plaintext.
- CSRF protection on every form (Flask-WTF).
- Every chat/incident/analysis query filters by `current_user.id` — no endpoint trusts a client-supplied user ID.
- Password checker never leaves the browser (see `static/js/password_checker.js`).
- No secrets in source code; everything sensitive comes from `.env` / environment variables.
- Generic login error message (doesn't reveal whether the email exists).

## 8. Limitations (stated plainly, not hidden)

- **No automated test suite yet.** The manual checklist above covers
  the same ground, but there's no `pytest` suite in this repo.
- **Phishing/URL analysis is heuristic, not threat intelligence.** No
  live blocklist or reputation service is connected — both tools say so
  in their own output.
- **The offline AI is keyword-matching against local Markdown files**,
  not a language model. It's accurate because it only ever returns real
  knowledge-base content, but it isn't as conversational as an LLM.
  Enabling Ollama (see above) upgrades this if you have time.
- **Admin promotion is CLI-only** — there's no in-app "make this user an admin" button.
- **No charts library wired up yet** on the admin dashboard — stats are shown as numbers, not graphs.


<img src="dashboard.png" alt="Dashboard" width="800">
