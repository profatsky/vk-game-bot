from vkbottle import Keyboard, Text, KeyboardButtonColor

main_menu_keyboard = (
    Keyboard()
    .add(Text('📄 Профиль', payload={'main_menu': 'profile'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('☎ Поддержка', payload={'main_menu': 'help'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('🎮 Игры', payload={'main_menu': 'games'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('⛏ Заработок', payload={'main_menu': 'income'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('🏬 Магазин', payload={'main_menu': 'shop'}), color=KeyboardButtonColor.PRIMARY)
)

shop_menu_keyboard = (
    Keyboard()
    .add(Text('✏ Кастомизация персонажа', payload={'shop_menu': 'character'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📼 Видеокарты', payload={'mining_menu': 'buy_cards'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
)
