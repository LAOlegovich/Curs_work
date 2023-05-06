import os, json

def get_settings(key):
    """метод получения авторизационных данных"""
    try:
        with open(os.getcwd() + '/settings.json', 'r', encoding='utf-8') as f_s:
            return json.load(f_s)[key]
    except FileNotFoundError:
        print('Файл с параметрами не найден, попробуйте задать их вручную!')
        exit()


def max_in_list(my_list):
    dict_for_sort = {'s': 1, 'm': 2, 'x': 3, 'o': 4,
                     'p': 5, 'q': 6, 'r': 7, 'y': 8, 'z': 9, 'w': 10}
    return sorted(my_list, key=lambda x: dict_for_sort[x["type"]])[-1]

def make_json_uploaded_files(json_body = []):
    try:
        with open(os.getcwd()+'/uploaded_files.json', 'w') as js_file:
            json.dump(json_body, js_file)
    except Exception as e:
            print(f'В процедуре построения json-file произошла ошибка:{e.args[0]}')
    return