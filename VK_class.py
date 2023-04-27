import requests
import json, datetime
import os, tqdm

from pprint import pprint

class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}
       self.__json_foto = []

   def get_user_photo_property(self, user_id, album_id = 'profile', count = 5):
       self.add_to_log('Запущена процедура получения ссылок для загрузки фото')
       url = 'https://api.vk.com/method/photos.get'
       params = {'user_id': user_id, 'album_id': album_id, 'count': count, 'extended':1, 'photo_sizes':1}
       try:
            responce = requests.get(url, params ={**self.params, **params})
            dict_of_pict = {}
            for url_f in responce.json()['response']['items']:
                if f"{url_f['likes']['count']}" in dict_of_pict:
                    dict_of_pict[f"{url_f['likes']['count']}_{url_f['date']}"] = max_in_list(url_f['sizes'])['url']
                    self.__json_foto.append({'file_name':f"{url_f['likes']['count']}_{url_f['date']}.jpg", 'size':max_in_list(url_f['sizes'])['type']})
                else:
                    dict_of_pict[f"{url_f['likes']['count']}"] = max_in_list(url_f['sizes'])['url']
                    self.__json_foto.append({'file_name':f"{url_f['likes']['count']}.jpg", 'size':max_in_list(url_f['sizes'])['type']})
       except Exception as e:
           self.add_to_log(f'Ошибка {repr(e)} в процедуре построения перечня ссылок на фото')
           exit()
       self.add_to_log(f'Успешно получены ссылки на {len(dict_of_pict)} фотографий для загрузки')
       return dict_of_pict
   
   
   def make_json_uploaded_files(self):
        self.add_to_log('Запущена процедура построения json-file с перечнем загруженных на ЯДиск фото')
        try:
            with open(os.getcwd()+'/uploaded_files.json','w') as js_file:
                json.dump(self.__json_foto, js_file)
        except Exception as e:
            self.add_to_log(f'В процедуре построения json-file произошла ошибка:{e.args[0]}')
        self.add_to_log('Процедура построения json-file с перечнем загруженных на ЯДиск фото успешно выполнена')    
        return

   def add_to_log(self, text):
        with open(os.getcwd()+'/log.txt', 'a', encoding= 'utf-8') as file:
            file.write(f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:'+text+'\n')

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        """Метод настраивает заголовок запроса"""
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
   
    def _upload_list_of_photo(self, **dict_of_pict):
        """Метод загружает файлы, расположенные по содержащимся в dict_of_pict url-адресах на яндекс диск"""
        header = self.get_headers()
        param1 = {"path": f'Загрузка_{datetime.date.today()}', "overwrite": "true"}
        try:
            requests.put("https://cloud-api.yandex.net/v1/disk/resources/", headers = header, params = param1)
            for i, val in tqdm.tqdm(dict_of_pict.items(), desc = f'Загрузка файлов'):
                param = {"path": 'Загрузка_'+str(datetime.date.today())+f'/{i}.jpg', "overwrite": "true", "url": val}
                res = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload", headers=header, params=param, stream = True)
                size_foto = requests.get(val, stream=True).headers['Content-length']
                self.add_to_log(f'Успешно загружена фотография {i}.jpg размером {round(int(size_foto)/1024)}Kb')
        except Exception as e:
            self.add_to_log(f'В процедуре загрузки файлов на ЯДиск произошла ошибка: {e.args[0]}')
            exit()
        return   
    
    def add_to_log(self, text):
        with open(os.getcwd()+'/log.txt', 'a', encoding= 'utf-8') as file:
            file.write(f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:'+text+'\n')

    def Backup_VKphoto_to_YDisk(self, user_id = None, access_token = None, album_id = 'profile', count = 5):
        try:
            if access_token == None:
                access_token = get_settings('VKtoken')
            if user_id == None:
                user_id = get_settings('VKid')
            vk = VK(access_token, user_id)
            par = vk.get_user_photo_property(user_id, album_id, count)
            vk.make_json_uploaded_files()
            self._upload_list_of_photo(**par)
        except Exception as e:
            self.add_to_log(f'В процедуре загрузки фото пользователя из Вконтакте произошла ошибка:{e.args[0]}')
            exit()
        
        self.add_to_log('Процедура загрузки фото пользователя из Вконтакте успешно выполнена')
        return


def get_settings(key):
    """метод получения авторизационных данных"""
    try:
        with open(os.getcwd() + '/settings.json','r',encoding= 'utf-8') as f_s:
            return json.load(f_s)[key] 
    except FileNotFoundError:
        print('Файл с параметрами не найден, попробуйте задать их вручную!')
        exit()
          
       
def max_in_list(my_list):
    dict_for_sort = {'s':1, 'm':2, 'x':3, 'o':4,'p':5,'q':6,'r':7,'y':8,'z':9,'w':10}
    return sorted(my_list, key = lambda x:dict_for_sort[x["type"]])[-1]

if __name__ == '__main__':
    uploader = YaUploader(get_settings('Ytoken'))
    uploader.Backup_VKphoto_to_YDisk(count = 15)





