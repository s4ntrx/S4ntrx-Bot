# Phishing

## What is phishing?
Phishing is a social-engineering attack where an attacker pretends to be someone you trust (a bank, your school, a delivery company, a friend) to trick you into giving up passwords, one-time codes or money, or into clicking a malicious link or opening an infected file. It works because it targets people, not software: even a fully patched device can't stop you from typing your password into a fake page.

## Types of phishing
- **Email phishing:** mass messages pretending to be a known brand.
- **Spear phishing:** targeted at one person, using details like your name, course or teacher.
- **Whaling and business email compromise (BEC):** impersonating a boss or executive to request payments or data.
- **Smishing:** phishing by SMS or messaging apps.
- **Vishing:** phishing by phone call, sometimes with a cloned or AI-generated voice.
- **Quishing:** a malicious QR code that leads to a fake login page.
- **Clone phishing:** a real email you received before is copied, with the link or attachment swapped for a malicious one.

## How to spot a phishing message (warning signs)
- Urgency or threats ("your account will be closed in 24 hours").
- A request for passwords, one-time codes, card numbers or payment.
- A sender address that doesn't match the organisation, or a display name that hides the real address.
- Generic greetings like "Dear customer" from a service that should know your name.
- Links whose real destination differs from the text shown.
- Unexpected attachments, especially .zip, .html, .exe or Office files asking you to "enable macros".
- Odd wording or formatting, though well-written phishing exists too, so a clean message isn't proof it's safe.
- A prize, refund or job offer you never applied for.

## How to check a link or sender safely
Don't click. On a computer, hover over the link to preview the real address; on a phone, press and hold. Read the domain from right to left up to the first single slash: in paypal.com.account-check.net the real domain is account-check.net. Watch for lookalikes such as rn instead of m, or a zero instead of the letter o. Paste suspicious links into the URL Analyzer tool, and suspicious text into the Phishing Detector. Then confirm with the organisation using a phone number or website you already know, not the one in the message.

## What to do if you suspect phishing
1. Don't click links, open attachments or reply.
2. Verify through a separate, trusted channel (call the organisation directly).
3. Report it using your email app's "Report phishing" option and tell your school's IT or security contact.
4. Delete the message afterwards.
5. If it was a text or chat message, block the sender and report it in the app.

## What if I already clicked or entered my password?
Act quickly, calmly and in this order: disconnect from the network if you downloaded a file; change the password on that account from a different, trusted device; change it anywhere else you reused it; turn on multi-factor authentication; sign out of all other sessions; check the account for new forwarding rules or changed recovery details; run a security scan if a file was opened; and tell your school's IT contact. If it involved a bank card or payment, contact the bank right away. Then file an incident report here so it is recorded.

## Why attackers use phishing
It's cheap, scalable and effective. Stolen credentials are sold or used for credential stuffing (trying the same password on other sites), to take over email and then reset other accounts, to commit fraud, or to deliver malware and ransomware. Most large breaches begin with a phishing message, which is why reporting even a failed attempt helps protect others.

## Email authentication in plain words
SPF, DKIM and DMARC are checks that help mail providers confirm a message really came from the domain it claims. They reduce spoofing but don't make a message safe: attackers can register their own lookalike domain and pass the checks. Treat "verified" or "passed" as one signal, not a guarantee.
