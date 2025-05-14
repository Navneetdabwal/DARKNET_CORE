import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from threading import Thread

TOKEN = os.getenv("BOT_TOKEN")  # Set your bot token in environment
bot = Bot(token=TOKEN)
app = Flask(__name__)

# To hold user state temporarily
user_sessions = {}

# Developer credit
DEV_CREDIT = "👨‍💻 Developer: Navneet Dabwal\n🚀 Powered by TurboFollower_Bot"

# 3 websites login+boost logic
def send_followers(fake_username, fake_password, target_username):
    results = []

    # Example websites – mimic form data
    websites = [
        {
            "name": "followersize",
            "url": "https://followersize.com/tools/send-follower/60833803130",
            "form": {"username": fake_username, "password": fake_password}
        },
        {
            "name": "takipciking",
            "url": "https://takipciking.net/login",
            "form": {"username": fake_username, "password": fake_password}
        },
        {
            "name": "fastfollow",
            "url": "https://fastfollow.in/tools/send-follower/60833803130",
            "form": {"username": fake_username, "password": fake_password}
        }
    ]

    for site in websites:
        try:
            session = requests.Session()
            login = session.post(site["url"], data=site["form"], timeout=10)
            if login.status_code == 200:
                # Mimic sending followers
                send_url = site["url"]
                data = {"userID": target_username, "adet": 100}
                send = session.post(send_url, data=data, timeout=10)
                if send.status_code == 200:
                    results.append(f"✅ {site['name']} → Sent 100 followers")
                else:
                    results.append(f"⚠️ {site['name']} → Send failed")
            else:
                results.append(f"❌ {site['name']} → Login failed")
        except Exception as e:
            results.append(f"❌ {site['name']} → Error: {str(e)}")

    return "\n".join(results)

# /start command
def start(update: Update, context):
    user_id = update.effective_chat.id
    user_sessions[user_id] = {"step": 1}
    update.message.reply_text(
        "**Welcome to TurboFollower_Bot!**\n\nPlease send your fake Instagram login like this:\n\n`username|password`\n\n" + DEV_CREDIT,
        parse_mode="Markdown"
    )

# Handle messages
def handle_message(update: Update, context):
    user_id = update.effective_chat.id
    msg = update.message.text.strip()

    if user_id not in user_sessions:
        update.message.reply_text("Please send /start first.")
        return

    session = user_sessions[user_id]

    if session["step"] == 1:
        if "|" not in msg:
            update.message.reply_text("Invalid format. Use `username|password`", parse_mode="Markdown")
            return

        username, password = msg.split("|", 1)
        session["fake_username"] = username
        session["fake_password"] = password
        session["step"] = 2

        update.message.reply_text("Great! Now send the real Instagram username where you want followers.")

    elif session["step"] == 2:
        target_username = msg
        update.message.reply_text(f"Sending followers to @{target_username}...\nPlease wait...")

        result = send_followers(session["fake_username"], session["fake_password"], target_username)
        update.message.reply_text(result + "\n\n" + DEV_CREDIT)

        session["step"] = 1  # reset session

# Flask webhook route
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return f'TurboFollower_Bot by Navneet Dabwal is running.'

# Set up dispatcher
dp = Dispatcher(bot, None, workers=0)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Run Flask in thread
def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

Thread(target=run).start()