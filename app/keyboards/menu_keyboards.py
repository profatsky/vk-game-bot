from vkbottle import Keyboard, Text, KeyboardButtonColor

main_menu_keyboard = (
    Keyboard()
    .add(Text('📄 Профиль', payload={'main_menu': 'profile'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('☎ Поддержка', payload={'main_menu': 'help'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('🎮 Игры', payload={'main_menu': 'games'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('⛏ Заработок', payload={'main_menu': 'income'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('🏬 Магазин', payload={'choice': 'shop'}), color=KeyboardButtonColor.PRIMARY)
)
