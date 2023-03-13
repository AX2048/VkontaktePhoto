import requests, json, time, os
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
    
VK_USER_ID = config.get('auth', 'VK_USER_ID')
VK_TOKEN = config.get('auth', 'VK_TOKEN')
SAVED_PHOTO_FOLDER = config.get('path', 'SAVED_PHOTO_FOLDER')
JSON_FOLDER = config.get('path', 'JSON_FOLDER')
    
    
# вернуть текущую дату и время
def print_current_data_time():
    current_datetime = datetime.now()
    #print('DT :: ', current_datetime)
    return(current_datetime)


# Запись в json
def write_json(data, filename_json, rewrite):
    with open(str(JSON_FOLDER + filename_json), rewrite) as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Очистка json
def clear_json(filename_json):
    f = open(str(JSON_FOLDER + filename_json), "w")
    f.close()


# Информация об альбомах аккаунта
def view_albums():
    print(f"\nview_albums :: BEGIN\n")
    fname = 'response_get_albums.json'
    r = requests.get("https://api.vk.com/method/photos.getAlbums", params={
        'owner_id': VK_USER_ID,
	    'access_token': VK_TOKEN,
        'v': 5.131,
        #'album_ids': -15,
        'need_system': 1 # 1 — будут возвращены системные альбомы, имеющие отрицательные идентификаторы.
    })
    write_json(r.json(), fname, "w")
    s = r.json()
    i = s["response"]['items']
    l = len(i)
    print(f"| Найдено альбомов :: {l} |\n")
    
    j = 0
    while j < l: 
        print(f"| # {j} | ID :: {i[j]['id']} | Название :: {i[j]['title']} | Колличество фото :: {i[j]['size']} |")
        time.sleep(0.02)
        j = j + 1
    
    print(f"\n| Запись вывода в фаил :: {fname} |\n")
    print(f"view_albums :: END\n")


# Прходим по списку фото (нужно с помощью offset=0, count=50!!!)
def get_photo_data(offset=0, count=50):

    
    p = requests.get("https://api.vk.com/method/photos.get", params={
        'owner_id': VK_USER_ID,
	    'access_token': VK_TOKEN,
        'v': 5.131,
        'album_ids': 'saved',
        'rev': 0,
        'photo_sizes': 1,
        'album_id': '-15',
        'offset': offset,
		'count': count
    })    
    return json.loads(p.text)


def get_photo_list():
    print(f"\nget_photo_list :: BEGIN\n")
    fname = "album_photo_list.json"
    clear_json(fname)
    
    data = get_photo_data()
    count_foto = data["response"]["count"]
    i = 0
    c = 0
    count = 50
    
    print(f'Album ID :: {data["response"]["items"][1]["album_id"]}')
    print(f'Album count :: {count_foto}\n')
    
    #count_foto = 10
    
    while i <= count_foto:
        if i != 0:
            data = get_photo_data(offset=i, count=count)
        
        for inter in data["response"]["items"]:
            photo_j = inter["sizes"][-1]
            write_json(photo_j, fname, "a")
            c = c + 1
            print(f'| {c} | URL :: {photo_j["url"].split("?")[0]}')
            #counter = count_foto - c
            #counter = c
            #photoname = str(str(counter).zfill(4) + "_" + photo_j["url"].split("/")[-1].split("?")[0])
            #print(f'| {c} | URL :: {photoname}')     
            time.sleep(0.02)            
     
        i += count
    print(f"\nget_photo_list :: END\n")


def get_photo_img():
    print(f"\nget_photo_img :: BEGIN\n")
    
    data = get_photo_data()
    count_foto = data["response"]["count"]
    i = 0
    c = 0
    count = 50
    u = len(str(count_foto))
    print(f'Album count :: {count_foto} | {u} \n')
    
    
    while i <= count_foto:
        if i != 0:
            data = get_photo_data(offset=i, count=count)

        for files in data["response"]["items"]:
            file_url = files["sizes"][-1]["url"]
            photo_j = files["sizes"][-1]
            #filename = file_url.split("/")[-1]
            c = c + 1 
            api = requests.get(file_url)
            
            counter = c
            photoname = str(str(counter).zfill(u) + "_" + str(VK_USER_ID) + "_" + photo_j["url"].split("/")[-1].split("?")[0])
            
            print(f'| {c} | Name :: {photoname} | URL :: {file_url} |')
            time.sleep(0.02)

            with open(str(SAVED_PHOTO_FOLDER) + photoname, "wb") as file:
                file.write(api.content)
        i += count
    print(f"\nget_photo_img :: END\n")


def main():
    print('\nMAIN BEGIN\n')
    
    print(VK_USER_ID)
    print('')
    print(VK_TOKEN)
    print('')
    print(SAVED_PHOTO_FOLDER)
    print('')
    print(JSON_FOLDER)
    
    print('')
    print('CWD :: ', os.getcwd(),'\n')
    print("DT :: ", print_current_data_time())

    view_albums()
    get_photo_list()
    get_photo_img()
    print('\nMAIN END\n')
    

if __name__ == "__main__":
	main()