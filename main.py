import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Webhook route
@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# Index route
@app.route("/", methods=['GET'])
def index():
    return "I'm alive via webhook!"

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🇷🇺👋 Добро пожаловать!\n"
        "Вы можете анонимно отправить отзыв в виде текста, голосового сообщения или фотографии.\n\n"
        "🇺🇿👋 Xush kelibsiz!\n"
        "Matn, ovozli xabar yoki surat ko‘rinishida anonim fikr bildirishingiz mumkin.\n\n"
        "🇺🇸👋 Welcome!\n"
        "You can anonymously send feedback as text, voice message, or photo."
    )
    bot.send_message(message.chat.id, welcome_text)

# Текст
@bot.message_handler(func=lambda message: message.text and message.text != "/start")
def handle_text(message):
    reply_text = (
        "✅ Спасибо за ваш отзыв! Вы помогаете нам стать лучше.\n"
        "✅ Fikringiz uchun rahmat! Bizga yanada yaxshilanishga yordam beryapsiz.\n"
        "✅ Thank you for your feedback! You help us become better."
    )
    bot.send_message(message.chat.id, reply_text)
    feedback = f"📩 Новый текстовый отзыв от @{message.from_user.username or 'аноним'}:\n\n{message.text}"
    bot.send_message(ADMIN_CHAT_ID, feedback)

# Голос
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    reply_text = (
        "🎤 Спасибо за ваш голосовой отзыв!\n"
        "🎤 Ovozingiz uchun rahmat!\n"
        "🎤 Thank you for your voice message!"
    )
    bot.send_message(message.chat.id, reply_text)
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)

# Фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    reply_text = (
        "📷 Спасибо за фото! Мы обязательно его рассмотрим.\n"
        "📷 Surat uchun rahmat! Albatta ko‘rib chiqamiz.\n"
        "📷 Thank you for the photo! We will definitely review it."
    )
    bot.send_message(message.chat.id, reply_text)
    photo_file_id = message.photo[-1].file_id
    caption = f"🖼 Фотоотзыв от @{message.from_user.username or 'аноним'}"
    bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption)

# Установка Webhook при запуске
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{API_TOKEN}")
    app.run(host="0.0.0.0", port=8080)
