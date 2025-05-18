import os
from flask import Flask, request
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

CHANNEL_LINK = "https://t.me/NSA_Network"
DEV_NAME = "Navneet Dabwal"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK),
        types.InlineKeyboardButton("Verify", callback_data="verify")
    )
    bot.send_message(
        message.chat.id,
        f"""<b>Welcome to</b> <code>DARKNET CORE</code>\n
<b>Developer:</b> <i>{DEV_NAME}</i>\n
Choose an option to proceed below:""",
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "verify":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("IP Info", callback_data="ip_info"),
            types.InlineKeyboardButton("Fake Address", callback_data="fake_address"),
            types.InlineKeyboardButton("BIN Info", callback_data="bin_info"),
            types.InlineKeyboardButton("CC Checker", callback_data="cc_check"),
            types.InlineKeyboardButton("CC Generator", callback_data="cc_gen"),
            types.InlineKeyboardButton("Dark BIN", callback_data="darkbin")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Select a feature below:",
            reply_markup=markup
        )

    elif call.data == "ip_info":
        bot.send_message(call.message.chat.id, "Send IP address:")
        bot.register_next_step_handler(call.message, trace_ip)

    elif call.data == "fake_address":
        bot.send_message(call.message.chat.id, "Name: John Doe\nAddress: 123 Fake Street\nCity: Faketown\nPhone: +1 555-1234")

    elif call.data == "bin_info":
        bot.send_message(call.message.chat.id, "Send BIN:")
        bot.register_next_step_handler(call.message, bin_info)

    elif call.data == "cc_check":
        bot.send_message(call.message.chat.id, "Send CC to check (xxxx|mm|yyyy|cvv):")
        bot.register_next_step_handler(call.message, cc_checker)

    elif call.data == "cc_gen":
        bot.send_message(call.message.chat.id, "Send BIN to generate CCs:")
        bot.register_next_step_handler(call.message, cc_generator)

    elif call.data == "darkbin":
        bot.send_message(call.message.chat.id, "Send BIN to check dark web:")
        bot.register_next_step_handler(call.message, darkbin_check)

# Features
def trace_ip(message):
    ip = message.text.strip()
    bot.send_message(message.chat.id, f"Device Info for {ip}:\nModel: Android\nISP: Jio\nLocation: Delhi")

def bin_info(message):
    bin_number = message.text.strip()
    bot.send_message(message.chat.id, f"BIN Info for {bin_number}:\nBank: HDFC\nType: VISA\nCountry: India")

def cc_checker(message):
    cc = message.text.strip()
    bot.send_message(message.chat.id, f"Checking {cc}...\nStatus: Live\nBalance: $1234.56")

def cc_generator(message):
    bin_input = message.text.strip()
    bot.send_message(message.chat.id, f"Generated CC:\n{bin_input[:-6]}XXXXXX|06|2028|123")

def darkbin_check(message):
    bin_num = message.text.strip()
    bot.send_message(message.chat.id, f"{bin_num} is leaked on dark web sources!")

# Webhook
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def home():
    return "Bot Running - DARKNET CORE", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
