# CuteBotYTD

<div style="display: flex; justify-content: center;">
<div style="width: 80%;">
<div style="text-align: center">

![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)&nbsp;
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat-squeare&logo=telegram&logoColor=white)&nbsp;

CuteBot YTD is the acronym for CuteBot YouTube Downloader.

## About the project
The objective of this project is to develop a bot for the Telegram platform capable of downloading videos and
audios from YouTube videos and sending them to the user who made the request. Throughout this README you will 
find instructions for creating your own bot and executing this code.

## Creating a bot
The first step to creating a bot is to start a conversation with [BotFather](https://telegram.me/BotFather),
BotFather is a bot from Telegram itself that creates other bots.
After that follow these simple steps:

1. Start a conversation with /start
2. Enter /newbot command
3. Make a name for your bot, don't be worry you can change it later
4. Make a username for your bot, be carefull you CANNOT change after this
5. Copy the API TOKEN

Congratulations, you made a bot!

## Dependencies

- FFMPEG
- Python 3.7 or superior

## Install FFMPEG

Windows:
```sh
https://www.ffmpeg.org/download.html#build-windows
```

MacOS
```sh
brew install ffmpeg
``` 

Linux (Ubuntu)
```sh
sudo apt-get install ffmpeg
``` 

## Running the code
First of all clone this repository into you computer

```sh 
  git clone https://github.com/DaniloNicacio/TelegramBot.git
```

CD into folder

```sh
  cd TelegramBot
```

Create a .env file to save your API TOKEN, in this example we are using Nano but feel free to use any editor you want

```sh
  nano .env
```

Use this structure in your .env file:

```sh
  BOT_TOKEN="YOUR_TOKEN_GOES_HERE"
```

After this install the python dependencies with:

```sh
  pip install -r requirements.txt
```

And run the code with:

```sh
  python main.py
```

or

```sh
  python3 main.py
```

## Testing the bot

To test your bot open the Telegram into you Browser or Mobile App and search for the bot username,
the username has this structure: @botusername

The bot only have three commands:

### /downloadvideo <i>url or video name</i>
This command will download the video and send it to user, due to internet conection and file size maybe gonna take a while to send it

### /downloadaudio <i>url or video name</i>
This command will download the audio and send it to user, this command have support to playlists too

### /start
Basically is a welcome message with the commands and previous funcionalities

## Limitations

After all my tests i can list these limitations:

- It's not possible to download videos from playlist links
- Videos that exceed 1 hour cannot be downloaded
- If one of the videos in playlist is privated, the /downloadaudio will not send the audios
- The bot does not handle if the user inserts a link that is not from YouTube
- The get_url function will only return the first result of the search case the user enter a name instead a valid url
- The download commands can accept the name of the video, but if the video name contains spaces it will download the video based on the first word
- If the user enters a name with an accent in the download commands, the bot will not be able to download the video
