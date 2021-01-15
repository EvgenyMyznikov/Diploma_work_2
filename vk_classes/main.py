from vk_processing import VkProcessing

get_rec = VkProcessing()
user_info = get_rec.get_user_info('ins user_id')
get_rec.process_user_info(user_info)
search_res = get_rec.users_search()
get_rec.getting_search_list(search_res)
candidates = get_rec.get_candidates()
get_rec.write_json(candidates)
upload_url = get_rec.get_upload_url('ins user_id')
upload_file = get_rec.get_upload_file()
get_rec.upload_file(upload_url, upload_file)
get_rec.delete_json()
