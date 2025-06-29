
from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "7577417748:AAGCYqLMeULF5Qr39nO8uJk4X2f1n3eWzF0"
API_URL = "https://api.aichatos.cloud/api/gpt3"

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

YOUR_RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL', 'https://your-app-name.onrender.com')
WEBHOOK_PATH = f"/webhook/{TELEGRAM_TOKEN}"

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
            return f"خطا از سمت AI ❌ وضعیت: {response.status_code}"
    except Exception as e:
        return f"مشکل در API ❌\n{str(e)}"

@app.route('/', methods=['GET'])
def index():
    return "Bot is running! ✅"

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]
        ai_reply = ask_ai(user_message)

        send_text = f"🌱 {ai_reply}"
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": send_text
        })

    return '', 200

def set_webhook():
    webhook_url = YOUR_RENDER_URL + WEBHOOK_PATH
    set_url = f"{TELEGRAM_API_URL}/setWebhook"
    response = requests.post(set_url, json={"url": webhook_url})
    print("Webhook set status:", response.text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    set_webhook()
    app.run(host='0.0.0.0', port=port)
