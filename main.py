import time
import telebot
from dotenv import load_dotenv
import os
import yt_dlp
import urllib.request
import re

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)

ydl_audio_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ydl_video_opts = {
    'format': 'bestvideo+bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
}

# Helper function to get the YouTube video URL from a search query
def get_video_url(query):
    if "youtube.com" in query:
        url = query
    else:
        search_keyword = query.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
    return url

def download_video(ydl_opts, url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        file_path = ydl.prepare_filename(info)
        ydl.download([url])
    return file_path

@bot.message_handler(commands=["downloadvideo"])
def downloadvideo(message):
    text = message.text.split(' ', 1)  # divide a mensagem em duas partes
    if len(text) > 1:
        video_url = text[1]
        bot.send_message(message.chat.id, "Estou baixando o vídeo por favor aguarde...")
        url = get_video_url(video_url)
        file_path = download_video(ydl_video_opts, url)
        
        # Verifica se o arquivo .mp4 existe
        mp4_file_path = file_path.replace('.webm', '.mp4')
        if os.path.exists(mp4_file_path):
            bot.send_message(message.chat.id, "Aqui está o vídeo:")
            with open(mp4_file_path, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)
    else:
        bot.send_message(message.chat.id, "Por favor, forneça a URL do vídeo ou o nome. Exemplo: /downloadvideo urldovideo")

@bot.message_handler(commands=["start"])
def send_hello(message):
    bot.reply_to(message, 
                 """
                 Hello, i'am BotFofo! My function is download videos from youtube! Choose a option from bellow:\n
/downloadvideo Download a video with the best quality possible\n
/downloadaudio Download a audio from video with the best quality possible""")
    
def verify(message):
    return True

@bot.message_handler(func=verify)
def reply(message):
    bot.reply_to(message, "Hello how can i help you?")

bot.infinity_polling()