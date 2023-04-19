from vkbottle import Keyboard, Text, KeyboardButtonColor

character_shop_keyboard = (
    Keyboard()
    .add(Text("🎨 Цвет кожи", payload={'character_shop': 'skin'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("🎭 Лицо", payload={'character_shop': 'face'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("✂ Прическа", payload={'character_shop': 'haircut'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("👕 Одежда", payload={'character_shop': 'clothes'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("◀🏬 В магазин", payload={'menu': 'shop'}))
)
