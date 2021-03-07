import requests
import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_classes.vk_config import my_token, gp_token, vk_api_url
from vk_api.exceptions import ApiError


class VkRequests:

	def __init__(self):
		self.url = vk_api_url
		self.vk_token = my_token
		self.vk_group_token = gp_token
		self.vk_session = vk_api.VkApi(token=gp_token)
		self.session_api = self.vk_session.get_api()
		self.longpoll = VkLongPoll(self.vk_session)
		self.event_type = VkEventType
		self.search_list = []
		self.sex = 0

	def get_countries(self):
		params = {
			'access_token': self.vk_token,
			'need_all': 1,
			'count': 1000,
			'v': 5.126
		}
		try:
			response = requests.get(self.url + 'database.getCountries', params=params)
			countries = response.json()['response']['items']
			return countries
		except ApiError:
			return 'Нет доступа'
		except KeyError:
			return 'Проблема'

	def get_cities(self, country):
		params = {
			'access_token': self.vk_token,
			'country_id': country,
			'need_all': 0,
			'count': 1000,
			'v': 5.126
		}
		try:
			response = requests.get(self.url + 'database.getCities', params=params)
			cities = response.json()['response']['items']
			return cities
		except ApiError:
			return 'Нет доступа'
		except KeyError:
			return 'Проблема'

	def get_user_info(self, user_id):
		""" Получаем информацию о пользователе из VK по id """
		params = {
			'access_token': self.vk_group_token,
			'user_ids': user_id,
			'fields': 'bdate, sex, city, relation',
			'v': 5.126
		}
		try:
			response = requests.get(self.url + 'users.get', params=params)
			user_info = response.json()['response'][0]
			return user_info
		except ApiError:
			return 'Нет доступа'
		except KeyError:
			return 'Проблема'

	def users_search(self, city, min_age, max_age):
		""" Поиск подходящих под условия вариантов """
		if self.sex == 1:
			self.sex = 2
		else:
			self.sex = 1
		params = {
			'access_token': self.vk_token,
			'count': 1000,
			'city': city,
			'sex': self.sex,
			'status': 6,
			'age_from': min_age,
			'age_to': max_age,
			'has_photo': 1,
			'v': 5.126
		}
		try:
			response = requests.get(self.url + 'users.search', params=params)
			search_res = response.json()['response']['items']
			return search_res
		except ApiError:
			return 'Нет доступа'
		except KeyError:
			return 'Проблема'

	def get_photos(self, candidate_id):
		""" Получаем фотографии по id """
		params = {
			'access_token': self.vk_token,
			'owner_id': candidate_id,
			'album_id': 'profile',
			'rev': 0,
			'extended': 1,
			'count': 10,
			'v': 5.126
		}
		try:
			response = requests.get(self.url + 'photos.get', params=params)
			photo_res = response.json()['response']['items']
			return photo_res
		except ApiError:
			return 'Нет доступа'
		except KeyError:
			return 'Проблема'

	def get_upload_url(self, user_id):
		""" Получаем ссылку на сервер загрузки файла """
		params = {
			'access_token': self.vk_group_token,
			'type': 'doc',
			'peer_id': user_id,
			'v': 5.126
		}
		try:
			response = requests.get(self.url + 'docs.getMessagesUploadServer', params=params)
			upload_url = response.json()['response']['upload_url']
			return upload_url
		except ApiError:
			return 'Нет доступа'
		except KeyError:
			return 'Проблема'

	@staticmethod
	def get_upload_file():
		""" Файл для загрузки """
		upload_file = {'file': ('matches.json', open('matches.json', 'rb'))}
		return upload_file

	def upload_file(self, upload_url, upload_file):
		""" Загружаем подготовленный файл на сервер ВК """
		response = requests.post(upload_url, files=upload_file)
		save_file = self.vk_session.method('docs.save', {
			'file': response.json()['file'],
			'title': 'Matches',
			'v': 5.126
		})['doc']['url']
		return save_file

	def write_msg(self, user_id, text):
		""" Метод для отправки сообщений """
		params = {
			'access_token': self.vk_group_token,
			'user_id': user_id,
			'message': text,
			'random_id': randrange(10 ** 7),
			'v': 5.126
		}
		response = requests.get(self.url + 'messages.send', params=params)
		return response
