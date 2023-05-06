import VK_class as V_K
import common_func as C_F
import requests, datetime, tqdm, os

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
        """Метод загружает файлы, расположенные по содержащимся
          в dict_of_pict url-адресах на яндекс диск"""
        header = self.get_headers()
        param1 = {"path": f'Загрузка_{datetime.date.today()}',
                  "overwrite": "true"}
        try:
            requests.put("https://cloud-api.yandex.net/v1/disk/resources/",
                         headers=header, params=param1)
            for i, val in tqdm.tqdm(dict_of_pict.items(), desc=f'Загрузка файлов'):
                param = {"path": 'Загрузка_' +
                         str(datetime.date.today())+f'/{i}.jpg', 
                         "overwrite": "true", "url": val}
                res = requests.post(
                    "https://cloud-api.yandex.net/v1/disk/resources/upload",
                      headers=header, params=param, stream=True)
                size_foto = requests.get(
                    val, stream=True).headers['Content-length']
                self.add_to_log(
                    f'Успешно загружена фотография {i}.jpg '
                    f'размером {round(int(size_foto)/1024)}Kb')
        except Exception as e:
            self.add_to_log(
                f'В процедуре загрузки файлов на ЯДиск произошла ошибка: {repr(e)}')
            exit()
        return

    def add_to_log(self, text):
        with open(os.getcwd()+'/log.txt', 'a', encoding='utf-8') as file:
            file.write(
                f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:'
                f'{text}\n')

    def Backup_VKphoto_to_YDisk(self, album_id='profile', count=5):
        try:
            access_token = C_F.get_settings('VKtoken')
            user_id = C_F.get_settings('VKid')
            vk = V_K.VK(access_token, user_id)
            par = vk.get_user_photo_property(album_id, count)
            self._upload_list_of_photo(**par)
        except Exception as e:
            C_F.make_json_uploaded_files()
            self.add_to_log(
                f'В процедуре загрузки фото пользователя из '
                    f'Вконтакте произошла ошибка:{e.args[0]}')
            exit()

        self.add_to_log(
            'Процедура загрузки фото пользователя из Вконтакте успешно выполнена')
        C_F.make_json_uploaded_files(vk.json_foto)
        return 