from vkbottle import Keyboard, Text, KeyboardButtonColor

income_menu_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('🔆 Ежедневный бонус', payload={'income_menu': 'bonus'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🔨 Работа', payload={'income_menu': 'work'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🖥 Майнинг', payload={'income_menu': 'mining'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
        .get_json()
)

mining_menu_keyboard = (
    Keyboard()
    .add(Text('💰 Получить прибыль', payload={'mining_menu': 'get_income'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('📼 Купить видеокарты', payload={'shop_menu': 'gpu'}), color=KeyboardButtonColor.POSITIVE)
    .add(Text('📼 Продать видеокарты', payload={'mining_menu': 'sell_cards'}), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
)
