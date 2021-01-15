import requests
import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_classes.vk_config import my_token, gp_token, vk_api_url


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
        self.city = 0
        self.age = 0

    def get_user_info(self, user_id):
        """ Получаем информацию о пользователе из VK по id """
        params = {
            'access_token': self.vk_group_token,
            'user_ids': user_id,
            'fields': 'bdate, sex, city',
            'v': 5.126
        }
        # response = requests.get(self.url + 'users.get', params=params)
        user_info = self.vk_session.method('users.get', values=params)[0]
        # print(user_info)
        return user_info

    def users_search(self):
        """ Поиск подходящих под условия вариантов """
        if self.sex == 1:
            self.sex = 2
        else:
            self.sex = 1
        params = {
            'access_token': self.vk_token,
            'count': 1000,
            'city': self.city,
            'sex': self.sex,
            'status': 6,
            'age_from': 18,
            'age_to': self.age,
            'has_photo': 1,
            'v': 5.126
        }
        response = requests.get(self.url + 'users.search', params=params)
        search_res = response.json()['response']['items']
        return search_res

    def get_photos(self, candidate_id):
        """ Получаем фотографии по id """
        params = {
            'access_token': self.vk_token,
            'owner_id': candidate_id,
            'album_id': 'profile',
            'rev': 0,
            'extended': 1,
            'count': 50,
            'v': 5.126
        }
        response = requests.get(self.url + 'photos.get', params=params)
        photo_res = response.json()['response']['items']
        return photo_res

    def get_upload_url(self, user_id):
        """ Получаем ссылку на сервер загрузки файла """
        upload_url = self.vk_session.method('docs.getMessagesUploadServer', {
            'type': 'doc',
            'peer_id': user_id
        })['upload_url']
        return upload_url

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
        self.vk_session.method('messages.send', {
            'user_id': user_id,
            'message': text,
            'random_id': randrange(10 ** 7)
        })
