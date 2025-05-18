import os
import random
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Dispatcher, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

CHANNEL_LINK = "https://t.me/NSA_Network"

# ---------------- Start Message ----------------
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("✅ Verify", callback_data="verify")],
        [InlineKeyboardButton("Join Main Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = (
        "╔══『 **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗗𝗔𝗥𝗞𝗡𝗘𝗧 𝗖𝗢𝗥𝗘** 』══\n"
        "║\n"
        "╠ ⚡ 𝘿𝙚𝙫: Navneet Dabwal\n"
        "╠ ⚙️ 𝘽𝙤𝙩: Ultimate OSINT + CC Toolkit\n"
        "╠ 🔐 Powered by Underground Intelligence\n"
        "║\n"
        "╚═══════════════════════╝"
    )
    update.message.reply_text(msg, reply_markup=reply_markup)

# ---------------- Verify ----------------
def verify_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("IP Info", callback_data="ip")],
        [InlineKeyboardButton("BIN Info", callback_data="bin")],
        [InlineKeyboardButton("CC Gen", callback_data="ccgen")],
        [InlineKeyboardButton("CC Check", callback_data="ccchk")],
        [InlineKeyboardButton("Fake Address", callback_data="fake")],
        [InlineKeyboardButton("Dark BIN Check", callback_data="dark")]
    ]
    query.edit_message_text("Choose a command:", reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------- IP Info ----------------
def ipinfo(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Send an IP address to trace:")

def ip_lookup(update: Update, context: CallbackContext):
    ip = update.message.text.strip()
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json").json()
        msg = (
            f"IP: {r.get('ip')}\nCity: {r.get('city')}\nRegion: {r.get('region')}\n"
            f"Country: {r.get('country_name')}\nISP: {r.get('org')}\nLatitude: {r.get('latitude')}\nLongitude: {r.get('longitude')}"
        )
    except:
        msg = "Invalid IP or API error."
    update.message.reply_text(msg)

# ---------------- BIN Info ----------------
def bininfo(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Send BIN to check:")

def bin_lookup(update: Update, context: CallbackContext):
    bin = update.message.text.strip().replace(" ", "")[:6]
    r = requests.get(f"https://lookup.binlist.net/{bin}")
    if r.status_code == 200:
        j = r.json()
        msg = (
            f"Scheme: {j.get('scheme')}\nBrand: {j.get('brand')}\nType: {j.get('type')}\n"
            f"Bank: {j['bank']['name']}\nCountry: {j['country']['name']} {j['country']['emoji']}"
        )
    else:
        msg = "Invalid BIN or not found."
    update.message.reply_text(msg)

# ---------------- CC Gen ----------------
def ccgen(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Send BIN (6-16 digits):")

def generate_cc(bin):
    bin = bin.ljust(16, "x")
    cc_list = []
    for _ in range(10):
        cc = ""
        for c in bin:
            cc += str(random.randint(0,9)) if c.lower() == "x" else c
        mm = str(random.randint(1,12)).zfill(2)
        yy = str(random.randint(25,29))
        cvv = str(random.randint(100,999))
        cc_list.append(f"{cc}|{mm}|20{yy}|{cvv}")
    return "\n".join(cc_list)

def ccgen_input(update: Update, context: CallbackContext):
    bin = update.message.text.strip()
    update.message.reply_text(generate_cc(bin))

# ---------------- CC Checker ----------------
def ccchk(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Simulated CC Checker: Send CC in format `xxxx|MM|YYYY|CVV`")

def cc_check(update: Update, context: CallbackContext):
    cc = update.message.text.strip()
    update.message.reply_text(f"Live: {random.choice([True, False])} [SIMULATED]")

# ---------------- Fake Address ----------------
def fake(update: Update, context: CallbackContext):
    update.callback_query.answer()
    countries = ["US", "India", "Canada", "Germany"]
    keyboard = [[InlineKeyboardButton(c, callback_data=f"fake_{c}")] for c in countries]
    update.callback_query.message.reply_text("Select country:", reply_markup=InlineKeyboardMarkup(keyboard))

def fake_address_callback(update: Update, context: CallbackContext):
    c = update.callback_query.data.split("_")[1]
    update.callback_query.answer()
    fake_data = {
        "US": "John Smith\n1234 Elm St\nNYC, NY 10001\n+1 202-555-0182",
        "India": "Raj Sharma\nC-54, Lajpat Nagar\nDelhi, 110024\n+91 9876543210",
        "Canada": "Emma Brown\n67 Maple Ave\nToronto, ON M4C 1Z3\n+1 416-555-0123",
        "Germany": "Hans Müller\nBerliner Str. 23\nBerlin, 10117\n+49 30 123456"
    }
    update.callback_query.message.reply_text(fake_data.get(c, "Not available."))

# ---------------- Dark BIN ----------------
def dark(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.message.reply_text("Send BIN to check dark leak:")
    
def dark_lookup(update: Update, context: CallbackContext):
    bin = update.message.text.strip()[:6]
    result = random.choice(["Leaked", "Not Found", "Suspicious Activity"])
    update.message.reply_text(f"Result: {result}")

# ---------------- Handlers ----------------
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
dispatcher.add_handler(CallbackQueryHandler(ipinfo, pattern="ip"))
dispatcher.add_handler(CallbackQueryHandler(bininfo, pattern="bin"))
dispatcher.add_handler(CallbackQueryHandler(ccgen, pattern="ccgen"))
dispatcher.add_handler(CallbackQueryHandler(ccchk, pattern="ccchk"))
dispatcher.add_handler(CallbackQueryHandler(fake, pattern="fake"))
dispatcher.add_handler(CallbackQueryHandler(fake_address_callback, pattern=r"fake_"))
dispatcher.add_handler(CallbackQueryHandler(dark, pattern="dark"))

dispatcher.add_handler(MessageHandler(Filters.regex(r"^\d{1,3}(\.\d{1,3}){3}$"), ip_lookup))
dispatcher.add_handler(MessageHandler(Filters.regex(r"^\d{6,16}$"), bin_lookup))
dispatcher.add_handler(MessageHandler(Filters.regex(r"^\d{16}\|\d{2}\|\d{4}\|\d{3,4}$"), cc_check))
dispatcher.add_handler(MessageHandler(Filters.regex(r"^\d{6,16}$"), ccgen_input))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dark_lookup))

# ---------------- Webhook ----------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Darknet Core Bot Running!"

if __name__ == "__main__":
    bot.set_webhook(f"https://your-app-name.onrender.com/{TOKEN}")
    app.run(port=5000)
