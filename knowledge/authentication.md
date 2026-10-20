# Authentication

## What is multi-factor authentication (MFA)?
MFA, also called 2FA or two-step verification, asks for more than one proof of identity when you log in. The factors are something you know (a password or PIN), something you have (a phone, security key or authenticator app) and something you are (a fingerprint or face). A stolen password alone is then not enough to get into your account. Turning on MFA blocks the large majority of automated account takeovers, so it is one of the best security steps you can take.

## Which MFA methods are strongest?
From weakest to strongest: SMS codes, then authenticator app codes, then app push approvals with number matching, then passkeys and hardware security keys (FIDO2). Any MFA is far better than none. SMS can be intercepted through SIM swapping and fake login pages can trick you into typing codes, while passkeys and hardware keys are resistant to phishing because they only work on the genuine website.

## What is an authenticator app?
An authenticator app (such as Google Authenticator, Microsoft Authenticator or an open-source alternative) generates a six-digit code that changes about every 30 seconds. It works without mobile signal and isn't exposed to SIM swapping. When you set one up, you scan a QR code. Save the backup codes the service shows you, and move the app carefully when you change phones, or you may lock yourself out.

## What is MFA fatigue or prompt bombing?
Attackers who already have your password may trigger a flood of approval requests, hoping you'll tap "Approve" just to make them stop, or they may call pretending to be IT and ask you to approve. Never approve a request you didn't start. If you get unexpected prompts, deny them, change your password immediately and report it. Number-matching prompts and passkeys reduce this risk.

## What is SIM swapping?
In a SIM swap, a criminal persuades your mobile carrier to move your number onto their SIM, then receives your SMS codes and calls. To reduce the risk, set a PIN or lock on your carrier account, avoid SMS for important accounts where an app or key is available, and don't publish your phone number widely.

## Authentication vs authorization
Authentication proves who you are (logging in). Authorization decides what you are allowed to do once you're in (reading a file, editing a grade, accessing an admin page). Both are needed: a system that checks identity but not permissions might let any logged-in user see other users' data. In this app, for example, every query is filtered by the logged-in user so students can only see their own chats and reports.

## What are recovery codes and why keep them?
Recovery codes are one-time backup codes that let you back into an account if you lose your MFA device. Store them offline or in your password manager, not on the same phone. Review your account's recovery email and phone number, because an attacker who controls those can reset your account.

## Safe login habits
Log out of shared or public computers and don't tick "remember me" there. Be careful with "Sign in with Google/Microsoft/Facebook" prompts and with apps asking permission to read your mail or files, since fake permission requests are a common trick. Review which apps have access to your accounts and remove ones you don't use. Use a lock screen PIN or biometric on every device.
