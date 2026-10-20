# Cybersecurity Basics

## What is cybersecurity?
Cybersecurity is the practice of protecting devices, accounts, networks and data from attack, damage or unauthorised access. It combines technology (updates, encryption, backups), processes (how to report and respond) and people (habits like spotting phishing). Because attackers target people as much as software, good habits matter as much as good tools.

## What is the CIA triad?
The core goals of security are **Confidentiality** (only authorised people can see the data), **Integrity** (the data stays accurate and unaltered) and **Availability** (systems and data are accessible when needed). Different attacks hit different goals: a data leak breaks confidentiality, tampering with grades breaks integrity and ransomware or a DDoS attack breaks availability.

## Threat, vulnerability and risk
A **threat** is something that could cause harm, such as a criminal or malware. A **vulnerability** is a weakness it can use, such as an unpatched app or a reused password. **Risk** is the chance of harm combined with how bad it would be. You reduce risk by removing vulnerabilities, blocking threats and limiting the damage if something goes wrong.

## Who are the attackers?
- **Cybercriminals:** motivated by money, using phishing, fraud and ransomware.
- **Opportunists and script kiddies:** use ready-made tools, often for notoriety.
- **Insiders:** people with legitimate access who misuse it, deliberately or by accident.
- **Hacktivists:** driven by political or social causes.
- **State-sponsored groups:** well-funded groups focused on espionage or disruption.
Most everyday attacks on students are financially motivated and automated, not personal.

## What are the core security principles?
**Defense in depth:** use several layers so one failure isn't fatal. **Least privilege:** give people and apps only the access they need. **Secure by default:** safe settings should be on from the start. **Keep it updated:** patches fix known vulnerabilities. **Assume breach:** plan for recovery with backups and an incident plan. **Verify, don't trust:** confirm identity before acting on requests.

## What basic habits keep me safe?
1. Use a unique, long password for every account, ideally with a password manager.
2. Turn on multi-factor authentication, starting with email.
3. Install updates promptly on every device and app.
4. Back up important files, with one copy offline.
5. Think before you click links or open attachments.
6. Install apps only from official sources.
7. Lock your devices with a PIN or biometric.
8. Share less personal information online.
9. Report problems early.

## How do I back up my files?
Follow the 3-2-1 rule: keep 3 copies of important files, on 2 different types of storage (for example your laptop plus an external drive or cloud storage), with 1 copy offline or off-site so ransomware or theft can't reach it. Use automatic backup (File History or Time Machine, or a trusted cloud service), encrypt backups that hold personal data, and occasionally restore a file to prove the backup works. Back up before you reset or repair a device. A backup is your best protection against ransomware, hardware failure, theft and accidents.

## Do I need antivirus, and which one should I use?
Most people are well served by the antivirus built into their operating system, such as Microsoft Defender on Windows, as long as it is switched on and kept updated. There is no single "best" product, and paid suites aren't always better. Whatever you use, install it from the official source, keep automatic updates on, and ignore pop-ups that claim your device is infected and push you to buy "protection": fake antivirus is a common scam. Antivirus is one layer; updates, backups and careful clicking matter just as much.

## What are common web application attacks?
- **SQL injection:** sending database commands through an input box to read or change data. Prevented by parameterised queries.
- **Cross-site scripting (XSS):** getting a site to run an attacker's script in other users' browsers. Prevented by escaping output.
- **Cross-site request forgery (CSRF):** tricking a logged-in user's browser into sending an unwanted request. Prevented with CSRF tokens.
- **Brute force and credential stuffing:** repeated login guesses. Prevented with rate limits and MFA.
- **Insecure direct object reference (IDOR):** changing an ID in a URL to see someone else's data. Prevented by checking ownership on every request.
- **Zero-day:** an attack on a vulnerability that has no patch yet.

## Cybersecurity glossary
- **Encryption:** scrambling data so only someone with the key can read it.
- **Hashing:** a one-way transformation used to store passwords safely.
- **Patch:** an update that fixes a security flaw.
- **Exploit:** code or a technique that uses a vulnerability.
- **Payload:** the harmful part of an attack.
- **Botnet:** a network of infected devices controlled by an attacker.
- **Firewall:** a filter for network traffic.
- **VPN:** an encrypted tunnel for your traffic.
- **MFA/2FA:** more than one proof of identity at login.
- **Antivirus/EDR:** software that detects and blocks malicious activity.
- **Data breach:** unauthorised exposure of data.
- **Social engineering:** manipulating people to gain access.
