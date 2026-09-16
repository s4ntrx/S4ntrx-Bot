# Cybersecurity Fundamentals

## The CIA triad
- **Confidentiality** — only authorized people can access data.
- **Integrity** — data isn't altered without authorization.
- **Availability** — systems and data are accessible when needed.

## Data breaches
A data breach is unauthorized access to or disclosure of data. If a
service you use is breached: change your password there (and anywhere
you reused it), enable MFA, and monitor for suspicious activity —
especially if financial or identity data was involved.

## Identity theft
Occurs when someone uses your personal information without permission,
typically for fraud. Warning signs include unfamiliar accounts/charges,
denied credit for no reason, or missing expected mail/bills.

## Cybersecurity careers
Common entry paths: SOC analyst, penetration tester, security engineer,
GRC (governance/risk/compliance) analyst, incident responder. Useful
starting points: general IT/networking fundamentals, a home lab, and
entry-level certifications (e.g., CompTIA Security+).

## Secure coding basics
- Validate and sanitize all input; never trust client-side validation alone.
- Use parameterized queries — never build SQL with string concatenation.
- Escape output to prevent XSS.
- Never hard-code secrets in source code — use environment variables.
- Fail closed: on error, deny access rather than defaulting to allow.
