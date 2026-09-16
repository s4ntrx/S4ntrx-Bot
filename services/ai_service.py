"""
AI provider abstraction for S4ntrx Bot.

    AIProvider (interface)
        |
        ├── KnowledgeBaseProvider   -- default, offline, always works
        |
        └── OllamaProvider          -- optional, requires a running Ollama server

Swapping providers never touches routes/templates — only config.py's
AI_PROVIDER value and get_ai_provider() below.
"""
import os
import re
import glob
from abc import ABC, abstractmethod

KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge")

SYSTEM_PROMPT = (
    "You are S4ntrx Bot, a cybersecurity education assistant for students. "
    "Explain concepts clearly, avoid unnecessary jargon, give practical "
    "defensive advice, and never claim to have scanned or fixed a real "
    "device. If unsure, say so plainly."
)


class AIProvider(ABC):
    @abstractmethod
    def generate_reply(self, message: str, history: list[dict], user_name: str | None = None) -> str:
        """Return a plain-text reply to `message`, given prior turns as
        a list of {"sender": "user"|"bot", "message": str} and, when
        available, the student's display name for personalization."""
        raise NotImplementedError


class KnowledgeBaseProvider(AIProvider):
    """Keyword-matches the student's message against the local knowledge
    base and returns a relevant excerpt. No network calls, no external
    dependency — this is what makes S4ntrx Bot work with zero setup."""

    def __init__(self, knowledge_dir: str = KNOWLEDGE_DIR):
        self.documents = self._load_documents(knowledge_dir)

    @staticmethod
    def _load_documents(knowledge_dir: str) -> list[dict]:
        docs = []
        for path in sorted(glob.glob(os.path.join(knowledge_dir, "*.md"))):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            title = title_match.group(1) if title_match else os.path.basename(path)
            docs.append({"title": title, "text": text, "words": set(re.findall(r"[a-z]+", text.lower()))})
        return docs

    def _best_match(self, message: str):
        query_words = set(re.findall(r"[a-z]+", message.lower()))
        if not query_words or not self.documents:
            return None
        scored = [
            (len(query_words & doc["words"]), doc) for doc in self.documents
        ]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        best_score, best_doc = scored[0]
        return best_doc if best_score > 0 else None

    def generate_reply(self, message: str, history: list[dict], user_name: str | None = None) -> str:
        greeting_words = {"hi", "hello", "hey"}
        words = set(re.findall(r"[a-z]+", message.lower()))
        if words & greeting_words and len(words) <= 3:
            return (
                "Hi! I'm S4ntrx Bot. Ask me about phishing, malware, passwords, "
                "MFA, safe browsing, or what to do if you suspect an incident."
            )

        doc = self._best_match(message)
        if doc is None:
            return (
                "I don't have a confident answer for that from my current "
                "knowledge base. Try asking about phishing, malware, ransomware, "
                "passwords, MFA, network security, social engineering, or "
                "incident response — or use the Phishing Detector / URL "
                "Analyzer tools for something you're looking at right now."
            )

        # Return the section most relevant to the query, not the whole doc,
        # to keep replies focused and chat-sized.
        sections = re.split(r"\n(?=##\s)", doc["text"])
        query_words = set(re.findall(r"[a-z]+", message.lower()))
        best_section = max(
            sections, key=lambda s: len(query_words & set(re.findall(r"[a-z]+", s.lower())))
        )
        reply = best_section.strip()
        if len(reply) > 900:
            reply = reply[:900].rsplit("\n", 1)[0] + "\n…"
        return reply


class OllamaProvider(AIProvider):
    """Talks to a locally running Ollama server. Requires Ollama installed
    and a model pulled — see README before enabling (AI_PROVIDER=ollama)."""

    def __init__(self, host: str, model: str):
        self.host = host.rstrip("/")
        self.model = model

    def generate_reply(self, message: str, history: list[dict], user_name: str | None = None) -> str:
        import requests  # imported lazily so this file has no hard dependency on it

        system_content = SYSTEM_PROMPT
        if user_name:
            system_content += (
                f" You are talking with {user_name}, a student. Address them by "
                "name occasionally (not every message), keep track of what they've "
                "already asked in this conversation so you don't repeat yourself, "
                "and tailor examples to a student audience. Give complete, "
                "well-organized answers — use short paragraphs or bullet points "
                "for multi-part answers — rather than one-line responses, but "
                "don't pad with filler just to sound longer."
            )

        messages = [{"role": "system", "content": system_content}]
        for turn in history[-10:]:
            role = "user" if turn["sender"] == "user" else "assistant"
            messages.append({"role": role, "content": turn["message"]})
        messages.append({"role": "user", "content": message})

        try:
            resp = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": 700,  # allow longer answers than Ollama's default
                        "temperature": 0.6,
                    },
                },
                timeout=60,  # bigger models can take longer, especially on first load
            )
            resp.raise_for_status()
            return resp.json()["message"]["content"]
        except Exception:
            # Never crash the chat route because Ollama is down — degrade
            # to the offline provider instead.
            return KnowledgeBaseProvider().generate_reply(message, history, user_name)


def get_ai_provider(app_config) -> AIProvider:
    if app_config.get("AI_PROVIDER") == "ollama":
        return OllamaProvider(app_config["OLLAMA_HOST"], app_config["OLLAMA_MODEL"])
    return KnowledgeBaseProvider()
