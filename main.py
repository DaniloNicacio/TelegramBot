import telebot
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=["start"])
def send_hello(message):
    bot.reply_to(message, "Hello World!")
    
bot.infinity_polling()