from vk_classes.vk_requests import VkRequests
import time
import json
import os


class VkProcessing(VkRequests):

    def __init__(self):
        super().__init__()
        self.name = ''

    def process_user_info(self, user_info):
        """Получаем информацию о людях, подходящих под условия, на основании информации о пользователе из VK:
        возраст,пол,город,семейное положение.
        """
        self.age = 2021 - int(user_info['bdate'][-4:])
        self.city = user_info['city']['id']
        self.sex = user_info['sex']
        self.name = user_info['first_name']
        return self.age, self.city, self.sex, self.name

    def getting_search_list(self, search_res):
        """ Получаем список результатов поиска """
        for search in search_res:
            first_name = search['first_name']
            last_name = search['last_name']
            found_id = search['id']
            vk_url = f'vk.com/id{found_id}'
            self.search_list.append((vk_url, first_name + ' ' + last_name))
        # print(self.search_list)
        return self.search_list

    @staticmethod
    def top_photos(photo_res):
        """ Отбираем 3 лучшие фотографии по лайкам """
        photos = []
        for elem in photo_res:
            photo = elem['sizes'][-1]['url']
            likes = elem['likes']['count']
            photos.append((likes, photo))
        photos = sorted(photos, reverse=True)
        top_photos = []
        for elem in photos[0:3]:
            like = elem[0]
            best_photo = elem[1]
            top_photos.append({f'Likes:{like}': best_photo})
        return top_photos

    def get_candidates(self):
        """ Получаем список из 10 кандидатов """
        candidates = []
        counter = 1
        for elem in self.search_list:
            if counter < 11:
                candidate_id = int(elem[0][9:])
                get_photo = VkRequests.get_photos(self, candidate_id)
                top_photo = VkProcessing.top_photos(get_photo)
                self.search_list.pop(0)
                time.sleep(0.5)
                data = {f'{counter}': {'Name': elem[1], 'Photo': top_photo, 'URL': elem[0]}}
                counter += 1
                candidates.append(data)
        return candidates

    @staticmethod
    def write_json(candidates):
        """ Записываем полученный список в json файл """
        matches = {'Matches': candidates}
        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, ensure_ascii=False, indent=4)
            return matches

    @staticmethod
    def delete_json():
        """ Удаление файла из папки """
        json_to_delete = 'matches.json'
        if os.path.isfile(json_to_delete):
            os.remove(json_to_delete)
        else:
            print('Error:File not found!')
