from vkbottle import Keyboard, Text

register_choice_keyboard = Keyboard(one_time=True).\
    add(Text('1️⃣', payload={'choice': 1}))\
    .add(Text('2️⃣', payload={'choice': 2}))\
    .add(Text('3️⃣', payload={'choice': 3}))\
    .get_json()
