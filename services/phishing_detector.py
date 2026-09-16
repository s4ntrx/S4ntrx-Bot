import re

URGENCY_PATTERNS = [
    r"\burgent\b", r"\bimmediately\b", r"\bact now\b", r"\bwithin 24 hours\b",
    r"\bfinal notice\b", r"\baccount.{0,15}(suspend|close|lock)", r"\bexpires? (today|soon)\b",
]
THREAT_PATTERNS = [
    r"\blegal action\b", r"\bpenalty\b", r"\byour account will be\b", r"\bfailure to\b",
]
CREDENTIAL_REQUEST_PATTERNS = [
    r"\bverify your (account|password|identity)\b", r"\bconfirm your (password|details|identity)\b",
    r"\benter your password\b", r"\blog ?in to verify\b", r"\bupdate your payment\b",
]
FINANCIAL_REQUEST_PATTERNS = [
    r"\bwire transfer\b", r"\bgift card\b", r"\bbank details\b", r"\bcredit card number\b",
    r"\brefund\b.{0,20}\bclick\b",
]
SECRECY_PATTERNS = [
    r"\bdo not tell\b", r"\bkeep this confidential\b", r"\bbetween (you and me|us)\b",
]
REWARD_PATTERNS = [
    r"\byou('| ha)ve won\b", r"\bcongratulations\b.{0,20}\b(selected|winner)\b", r"\bclaim your prize\b",
]
VERIFICATION_PATTERNS = [
    r"\bverify your account\b", r"\bconfirm your identity\b", r"\breactivate your account\b",
]

LINK_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
IP_URL_PATTERN = re.compile(r"https?://\d{1,3}(\.\d{1,3}){3}")


def _count_matches(text: str, patterns: list[str]) -> int:
    return sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))


def analyze_message(text: str) -> dict:
    """Analyze free-text (email/SMS/social message) for phishing indicators.
    Returns a dict with risk_level, indicators found, and guidance. This is
    a heuristic tool, not a verdict — it can't prove intent."""

    text = text or ""
    indicators = []

    if _count_matches(text, URGENCY_PATTERNS):
        indicators.append("Urgency language pressuring quick action")
    if _count_matches(text, THREAT_PATTERNS):
        indicators.append("Threatening language (legal action, penalties, account loss)")
    if _count_matches(text, CREDENTIAL_REQUEST_PATTERNS):
        indicators.append("Requests to verify/confirm a password or identity")
    if _count_matches(text, FINANCIAL_REQUEST_PATTERNS):
        indicators.append("Requests for financial information or payment")
    if _count_matches(text, SECRECY_PATTERNS):
        indicators.append("Requests for secrecy")
    if _count_matches(text, REWARD_PATTERNS):
        indicators.append("Fake reward or prize claim")
    if _count_matches(text, VERIFICATION_PATTERNS):
        indicators.append("Fake account verification request")

    links = LINK_PATTERN.findall(text)
    if links:
        indicators.append(f"Contains {len(links)} link(s) — verify the destination before clicking")
    if IP_URL_PATTERN.search(text):
        indicators.append("Link points to a raw IP address instead of a domain")

    # Very rough sender/domain mismatch heuristic: a display name that
    # looks like a company/bank but a link to an unrelated-looking domain.
    if re.search(r"\b(bank|paypal|amazon|microsoft|apple|google)\b", text, re.IGNORECASE) and links:
        known_domains = {"paypal.com", "amazon.com", "microsoft.com", "apple.com", "google.com"}
        for link in links:
            domain_match = re.search(r"https?://(?:www\.)?([^/\s]+)", link, re.IGNORECASE)
            if domain_match and not any(domain_match.group(1).lower().endswith(d) for d in known_domains):
                indicators.append("Mentions a well-known brand but links to an unrelated domain")
                break

    # Crude grammar/anomaly signal: multiple consecutive exclamation marks
    # or ALL CAPS words, common in scam messages.
    if re.search(r"!!+", text) or len(re.findall(r"\b[A-Z]{4,}\b", text)) >= 2:
        indicators.append("Unusual formatting (excessive punctuation or capitalization)")

    score = len(indicators)
    if score == 0:
        risk_level = "LOW"
    elif score <= 2:
        risk_level = "MEDIUM"
    elif score <= 4:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    if risk_level == "LOW":
        recommendation = (
            "No strong phishing indicators found by this tool. Still use "
            "normal caution with unexpected messages — this analysis is "
            "heuristic, not a guarantee of safety."
        )
    elif risk_level == "MEDIUM":
        recommendation = (
            "Some suspicious signals present. Don't click links or reply "
            "with information; verify the sender through a separate, "
            "known channel before acting."
        )
    else:
        recommendation = (
            "Multiple strong phishing indicators found. Do not click any "
            "links, do not reply, and do not provide any information. "
            "Report this message to your school's IT/security administrator."
        )

    return {
        "risk_level": risk_level,
        "indicators": indicators,
        "indicator_count": score,
        "explanation": (
            f"{score} phishing indicator(s) detected out of the patterns this "
            "tool checks for. This is a heuristic assessment based on message "
            "content only — it cannot confirm whether the sender or link is "
            "actually malicious."
        ),
        "recommendation": recommendation,
    }
