import os
import telebot
import requests
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- /start Command ---
@bot.message_handler(commands=["start"])
def start(msg):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        telebot.types.InlineKeyboardButton("BIN Info", callback_data="bin"),
        telebot.types.InlineKeyboardButton("CC Gen", callback_data="ccgen"),
        telebot.types.InlineKeyboardButton("CC Check", callback_data="cccheck"),
        telebot.types.InlineKeyboardButton("Fake Address", callback_data="fake"),
        telebot.types.InlineKeyboardButton("IP Lookup", callback_data="ip"),
        telebot.types.InlineKeyboardButton("Dark BIN Check", callback_data="dark")
    )
    ch = "https://t.me/NSA_Network"
    verify = telebot.types.InlineKeyboardMarkup()
    verify.add(telebot.types.InlineKeyboardButton("Main Channel", url=ch))
    bot.send_message(msg.chat.id, f"""
<b>✦ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗗𝗔𝗥𝗞𝗡𝗘𝗧 𝗖𝗢𝗥𝗘</b>

<b>⚙ Dev:</b> <code>Navneet Dabwal</code>
<b>🧠 Power:</b> Advanced BIN, CC & IP Tools
<b>➕ Use below features:</b>
""", parse_mode="HTML", reply_markup=markup)
    bot.send_message(msg.chat.id, "Join the main channel (optional):", reply_markup=verify)

# --- BIN Info ---
@bot.callback_query_handler(func=lambda call: call.data == "bin")
def bininfo(call):
    msg = bot.send_message(call.message.chat.id, "Enter BIN to check:")
    bot.register_next_step_handler(msg, check_bin)

def check_bin(msg):
    bin_num = msg.text.strip().replace(" ", "")
    res = requests.get(f"https://lookup.binlist.net/{bin_num}")
    if res.status_code != 200:
        bot.send_message(msg.chat.id, "Invalid BIN or not found.")
        return
    data = res.json()
    text = f"""
<b>BIN:</b> {bin_num}
<b>Scheme:</b> {data.get('scheme')}
<b>Brand:</b> {data.get('brand')}
<b>Type:</b> {data.get('type')}
<b>Bank:</b> {data['bank']['name'] if 'bank' in data else 'N/A'}
<b>Country:</b> {data['country']['name'] if 'country' in data else 'N/A'}
"""
    bot.send_message(msg.chat.id, text, parse_mode="HTML")

# --- CC Generator ---
@bot.callback_query_handler(func=lambda call: call.data == "ccgen")
def ccgen(call):
    msg = bot.send_message(call.message.chat.id, "Enter BIN (6-8 digits):")
    bot.register_next_step_handler(msg, generate_cc)

def generate_cc(msg):
    import random
    bin = msg.text.strip()
    months = [f"{i:02}" for i in range(1, 13)]
    years = [str(y) for y in range(2025, 2031)]
    generated = []
    for _ in range(10):
        cc = bin + ''.join(str(random.randint(0, 9)) for _ in range(16 - len(bin)))
        mm = random.choice(months)
        yy = random.choice(years)
        cvv = str(random.randint(100, 999))
        generated.append(f"{cc}|{mm}|{yy}|{cvv}")
    bot.send_message(msg.chat.id, "<b>Generated CCs:</b>\n" + "\n".join(generated), parse_mode="HTML")

# --- CC Check (Luhn only) ---
@bot.callback_query_handler(func=lambda call: call.data == "cccheck")
def cccheck(call):
    msg = bot.send_message(call.message.chat.id, "Enter CC (format: xxxx|mm|yyyy|cvv):")
    bot.register_next_step_handler(msg, validate_cc)

def validate_cc(msg):
    cc = msg.text.strip().split("|")[0]
    if not cc.isdigit():
        bot.send_message(msg.chat.id, "Invalid format.")
        return

    def luhn(card):
        digits = [int(i) for i in card][::-1]
        total = 0
        for i, d in enumerate(digits):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        return total % 10 == 0

    result = "Valid" if luhn(cc) else "Invalid"
    bot.send_message(msg.chat.id, f"<b>Card:</b> {cc}\n<b>Status:</b> {result}", parse_mode="HTML")

# --- Fake Address Generator ---
@bot.callback_query_handler(func=lambda call: call.data == "fake")
def fake(call):
    fake_data = {
        "name": "Alex Parker",
        "address": "123 Elm Street",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "USA",
        "email": "alex.parker@example.com",
        "phone": "+1 202-555-0147"
    }
    text = f"""
<b>Name:</b> {fake_data['name']}
<b>Address:</b> {fake_data['address']}
<b>City:</b> {fake_data['city']}
<b>State:</b> {fake_data['state']}
<b>Zip:</b> {fake_data['zip']}
<b>Country:</b> {fake_data['country']}
<b>Email:</b> {fake_data['email']}
<b>Phone:</b> {fake_data['phone']}
"""
    bot.send_message(call.message.chat.id, text, parse_mode="HTML")

# --- IP Lookup ---
@bot.callback_query_handler(func=lambda call: call.data == "ip")
def iplook(call):
    msg = bot.send_message(call.message.chat.id, "Send an IP to lookup:")
    bot.register_next_step_handler(msg, lookup_ip)

def lookup_ip(msg):
    ip = msg.text.strip()
    res = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
    if res.get("status") != "success":
        bot.send_message(msg.chat.id, "IP not found.")
        return
    text = f"""
<b>IP:</b> {ip}
<b>ISP:</b> {res.get('isp')}
<b>Org:</b> {res.get('org')}
<b>City:</b> {res.get('city')}
<b>Region:</b> {res.get('regionName')}
<b>Country:</b> {res.get('country')}
<b>Timezone:</b> {res.get('timezone')}
<b>Device Info:</b> {res.get('as')}
"""
    bot.send_message(msg.chat.id, text, parse_mode="HTML")

# --- Dark BIN Checker ---
@bot.callback_query_handler(func=lambda call: call.data == "dark")
def dark(call):
    msg = bot.send_message(call.message.chat.id, "Enter BIN to check dark leak:")
    bot.register_next_step_handler(msg, dark_check)

def dark_check(msg):
    bin = msg.text.strip()
    risky_bins = ["4700", "6011", "3528"]
    risk = "High" if any(bin.startswith(r) for r in risky_bins) else "Low"
    bot.send_message(msg.chat.id, f"<b>BIN:</b> {bin}\n<b>Dark Web Risk:</b> {risk}", parse_mode="HTML")

# --- Flask Webhook Setup ---
@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "OK", 200
    return "Bot is Running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
