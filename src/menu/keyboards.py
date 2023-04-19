from vkbottle import Keyboard, Text, KeyboardButtonColor

main_menu_keyboard = (
    Keyboard()
    .add(Text('📄 Профиль', payload={'menu': 'profile'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('☎ Поддержка', payload={'menu': 'help'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('🎮 Игры', payload={'menu': 'games'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('⛏ Заработок', payload={'menu': 'income'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('🏬 Магазин', payload={'menu': 'shop'}), color=KeyboardButtonColor.PRIMARY)
)

shop_menu_keyboard = (
    Keyboard()
    .add(Text('✏ Кастомизация персонажа', payload={'shop_menu': 'character'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📼 Видеокарты', payload={'shop_menu': 'gpu'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ В главное меню', payload={'menu': 'back'}))
)

income_menu_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('🔆 Ежедневный бонус', payload={'income_menu': 'bonus'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🔨 Работа', payload={'income_menu': 'jobs'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🖥 Майнинг', payload={'income_menu': 'mining'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'menu': 'back'}))
        .get_json()
)
