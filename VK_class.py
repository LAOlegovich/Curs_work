import requests
import json
import datetime, os
import common_func as C_F



class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.id = user_id
        self.json_foto = []

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self,user_id):
        if C_F.get_settings('Is_screen_name') == 'False':
            self.__id = user_id
        else:
            url = 'https://api.vk.com/method/resolveScreenName'
            params = {**self.params, 'screen_name':user_id}
            resp = requests.get(url,params= params).json()
            if resp['response']['type'] == 'user':
                self.__id = resp['response']['object_id']
            else:
                self.__id = None




    def get_user_photo_property(self, album_id='profile', count=5):
        self.add_to_log(
            'Запущена процедура получения ссылок для загрузки фото')
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id':self.__id,'album_id': album_id,
                  'count': count, 'extended': 1, 'photo_sizes': 1}
        try:
            responce = requests.get(url, params={**self.params, **params})
            dict_of_pict = {}
            for url_f in responce.json()['response']['items']:
                if f"{url_f['likes']['count']}" in dict_of_pict:
                    dict_of_pict[f"{url_f['likes']['count']}_"+
                        datetime.datetime.utcfromtimestamp(
                        url_f['date']).strftime("%d_%m_%Y")] = C_F.max_in_list(
                        url_f['sizes'])['url']
                    self.json_foto.append(
                        {'file_name': f"{url_f['likes']['count']}_"+
                         datetime.datetime.utcfromtimestamp(
                           url_f['date']).strftime("%d_%m_%Y")+".jpg",
                          'size': C_F.max_in_list(url_f['sizes'])['type']})
                else:
                    dict_of_pict[f"{url_f['likes']['count']}"] = C_F.max_in_list(
                        url_f['sizes'])['url']
                    self.json_foto.append(
                        {'file_name': f"{url_f['likes']['count']}.jpg", 
                         'size': C_F.max_in_list(url_f['sizes'])['type']})
        except Exception as e:
            self.add_to_log(
                f'Ошибка {repr(e)} в процедуре построения перечня ссылок на фото')
            exit()
        self.add_to_log(
            f'Успешно получены ссылки на {len(dict_of_pict)} фотографий для загрузки')
        return dict_of_pict


    def add_to_log(self, text):
        with open(os.getcwd()+'/log.txt', 'a', encoding='utf-8') as file:
            file.write(
                f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:'
                f'{text}\n')

