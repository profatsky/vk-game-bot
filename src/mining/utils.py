from vkbottle import Keyboard, Text

from menu.utils import generate_choice_keyboard_with_numbers


def generate_sell_gpu_keyboard(numbers: list[int]) -> Keyboard:
    keyboard = generate_choice_keyboard_with_numbers(numbers).row()
    keyboard.add(Text('◀ Назад', payload={'choice': 'back'}))
    return keyboard
