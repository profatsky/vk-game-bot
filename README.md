# vk-game-bot
## Описание

Игровой чат-бот в ВКонтакте
* [VKBottle](https://github.com/vkbottle/vkbottle)
* [Pillow для генерации изображений](https://github.com/python-pillow/Pillow)
* [Tortoise ORM](https://github.com/tortoise/tortoise-orm)
* [Aerich для миграций](https://github.com/tortoise/aerich)
* БД MySQL

## Основной функционал:
* Регистрация и создание персонажа
![register](app/assets/gif/register.gif)
---
* Изменение внешности персонажа (одежда, прическа, лицо, цвет кожи)
![shop](app/assets/gif/shop.gif)
---
* Заработок монеток (покупка видеокарт, приносящих прибыль)
![cards](app/assets/gif/cards.gif)
--- 
* Игры (блэкджек, камень-ножницы-бумага, монетка)
![game](app/assets/gif/game.gif)

## Настройка виртуального окружения и установка зависимостей
```
> python -m venv venv

> venv\Scripts\activate.bat - для Windows

> source venv/bin/activate - для Linux и MacOS

> python -m pip install -r requirements.txt
```

## Конфиг
Переименуйте файл .env.example в .env, укажите токен сообщества ВК и необходимые данные для подключения к MySQL
```
TOKEN = токен сообщества ВК

DB_NAME = имя БД
DB_HOST = localhost
DB_USER = пользователь БД
DB_PASSWORD = пароль БД
```

### Возникли вопросы?
ВКонтакте: https://vk.com/profatsky

Telegram: @profatsky