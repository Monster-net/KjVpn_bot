
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
import telebot
from telebot import types


# Telegram settings
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = telebot.TeleBot(TOKEN)


# 3X-UI settings: use existing Render environment variables
XUI_BASE_URL = os.environ.get("XUI_BASE_URL", "").rstrip("/")
XUI_API_TOKEN = os.environ.get("XUI_API_TOKEN", "")
INBOUND_ID = os.environ.get("INBOUND_ID", "")


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def test_xui_connection():
    if not XUI_BASE_URL or not XUI_API_TOKEN:
        print("XUI_ERROR: XUI_BASE_URL or XUI_API_TOKEN is missing")
        return

    if not INBOUND_ID:
        print("XUI_ERROR: INBOUND_ID is missing")
        return

    url = XUI_BASE_URL + "/panel/api/inbounds/list"

    headers = {
        "Authorization": f"Bearer {XUI_API_TOKEN}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        print("XUI_HTTP_STATUS:", response.status_code)
        print("INBOUND_ID_CONFIGURED:", INBOUND_ID)

        if response.ok:
            try:
                data = response.json()
                if isinstance(data, dict):
                    print("XUI_API_SUCCESS:", data.get("success"))
                    print("XUI_API_MESSAGE:", str(data.get("msg", ""))[:200])
                else:
                    print("XUI_API_RESPONSE_TYPE:", type(data).__name__)
            except ValueError:
                print("XUI_RESPONSE: non-JSON response")
        else:
            print("XUI_ERROR: HTTP request failed")

    except requests.RequestException as error:
        print("XUI_CONNECTION_ERROR:", type(error).__name__)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()

    btn_buy = types.InlineKeyboardButton(
        "🛒 خرید اشتراک VPN",
        callback_data="buy"
    )

    markup.add(btn_buy)

    bot.reply_to(
        message,
        "سلام! به ربات خرید اشتراک خوش آمدید.\n"
        "برای خرید و پرداخت با ترونارد روی دکمه زیر کلیک کنید:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == "buy")
def callback_query(call):
    bot.answer_callback_query(call.id)

    bot.send_message(
        call.message.chat.id,
        "جهت پرداخت آنی با ترونارد، لطفاً به لینک زیر مراجعه کنید:\n"
        "(لینک درگاه شما اینجا قرار می‌گیرد)"
    )


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler
    )

    server.serve_forever()


if __name__ == "__main__":
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    print("Bot is running...")

    test_xui_connection()

    bot.infinity_polling()
```
