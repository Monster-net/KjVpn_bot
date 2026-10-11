
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = telebot.TeleBot(TOKEN)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton(
        "🛒 خرید اشتراک VPN",
        callback_data='buy'
    )
    markup.add(btn_buy)

    bot.reply_to(
        message,
        "سلام! به ربات خرید اشتراک خوش آمدید.\n"
        "برای خرید و پرداخت با ترونارد روی دکمه زیر کلیک کنید:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def callback_query(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "جهت پرداخت آنی با ترونارد، لطفاً به لینک زیر مراجعه کنید:\n"
        "(لینک درگاه شما اینجا قرار می‌گیرد)"
    )


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    print("Bot is running...")
    bot.infinity_polling()

