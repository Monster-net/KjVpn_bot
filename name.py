import os
import telebot
from telebot import types

# توکن ربات از متغیرهای محیطی خوانده می‌شود
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("🛒 خرید اشتراک VPN", callback_data='buy')
    markup.add(btn_buy)
    
    bot.reply_to(message, "سلام! به ربات خرید اشتراک خوش آمدید.\nبرای خرید و پرداخت با ترونارد روی دکمه زیر کلیک کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def callback_query(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "جهت پرداخت آنی با ترونارد، لطفاً به لینک زیر مراجعه کنید:\n(لینک درگاه شما اینجا قرار می‌گیرد)")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
