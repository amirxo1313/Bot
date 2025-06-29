
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات تلگرام
TELEGRAM_TOKEN = "7577417748:AAGCYqLMeULF5Qr39nO8uJk4X2f1n3eWzF0"

# API Endpoint رایگان (مثال)
API_URL = "https://api.aichatos.cloud/api/gpt3"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام بهنوش عزیزم! من Amir هستم 🤖 بیا باهم حرف بزنیم ❤️")

def ask_ai(message_text):
    try:
        payload = {
            "prompt": message_text,
            "user": "behnoush"
        }
        response = requests.post(API_URL, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result.get('text', 'نتونستم جواب بدم 😔')
        else:
            return f"خطا از سمت سرور AI ❌ کد وضعیت: {response.status_code}"
    except Exception as e:
        return f"مشکل در اتصال به API ❌\n{str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_reply = ask_ai(user_message)
    await update.message.reply_text(ai_reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
