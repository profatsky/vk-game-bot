from vkbottle.tools import Keyboard, KeyboardButtonColor, Text

buy_graphics_card_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text('📼 Low', payload={'choice': ("low_card", 1500)}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('📼 Medium', payload={'choice': ("medium_card", 7500)}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('📼 High', payload={'choice': ("high_card", 25000)}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀🏬 В магазин', payload={'choice': 'shop'}))
        .get_json()
)


customize_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text("🎨 Цвет кожи", payload={'customize': 'skin'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("🎭 Лицо", payload={'customize': 'face'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("✂ Прическа", payload={'customize': 'haircut'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("👕 Одежда", payload={'customize': 'clothes'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text("◀🏬 В магазин", payload={'choice': 'shop'}))
        .get_json()
)

choose_keyboard_shop_1 = (
    Keyboard(one_time=False, inline=False)
        .add(Text('1️⃣', payload={'choice': 1}))
        .add(Text('2️⃣', payload={'choice': 2}))
        .add(Text('3️⃣', payload={'choice': 3}))
        .row()
        .add(Text('◀🏬 В магазин', payload={"choice": "shop"}))
        .get_json()
)

choose_keyboard_shop_2 = (
    Keyboard(one_time=False, inline=False)
        .add(Text('1️⃣', payload={'choice': 1}))
        .add(Text('2️⃣', payload={'choice': 2}))
        .add(Text('3️⃣', payload={'choice': 3}))
        .row()
        .add(Text('◀🏬 В магазин', payload={"choice": "shop"}))
        .add(Text('▶ След.стр', payload={"choice": "next"}))
        .get_json()
)

choose_keyboard_shop_3 = (
    Keyboard(one_time=False, inline=False)
        .add(Text('4️⃣', payload={'choice': 4}))
        .add(Text('5️⃣', payload={'choice': 5}))
        .add(Text('6️⃣', payload={'choice': 6}))
        .row()
        .add(Text('◀🏬 В магазин', payload={"choice": "shop"}))
        .add(Text('◀ Пред.стр', payload={"choice": "prev"}))
        .get_json()
)

choose_keyboard_shop_4 = (
    Keyboard(one_time=False, inline=False)
        .add(Text('4️⃣', payload={'choice': 4}))
        .add(Text('5️⃣', payload={'choice': 5}))
        .add(Text('6️⃣', payload={'choice': 6}))
        .row()
        .add(Text('◀ Пред.стр', payload={"choice": "prev"}))
        .add(Text('▶ След.стр', payload={"choice": "next"}))
        .row()
        .add(Text('◀🏬 В магазин', payload={"choice": "shop"}))
        .get_json()
)

choose_keyboard_shop_5 = (
    Keyboard(one_time=False, inline=False)
        .add(Text('7️⃣', payload={'choice': 7}))
        .add(Text('8️⃣', payload={'choice': 8}))
        .add(Text('9️⃣', payload={'choice': 9}))
        .row()
        .add(Text('◀🏬 В магазин', payload={"choice": "shop"}))
        .add(Text('◀ Пред.стр', payload={"choice": "prev"}))
        .get_json()
)
