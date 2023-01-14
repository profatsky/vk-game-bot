from vkbottle import Keyboard, Text, KeyboardButtonColor

mining_keyboard = (
    Keyboard()
    .add(Text('💰 Получить прибыль', payload={'mining_menu': 'get_income'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('📼 Купить видеокарты', payload={'mining_menu': 'buy_cards'}), color=KeyboardButtonColor.POSITIVE)
    .add(Text('📼 Продать видеокарты', payload={'mining_menu': 'sell_cards'}), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
)
