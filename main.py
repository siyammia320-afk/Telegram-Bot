from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import time
import threading
import re
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ==================== কনফিগারেশন ====================
BASE_URL = "https://mknetworkbd.com"
LOGIN_EMAIL = "marcomax962@gmail.com"
LOGIN_PASSWORD = "Ashik515385"
SESSION = requests.Session()
LOGGED_IN = False

def mk_login():
    global LOGGED_IN, SESSION
    login_url = f"{BASE_URL}/login.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"login_id": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    try:
        response = SESSION.post(login_url, headers=headers, data=data, timeout=15)
        if response.status_code == 302 or "index.php" in response.text:
            LOGGED_IN = True
            print("✅ MKNetwork Login Success!")
            return True
    except Exception as e:
        print(f"Login Failed: {e}")
    return False

# ==================== রেঞ্জ ফাংশন ====================
def get_live_ranges():
    if not LOGGED_IN:
        mk_login()
    try:
        response = SESSION.get(f"{BASE_URL}/console.php?ajax=1", timeout=15)
        if response.status_code == 200:
            data = response.json()
            feed = data.get("feed", [])
            ranges = []
            for item in feed:
                service_name = item.get("service_name", "")
                rng = item.get("range")
                if rng and service_name.lower() in ["facebook", "instagram"]:
                    full_name = "Facebook" if service_name.lower() == "facebook" else "Instagram"
                    ranges.append({
                        "range": str(rng).upper().strip(),
                        "service": full_name
                    })
            return ranges
    except Exception as e:
        print(f"Ranges error: {e}")
    return []

def fetch_number(range_code):
    if not LOGGED_IN:
        mk_login()
    url = f"{BASE_URL}/API/api_handler_test.php"
    boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": f"multipart/form-data; boundary={boundary}"}
    body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\nget_number\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"range\"\r\n\r\n{range_code}\r\n--{boundary}--\r\n"
    try:
        response = SESSION.post(url, headers=headers, data=body, timeout=15)
        if response.status_code == 200:
            data = response.json()
            number = data.get("number", "")
            if number:
                return str(number).replace("+", "").strip()
    except Exception as e:
        print(f"Fetch error: {e}")
    return None

def check_otp_for_number(phone):
    if not LOGGED_IN:
        mk_login()
    try:
        response = SESSION.get(f"{BASE_URL}/API/api_handler_test.php?action=get_history&filter=all&page=1&limit=50", timeout=15)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("data", []):
                if item.get("phone_number") == phone and item.get("status") == "success":
                    full_msg = item.get("full_sms_list", "")
                    if full_msg:
                        otp_match = re.search(r'\d{4,8}', full_msg)
                        if otp_match:
                            return otp_match.group()
    except Exception as e:
        print(f"OTP error: {e}")
    return None

# ==================== ডাটাবেস ====================
NUMBERS_FILE = "active_numbers.json"

def load_numbers():
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_numbers(numbers):
    with open(NUMBERS_FILE, "w") as f:
        json.dump(numbers, f)

# ==================== API রাউট ====================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get_ranges')
def get_ranges():
    ranges = get_live_ranges()
    return jsonify(ranges)

@app.route('/api/get_number', methods=['POST'])
def get_number():
    data = request.json
    range_code = data.get('range')
    number = fetch_number(range_code)
    if number:
        active = load_numbers()
        active.append({
            "phone": number,
            "range": range_code,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "otp": None,
            "status": "waiting"
        })
        save_numbers(active)
        return jsonify({"success": True, "number": number})
    return jsonify({"success": False, "error": "No number available"})

@app.route('/api/active_numbers')
def get_active():
    active = load_numbers()
    for i, num in enumerate(active):
        if not num.get("otp"):
            otp = check_otp_for_number(num["phone"])
            if otp:
                active[i]["otp"] = otp
                active[i]["status"] = "completed"
                save_numbers(active)
    return jsonify(active)

# ==================== HTML টেমপ্লেট ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>ARAFAT OTP</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0f1e;
            font-family: 'Segoe UI', -apple-system, sans-serif;
            min-height: 100vh;
            padding: 16px;
        }
        .container { max-width: 550px; margin: 0 auto; }
        
        .header {
            background: linear-gradient(135deg, #1e2a47, #0f172a);
            border-radius: 28px;
            padding: 16px 20px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #3b4b77;
        }
        .header h1 { font-size: 1.3rem; color: #3b82f6; }
        .menu-btn {
            background: #1e2a47;
            border: none;
            font-size: 1.6rem;
            cursor: pointer;
            padding: 4px 12px;
            border-radius: 30px;
            color: white;
        }
        
        .menu-panel {
            display: none;
            background: #0f1422;
            border-radius: 24px;
            padding: 12px;
            margin-bottom: 16px;
            border: 1px solid #2a3550;
        }
        .menu-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .menu-btn-item {
            background: #1e2a47;
            border: 1px solid #3b4b77;
            padding: 8px 18px;
            border-radius: 30px;
            color: white;
            cursor: pointer;
            font-weight: bold;
            font-size: 13px;
        }
        
        .card {
            background: #0f1422;
            border-radius: 24px;
            padding: 16px;
            margin-bottom: 16px;
            border: 1px solid #2a3550;
        }
        .card h2 {
            color: #b9d0ff;
            font-size: 1rem;
            margin-bottom: 12px;
            border-left: 3px solid #3b82f6;
            padding-left: 10px;
        }
        
        .range-list {
            max-height: 400px;
            overflow-y: auto;
        }
        .range-item {
            background: #111827;
            border-radius: 12px;
            padding: 10px 12px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .range-info {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .range-code {
            font-family: monospace;
            font-size: 14px;
            font-weight: bold;
            color: #3b82f6;
            background: #0a0f1e;
            padding: 4px 10px;
            border-radius: 20px;
        }
        .range-service {
            background: #1e2a47;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            color: #8aa3d0;
        }
        .copy-btn {
            background: #2a3550;
            border: none;
            padding: 5px 12px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-size: 11px;
        }
        .copy-btn:active { background: #3b82f6; }
        
        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            color: #b9d0ff;
            font-size: 12px;
            display: block;
            margin-bottom: 6px;
        }
        .input-group input {
            width: 100%;
            background: #111827;
            border: 1px solid #2a3550;
            padding: 12px;
            border-radius: 16px;
            color: white;
            font-family: monospace;
            font-size: 14px;
        }
        .get-number-btn {
            background: #3b82f6;
            border: none;
            padding: 12px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            width: 100%;
            cursor: pointer;
            font-size: 14px;
        }
        
        .numbers-list {
            max-height: 350px;
            overflow-y: auto;
            margin-top: 15px;
        }
        .number-card {
            background: #111827;
            border-radius: 14px;
            padding: 12px;
            margin-bottom: 8px;
            border-left: 3px solid #3b82f6;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }
        .number-phone {
            font-family: monospace;
            font-size: 15px;
            font-weight: bold;
            color: white;
        }
        .number-time {
            font-size: 9px;
            color: #6b7280;
            margin-top: 3px;
        }
        .number-status {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .otp-code {
            background: #10b981;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
            font-family: monospace;
        }
        .waiting {
            background: #f59e0b;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
        }
        .num-copy-btn {
            background: #2a3550;
            border: none;
            padding: 5px 12px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-size: 11px;
        }
        .empty {
            text-align: center;
            padding: 20px;
            color: #6b7280;
        }
        
        .toast {
            position: fixed;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: #1f2937;
            color: white;
            padding: 10px;
            border-radius: 12px;
            text-align: center;
            display: none;
            z-index: 1000;
            font-size: 13px;
        }
        
        .hidden { display: none; }
        
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #0f1422; }
        ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 ARAFAT OTP</h1>
            <button class="menu-btn" onclick="toggleMenu()">☰</button>
        </div>
        
        <div id="menuPanel" class="menu-panel">
            <div class="menu-buttons">
                <button class="menu-btn-item" onclick="showConsole()">📡 Console</button>
                <button class="menu-btn-item" onclick="showGetNumber()">📞 GET NUMBER</button>
            </div>
        </div>
        
        <!-- Console Section -->
        <div id="consoleSection" class="card">
            <h2>📡 Live Ranges (Auto Refresh 2s)</h2>
            <div id="rangeList" class="range-list">
                <div class="empty">Loading ranges...</div>
            </div>
        </div>
        
        <!-- GET NUMBER Section -->
        <div id="getNumberSection" class="card hidden">
            <h2>📞 GET NUMBER</h2>
            <div class="input-group">
                <label>📌 Enter Range Code</label>
                <input type="text" id="rangeInput" placeholder="Enter range code...">
            </div>
            <button class="get-number-btn" onclick="getNumber()">🚀 GET NUMBER</button>
            
            <!-- Numbers List -->
            <div id="numbersList" class="numbers-list">
                <div class="empty">No numbers yet. Get a number!</div>
            </div>
        </div>
    </div>
    
    <div id="toast" class="toast"></div>
    
    <script>
        let activeNumbers = [];
        
        // Load saved range from localStorage when page loads
        function loadSavedRange() {
            const savedRange = localStorage.getItem('saved_range');
            if(savedRange) {
                document.getElementById('rangeInput').value = savedRange;
            }
        }
        
        // Save range to localStorage when user types
        function saveRange() {
            const range = document.getElementById('rangeInput').value;
            localStorage.setItem('saved_range', range);
        }
        
        function toggleMenu() {
            const menu = document.getElementById('menuPanel');
            menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
        }
        
        function showConsole() {
            document.getElementById('consoleSection').classList.remove('hidden');
            document.getElementById('getNumberSection').classList.add('hidden');
            document.getElementById('menuPanel').style.display = 'none';
            loadRanges();
        }
        
        function showGetNumber() {
            document.getElementById('consoleSection').classList.add('hidden');
            document.getElementById('getNumberSection').classList.remove('hidden');
            document.getElementById('menuPanel').style.display = 'none';
            loadActiveNumbers();
            loadSavedRange();  // Load saved range when opening GET NUMBER
        }
        
        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 2000);
        }
        
        // Load Live Ranges
        async function loadRanges() {
            try {
                const res = await fetch('/api/get_ranges');
                const ranges = await res.json();
                const container = document.getElementById('rangeList');
                if(ranges.length === 0) {
                    container.innerHTML = '<div class="empty">No ranges available</div>';
                    return;
                }
                container.innerHTML = ranges.map(r => `
                    <div class="range-item">
                        <div class="range-info">
                            <span class="range-code">📡 ${r.range}</span>
                            <span class="range-service">${r.service}</span>
                        </div>
                        <button class="copy-btn" onclick="copyRange('${r.range}')">📋 Copy</button>
                    </div>
                `).join('');
            } catch(e) {
                console.log(e);
            }
        }
        
        // Copy range (only copy, does NOT change GET NUMBER input)
        function copyRange(range) {
            navigator.clipboard.writeText(range);
            showToast(`✅ Copied: ${range}`);
        }
        
        // Get Number
        async function getNumber() {
            const range = document.getElementById('rangeInput').value.trim();
            if(!range) {
                showToast('❌ Please enter a range code!');
                return;
            }
            
            showToast(`⏳ Getting number from ${range}...`);
            
            const res = await fetch('/api/get_number', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ range: range })
            });
            const data = await res.json();
            
            if(data.success) {
                showToast(`✅ Got number: ${data.number}`);
                loadActiveNumbers();
            } else {
                showToast(`❌ ${data.error}`);
            }
        }
        
        // Load Active Numbers
        async function loadActiveNumbers() {
            const res = await fetch('/api/active_numbers');
            activeNumbers = await res.json();
            const container = document.getElementById('numbersList');
            
            if(activeNumbers.length === 0) {
                container.innerHTML = '<div class="empty">No numbers yet. Get a number!</div>';
                return;
            }
            
            container.innerHTML = activeNumbers.map(num => `
                <div class="number-card">
                    <div>
                        <div class="number-phone">📱 ${num.phone}</div>
                        <div class="number-time">🕐 ${num.time}</div>
                    </div>
                    <div class="number-status">
                        ${num.otp ? 
                            `<div class="otp-code">🔐 ${num.otp}</div>` : 
                            `<div class="waiting">⏳ Waiting for OTP...</div>`
                        }
                        <button class="num-copy-btn" onclick="copyNumber('${num.phone}')">📋 Copy</button>
                    </div>
                </div>
            `).join('');
        }
        
        function copyNumber(phone) {
            navigator.clipboard.writeText(phone);
            showToast(`✅ Copied: ${phone}`);
        }
        
        // Auto refresh ranges every 2 seconds (only when console visible)
        setInterval(() => {
            if(document.getElementById('consoleSection') && 
               !document.getElementById('consoleSection').classList.contains('hidden')) {
                loadRanges();
            }
        }, 2000);
        
        // Auto refresh active numbers every 5 seconds (only when get number visible)
        setInterval(() => {
            if(document.getElementById('getNumberSection') && 
               !document.getElementById('getNumberSection').classList.contains('hidden')) {
                loadActiveNumbers();
            }
        }, 5000);
        
        // Event listener for range input to save to localStorage
        const rangeInput = document.getElementById('rangeInput');
        rangeInput.addEventListener('input', saveRange);
        
        // Initial load
        loadRanges();
        loadSavedRange();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("=" * 55)
    print("🎯 ARAFAT OTP WebApp")
    print("=" * 55)
    print("🌐 Open: http://localhost:5000")
    print("=" * 55)
    print("📡 Console: রেঞ্জ দেখাবে + কপি বাটন")
    print("📞 GET NUMBER: যা বসাবেন সেটাই সেভ থাকবে")
    print("📱 নাম্বার আসলে দেখাবে + OTP স্ট্যাটাস")
    print("=" * 55)
    mk_login()
    app.run(host='0.0.0.0', port=5000, debug=True)
