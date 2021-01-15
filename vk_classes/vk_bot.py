from vk_classes.vk_processing import VkProcessing

bot = VkProcessing()

for event in bot.longpoll.listen():
    if event.type == bot.event_type.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            if msg == 'привет' or msg == 'ку' or msg == 'хай' or msg == 'хелло':
                user_info = bot.get_user_info(user_id)
                bot.process_user_info(user_info)
                bot.write_msg(user_id, f'Здравствуйте, {bot.name}!')
            elif msg == 'пока' or msg == 'бб' or msg == 'до свидания':
                bot.write_msg(user_id, 'До свидания!')
            elif msg == f'{user_id}':
                info = bot.get_user_info(user_id)
                bot.process_user_info(info)
                search_res = bot.users_search()
                bot.getting_search_list(search_res)
                candidates = bot.get_candidates()
                bot.write_json(candidates)
                upload_url = bot.get_upload_url(user_id)
                upload_file = bot.get_upload_file()
                bot.write_msg(user_id, f'Ваш список кандидатов:\n{bot.upload_file(upload_url, upload_file)}')
                bot.delete_json()
            elif msg == '-' or msg == 'дальше' or msg == 'нет':
                candidates = bot.get_candidates()
                bot.write_json(candidates)
                upload_url = bot.get_upload_url(user_id)
                upload_file = bot.get_upload_file()
                bot.write_msg(user_id, f'Ваш список кандидатов:\n{bot.upload_file(upload_url, upload_file)}')
                bot.delete_json()
            else:
                bot.write_msg(user_id, 'Я вас не понимаю =(')
