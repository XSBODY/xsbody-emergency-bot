import telebot
from flask import Flask, request
import time
import os

# Получаем токен
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает!", 200

# Webhook без токена в URL!
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

# Команды
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📋 Этапы запуска", "👩‍💼 Контакты УК", "📎 Полезные ссылки", "💬 Поддержка")
    bot.send_message(message.chat.id, "Привет! Я emergency‑куратор.", reply_markup=markup)

# Меню
@bot.message_handler(func=lambda m: True)
def handle_menu(message):
    if message.text == "📋 Этапы запуска":
        bot.send_message(message.chat.id, "Этап: Поиск помещения")
    elif message.text == "👩‍💼 Контакты УК":
        bot.send_message(message.chat.id, "Контакты: @ks_admin, @natalia_xs, @regina_xs")
    elif message.text == "📎 Полезные ссылки":
        bot.send_message(message.chat.id, "Полезно: https://xsbodyfit.getcourse.ru")
    elif message.text == "💬 Поддержка":
        bot.send_message(message.chat.id, "Пиши @regina_xs")
    else:
        bot.send_message(message.chat.id, "Не понял, выбери из меню.")

# Установка webhook — теперь правильно
with app.app_context():
    bot.remove_webhook()
    time.sleep(2)
    bot.set_webhook(url="https://xsbody-emergency-bot.onrender.com/webhook")
