# Authentication & MFA

## Authentication factors
- **Something you know** — password, PIN
- **Something you have** — phone, hardware key, authenticator app
- **Something you are** — fingerprint, face recognition

## Multi-factor authentication (MFA)
MFA requires two or more of the factors above. Even if your password is
stolen, an attacker can't log in without the second factor.

Preferred MFA methods, from strongest to weakest:
1. Hardware security keys (e.g., FIDO2/U2F)
2. Authenticator apps (TOTP codes)
3. Push notifications
4. SMS codes (better than nothing, but vulnerable to SIM-swap attacks)

## Session security
- Log out of shared or public computers.
- Review "recent activity"/"active sessions" on important accounts
  periodically and revoke anything you don't recognize.
- Be cautious of "MFA fatigue" attacks, where an attacker repeatedly
  triggers push notifications hoping you'll approve one by mistake —
  never approve a login you didn't initiate.
