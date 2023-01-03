from vkbottle.tools import Keyboard, KeyboardButtonColor, Text


mining_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text('💰 Получить прибыль', payload={'mining_menu': 'get_income'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('📼 Купить видеокарты', payload={'mining_menu': 'buy_cards'}), color=KeyboardButtonColor.POSITIVE)
        .add(Text('📼 Продать видеокарты', payload={'mining_menu': 'sell_cards'}), color=KeyboardButtonColor.NEGATIVE)
        .row()
        .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
        .get_json()
)
