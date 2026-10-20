# Security Glossary

## What is encryption?
Encryption scrambles data using a key so that only someone with the right key can read it. It protects messages, files, passwords in transit and stored data. Without the key, intercepted or stolen encrypted data looks like random noise. HTTPS, Wi-Fi security (WPA3), phone storage and messaging apps all rely on encryption.

## What is end-to-end encryption?
End-to-end encryption means only you and the person you're talking to can read a message. Even the company running the app can't see it, because the keys stay on the devices. It protects against eavesdropping on the network and against provider breaches, but not against someone who gets access to an unlocked phone or a backup that isn't encrypted.

## What is hashing?
Hashing turns data into a fixed-length fingerprint using a one-way function: you can't turn the fingerprint back into the original. Websites store password hashes instead of passwords, and file hashes are used to check a download wasn't altered. Good systems add a random "salt" to each password before hashing so identical passwords don't produce identical hashes.

## What is a hacker?
A hacker is someone who explores and manipulates computer systems. The word is used for different people. **White-hat** (ethical) hackers test systems with permission to fix weaknesses. **Black-hat** hackers break in for crime or harm. **Grey-hat** hackers sit in between, often finding flaws without permission but without criminal intent. Breaking into systems you don't have permission to test is illegal in most countries, even if you mean no harm.

## What is ethical hacking or penetration testing?
Penetration testing is authorised, planned hacking: a security professional tries to break into a system to find weaknesses before criminals do, then reports how to fix them. It requires written permission and a defined scope. Students can practise legally on purpose-built labs and capture-the-flag (CTF) games rather than on real websites or networks.

## What is a bug bounty?
A bug bounty is a programme where an organisation pays or rewards people who responsibly report security flaws in its systems. Researchers must follow the programme's rules and scope and report privately so the flaw can be fixed before it is public.

## What are cookies?
Cookies are small pieces of data a website stores in your browser. Session cookies keep you logged in and remember your cart. Tracking cookies, often from third parties, follow you across sites to build an advertising profile. If an attacker steals a session cookie they can sometimes take over your logged-in session, which is why you should log out on shared computers and keep your browser updated.

## What is the dark web?
The internet has three layers. The surface web is what search engines index. The deep web is everything behind logins or paywalls, like your email, bank and school portal, and it is completely normal. The dark web is a small part that needs special software such as Tor to reach. It has legitimate uses like privacy for journalists and activists, but also criminal markets where stolen data is sold. You don't need it for everyday safety, and it is risky to explore.

## What is a zero-day vulnerability?
A zero-day is a security flaw that the software maker doesn't know about yet or hasn't fixed, so there have been "zero days" to patch it. Attackers who find one can exploit it before any defence exists. You can't prevent zero-days, but you reduce the damage by updating promptly once a patch is released, using least privilege and keeping backups.

## What is a brute-force attack?
A brute-force attack tries many passwords or keys until one works. Attackers use software that can try millions of guesses. Long, unique passwords make it impractical, while rate limiting, account lockouts and multi-factor authentication stop it on websites.

## What is a DDoS attack?
A distributed denial-of-service (DDoS) attack floods a website or service with traffic from many devices, often a botnet of infected computers, so real users can't get in. It attacks availability rather than stealing data. Defences include traffic filtering, content delivery networks and extra capacity.

## What is a backdoor?
A backdoor is a hidden way to get into a system while bypassing normal login. Attackers install one after breaking in so they can return later, and some malware includes one. Regular updates, security scans and removing unknown accounts or remote-access tools help find and close backdoors.

## What is an exploit?
An exploit is code or a method that takes advantage of a vulnerability to do something the software wasn't meant to do, such as running malicious code. The vulnerability is the weakness, the exploit is the tool that uses it, and a patch is the fix.

## What is an IP address?
An IP address is the number that identifies a device on a network, like a postal address for data. Your home has a public IP address assigned by your internet provider, and devices inside have private ones. Websites see your public IP, which can reveal your rough location, and a VPN replaces it with the VPN's address.

## What is DNS?
The Domain Name System turns names like example.com into the IP addresses computers use, like a phone book for the internet. Attackers can try to tamper with it (DNS spoofing or pharming) to send you to a fake site, which is why you should check the address and the connection and use a trusted DNS provider.

## What is TLS and what is a digital certificate?
TLS (the successor to SSL) is the technology behind HTTPS that encrypts traffic between your browser and a website. A digital certificate is a file that proves a website's identity and holds its public key, issued by a trusted certificate authority. A valid certificate means the connection is encrypted and tied to that domain. It doesn't prove the site is trustworthy.

## What is a proxy server?
A proxy server sits between you and the internet and passes your requests along, so websites see the proxy's address instead of yours. Organisations use proxies to filter and log traffic. Free public proxies are risky because the operator can read and alter what passes through.

## What is a sandbox?
A sandbox is an isolated environment where a program can run without being able to affect the rest of the system. Browsers, phones and security researchers use sandboxes so that suspicious files can be examined or run without harming the real device.

## What is a honeypot?
A honeypot is a decoy system set up to look valuable so attackers waste time on it. Defenders watch what attackers do there to learn their methods and to detect intrusions early. Nothing real is stored on it.

## What is a digital signature?
A digital signature uses cryptography to prove who created a message or file and that it hasn't been changed since. It's used to sign software updates, documents and emails. If a single character is altered, the signature stops verifying.

## What is biometric authentication?
Biometrics use something about your body, such as a fingerprint, face or iris, to unlock a device or account. They're convenient and hard to guess, but you can't change a fingerprint if it leaks, so they work best as a convenience on top of a PIN or as one factor in multi-factor authentication.

## What is spam?
Spam is unwanted bulk messages, usually advertising but often scams or phishing. Don't reply, click links or "unsubscribe" in suspicious messages, since that confirms your address is active. Mark them as spam so your email provider learns to filter them.

## What is OSINT?
Open-source intelligence (OSINT) means gathering information from public sources such as social media, websites and public records. Security professionals use it legitimately, and attackers use it to prepare convincing scams. Reducing what you share publicly makes you a harder target.
