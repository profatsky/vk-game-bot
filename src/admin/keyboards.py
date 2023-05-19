from vkbottle import Keyboard, Text, KeyboardButtonColor

admin_menu_keyboard = (
    Keyboard()
    .add(Text('⁉ Обращения', payload={'admin': 'support'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📃 Список администраторов', payload={'admin': 'admin_list'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ В главное меню', payload={'menu': 'back'}))
)

support_menu_keyboard = (
    Keyboard()
    .add(Text('💬 Открытые обращения', payload={'support': 'unanswered'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('✔ Закрытые обращения', payload={'support': 'answered'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('⭐ Обращения закрытые мной', payload={'support': 'answered_by_me'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ В админ панель', payload={'menu': 'admin'}))
)

back_to_support_menu_keyboard = (
    Keyboard()
    .add(Text('◀ В меню тех.поддержки', payload={'admin': 'support'}))
)
