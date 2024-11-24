from PIL import Image, ImageDraw, ImageFont

from core.settings import MAIN_FONT_PATH


def create_color_choice_image(colors: list[str], choice_numbers: list[int]) -> Image:
    if 1 < len(colors) < 3:
        raise ValueError('На одном изображении может находиться не менее 1 и не более 3 цветов')

    if len(choice_numbers) != len(colors):
        raise ValueError('Количество номеров для выбора должно быть равно количеству цветов на изображении')

    background_image = Image.new('RGB', (600, 300), color='#F5F5F5')
    draw_context = ImageDraw.Draw(background_image)

    font = ImageFont.truetype(MAIN_FONT_PATH, size=50)

    x_coordinate = 0
    for index, color in enumerate(colors):
        draw_context.rectangle(
            (40 + x_coordinate, 128, 140 + x_coordinate, 228),
            fill=f'#{color}',
            outline='black',
            width=3
        )
        draw_context.rectangle(
            (66 + x_coordinate, 18, 116 + x_coordinate, 68),
            fill='white',
            outline='black',
            width=3
        )
        draw_context.text(
            (81 + x_coordinate, 20),
            str(choice_numbers[index]),
            font=font,
            fill='black'
        )
        x_coordinate += 208
    return background_image
