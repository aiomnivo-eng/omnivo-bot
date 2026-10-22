import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

def research(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        r = requests.get(url, timeout=10).json()
        abstract = r.get("AbstractText")
        if abstract:
            return abstract
        wiki = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}", timeout=10).json()
        if "extract" in wiki:
            return wiki["extract"]
        return "No info found, try different keyword."
    except Exception as e:
        return f"Error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am Omnivo Research Bot. Send any topic, I will research for you!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text
    await update.message.reply_text(f"Researching: {q} ...")
    result = research(q)
    await update.message.reply_text(f"Result:\n\n{result}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
