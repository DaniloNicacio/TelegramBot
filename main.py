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

def get_video_url(query):
    if "youtube.com" in query or "youtu.be" in query:
        url = query
    else:
        search_keyword = query.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        if video_ids:
            url = "https://www.youtube.com/watch?v=" + video_ids[0]
        else:
            url = None
    return url

def seconds_to_minutes(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"

def download_video(ydl_opts, url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        file_path = ydl.prepare_filename(info)
        ydl.download([url])
    
    if ydl_opts == ydl_video_opts:
        mp4_file_path = file_path.replace('.webm', '.mp4')
        if os.path.exists(mp4_file_path):
            video_name = info.get('title', 'Unknown')
            duration_seconds = info.get('duration', 'Unknown')
            duration_formatted = seconds_to_minutes(duration_seconds)
            file_size = os.path.getsize(mp4_file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            return mp4_file_path, video_name, duration_formatted, file_size_mb
        else:
            return None, None, None, None
    else:
        mp3_file_path = file_path.replace('.webm', '.mp3')
        if os.path.exists(mp3_file_path):
            video_name = info.get('title', 'Unknown')
            duration_seconds = info.get('duration', 'Unknown')
            duration_formatted = seconds_to_minutes(duration_seconds)
            file_size = os.path.getsize(mp3_file_path)
            file_size_mb = file_size / (1024 * 1024)
            
            return mp3_file_path, video_name, duration_formatted, file_size_mb
        else:
            return None, None, None, None

def send_audio_messages(chat_id, audio_files):
    for audio_file in audio_files:
        with open(audio_file, 'rb') as audio:
            bot.send_audio(chat_id, audio, timeout= 5000)
        os.remove(audio_file)

@bot.message_handler(commands=["downloadvideo"])
def downloadvideo(message):
    text = message.text.split(' ', 1)
    if len(text) > 1:
        video_url = text[1]
        url = get_video_url(video_url)
        info = yt_dlp.YoutubeDL().extract_info(url, download=False, process=False)
        
        if 'entries' in info:
            bot.send_message(message.chat.id, "Please, do not put playlists url here, use /downloadaudio instead")
        else:
            bot.send_message(message.chat.id, "I'm downloading the video, please wait…\nNote: The waiting time may vary according to the size of the video.")
            mp4_file_path, video_name, duration_formatted, file_size_mb = download_video(ydl_video_opts, url)
            if mp4_file_path:
                bot.send_message(message.chat.id, f"Here is the video:\nTitle: {video_name}\nDuration: {duration_formatted}\nFile Size: {file_size_mb:.2f} MB")
                with open(mp4_file_path, 'rb') as video_file:
                    bot.send_video(message.chat.id, video_file, timeout= 5000)
                os.remove(mp4_file_path)
            else:
                bot.send_message(message.chat.id, "Timeout problem :/, please try again")
                for file in os.listdir():
                    if file.endswith(".webm"):
                        os.remove(file)
    else:
        bot.send_message(message.chat.id, "Please provide the video URL or name. Example: /downloadvideo videourl")

@bot.message_handler(commands=["downloadaudio"])
def downloadaudio(message):
    text = message.text.split(' ', 1)
    if len(text) > 1:
        video_url = text[1]
        bot.send_message(message.chat.id, "I'm downloading the audio, please wait…\nNote: The waiting time may vary according to the size of the video.")
        url = get_video_url(video_url)
        info = yt_dlp.YoutubeDL().extract_info(url, download=False, process=False)
        
        if 'entries' in info:
            bot.send_message(message.chat.id, "Playlist detected. Downloading all audios in the playlist.")
            audio_files = []
            for entry in info['entries']:
                audio_url = entry['url']
                mp3_file_path, video_name, duration_formatted, file_size_mb = download_video(ydl_audio_opts, audio_url)
                if mp3_file_path:
                    audio_files.append(mp3_file_path)
            send_audio_messages(message.chat.id, audio_files)
            bot.send_message(message.chat.id, "All audios from the playlist have been downloaded.")
        else:
            # This is a single video
            mp3_file_path, video_name, duration_formatted, file_size_mb = download_video(ydl_audio_opts, url)
            if mp3_file_path:
                bot.send_message(message.chat.id, f"Here is the audio:\nTitle: {video_name}\nDuration: {duration_formatted}\nFile Size: {file_size_mb:.2f} MB")
                with open(mp3_file_path, 'rb') as audio_file:
                    bot.send_audio(message.chat.id, audio_file, timeout= 5000)
                os.remove(mp3_file_path)
            else:
                bot.send_message(message.chat.id, "Timeout problem :/, please try again")
                for file in os.listdir():
                    if file.endswith(".webm"):
                        os.remove(file)
    else:
        bot.send_message(message.chat.id, "Please provide the video URL or name. Example: /downloadvideo videourl")

@bot.message_handler(commands=["start"])
def send_hello(message):
    bot.reply_to(message, 
                 """
                 Hello, i'am BotFofo! My function is download videos from youtube! Choose a option from bellow:\n
/downloadvideo Download a video with the best quality possible\n
/downloadaudio Download a audio from video with the best quality possible\n
Note: Please, do not put videos with more than 1 hour duration, i can't handle videos with that size\n
Do not put playlists url in video download command, i don't have support for this...\n
But feel free to put in audio download command :)""")
    
def verify(message):
    return True

@bot.message_handler(func=verify)
def reply(message):
    bot.reply_to(message, "Hello how can i help you?")

bot.infinity_polling()
