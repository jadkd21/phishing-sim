#!/usr/bin/env python3
"""
Phishing Simulation - security awareness training
A fake login page for a FICTIONAL company ("SecureMail").
Send the link to people who AGREED to be tested, see who takes
the bait, then the page itself teaches them what gave it away.

THE RULES (non-negotiable):
  1. Only test people who consented beforehand.
  2. Never impersonate a real company (no Gmail/Microsoft clones).
  3. This tool NEVER stores passwords - it only logs THAT someone
     submitted, then shows them what a real attacker would have taken.

How to run:
    pip install flask
    python app.py
    Share:  http://<your-ip>:5000/?id=mom   (one link per person)

    Find your IP with:  ipconfig   (look for IPv4 Address)
"""

from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
LOGFILE = "sim_results.log"

LOGIN_PAGE = """
<!doctype html><html><head><title>SecureMail - Sign in</title>
<style>
body{font-family:Arial,sans-serif;background:#f0f2f5;display:flex;
justify-content:center;align-items:center;height:100vh;margin:0}
.box{background:#fff;padding:40px;border-radius:8px;width:340px;
box-shadow:0 2px 10px rgba(0,0,0,.15);text-align:center}
h1{color:#1a73e8}input{width:100%;padding:10px;margin:8px 0;box-sizing:border-box}
button{background:#1a73e8;color:#fff;border:0;padding:10px;width:100%;
font-size:16px;border-radius:4px;cursor:pointer}
.warn{color:#b00;font-size:13px}
</style></head><body><div class="box">
<h1>SecureMail</h1>
<p class="warn">Urgent: unusual activity detected.<br>Verify your identity within 24 hours or your account will be locked.</p>
<form method="post" action="/submit">
<input type="hidden" name="participant" value="{{ participant }}">
<input name="username" placeholder="Email address" required>
<input name="password" type="password" placeholder="Password" required>
<button>Verify now</button>
</form></div></body></html>
"""

CAUGHT_PAGE = """
<!doctype html><html><head><title>Simulation complete</title>
<style>
body{font-family:Arial,sans-serif;background:#fff8e1;display:flex;
justify-content:center;align-items:center;min-height:100vh;margin:0}
.box{background:#fff;padding:40px;border-radius:8px;max-width:560px;
box-shadow:0 2px 10px rgba(0,0,0,.15)}
h1{color:#b00}li{margin:8px 0}
</style></head><body><div class="box">
<h1>Gotcha, {{ participant }}! This was a test.</h1>
<p>No harm done - <b>your password was NOT saved anywhere.</b>
A real attacker would now own your account. Here's what gave it away:</p>
<ul>
<li><b>Urgency:</b> "within 24 hours or locked" - fear makes you click first, think later.</li>
<li><b>The link:</b> it didn't go to a real SecureMail address. Always hover before you click.</li>
<li><b>Generic greeting:</b> real companies use your name, not "dear user" energy.</li>
<li><b>It asked for your password</b> out of nowhere, via an emailed link.</li>
</ul>
<p><b>The habit:</b> suspicious email? Don't click - open the real site yourself
and check there. This test was run by Jad with your permission, to keep you safe.</p>
</div></body></html>
"""


@app.route("/")
def login():
    participant = request.args.get("id", "friend")
    return render_template_string(LOGIN_PAGE, participant=participant)


@app.route("/submit", methods=["POST"])
def submit():
    participant = request.form.get("participant", "unknown")
    # The password is in request.form but we DELIBERATELY never store it.
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {participant} | {ip} | submitted (password NOT stored)\n")
    print(f"  [!] {participant} took the bait at {ts} (from {ip})", flush=True)
    return redirect(url_for("caught", id=participant))


@app.route("/caught")
def caught():
    participant = request.args.get("id", "friend")
    return render_template_string(CAUGHT_PAGE, participant=participant)


if __name__ == "__main__":
    print("=" * 60)
    print("  PHISHING SIMULATION - training only, consent required")
    print("  Results go to sim_results.log (passwords never stored)")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000)
