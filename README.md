# Phishing Simulation

A security-awareness training tool: a fake login page for a fictional
company, a tracker for who takes the bait, and a debrief page that
teaches them what gave it away.

## The rules

1. **Consent first.** Only test people who agreed beforehand. Surprising
   someone with a phish they didn't sign up for is just phishing.
2. **Fictional company only.** The page pretends to be "SecureMail", which
   doesn't exist. Never clone Gmail, Microsoft, or any real brand.
3. **No password storage.** The app logs THAT someone submitted — never
   the password itself. The debrief page tells them so.

## How to run

1. `pip install flask`
2. `python app.py`
3. Find your IP: `ipconfig` (IPv4 Address, e.g. 192.168.1.50)
4. Give each willing participant their own link:
   `http://192.168.1.50:5000/?id=mom`
5. They must be on your Wi-Fi (or you port-forward — skip that for now)
6. Watch results land in `sim_results.log`, then discuss the debrief

## Email template (send from YOUR address)

> Subject: Action required: verify your SecureMail account
>
> Hi,
>
> We detected unusual sign-in activity on your SecureMail account.
> Please verify your identity within 24 hours or your account will
> be locked: http://192.168.1.50:5000/?id=mom
>
> — SecureMail Security Team

## What I learned

- How phishing actually works end to end: lure, fake page, credential
  capture — and why the debrief matters more than the trick
- The red flags: urgency, generic greetings, emailed links asking for
  passwords, mismatched URLs
- Flask routing, forms, and redirects
- Ethics in security: consent, no real brands, no password storage —
  the same rules professional red teams follow
- Why companies run these simulations on their own employees

## Note

This is a training tool for willing participants on your own network.
Sending deceptive emails to people who didn't agree is phishing,
full stop — regardless of intent.
