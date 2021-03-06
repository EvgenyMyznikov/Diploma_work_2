from vk_classes.vk_requests import VkRequests
import time
import json
import os


class VkProcessing(VkRequests):

	def __init__(self):
		super().__init__()

	def process_user_info(self, user_info):
		"""Получаем информацию о людях, подходящих под условия, на основании информации о пользователе из VK:
		пол.
		"""
		self.sex = user_info['sex']
		return self.sex

	def getting_search_list(self, search_res):
		"""Получаем результаты поиска по условиям пользователя VK: Имя, Фамилия, ссылка на страницу"""
		for search in search_res:
			first_name = search['first_name']
			last_name = search['last_name']
			found_id = search['id']
			vk_url = f'vk.com/id{found_id}'
			self.search_list.append((vk_url, first_name + ' ' + last_name))
		return self.search_list

	@staticmethod
	def get_photos_list(photo_res):
		"""Получаем фотографии профиля пользователя"""
		photos = []
		for elem in photo_res:
			photo = elem['sizes'][-1]['url']
			likes = elem['likes']['count']
			photos.append((likes, photo))
		photos = sorted(photos, reverse=True)
		return photos

	@staticmethod
	def top_photos(photos):
		"""Сортируем фотографии по лайкам и отбираем три лучших"""
		top_photos = []
		for elem in photos[0:3]:
			like = elem[0]
			best_photo = elem[1]
			top_photos.append({f'Likes:{like}': best_photo})
		return top_photos

	def get_candidates(self):
		"""Подготавливаем шаблон с результатом поиска и лучшими фотографиями конкретного результата поиска"""
		candidates = []
		counter = 1
		for elem in self.search_list:
			if counter < 10:
				candidate_id = int(elem[0][9:])
				get_photo = VkRequests.get_photos(self, candidate_id)
				photo_list = VkProcessing.get_photos_list(get_photo)
				top_photo = VkProcessing.top_photos(photo_list)
				self.search_list.pop(0)
				time.sleep(0.5)
				data = {f'{counter}': {'Name': elem[1], 'Photo': top_photo, 'URL': elem[0]}}
				counter += 1
				candidates.append(data)
		return candidates

	@staticmethod
	def write_json(candidates):
		"""Записываем JSON файл"""
		matches = {'Matches': candidates}
		with open('matches.json', 'w', encoding='utf-8') as f:
			json.dump(matches, f, ensure_ascii=False, indent=4)
			return matches

	@staticmethod
	def delete_json():
		"""Удаляем JSON файл"""
		json_to_delete = 'matches.json'
		if os.path.isfile(json_to_delete):
			os.remove(json_to_delete)
		else:
			print('Error:File not found!')

