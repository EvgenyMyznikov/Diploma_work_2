from vk_classes.vk_processing import VkProcessing
from Tests.test_config import my_token, vk_id, gp_token, vk_api_url
import requests
from random import randrange
from vk_classes.vk_config import my_token, gp_token, vk_api_url

"""Для начала тестирования необходимо в файл test_config.py внести ваш персональный и групповой токен VK,
а также указать id вашей страницы VK"""


class TestVKRequests:
	def test_get_countries(self):
		params = {
			'access_token': my_token,
			'need_all': 1,
			'count': 1000,
			'v': 5.126
		}
		response = requests.get(vk_api_url + 'database.getCountries', params=params)
		assert response.status_code == 200

	def test_get_cities(self):
		params = {
			'access_token': my_token,
			'country_id': 1,
			'need_all': 0,
			'count': 1000,
			'v': 5.126
		}
		response = requests.get(vk_api_url + 'database.getCities', params=params)
		assert response.status_code == 200

	def test_get_user_info(self):
		params = {
			'access_token': gp_token,
			'user_ids': vk_id,
			'fields': 'bdate, sex, city, relation',
			'v': 5.126
		}
		response = requests.get(vk_api_url + 'users.get', params=params)
		assert response.status_code == 200

	def test_write_msg(self):
		params = {
			'access_token': gp_token,
			'user_id': vk_id,
			'message': 'Test',
			'random_id': randrange(10 ** 7),
			'v': 5.126
		}
		response = requests.get(vk_api_url + 'messages.send', params=params)
		assert response.status_code == 200

	def test_users_search(self):
		params = {
			'access_token': my_token,
			'count': 1000,
			'city': 1,
			'sex': 1,
			'status': 6,
			'age_from': 20,
			'age_to': 25,
			'has_photo': 1,
			'v': 5.126
		}
		response = requests.get(vk_api_url + 'users.search', params=params)
		assert response.status_code == 200

	def test_get_photos(self):
		params = {
			'access_token': my_token,
			'owner_id': vk_id,
			'album_id': 'profile',
			'rev': 0,
			'extended': 1,
			'count': 10,
			'v': 5.126
		}
		response = requests.get(vk_api_url + 'photos.get', params=params)
		assert response.status_code == 200

	def test_get_upload_url(self):
		params = {
			'access_token': gp_token,
			'type': 'doc',
			'peer_id': vk_id}
		response = requests.get(vk_api_url + 'docs.getMessagesUploadServer', params=params)
		assert response.status_code == 200


class TestVkProcessing:
	vk_proc = VkProcessing()

	def test_process_user_info(self):
		self.vk_proc.process_user_info({'sex': 1})
		assert self.vk_proc.sex == 1

	def test_getting_search_list(self):
		search_res = [{
			"id": 41609559,
			"first_name": "Евгений",
			"last_name": "Мызников",
		}]
		search_list = self.vk_proc.getting_search_list(search_res)
		assert search_list == [('vk.com/id41609559', 'Евгений Мызников')]

	def test_get_photo_list(self):
		photo_res = self.vk_proc.get_photos(41609559)
		photos = self.vk_proc.get_photos_list(photo_res)
		assert photos != []

	def test_get_top_photos(self):
		vk_proc = VkProcessing()
		photo_res = vk_proc.get_photos(41609559)
		photos = vk_proc.get_photos_list(photo_res)
		top_photos = vk_proc.top_photos(photos)
		assert top_photos != []
