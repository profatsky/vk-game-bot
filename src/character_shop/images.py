from collections.abc import Iterable, Sequence

from PIL import ImageFont, ImageDraw, Image

from users.images import create_choice_image
from users.models_representations import Character


def create_shop_image(
        characters: Iterable[Character],
        choice_numbers: Iterable[int],
        prices: Sequence[int]
) -> Image:

    choice_image = create_choice_image(characters, choice_numbers)
    font = ImageFont.truetype('assets/fonts/Fifaks10DEV1.ttf', size=40)
    draw_context = ImageDraw.Draw(choice_image)
    draw_context.text(
        (81 - 12 * len(str(prices[0])), 79),
        f'${prices[0]:,}'.replace(',', '.'),
        font=font,
        fill='black'
    )
    draw_context.text(
        (288 - 12 * len(str(prices[1])), 79),
        f'${prices[1]:,}'.replace(',', '.'),
        font=font,
        fill='black'
    )
    draw_context.text(
        (497 - 12 * len(str(prices[2])), 79),
        f'${prices[2]:,}'.replace(',', '.'),
        font=font,
        fill='black'
    )
    return choice_image
