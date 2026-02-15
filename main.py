import os

import requests


# TO DO
# можно написать функцию, которая будет стирать скачанное фото, после публикации

def download_comics(url):
	payload_url = f'{url}info.0.json'
	response = requests.get(payload_url)
	response_payload = response.json()
	img_url = response_payload['img']

	response_img = requests.get(img_url)
	response_img.raise_for_status()
	file_ext = get_ext_from_url(response_img.url)
	with open(f'images/comics{file_ext}', 'wb') as file:
		file.write(response_img.content)

def get_ext_from_url(url):
	ext = os.path.splitext(url)[1]
	return ext


if __name__ == '__main__':
	os.makedirs('images', exist_ok=True)
	url = 'https://xkcd.com/353/'
	download_comics(url)