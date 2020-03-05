import feedparser
import telebot
# from telegram import Bot
# from telegram import Update
# from telegram.ext import CommandHandler
# from telegram.ext import Filters
# from telegram.ext import MessageHandler
# from telegram.ext import Updater

# from bs4 import BeautifulSoup

from config import TG_API_URL
from config import TG_TOKEN

token = TG_TOKEN
base_url = TG_API_URL

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start','help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я (в будущем) бот для автопарсинга новых выпусков с PODSTER.FM\n\nПришли мне сообщение вида /rss "адрес RSS"')

@bot.message_handler(commands=['rss'])
def get_last_episode(message):
	text = message.text
	rss_url = text.replace("/rss ","")
	parser = feedparser.parse(rss_url)

	entry = parser.entries[0]
	title = entry.title
	mp3_url = entry.links[0].href
	mp3_url_2 = "{}/download/audio.mp3".format(mp3_url)
	description = entry.content[0].value
	episode_text = text = "{}\n\n{}\n\n{}".format(title,description,mp3_url)

	bot.send_message(message.chat.id, episode_text)
	audio = open('https://radiotony.podster.fm/1/download/audio.mp3', 'r')
	bot.send_audio(message.chat.id, audio)
	bot.send_audio(message.chat.id, "FILEID")

# def get_rss(bot: Bot, update: Update):


# 	bot.send_audio(
# 		chat_id=update.message.chat_id,
# 		audio=open(mp3_url_2, 'rb')
# 	)

# def main():
# 	bot = Bot(
# 		token=TG_TOKEN,
# 		base_url=TG_API_URL,
# 	)
# 	updater = Updater(
# 		bot=bot,	
# 	)

# 	start_handler = CommandHandler("start", do_start)
# 	message_handler = MessageHandler(Filters.text, get_rss)
	
# 	updater.dispatcher.add_handler(start_handler)
# 	updater.dispatcher.add_handler(message_handler)

# 	updater.start_polling()
# 	updater.idle()

bot.polling()
