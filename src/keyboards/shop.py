from vkbottle import Keyboard, Text, KeyboardButtonColor

character_shop_keyboard = (
    Keyboard()
    .add(Text("🎨 Цвет кожи", payload={'character_shop': 'skin'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("🎭 Лицо", payload={'character_shop': 'face'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("✂ Прическа", payload={'character_shop': 'haircut'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("👕 Одежда", payload={'character_shop': 'clothes'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("◀🏬 В магазин", payload={'main_menu': 'shop'}))
)


gpu_shop_keyboard = (
    Keyboard()
    .add(Text('📼 Low', payload={'choice': 1}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📼 Medium', payload={'choice': 2}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('📼 High', payload={'choice': 3}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀🏬 В магазин', payload={'choice': 'back_to_shop'}))
)
