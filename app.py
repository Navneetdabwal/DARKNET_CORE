import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from utils import scrape_stream_link

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the Ultimate Movie Bot!\n\n"
        "Just send the name of any movie (even newly released ones), and I'll try to find a streaming link for you.\n\n"
        "____________________________________\n"
        "👨‍💻 *Bot Developer:* `『𝙉𝘼𝙑𝙉𝙀𝙀𝙏 𝘿𝘼𝘽𝙒𝘼𝙇』`\n"
        "____________________________________",
        parse_mode="Markdown"
    )

async def movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text
    await update.message.reply_text("🔍 Searching for a streamable version...")

    video_url = scrape_stream_link(movie_name)

    if not video_url:
        await update.message.reply_text("❌ Movie not found or not streamable.")
        return

    msg = await update.message.reply_video(
        video=video_url,
        caption=(
            f"🎬 Movie: {movie_name.title()}\n\n"
            "⚠️ This video will be deleted in 1 minute. Forward it now if you want to keep it!"
        )
    )
    await asyncio.sleep(60)
    try:
        await msg.delete()
    except:
        pass

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie_handler))
app.run_polling()
