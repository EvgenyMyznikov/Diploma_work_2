from vk_classes.vk_requests import VkRequests
from vk_classes.vkinder_db import Client, Photos, SearchData, engine
from sqlalchemy.orm import sessionmaker


class SQLiteClient:

	def __init__(self):
		self.Session = sessionmaker(bind=engine)
		self.session = self.Session()
		self.info = VkRequests()

	def save_user(self, user_id):
		vk_info = self.info.get_user_info(user_id)
		clients = []
		for row in self.session.query(Client.vk_id.label('vk_id_label')).all():
			clients.append(row.vk_id_label)
		if user_id not in clients:
			vk_user_info = Client(
				vk_id=vk_info['id'],
				first_name=vk_info['first_name'],
				last_name=vk_info['last_name'],
				sex=vk_info['sex'],
				city=vk_info['city']['id'],
				url='https://vk.com/id' + str(user_id)
			)
			self.session.add(vk_user_info)
			self.session.commit()

	def save_user_result(self, candidates, user_id):
		counter = 1
		for elem in candidates:
			variants = SearchData(
				vk_id=int(elem[f'{counter}']['URL'][9:]),
				name=elem[f'{counter}']['Name'],
				url=elem[f'{counter}']['URL'],
				client_id=user_id
			)
			counter += 1
			self.session.add(variants)
		self.session.commit()

	def save_photos(self, candidates, user_id):
		counter = 1
		for elem in candidates:
			for photo in elem[f'{counter}']['Photo']:
				for el in photo.items():
					user_photo = Photos(
						likes=el[0],
						url=el[1],
						variant_id=int(elem[f'{counter}']['URL'][9:]),
						client_id=user_id
					)
					self.session.add(user_photo)
			counter += 1
		self.session.commit()

	def query_to_result(self):
		for instance in self.session.query(SearchData).order_by(SearchData.id):
			print(instance.vk_id, instance.name, instance.url)


if __name__ == '__main__':
	sq = SQLiteClient()
	sq.save_user()
