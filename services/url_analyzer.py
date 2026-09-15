import re
from urllib.parse import urlparse

IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm", "banking",
    "signin", "webscr", "password", "billing",
]
SUSPICIOUS_TLDS = {".zip", ".mov", ".xyz", ".top", ".click", ".gq", ".tk", ".work", ".rest"}
LOOKALIKE_BRANDS = ["paypal", "amazon", "microsoft", "apple", "google", "facebook", "bankofamerica"]


def analyze_url(raw_url: str) -> dict:
    """Analyze a URL's structural characteristics for phishing risk
    indicators. This is NOT threat intelligence — it cannot confirm a
    URL is malicious, only flag structural red flags."""

    raw_url = (raw_url or "").strip()
    indicators = []

    url = raw_url if re.match(r"^https?://", raw_url, re.IGNORECASE) else f"http://{raw_url}"
    try:
        parsed = urlparse(url)
    except ValueError:
        return {
            "url": raw_url,
            "risk_level": "MEDIUM",
            "indicators": ["Could not parse this as a valid URL"],
            "indicator_count": 1,
            "explanation": "The input doesn't parse as a well-formed URL.",
            "recommendation": "Double check the URL and try again.",
        }

    host = parsed.hostname or ""

    if parsed.scheme == "http":
        indicators.append("Uses HTTP instead of HTTPS (traffic is not encrypted)")

    if IP_PATTERN.match(host):
        indicators.append("Domain is a raw IP address rather than a named domain")

    if parsed.port and parsed.port not in (80, 443):
        indicators.append(f"Uses a non-standard port ({parsed.port})")

    subdomain_count = max(host.count("."), 0)
    if subdomain_count >= 3:
        indicators.append("Excessive number of subdomains")

    if len(raw_url) > 100:
        indicators.append("Unusually long URL")

    if any(kw in raw_url.lower() for kw in SUSPICIOUS_KEYWORDS):
        indicators.append("Contains keywords commonly used in credential-phishing URLs")

    if "%" in raw_url:
        indicators.append("Contains encoded characters, which can obscure the real destination")

    if any(host.lower().endswith(tld) for tld in SUSPICIOUS_TLDS):
        indicators.append("Uses a domain extension frequently abused for phishing/spam")

    for brand in LOOKALIKE_BRANDS:
        if brand in host.lower().replace("-", "").replace(".", "") and not host.lower().endswith(f"{brand}.com"):
            indicators.append(f"Domain resembles '{brand}' but isn't the official domain")
            break

    if "@" in raw_url:
        indicators.append("Contains an '@' symbol, which can be used to disguise the real destination")

    if "-" in host and subdomain_count >= 2:
        indicators.append("Domain uses hyphens combined with multiple subdomains, a common obfuscation pattern")

    score = len(indicators)
    if score == 0:
        risk_level = "LOW"
    elif score <= 2:
        risk_level = "MEDIUM"
    elif score <= 4:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    recommendation = {
        "LOW": "No strong structural red flags found. This does not confirm the site is safe — stay cautious with anything unexpected.",
        "MEDIUM": "Some structural red flags found. Avoid entering credentials or personal information until you can verify the site independently.",
        "HIGH": "Multiple structural red flags found. Avoid visiting this URL or entering any information.",
        "CRITICAL": "Numerous strong red flags found. Treat this URL as suspicious and avoid interacting with it. Report it if it was sent to you unexpectedly.",
    }[risk_level]

    return {
        "url": raw_url,
        "risk_level": risk_level,
        "indicators": indicators,
        "indicator_count": score,
        "explanation": (
            "This analysis is based only on the URL's structure — no live "
            "threat-intelligence service is connected. A URL with no "
            "indicators here is 'not obviously suspicious,' not "
            "'confirmed safe,' and a flagged URL is 'suspicious,' not "
            "'confirmed malicious.'"
        ),
        "recommendation": recommendation,
    }
