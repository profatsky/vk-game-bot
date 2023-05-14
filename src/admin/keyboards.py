from vkbottle import Keyboard, Text, KeyboardButtonColor

admin_menu_keyboard = (
    Keyboard()
    .add(Text('⁉ Обращения', payload={'admin': 'support'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📃 Список администраторов', payload={'admin': 'admin_list'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ В главное меню', payload={'menu': 'back'}))
)
