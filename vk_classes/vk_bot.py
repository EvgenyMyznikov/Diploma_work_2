print('bot started...')
stop = False
while not stop:
	try:

		from vk_classes.vk_processing import VkProcessing
		from vk_classes.session import SQLiteClient
		import time


		class VKinderBot:

			def __init__(self):
				self.bot = VkProcessing()
				self.sq = SQLiteClient()
				self.cntry = 0
				self.town = 0
				self.countries = []
				self.cities = []
				self.min_age = int()
				self.max_age = int()

			def say_hello(self, user_id):
				user_info = self.bot.get_user_info(user_id)
				self.sq.save_user(user_id)
				self.bot.process_user_info(user_info)
				self.bot.write_msg(user_id, f'Здравствуйте!')

			def all_countries(self):
				for country in self.bot.get_countries():
					self.countries.append((country['id'], country['title'].lower()))
				return self.countries

			def all_cities(self, cntry):
				for city in self.bot.get_cities(cntry):
					self.cities.append((city['id'], city['title'].lower()))
				return self.cities

			def find_user_country_id(self, msg):
				for country in self.countries:
					if msg == country[1]:
						self.cntry = int(country[0])
				return self.cntry

			def find_user_city_id(self, msg):
				for city in self.cities:
					if msg == city[1]:
						self.town = int(city[0])
				return self.town

			def get_variants_json(self, user_id):
				info = self.bot.get_user_info(user_id)
				self.bot.process_user_info(info)
				search_res = self.bot.users_search(city=self.town, min_age=self.min_age, max_age=self.max_age)
				self.bot.getting_search_list(search_res)
				candidates = self.bot.get_candidates()
				self.sq.save_user_result(candidates, user_id)
				self.sq.save_photos(candidates, user_id)
				self.bot.write_json(candidates)
				upload_url = self.bot.get_upload_url(user_id)
				upload_file = self.bot.get_upload_file()
				self.bot.write_msg(user_id, f'Ваш список кандидатов:\n{self.bot.upload_file(upload_url, upload_file)}')
				self.bot.delete_json()

			def next_variants(self, user_id):
				candidates = self.bot.get_candidates()
				self.sq.save_user_result(candidates, user_id)
				self.sq.save_photos(candidates, user_id)
				self.bot.write_json(candidates)
				upload_url = self.bot.get_upload_url(user_id)
				upload_file = self.bot.get_upload_file()
				self.bot.write_msg(user_id, f'Ваш список кандидатов:\n{self.bot.upload_file(upload_url, upload_file)}')
				self.bot.delete_json()

			def say_goodbye(self, user_id):
				self.bot.write_msg(user_id, f'До свидания!')

			def dont_understand(self, user_id):
				self.bot.write_msg(user_id, f'Я вас не понимаю =(')

			def need_min_age(self, user_id):
				self.bot.write_msg(user_id, 'Пожалуйста, напишите минимальный возраст поиска')

			def need_max_age(self, user_id):
				self.bot.write_msg(user_id, 'Пожалуйста, напишите максимальный возраст поиска')

			def need_country(self, user_id):
				self.bot.write_msg(user_id, 'Пожалуйста, напишите страну вашего проживания')

			def need_city(self, user_id):
				self.bot.write_msg(user_id, 'Пожалуйста, напишите город вашего проживания')

			def start(self):
				for event in self.bot.longpoll.listen():

					if event.type == self.bot.event_type.MESSAGE_NEW:

						if event.to_me:

							msg = event.text.lower()
							user_id = event.user_id

							if msg == 'привет' or msg == 'ку' or msg == 'хай' or msg == 'хелло':
								self.say_hello(user_id)
								self.all_countries()

							elif msg == 'пока' or msg == 'бб' or msg == 'до свидания':
								self.say_goodbye(user_id)

							elif msg == 'хочу найти пару':
								self.need_min_age(user_id)

							elif msg.isdigit():

								if self.min_age == 0:
									self.min_age = int(msg)
									self.need_max_age(user_id)

								elif self.min_age != 0:
									self.max_age = int(msg)
									self.need_country(user_id)

							elif msg in [country[1] for country in self.countries]:
								self.find_user_country_id(msg)
								self.need_city(user_id)
								self.all_cities(self.cntry)

							elif msg in [town[1] for town in self.cities]:
								self.find_user_city_id(msg)
								self.get_variants_json(user_id)
								self.sq.query_to_result()

							elif msg == '-' or msg == 'дальше' or msg == 'нет':
								self.next_variants(user_id)

							else:
								self.dont_understand(user_id)


		if __name__ == '__main__':
			bot = VKinderBot()
			bot.start()

	except Exception as error_msg:
		print(f'error!    {error_msg}')
		time.sleep(3)
		print('restart...')
