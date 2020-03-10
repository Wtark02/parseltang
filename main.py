#!/usr/bin/env python

import feedparser
import telebot
#from bs4 import BeautifulSoup
from config import TG_TOKEN

token = TG_TOKEN
bot = telebot.TeleBot('1137799389:AAGF_kLE4v0jUATJPAtlcXLR-6F0P_naZo8')

@bot.message_handler(commands=['start','help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я (в будущем) бот для автопарсинга новых выпусков\n\nПришли мне сообщение вида /rss "адрес RSS"')

@bot.message_handler(commands=['rss'])
def get_last_episode(message):
	text = message.text
	rss_url = text.replace("/rss ","")
	parser = feedparser.parse(rss_url)

	entry = parser.entries[0]
	title = entry.title
	mp3_url = entry.links[0].href
	mp3_url_2 = entry.enclosures[0].href
	description = entry.content[0].value
	description = description.replace("<p>","")
	description = description.replace("</p>","")
	description = description.replace("<br>","")
	episode_text = text = "{}\n\n{}\n\n{}".format(title,description,mp3_url)
	bot.send_message(message.chat.id, episode_text)
	try:
		audio = open(mp3_url_2, 'rb')
		bot.send_audio(message.chat.id, audio)
		bot.send_audio(message.chat.id, "FILEID")
	except Exception as e:
        	@bot.message_handler(commands = ['url'])
		def url(message):
		    markup = types.InlineKeyboardMarkup()
		    btn_my_site= types.InlineKeyboardButton(text='Слушать выпуск', url=mp3_url_2)
		    markup.add(btn_my_site)
		    bot.send_message(message.chat.id, "Нажми на кнопку, чтобы послушать новый выпуск", reply_markup = markup)

bot.polling()
