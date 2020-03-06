#!/usr/bin/env python

import feedparser
import telebot
#from bs4 import BeautifulSoup
from config import TG_TOKEN

token = TG_TOKEN
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
	try:
		audio = open('/tmp/audio.mp3', 'rb')
		bot.send_audio(message.chat.id, audio)
		bot.send_audio(message.chat.id, "FILEID")
	except Exception as e:
        	bot.send_message(message.chat.id, mp3_url_2)

bot.polling()
