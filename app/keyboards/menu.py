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
    .add(Text('📼 Видеокарты', payload={'shop_menu': 'gpu'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
)

games_menu_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('👋 Цуефа', payload={'games': 'tsuefa'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🃏 Blackjack', payload={'games': 'blackjack'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🦅 Монетка', payload={'games': 'coinflip'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
        .get_json()
)