import os

import requests
from environs import Env
import telegram


def get_comics(url):
	payload_url = f'{url}info.0.json'
	response = requests.get(payload_url)
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
	env = Env()
	env.read_env()
	chat_id = env.str('CHAT_ID')
	bot = telegram.Bot(token=env.str('BOT_TOKEN'))
	return bot, chat_id

def publish_post(text, photo):
	bot, chat_id = get_bot_inf()
	with open(photo, 'rb') as file:
		bot.send_photo(
			chat_id=chat_id,
			photo=file,
			caption=text
		)
	message = 'Пост опубликован'
	return message

def delete_comics(file_name):
		os.remove(file_name)


if __name__ == '__main__':
	url = 'https://xkcd.com/353/'
	text, file_name = get_comics(url)
	message = publish_post(text, file_name)
	delete_comics(file_name)
	print(message)
