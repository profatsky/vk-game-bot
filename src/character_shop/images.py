from collections.abc import Iterable

from PIL import ImageFont, ImageDraw, Image

from core.settings import MAIN_FONT_PATH
from users.images import create_choice_image
from users.models_representations import Character


def create_shop_image(
        characters: Iterable[Character],
        choice_numbers: Iterable[int],
        prices: Iterable[int]
) -> Image:
    choice_image = create_choice_image(characters, choice_numbers)
    font = ImageFont.truetype(MAIN_FONT_PATH, size=40)
    draw_context = ImageDraw.Draw(choice_image)

    x = 81
    for price in prices:
        draw_context.text(
            (x - 12 * len(str(price)), 79),
            f'${price:,}'.replace(',', '.'),
            font=font,
            fill='black'
        )
        x += 208

    return choice_image
