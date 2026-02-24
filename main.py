import os
from random import randint

import requests
from environs import Env
import telegram


def get_comics(url):
	''' Скачивает комикс и получает подпись к комиксу'''
	payload_url = f'{url}info.0.json'
	response = requests.get(payload_url)
	response.raise_for_status()
	response_payload = response.json()
	img_url = response_payload['img']

	post_scriptum_text = response_payload['alt']

	response_img = requests.get(img_url)
	response_img.raise_for_status()
	file_ext = get_ext_from_url(response_img.url)
	file_name = f'comics{file_ext}'
	with open(file_name, 'wb') as file:
		file.write(response_img.content)
	
	return post_scriptum_text, file_name

def get_ext_from_url(url):
	ext = os.path.splitext(url)[1]
	return ext

def get_bot_inf():
	'''Получает информацию о ТГ боте'''
	env = Env()
	env.read_env()
	chat_id = env.str('CHAT_ID')
	bot = telegram.Bot(token=env.str('BOT_TOKEN'))
	return bot, chat_id

def publish_post(text, photo):
	'''Публикует комикс в тг'''
	bot, chat_id = get_bot_inf()
	with open(photo, 'rb') as file:
		bot.send_photo(
			chat_id=chat_id,
			photo=file,
			caption=text
		)

def delete_comics(file_name):
		os.remove(file_name)

def get_num_last_comics():
	'''Получает номер последнего вышедшего комикса'''
	url = 'https://xkcd.com/info.0.json'
	response = requests.get(url)
	response.raise_for_status()
	response_payload = response.json()
	last_num = response_payload['num']
	return last_num

if __name__ == '__main__':
	last_comics_num = get_num_last_comics()
	random_comics_num = randint(1, last_comics_num)
	url = f'https://xkcd.com/{random_comics_num}/'
	text, file_name = get_comics(url)
	publish_post(text, file_name)
	delete_comics(file_name)