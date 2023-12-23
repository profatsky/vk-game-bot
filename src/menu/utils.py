from collections.abc import Iterable

from vkbottle import Keyboard, Text

from core.loader import admin_list
from menu.keyboards import admin_main_menu_keyboard, main_menu_keyboard


def get_main_menu_keyboard(vk_id: int) -> Keyboard:
    if vk_id in admin_list.storage:
        return admin_main_menu_keyboard
    return main_menu_keyboard


def generate_choice_keyboard_with_pagination(
        numbers: Iterable[int],
        prev_page: bool,
        next_page: bool,
        back_label: str
) -> Keyboard:
    keyboard = generate_choice_keyboard(numbers).row()
    prev_page_button = Text('◀ Пред.стр', payload={'choice': 'prev_page'})
    next_page_button = Text('▶ След.стр', payload={'choice': 'next_page'})
    back_button = Text(back_label, payload={'choice': 'back'})
    if prev_page and next_page:
        keyboard.add(prev_page_button)
        keyboard.add(next_page_button).row()
        keyboard.add(back_button)
    elif prev_page:
        keyboard.add(back_button)
        keyboard.add(prev_page_button)
    elif next_page:
        keyboard.add(back_button)
        keyboard.add(next_page_button)
    else:
        keyboard.add(back_button)
    return keyboard


def generate_choice_keyboard(numbers: Iterable[int]) -> Keyboard:
    emoji = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣️',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
    }
    keyboard = Keyboard()
    for number in numbers:
        result_number = ''.join([emoji[digit] for digit in str(number)])
        keyboard.add(Text(result_number, payload={'choice': number}))
    return keyboard
