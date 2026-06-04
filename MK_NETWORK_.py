import requests
import time
import threading
import re
import json
import os
import random
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ==================== কনফিগারেশন ====================
TELEGRAM_TOKEN = "8538833986:AAFcs3oH8BeUJ611gO3BKbPPCaKGbj_oops"
ADMIN_ID = 8509030775

BASE_URL = "https://mknetworkbd.com"
LOG_GROUP_ID = "-1003946237797"
OTP_GROUP_URL = "https://t.me/otpgroup_777"

# ==================== কান্ট্রি ফ্ল্যাগ এবং কোড ম্যাপ ====================
COUNTRY_FLAGS = {
    "Andorra": "🇦🇩", "United Arab Emirates": "🇦🇪", "Afghanistan": "🇦🇫", "Antigua and Barbuda": "🇦🇬",
    "Anguilla": "🇦🇮", "Albania": "🇦🇱", "Armenia": "🇦🇲", "Angola": "🇦🇴", "Antarctica": "🇦🇶",
    "Argentina": "🇦🇷", "American Samoa": "🇦🇸", "Austria": "🇦🇹", "Australia": "🇦🇺", "Aruba": "🇦🇼",
    "Aland Islands": "🇦🇽", "Azerbaijan": "🇦🇿", "Bosnia and Herzegovina": "🇧🇦", "Barbados": "🇧🇧",
    "Bangladesh": "🇧🇩", "Belgium": "🇧🇪", "Burkina Faso": "🇧🇫", "Bulgaria": "🇧🇬", "Bahrain": "🇧🇭",
    "Burundi": "🇧🇮", "Benin": "🇧🇯", "Saint Barthelemy": "🇧🇱", "Bermuda": "🇧🇲", "Brunei Darussalam": "🇧🇳",
    "Bolivia": "🇧🇴", "Bonaire": "🇧🇶", "Brazil": "🇧🇷", "Bahamas": "🇧🇸", "Bhutan": "🇧🇹",
    "Bouvet Island": "🇧🇻", "Botswana": "🇧🇼", "Belarus": "🇧🇾", "Belize": "🇧🇿", "Canada": "🇨🇦",
    "Cocos Islands": "🇨🇨", "Congo": "🇨🇩", "Central African Republic": "🇨🇫", "Congo Republic": "🇨🇬",
    "Switzerland": "🇨🇭", "Cote d'Ivoire": "🇨🇮", "Ivory Coast": "🇨🇮", "Cook Islands": "🇨🇰", "Chile": "🇨🇱",
    "Cameroon": "🇨🇲", "China": "🇨🇳", "Colombia": "🇨🇴", "Costa Rica": "🇨🇷", "Cuba": "🇨🇺",
    "Cape Verde": "🇨🇻", "Curacao": "🇨🇼", "Christmas Island": "🇨🇽", "Cyprus": "🇨🇾", "Czech Republic": "🇨🇿",
    "Germany": "🇩🇪", "Djibouti": "🇩🇯", "Denmark": "🇩🇰", "Dominica": "🇩🇲", "Dominican Republic": "🇩🇴",
    "Algeria": "🇩🇿", "Ecuador": "🇪🇨", "Estonia": "🇪🇪", "Egypt": "🇪🇬", "Western Sahara": "🇪🇭",
    "Eritrea": "🇪🇷", "Spain": "🇪🇸", "Ethiopia": "🇪🇹", "Finland": "🇫🇮", "Fiji": "🇫🇯",
    "Falkland Islands": "🇫🇰", "Micronesia": "🇫🇲", "Faroe Islands": "🇫🇴", "France": "🇫🇷", "Gabon": "🇬🇦",
    "United Kingdom": "🇬🇧", "Grenada": "🇬🇩", "Georgia": "🇬🇪", "French Guiana": "🇬🇫", "Guernsey": "🇬🇬",
    "Ghana": "🇬🇭", "Gibraltar": "🇬🇮", "Greenland": "🇬🇱", "Gambia": "🇬🇲", "Guinea": "🇬🇳",
    "Guadeloupe": "🇬🇵", "Equatorial Guinea": "🇬🇶", "Greece": "🇬🇷", "South Georgia": "🇬🇸", "Guatemala": "🇬🇹",
    "Guam": "🇬🇺", "Guinea-Bissau": "🇬🇼", "Guyana": "🇬🇾", "Hong Kong": "🇭🇰", "Heard Island": "🇭🇲",
    "Honduras": "🇭🇳", "Croatia": "🇭🇷", "Haiti": "🇭🇹", "Hungary": "🇭🇺", "Indonesia": "🇮🇩",
    "Ireland": "🇮🇪", "Israel": "🇮🇱", "Isle of Man": "🇮🇲", "India": "🇮🇳", "British Indian Ocean Territory": "🇮🇴",
    "Iraq": "🇮🇶", "Iran": "🇮🇷", "Iceland": "🇮🇸", "Italy": "🇮🇹", "Jersey": "🇯🇪", "Jamaica": "🇯🇲",
    "Jordan": "🇯🇴", "Japan": "🇯🇵", "Kenya": "🇰🇪", "Kyrgyzstan": "🇰🇬", "Cambodia": "🇰🇭",
    "Kiribati": "🇰🇮", "Comoros": "🇰🇲", "Saint Kitts and Nevis": "🇰🇳", "North Korea": "🇰🇵",
    "South Korea": "🇰🇷", "Kuwait": "🇰🇼", "Cayman Islands": "🇰🇾", "Kazakhstan": "🇰🇿",
    "Laos": "🇱🇦", "Lebanon": "🇱🇧", "Saint Lucia": "🇱🇨", "Liechtenstein": "🇱🇮", "Sri Lanka": "🇱🇰",
    "Liberia": "🇱🇷", "Lesotho": "🇱🇸", "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺", "Latvia": "🇱🇻",
    "Libya": "🇱🇾", "Morocco": "🇲🇦", "Monaco": "🇲🇨", "Moldova": "🇲🇩", "Montenegro": "🇲🇪",
    "Saint Martin": "🇲🇫", "Madagascar": "🇲🇬", "Marshall Islands": "🇲🇭", "North Macedonia": "🇲🇰",
    "Mali": "🇲🇱", "Myanmar": "🇲🇲", "Mongolia": "🇲🇳", "Macao": "🇲🇴", "Northern Mariana Islands": "🇲🇵",
    "Martinique": "🇲🇶", "Mauritania": "🇲🇷", "Montserrat": "🇲🇸", "Malta": "🇲🇹", "Mauritius": "🇲🇺",
    "Maldives": "🇲🇻", "Malawi": "🇲🇼", "Mexico": "🇲🇽", "Malaysia": "🇲🇾", "Mozambique": "🇲🇿",
    "Namibia": "🇳🇦", "New Caledonia": "🇳🇨", "Niger": "🇳🇪", "Norfolk Island": "🇳🇫", "Nigeria": "🇳🇬",
    "Nicaragua": "🇳🇮", "Netherlands": "🇳🇱", "Norway": "🇳🇴", "Nepal": "🇳🇵", "Nauru": "🇳🇷",
    "Niue": "🇳🇺", "New Zealand": "🇳🇿", "Oman": "🇴🇲", "Panama": "🇵🇦", "Peru": "🇵🇪",
    "French Polynesia": "🇵🇫", "Papua New Guinea": "🇵🇬", "Philippines": "🇵🇭", "Pakistan": "🇵🇰",
    "Poland": "🇵🇱", "Saint Pierre and Miquelon": "🇵🇲", "Pitcairn": "🇵🇳", "Puerto Rico": "🇵🇷",
    "Palestine": "🇵🇸", "Portugal": "🇵🇹", "Palau": "🇵🇼", "Paraguay": "🇵🇾", "Qatar": "🇶🇦",
    "Reunion": "🇷🇪", "Romania": "🇷🇴", "Serbia": "🇷🇸", "Russia": "🇷🇺", "Rwanda": "🇷🇼",
    "Saudi Arabia": "🇸🇦", "Solomon Islands": "🇸🇧", "Seychelles": "🇸🇨", "Sudan": "🇸🇩", "Sweden": "🇸🇪",
    "Singapore": "🇸🇬", "Saint Helena": "🇸🇭", "Slovenia": "🇸🇮", "Svalbard and Jan Mayen": "🇸🇯",
    "Slovakia": "🇸🇰", "Sierra Leone": "🇸🇱", "San Marino": "🇸🇲", "Senegal": "🇸🇳", "Somalia": "🇸🇴",
    "Suriname": "🇸🇷", "South Sudan": "🇸🇸", "Sao Tome and Principe": "🇸🇹", "El Salvador": "🇸🇻",
    "Sint Maarten": "🇸🇽", "Syria": "🇸🇾", "Eswatini": "🇸🇿", "Turks and Caicos Islands": "🇹🇨",
    "Chad": "🇹🇩", "French Southern Territories": "🇹🇫", "Togo": "🇹🇬", "Thailand": "🇹🇭",
    "Tajikistan": "🇹🇯", "Tokelau": "🇹🇰", "Timor-Leste": "🇹🇱", "Turkmenistan": "🇹🇲",
    "Tunisia": "🇹🇳", "Tonga": "🇹🇴", "Turkey": "🇹🇷", "Trinidad and Tobago": "🇹🇹",
    "Tuvalu": "🇹🇻", "Taiwan": "🇹🇼", "Tanzania": "🇹🇿", "Ukraine": "🇺🇦", "Uganda": "🇺🇬",
    "United States": "🇺🇸", "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿", "Vatican City": "🇻🇦",
    "Saint Vincent and the Grenadines": "🇻🇨", "Venezuela": "🇻🇪", "Virgin Islands British": "🇻🇬",
    "Virgin Islands US": "🇻🇮", "Vietnam": "🇻🇳", "Vanuatu": "🇻🇺", "Wallis and Futuna": "🇼🇫",
    "Samoa": "🇼🇸", "Yemen": "🇾🇪", "Mayotte": "🇾🇹", "South Africa": "🇿🇦", "Zambia": "🇿🇲",
    "Zimbabwe": "🇿🇼"
}

COUNTRY_SHORT = {
    "Cote d'Ivoire": "CI", "Ivory Coast": "CI",
    "Togo": "TG", "Sierra Leone": "SL",
    "Bangladesh": "BD", "Cameroon": "CM",
    "India": "IN", "Pakistan": "PK",
    "United Kingdom": "UK", "United States": "US",
    "Canada": "CA", "France": "FR", "Germany": "DE",
    "Unknown": "XX"
}

COUNTRY_CODES = {
    "225": "Cote d'Ivoire", "228": "Togo", "232": "Sierra Leone",
    "880": "Bangladesh", "237": "Cameroon", "91": "India", "92": "Pakistan",
    "44": "United Kingdom", "1": "United States"
}

# ==================== MKNetworkBD লগইন ====================
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
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/login.php",
        "x-requested-with": "mark.via.gp"
    }
    data = {
        "login_id": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    }
    
    try:
        response = SESSION.post(login_url, headers=headers, data=data, timeout=15)
        if response.status_code == 302 or "index.php" in response.text:
            LOGGED_IN = True
            print("✅ Login Success!")
            return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
    return False

# ==================== OTP এক্সট্রাক্ট ফাংশন (ইমপ্রুভড) ====================
def extract_otp_from_text(text):
    """
    ফুল SMS টেক্সট থেকে OTP বের করে
    উদাহরণ:
    "confirm code 283 283" -> "283283"
    "confirm code 82739" -> "82739"
    "828-828" -> "828828"
    "82729382" -> "82729382"
    """
    text = str(text)
    
    # প্রথমে সমস্ত স্পেস, হাইফেন, ডট, ড্যাশ বাদ দিন
    clean_text = re.sub(r'[-\s\.]', '', text)
    
    # প্যাটার্ন সমূহ (অর্ডার গুরুত্বপূর্ণ - বড় থেকে ছোট)
    patterns = [
        # ইন্সটাগ্রাম/ফেসবুক স্পেসিফিক
        r'(?:confirm|confirmation|verification|your|code|otp|is)[\s]*code[\s]*(\d{4,8})',
        r'(?:confirm|confirmation|verification|your)[\s]+(\d{4,8})',
        r'code[\s:;]+(\d{4,8})',
        r'otp[\s:;]+(\d{4,8})',
        
        # 8 ডিজিট (সবচেয়ে বড়)
        r'(\d{8})',
        # 7 ডিজিট
        r'(\d{7})',
        # 6 ডিজিট (সবচেয়ে কমন)
        r'(\d{6})',
        # 5 ডিজিট
        r'(\d{5})',
        # 4 ডিজিট
        r'(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            otp = match.group(1)
            if len(otp) >= 4:
                return otp
    
    # যদি কোন প্যাটার্ন ম্যাচ না করে, তাহলে সব সংখ্যা বের করুন
    digits = re.findall(r'\d+', clean_text)
    for digit in digits:
        if len(digit) >= 4:
            return digit
    
    return "N/A"

def get_country_info(range_code):
    clean_range = str(range_code).upper().replace("X", "").strip()
    for length in [3, 2]:
        prefix = clean_range[:length]
        if prefix in COUNTRY_CODES:
            country_name = COUNTRY_CODES[prefix]
            flag = COUNTRY_FLAGS.get(country_name, "🌍")
            short = COUNTRY_SHORT.get(country_name, "XX")
            return country_name, flag, short
    return "Unknown", "🌍", "XX"

def mask_number_for_group(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:4] + "*******" + phone_str[-4:]
    return phone_str[:4] + "*******"

def mask_number(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:7] + "XXX" + phone_str[-2:]
    return phone_str

# ==================== API ফাংশন ====================
def get_live_ranges(service):
    if not LOGGED_IN:
        mk_login()
    
    try:
        response = SESSION.get(f"{BASE_URL}/console.php?ajax=1", timeout=15)
        if response.status_code == 200:
            data = response.json()
            feed = data.get("feed", [])
            ranges = set()
            for item in feed:
                app_name = item.get("service_name", "").lower()
                if service.lower() in app_name:
                    rng = item.get("range")
                    if rng:
                        ranges.add(str(rng).upper().strip())
            return sorted(list(ranges))[:20]
    except Exception as e:
        print(f"Ranges error: {e}")
    return []

def fetch_number(range_code):
    if not LOGGED_IN:
        mk_login()
    
    url = f"{BASE_URL}/API/api_handler_test.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/getnum_test.php",
        "x-requested-with": "mark.via.gp",
        "Cookie": f"PHPSESSID={SESSION.cookies.get('PHPSESSID', '')}"
    }
    
    boundary = "----WebKitFormBoundary" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    
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

def check_otp():
    results = []
    if not LOGGED_IN:
        mk_login()
    
    try:
        response = SESSION.get(f"{BASE_URL}/API/api_handler_test.php?action=get_history&filter=all&page=1&limit=50", timeout=15)
        if response.status_code == 200:
            data = response.json()
            numbers_list = data.get("data", [])
            active = get_active_numbers()
            
            for phone in active:
                for item in numbers_list:
                    num = item.get("phone_number", "")
                    if phone == num and item.get("status") == "success":
                        # API থেকে আসা otps ফিল্ড ইগনোর করে ফুল মেসেজ ব্যবহার করুন
                        full_message = item.get("full_sms_list", "")
                        if full_message:
                            # ফুল মেসেজ থেকে OTP এক্সট্রাক্ট করুন
                            extracted_otp = extract_otp_from_text(full_message)
                            if extracted_otp != "N/A":
                                results.append({
                                    "phone": phone,
                                    "message": full_message,
                                    "otp": extracted_otp,
                                    "service": active[phone].get("service", "Unknown"),
                                    "country": active[phone].get("country", "Unknown"),
                                    "range": active[phone].get("range", "")
                                })
                                break
    except Exception as e:
        print(f"OTP check error: {e}")
    return results

# ==================== Monkey Patch ====================
_old_inline_dict = InlineKeyboardButton.to_dict
def _new_inline_dict(self):
    d = _old_inline_dict(self)
    if hasattr(self, 'style') and self.style:
        d['style'] = self.style
    return d
InlineKeyboardButton.to_dict = _new_inline_dict

_old_kb_dict = KeyboardButton.to_dict
def _new_kb_dict(self):
    d = _old_kb_dict(self)
    if hasattr(self, 'style') and self.style:
        d['style'] = self.style
    return d
KeyboardButton.to_dict = _new_kb_dict

def ibtn(text, callback_data=None, url=None, style=None):
    b = InlineKeyboardButton(text=text, callback_data=callback_data, url=url)
    if style: b.style = style
    return b

def rbtn(text, style=None):
    b = KeyboardButton(text=text)
    if style: b.style = style
    return b

# ==================== ডাটাবেস ====================
USER_DB = "users.json"
USER_DATA_DB = "user_data.json"
SETTINGS_DB = "settings.json"
WITHDRAWALS_DB = "withdrawals.json"
ACTIVE_NUMBERS_DB = "active_numbers.json"

def init_databases():
    files = {
        USER_DB: [],
        USER_DATA_DB: {},
        SETTINGS_DB: {"otp_price": 5.0, "min_withdraw": 50.0},
        WITHDRAWALS_DB: [],
        ACTIVE_NUMBERS_DB: {}
    }
    for file, default in files.items():
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump(default, f)

init_databases()

def get_user_balance(user_id):
    with open(USER_DATA_DB, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), {}).get("balance", 0.0)

def update_user_balance(user_id, amount):
    with open(USER_DATA_DB, "r") as f:
        data = json.load(f)
    uid = str(user_id)
    if uid not in data:
        data[uid] = {"balance": 0.0}
    data[uid]["balance"] = round(data[uid]["balance"] + amount, 2)
    with open(USER_DATA_DB, "w") as f:
        json.dump(data, f)

def get_all_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def add_user(user_id):
    with open(USER_DB, "r") as f:
        users = json.load(f)
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)
    
    with open(USER_DATA_DB, "r") as f:
        data = json.load(f)
    if str(user_id) not in data:
        data[str(user_id)] = {"balance": 0.0}
        with open(USER_DATA_DB, "w") as f:
            json.dump(data, f)

def get_settings():
    with open(SETTINGS_DB, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_DB, "w") as f:
        json.dump(settings, f)

def get_withdrawals():
    with open(WITHDRAWALS_DB, "r") as f:
        return json.load(f)

def save_withdrawals(withdraws):
    with open(WITHDRAWALS_DB, "w") as f:
        json.dump(withdraws, f)

def get_active_numbers():
    with open(ACTIVE_NUMBERS_DB, "r") as f:
        return json.load(f)

def save_active_numbers(numbers):
    with open(ACTIVE_NUMBERS_DB, "w") as f:
        json.dump(numbers, f)

def add_active_number(phone, chat_id, service, range_code):
    country_name, flag, short = get_country_info(range_code)
    data = get_active_numbers()
    data[str(phone)] = {
        "chat_id": chat_id,
        "service": service,
        "range": range_code,
        "country": country_name,
        "country_flag": flag,
        "country_short": short,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_active_numbers(data)

def remove_active_number(phone):
    data = get_active_numbers()
    if str(phone) in data:
        del data[str(phone)]
        save_active_numbers(data)

# ==================== OTP নোটিফিকেশন ====================
def send_otp_notification(chat_id, phone, service, otp, message, price, country, flag, country_short):
    masked = mask_number(phone)
    
    # ইনবক্স মেসেজ (পুরো ডিটেইলস)
    dm_msg = f"""✅ OTP RECEIVED!
━━━━━━━━━━━━━━━━━━━━
📱 Number: `{phone}`
🎯 Service: {service}
🌍 Country: {country}
━━━━━━━━━━━━━━━━━━━━
🔐 OTP Code: `{otp}`
━━━━━━━━━━━━━━━━━━━━
📩 Full SMS:
`{message[:200]}`
━━━━━━━━━━━━━━━━━━━━
💰 Income: +{price} BDT"""
    
    # OTP গ্রুপ মেসেজ
    service_short = "FB" if service.lower() == "facebook" else "IG" if service.lower() == "instagram" else "OTP"
    masked_phone = mask_number_for_group(phone)
    group_msg = f"{flag} {country_short} {service_short} {masked_phone}"
    
    # OTP বাটন
    markup = InlineKeyboardMarkup()
    markup.add(ibtn(f"🔐 {otp}", callback_data=f"copy_otp_{otp}", style="primary"))
    
    try:
        bot.send_message(chat_id, dm_msg, parse_mode="Markdown")
        bot.send_message(LOG_GROUP_ID, group_msg, reply_markup=markup)
    except Exception as e:
        print(f"Send error: {e}")

def send_number_received_notification(chat_id, numbers, service_name, range_code):
    numbers_text = "\n".join([f"✅ `{num}`" for num in numbers])
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        ibtn("📢 OTP GROUP", url=OTP_GROUP_URL, style="primary"),
        ibtn("🔄 Change Number", callback_data=f"change_number_{service_name}_{range_code}", style="success")
    )
    markup.add(ibtn("🔙 Back to Ranges", callback_data=f"back_to_ranges_{service_name}", style="danger"))
    
    msg = f"""🎯 Numbers Received!

{numbers_text}

🎯 Service: {service_name}

💡 OTP will appear here automatically!
💰 Earn {get_settings()['otp_price']} BDT per OTP"""
    
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

# ==================== কীবোর্ড ====================
def get_main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(rbtn("🎲 GET NUMBER", style="primary"))
    if user_id == ADMIN_ID:
        markup.row(rbtn("🛠 ADMIN PANEL", style="success"))
    markup.row(rbtn("💰 BALANCE", style="success"), rbtn("💳 WITHDRAWAL", style="success"))
    return markup

def get_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(rbtn("📢 BROADCAST", style="primary"), rbtn("📊 STATS", style="primary"))
    markup.row(rbtn("⚙️ PRICE", style="success"), rbtn("📂 PENDING", style="success"))
    markup.row(rbtn("🔙 BACK", style="danger"))
    return markup

def get_service_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(ibtn("📘 Facebook", callback_data="srv_facebook", style="primary"))
    markup.add(ibtn("📸 Instagram", callback_data="srv_instagram", style="danger"))
    markup.row(ibtn("🔙 Back", callback_data="back_main_menu", style="danger"))
    return markup

def get_range_keyboard(ranges, service):
    markup = InlineKeyboardMarkup()
    for i, r in enumerate(ranges[:10]):
        style = "primary" if i % 2 == 0 else "success"
        country_name, flag, short = get_country_info(r)
        markup.add(ibtn(f"{flag} {short} — {r}", callback_data=f"rng_{service}_{r}", style=style))
    markup.add(ibtn("🔄 Refresh", callback_data=f"refresh_{service}", style="primary"))
    markup.add(ibtn("🔙 Back", callback_data="back_to_services", style="danger"))
    return markup

# ==================== বট হ্যান্ডলার ====================
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id)
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👋 Welcome Admin!", reply_markup=get_admin_keyboard())
    else:
        bot.send_message(
            message.chat.id,
            f"✨ Welcome {message.from_user.first_name}! ✨\n\n💰 Balance: {get_user_balance(message.chat.id)} BDT",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard(message.chat.id)
        )

@bot.message_handler(func=lambda m: m.text == "🎲 GET NUMBER")
def handle_get_number(message):
    bot.send_message(message.chat.id, "🔍 Select Service:", reply_markup=get_service_keyboard())

@bot.message_handler(func=lambda m: m.text == "💰 BALANCE")
def handle_balance(message):
    bal = get_user_balance(message.chat.id)
    bot.send_message(message.chat.id, f"💰 Balance: `{bal}` BDT", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💳 WITHDRAWAL")
def handle_withdraw(message):
    bal = get_user_balance(message.chat.id)
    settings = get_settings()
    if bal < settings["min_withdraw"]:
        bot.send_message(message.chat.id, f"❌ Min withdraw: {settings['min_withdraw']} BDT\nYour balance: {bal} BDT")
    else:
        msg = bot.send_message(message.chat.id, "💳 Enter Bkash number:")
        bot.register_next_step_handler(msg, process_withdraw, bal)

@bot.message_handler(func=lambda m: m.text == "🔙 BACK")
def back_main(message):
    bot.send_message(message.chat.id, "🏠 Main Menu", reply_markup=get_main_keyboard(message.chat.id))

@bot.message_handler(func=lambda m: m.text == "🛠 ADMIN PANEL")
def admin_menu(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Admin Panel:", reply_markup=get_admin_keyboard())

def process_withdraw(message, amount):
    bkash = message.text.strip()
    if len(bkash) < 11 or not bkash.isdigit():
        bot.send_message(message.chat.id, "❌ Invalid Bkash number!")
        return
    
    withdrawals = get_withdrawals()
    req_id = len(withdrawals) + 1
    
    new_req = {
        "id": req_id,
        "user_id": message.chat.id,
        "bkash": bkash,
        "amount": amount,
        "status": "pending",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    withdrawals.append(new_req)
    save_withdrawals(withdrawals)
    update_user_balance(message.chat.id, -amount)
    
    bot.send_message(message.chat.id, f"✅ Withdrawal Request Submitted!\n💰 Amount: {amount} BDT\n📱 Bkash: {bkash}")
    bot.send_message(ADMIN_ID, f"🔔 New Withdrawal!\nUser: {message.chat.id}\nAmount: {amount} BDT\nBkash: {bkash}")

# ==================== এডমিন হ্যান্ডলার ====================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text in ["📢 BROADCAST", "📊 STATS", "⚙️ PRICE", "📂 PENDING"])
def admin_buttons(message):
    if message.text == "📢 BROADCAST":
        msg = bot.send_message(message.chat.id, "📢 Send broadcast message:")
        bot.register_next_step_handler(msg, broadcast_msg)
    elif message.text == "📊 STATS":
        users = len(get_all_users())
        active = len(get_active_numbers())
        settings = get_settings()
        bot.send_message(message.chat.id, f"📊 Stats\n👥 Users: {users}\n📱 Active: {active}\n💰 Price: {settings['otp_price']} BDT\n💳 Min: {settings['min_withdraw']} BDT")
    elif message.text == "⚙️ PRICE":
        msg = bot.send_message(message.chat.id, "💰 Enter new OTP price:")
        bot.register_next_step_handler(msg, edit_price)
    elif message.text == "📂 PENDING":
        pending = [w for w in get_withdrawals() if w["status"] == "pending"]
        if not pending:
            bot.send_message(message.chat.id, "📭 No pending withdrawals!")
            return
        for w in pending:
            markup = InlineKeyboardMarkup()
            markup.row(ibtn("✅ Approve", callback_data=f"approve_{w['id']}", style="success"), ibtn("❌ Reject", callback_data=f"reject_{w['id']}", style="danger"))
            bot.send_message(message.chat.id, f"📥 Request #{w['id']}\nUser: {w['user_id']}\nAmount: {w['amount']} BDT\nBkash: {w['bkash']}", reply_markup=markup)

def broadcast_msg(message):
    users = get_all_users()
    success = 0
    for uid in users:
        try:
            bot.send_message(uid, f"📢 Broadcast\n\n{message.text}")
            success += 1
            time.sleep(0.05)
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ Sent to {success} users!")

def edit_price(message):
    try:
        price = float(message.text)
        settings = get_settings()
        settings["otp_price"] = price
        save_settings(settings)
        bot.send_message(message.chat.id, f"✅ Price set to {price} BDT!")
    except:
        bot.send_message(message.chat.id, "❌ Invalid!")

# ==================== কলব্যাক হ্যান্ডলার ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data
    
    if data.startswith("copy_otp_"):
        otp_code = data.split("_")[2]
        bot.answer_callback_query(call.id, f"✅ OTP Copied: {otp_code}", show_alert=True)
        return
    
    if data == "back_main_menu":
        bot.edit_message_text("🏠 Main Menu", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if data == "back_to_services":
        bot.edit_message_text("🔍 Select Service:", chat_id, msg_id, reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("refresh_"):
        service = data.split("_")[1].upper()
        ranges = get_live_ranges(service)
        if ranges:
            bot.edit_message_text(f"🔥 Live Ranges for {service}:", chat_id, msg_id, reply_markup=get_range_keyboard(ranges, service.lower()))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("back_to_ranges_"):
        service = data.split("_")[3].upper()
        ranges = get_live_ranges(service)
        if ranges:
            bot.edit_message_text(f"🔥 Live Ranges for {service}:", chat_id, msg_id, reply_markup=get_range_keyboard(ranges, service.lower()))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("srv_"):
        service = data.split("_")[1].upper()
        ranges = get_live_ranges(service)
        if ranges:
            bot.edit_message_text(f"🔥 Live Ranges for {service}:", chat_id, msg_id, reply_markup=get_range_keyboard(ranges, service.lower()))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id, reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("rng_"):
        parts = data.split("_")
        service = parts[1].upper()
        range_code = parts[2]
        
        bot.edit_message_text(f"⏳ Getting 2 numbers from `{range_code}`...", chat_id, msg_id, parse_mode="Markdown")
        
        numbers_found = []
        for i in range(2):
            number = fetch_number(range_code)
            if number:
                numbers_found.append(number)
                add_active_number(number, chat_id, service.capitalize(), range_code)
            time.sleep(0.5)
        
        if numbers_found:
            bot.delete_message(chat_id, msg_id)
            send_number_received_notification(chat_id, numbers_found, service.capitalize(), range_code)
        else:
            bot.edit_message_text(f"❌ No number available!\n\nTry another range.", chat_id, msg_id, reply_markup=get_range_keyboard(get_live_ranges(service), service.lower()))
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("change_number_"):
        parts = data.split("_")
        service = parts[2]
        range_code = parts[3]
        
        bot.delete_message(chat_id, msg_id)
        loading_msg = bot.send_message(chat_id, f"⏳ Getting 2 new numbers...")
        
        numbers_found = []
        for i in range(2):
            number = fetch_number(range_code)
            if number:
                numbers_found.append(number)
                add_active_number(number, chat_id, service, range_code)
            time.sleep(0.5)
        
        bot.delete_message(chat_id, loading_msg.message_id)
        
        if numbers_found:
            send_number_received_notification(chat_id, numbers_found, service, range_code)
        else:
            bot.send_message(chat_id, "❌ No numbers available!", reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("approve_"):
        req_id = int(data.split("_")[1])
        withdrawals = get_withdrawals()
        for w in withdrawals:
            if w["id"] == req_id:
                w["status"] = "approved"
                save_withdrawals(withdrawals)
                bot.edit_message_text(f"✅ Approved #{req_id}", chat_id, msg_id)
                try:
                    bot.send_message(w["user_id"], f"✅ Your withdrawal of {w['amount']} BDT has been approved!\nSent to: {w['bkash']}")
                except:
                    pass
                break
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("reject_"):
        req_id = int(data.split("_")[1])
        withdrawals = get_withdrawals()
        for w in withdrawals:
            if w["id"] == req_id:
                w["status"] = "rejected"
                save_withdrawals(withdrawals)
                update_user_balance(w["user_id"], w["amount"])
                bot.edit_message_text(f"❌ Rejected #{req_id}", chat_id, msg_id)
                try:
                    bot.send_message(w["user_id"], f"❌ Your withdrawal request of {w['amount']} BDT was rejected!\nAmount refunded to balance.")
                except:
                    pass
                break
        bot.answer_callback_query(call.id)
        return

# ==================== OTP মনিটর ====================
sent_otps = set()

def otp_monitor():
    global sent_otps
    print("🔄 OTP Monitor Started (Using Full SMS)")
    while True:
        try:
            settings = get_settings()
            price = settings.get("otp_price", 5.0)
            otps = check_otp()
            
            for otp_data in otps:
                phone = otp_data["phone"]
                message = otp_data["message"]
                extracted_otp = otp_data["otp"]
                
                unique_key = f"{phone}_{extracted_otp}"
                
                if unique_key not in sent_otps:
                    sent_otps.add(unique_key)
                    
                    active = get_active_numbers()
                    if str(phone) in active:
                        chat_id = active[str(phone)]["chat_id"]
                        service = active[str(phone)]["service"]
                        country = active[str(phone)]["country"]
                        flag = active[str(phone)]["country_flag"]
                        country_short = active[str(phone)]["country_short"]
                        
                        update_user_balance(chat_id, price)
                        send_otp_notification(chat_id, phone, service, extracted_otp, message, price, country, flag, country_short)
                        remove_active_number(phone)
                        print(f"📱 OTP Found: {phone} | {service} | OTP: {extracted_otp}")
            
            if len(sent_otps) > 1000:
                sent_otps.clear()
                
        except Exception as e:
            print(f"Monitor Error: {e}")
        time.sleep(5)

# ==================== মেইন ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 OTP BOT (Full SMS Based OTP Extraction)")
    print("=" * 60)
    print("✅ OTP extracted from FULL SMS message")
    print("✅ Supports: 828-828 -> 828828")
    print("✅ Supports: confirm code 283 283 -> 283283")
    print("✅ Supports: 82739 -> 82739")
    print("✅ Supports: 82729382 -> 82729382")
    print("=" * 60)
    
    mk_login()
    threading.Thread(target=otp_monitor, daemon=True).start()
    
    print("✅ Bot Running!")
    print("=" * 60)
    
    bot.infinity_polling(timeout=60)