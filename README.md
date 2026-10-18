# Toxic Token: JWT Cracking to Authenticated RCE (Lab & Remediation)
An educational multi-stage security laboratory demonstrating how weak cryptographic signature handling collapses into full system compromise via an authenticated Remote Code Execution (RCE) vector. 
## 🌐 Project Architecture
- **Language:** Python 3.13+
- **Framework:** Flask, PyJWT
- **Attack Model:** Cryptographic Dictionary Attack -> Privilege Escalation -> OS Command Injection
---
## 🕵️ The Attack Chain
### Stage 1: Session Interception & Weak Key Recovery
The application uses the symmetric `HS256` algorithm with a weak dictionary-based secret key (`hacktify2026`). An attacker intercepts the user session cookie (`auth_token`) and cracks the signature hash offline.
### Stage 2: Token Forgery & Vertical Privilege Escalation
Using the cracked secret, the payload parameters are safely tampered with to change `"role": "guest"` to `"role": "admin"`. Re-injecting this forged token into browser storage successfully unlocks the hidden admin panel (`/admin/debug`).
### Stage 3: Authenticated Command Chaining & System RCE
The admin troubleshooting console pipes unfiltered strings into the host operating system shell wrapper (`shell=True`). Appending command separators chains background processes, allowing an attacker to read out files like `flag.txt`:
```text
FLAG{t0x1c_w3b_t0k3n_byp4ss_2026}
```
---
## 🛡️ Secure Remediation & Hardening Principles
The project includes a fully remediated implementation (`app_patched.py`) applying the following defense-in-depth security mitigations:
1. **Cryptographic Key Randomization:** Replaced static strings with high-entropy keys using `secrets.token_hex(32)`.
2. **Strict Input Sanitization:** Implemented a regular expression whitelist pattern (`r"^[a-zA-Z0-9.-]+$"`) to reject meta-characters.
3. **Parameter Isolation:** Stripped `shell=True` and passed input explicitly inside a command execution list argument array (`shell=False`).
---
## ⚙️ How to Run Locally
### 1. Install Dependencies
```bash
pip install Flask PyJWT
```
### 2. Run the Vulnerable Environment
```bash
python app_vulnerable.py
```
