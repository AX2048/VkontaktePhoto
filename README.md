![](vk_photo_title_e.png)

# VK SAVED PHOTO

Скрипт `VK_SAVED_IMAGES.py` преднозначен для скачивания фото из альбома "Сохранённые фотограйии".

До запуска нужно создать `.venv`: `python3 -m venv .venv` и установить модули `python -m pip install -r requirements.txt`.

Также рекомендую создать директории `SAVED_PHOTO/` и `json/` до запуска скрипта. 

Далее нужно создать файл `config.ini` со следующим содержанием:
```
[auth]
VK_USER_ID = [ид аккаунта пользователя ВК]
VK_TOKEN = [токен]
VK_APP_ID = [ид приложения ВК]

[path]
SAVED_PHOTO_FOLDER = SAVED_PHOTO/
JSON_FOLDER = json/
```
Заполняем поля:

1. Получаем `ид аккаунта пользователя ВК`: для этого нужно скопировать ид своего аккаунта. Если на главной у вас указано кастомное имя, то id аккаунта можно узнать зайдя в фото или музыку, например: https://vk.com/audios88888888 - `id = 88888888`

2. Получаем `ид приложения ВК`: для этого нужно создать приложение в ВК.

3. Получаем `токен`, для этого нужно перейти по ссылке https://oauth.vk.com/authorize?client_id=5490057&display=page&redirect_uri=http://example.com/callback&scope=photos&response_type=code&v=5.131 предварительно заменив `5490057` на `ид приложения ВК`, подробнее там -> [Authorization Code Flow для получения ключа доступа пользователя](https://dev.vk.com/ru/api/access-token/authcode-flow-user).

Фото сохраняет функция `get_photo_img()`

В директории `JSON_FOLDER` можно найти ответ на запрос `getAlbums` и список ссылок на фото в разном разрешении.

В директории `SAVED_PHOTO_FOLDER` будут скаченные фотографии.