from vkbottle.tools import Keyboard, KeyboardButtonColor, Text

admin_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text('📃 Список обращений', payload={'admin': 'reports'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
    .get_json()
)
