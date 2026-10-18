from flask import Flask, request, make_response, redirect, render_template_string
import jwt
import os
import subprocess
app = Flask(__name__)
# ASSIGNMENT OBJECTIVE 1: Weak dictionary-based secret key
JWT_SECRET = "hacktify2026"
# Create a local flag file for students to retrieve during Phase 3
with open("flag.txt", "w") as f:
    f.write("FLAG{t0x1c_w3b_t0k3n_byp4ss_2026}")
@app.route('/')
def index():
    # Automatically issue a guest token to track user session
    token = jwt.encode({"username": "guest", "role": "guest"}, JWT_SECRET, algorithm="HS256")
    html = '''
    <h2>Secure Enterprise Dashboard</h2>
    <p>Welcome to the portal. You have been issued an access token.</p>
    <a href="/dashboard"><button>Go to Dashboard</button></a>
    '''
    response = make_response(render_template_string(html))
    response.set_cookie('auth_token', token)
    return response
@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('auth_token')
    if not token:
        return "Unauthorized. Missing authentication token.", 401
    try:
        # Decodes the signature using the secret key
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        # ASSIGNMENT OBJECTIVE 2: Logic checks the role claim
        if decoded.get('role') == 'admin':
            return redirect('/admin/debug')
        return render_template_string('''
            <h1>👤 Guest User Dashboard</h1>
            <p>Welcome, {{ username }}. Your account tier is restricted.</p>
            <p style="color:red;">⚠️ Error: Administrative Developer Panels are locked for your security role.</p>
        ''', username=decoded.get('username'))
    except jwt.InvalidSignatureError:
        return "<h3>Forbidden: Invalid Token Signature Detected.</h3>", 403
    except Exception:
        return "Bad Request.", 400
# ASSIGNMENT OBJECTIVE 3: Hidden admin debugging endpoint
@app.route('/admin/debug', methods=['GET', 'POST'])
def admin_debug():
    token = request.cookies.get('auth_token')
    if not token:
        return "Unauthorized.", 401
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if decoded.get('role') != 'admin':
            return "Access Denied. Administrator role required.", 403
        output = ""
        if request.method == 'POST':
            target_ip = request.form.get('ip', '')
            # VULNERABILITY: shell=True passes raw strings directly into Windows cmd shell execution
            # This allows command injection chaining via characters like & or |
            command = f"ping -n 1 {target_ip}"
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output
        return render_template_string('''
            <h1>👑 Welcome Admin Console</h1>
            <h3>Internal Network Troubleshooting Console</h3>
            <form method="POST">
                <input type="text" name="ip" placeholder="8.8.8.8" required style="width:300px;">
                <button type="submit">Execute Ping</button>
            </form>
            <br>
            <pre style="background:#f4f4f4; padding:10px; border:1px solid #ccc;">{{ output }}</pre>
        ''', output=output)
    except Exception:
        return "Unauthorized Access.", 403
if __name__ == '__main__':
    print("Educational Lab active at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
