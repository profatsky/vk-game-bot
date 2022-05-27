<h1>vk-game-bot</h1>
<hr>
<h2>Описание</h2>
Игровой чат-бот в ВКонтакте, написанный на Python с помощью <a href="https://github.com/vkbottle/vkbottle">VKBottle</a> и <a href="https://github.com/python-pillow/Pillow">Pillow</a> (для визуализации).
<hr>
<h2>Основной функционал:</h2>
<ul>
    <li>Регистрация и создание персонажа</li>
    <img src="files/gif/register.gif">
    <hr>
    <li>Изменение внешности персонажа (одежда, прическа, лицо, цвет кожи)</li>
    <img src="files/gif//shop.gif">
    <hr>
    <li>Заработок монеток (покупка видеокарт, приносящих прибыль)</li>
    <img src="files/gif/cards.gif">
    <hr>
    <li>Игры (блэкджек, камень-ножницы-бумага, монетка)</li>
    <img src="files/gif/game.gif">
</ul>
<h2>Настройка и установка</h2>

```
$ git clone https://github.com/profatsky/vk-game-bot.git

$ cd vk-game-bot

$ python3 -m pip install -r requirements.txt
```
<p>После клонирования репозитория переименуйте файл .env.example в .env и укажите необходимые значения: токен и данные для подключения к MySQL</p>
