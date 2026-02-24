import os
from random import randint

import requests
from environs import Env
import telegram


def get_comic(url):
	''' Скачивает комикс и получает подпись к комиксу'''
	payload_url = f'{url}info.0.json'
	response = requests.get(payload_url)
	response.raise_for_status()
	response_payload = response.json()
	img_url = response_payload['img']

	post_scriptum_text = response_payload['alt']

	response_img = requests.get(img_url)
	response_img.raise_for_status()
	file_ext = os.path.splitext(response_img.url)[1]
	file_name = f'comic{file_ext}'
	with open(file_name, 'wb') as file:
		file.write(response_img.content)
	
	return post_scriptum_text, file_name


def publish_post(text, photo, chat_id, bot):
	'''Публикует комикс в тг'''
	with open(photo, 'rb') as file:
		bot.send_photo(
			chat_id=chat_id,
			photo=file,
			caption=text
		)

def delete_comic(file_name):
		os.remove(file_name)

def get_lust_comic_num():
	'''Получает номер последнего вышедшего комикса'''
	url = 'https://xkcd.com/info.0.json'
	response = requests.get(url)
	response.raise_for_status()
	response_payload = response.json()
	last_num = response_payload['num']
	return last_num

if __name__ == '__main__':
	env = Env()
	env.read_env()
	chat_id = env.str('CHAT_ID')
	bot_token = env.str('BOT_TOKEN')
	bot = telegram.Bot(token=bot_token)

	last_comic_num = get_lust_comic_num()
	random_comic_num = randint(1, last_comic_num)
	url = f'https://xkcd.com/{random_comic_num}/'
	text, file_name = get_comic(url)

	publish_post(text, file_name, chat_id, bot)
	delete_comic(file_name)