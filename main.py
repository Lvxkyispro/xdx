import telebot
from spotdl import Spotdl
import os

# Initialize your tokens
BOT_TOKEN = '7358264322:AAGSoQhHaMsQ5oDLJ6FIrUFYG-mLeHHZmCI'
SPOTIFY_CLIENT_ID = 'adeb4dba3b394d7eaca55156ada61e19'
SPOTIFY_CLIENT_SECRET = '288af4dc9b904c6b8e8da81395f282aa'

bot = telebot.TeleBot(BOT_TOKEN)

# Initialize spotdl with Spotify credentials
spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /dl {song name} to download music")

@bot.message_handler(commands=['dl'])
def download_music(message):
    try:
        # Get the song name from the message
        song_query = message.text.replace('/dl ', '')
        
        if not song_query:
            bot.reply_to(message, "Please provide a song name!")
            return

        # Send "downloading" message
        status_message = bot.reply_to(message, "🎵 Searching and downloading your song...")
        
        # Search and download the song
        songs = spotdl.search([song_query])
        song = spotdl.download(songs[0])
        
        # Send the downloaded song
        with open(song[0], 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)
        
        # Delete the downloaded file
        os.remove(song[0])
        
        # Delete the "downloading" message
        bot.delete_message(message.chat.id, status_message.message_id)
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Use /dl {song name} to download music")

# Start the bot
bot.polling()
