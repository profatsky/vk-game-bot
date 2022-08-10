# vk-game-bot
## Описание

Игровой чат-бот в ВКонтакте, написанный на Python с помощью <a href="https://github.com/vkbottle/vkbottle">VKBottle</a> и <a href="https://github.com/python-pillow/Pillow">Pillow</a> (для визуализации).

---
## Основной функционал:
* Регистрация и создание персонажа
![register](files/gif/register.gif)
---
* Изменение внешности персонажа (одежда, прическа, лицо, цвет кожи)
![shop](files/gif/shop.gif)
---
* Заработок монеток (покупка видеокарт, приносящих прибыль)
![cards](files/gif/cards.gif)
--- 
* Игры (блэкджек, камень-ножницы-бумага, монетка)
![game](files/gif/game.gif)

## Настройка и установка
```
> git clone https://github.com/profatsky/vk-game-bot.git

> cd vk-game-bot

> python -m venv venv

> venv\Scripts\activate.bat

> python3 -m pip install -r requirements.txt
```
После клонирования репозитория переименуйте файл .env
example в .env и укажите необходимые значения: токен и
данные для подключения к MySQL
