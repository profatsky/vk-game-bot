from vkbottle import Keyboard, Text, KeyboardButtonColor

gpu_shop_keyboard = (
    Keyboard()
    .add(Text('📼 Low', payload={'choice': 1}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📼 Medium', payload={'choice': 2}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📼 High', payload={'choice': 3}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀🏬 В магазин', payload={'choice': 'back_to_shop'}))
)
