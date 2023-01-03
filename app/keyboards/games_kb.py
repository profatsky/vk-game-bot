from vkbottle.tools import Keyboard, KeyboardButtonColor, Text


# Клавиатура игры "Камень, ножницы, бумага"
tsuefa_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text("👊Камень", payload={"tsuefa": "Камень"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("✌Ножницы", payload={"tsuefa": "Ножницы"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("✋Бумага", payload={"tsuefa": "Бумага"}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("◀ К списку игр", payload={"tsuefa": "back"}))
        .get_json()
)
# Клавиатуры игры "Монетка"
coin_flip_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text("🦅Орёл", payload={"coin_flip": "Орел"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("💰Решка", payload={"coin_flip": "Решка"}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("◀ К списку игр", payload={"coin_flip": "back"}))
        .get_json()
)

# Клавиатура игры "Блэкджек"
blackjack_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text("➕ Еще", payload={"blackjack": "more"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("⛔ СТОП", payload={"blackjack": "stop"}), color=KeyboardButtonColor.NEGATIVE)
        .get_json()
)
# Клавиатура для ставок
bet_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('Без ставки'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('◀ К списку игр'), color=KeyboardButtonColor.PRIMARY)
        .get_json()
)
# Клавиатура выбора
choice_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('Играть'), color=KeyboardButtonColor.POSITIVE)
        .add(Text('◀ К списку игр'), color=KeyboardButtonColor.NEGATIVE)
        .get_json()
)
