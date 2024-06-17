# vk-game-bot

![GitHub top language](https://img.shields.io/github/languages/top/profatsky/vk-game-bot)
![GitHub issues](https://img.shields.io/github/issues/profatsky/vk-game-bot)
![GitHub](https://img.shields.io/github/license/profatsky/vk-game-bot)
![GitHub Repo stars](https://img.shields.io/github/stars/profatsky/vk-game-bot)


Игровой чат-бот для ВКонтакте с функционалом **генерации изображений**. 

Чат-бот позволяет пользователям регистрироваться,
создавать и изменять персонажей, зарабатывать виртуальную валюту и тратить ее, играть в различные мини-игры. Имеется
функционал для администраторов и технической поддержки.

## 🛠️ Технологии
* [VKBottle](https://github.com/vkbottle/vkbottle)
* [Pillow для генерации изображений](https://github.com/python-pillow/Pillow)
* [Tortoise ORM](https://github.com/tortoise/tortoise-orm)
* [Aerich для миграций](https://github.com/tortoise/aerich)
* [SQLite](https://sqlite.org/)

## 🖼️ Основной функционал
Регистрация и создание персонажа
![register](src/assets/gif/register.gif)

Изменение внешности персонажа (одежда, прическа, лицо, цвет кожи)
![shop](src/assets/gif/shop.gif)

Заработок виртуальной валюты (покупка видеокарт для майнинга)
![cards](src/assets/gif/cards.gif)

Игры (блэкджек, камень-ножницы-бумага, монетка)
![game](src/assets/gif/game.gif)


## 🚀 Инструкция по настройке и запуску
### Настройка виртуального окружения и установка зависимостей
```
$ python -m venv venv

$ venv\Scripts\activate.bat - для Windows

$ source venv/bin/activate - для Linux и MacOS

$ python -m pip install -r requirements.txt
```

### Конфиг
Переименуйте файл .env.example в .env и укажите в нем токен вашего сообщества и ID вашего профиля ВК
```
TOKEN = токен сообщества ВК

ADMIN_ID = ID администратора
```

### Применение миграций
```
$ aerich upgrade
```

### Запуск
```
$ cd src

$ python main.py
```

## ⭐️ Понравился чат-бот?
Если вам понравился чат-бот, поставьте звездочку на этот репозиторий

## ❓Возникли вопросы?
Если у вас возникли вопросы, обращайтесь в [Telegram](https://t.me/profatsky) или [ВКонтакте](https://vk.com/profatsky)
