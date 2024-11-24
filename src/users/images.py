import itertools
from collections.abc import Iterable

from PIL import Image, ImageDraw, ImageFont

from core.settings import MAIN_FONT_PATH
from core.utils import open_image
from users.models_representations import User, Character


def create_character_image(
        skin_image_path: str,
        face_image_path: str | None = None,
        haircut_image_path: str | None = None,
        clothes_image_path: str | None = None
) -> Image:
    contour_image = open_image('contour.png')
    skin_image = open_image(skin_image_path)
    skin_image.paste(contour_image, (0, 0), contour_image)
    if face_image_path:
        face_image = open_image(face_image_path)
        skin_image.paste(face_image, (0, 0), face_image)
    if haircut_image_path:
        haircut_image = open_image(haircut_image_path)
        skin_image.paste(haircut_image, (0, 0), haircut_image)
    if clothes_image_path:
        clothes_image = open_image(clothes_image_path)
        skin_image.paste(clothes_image, (0, 0), clothes_image)

    skin_image = skin_image.resize((181, 181), Image.ANTIALIAS)
    return skin_image


def create_profile_image(user: User, vk_user_name: str) -> Image:
    background_image = Image.new('RGB', (600, 300), color=f'#{user.background_color}')
    draw_context = ImageDraw.Draw(background_image)
    font = ImageFont.truetype(MAIN_FONT_PATH, size=35)

    draw_context.text((55, 20), 'Имя:', font=font, fill='black')
    draw_context.text((55, 65), 'Ник:', font=font, fill='black')
    draw_context.text((55, 110), 'Банк:', font=font, fill='black')
    draw_context.text((55, 155), 'Статус:', font=font, fill='black')

    draw_context.text((140, 20), vk_user_name, font=font, fill='black')
    draw_context.text((140, 65), user.nickname, font=font, fill='black')
    draw_context.text((158, 110), f"${user.balance}", font=font, fill='black')
    draw_context.text((193, 155), user.status, font=font, fill='black')

    x_coordinate = 55
    for card in user.graphics_cards:
        if card:
            card_image = open_image(card.image_path)
        else:
            card_image = open_image('gpu/no_card.png')
        background_image.paste(card_image, (x_coordinate, 200), card_image)
        x_coordinate += 105

    character = user.character
    clothes = character.clothes
    if clothes:
        clothes = clothes.image_path
    character_image = create_character_image(
        skin_image_path=character.skin.image_path,
        face_image_path=character.face.image_path,
        haircut_image_path=character.haircut.image_path,
        clothes_image_path=clothes
    )
    background_image.paste(character_image, (404, 119), character_image)
    return background_image


def create_choice_image(characters: Iterable[Character], choice_numbers: Iterable[int]) -> Image:
    background_image = Image.new('RGB', (600, 300), color='#FFC700')
    draw_context = ImageDraw.Draw(background_image)
    font = ImageFont.truetype(MAIN_FONT_PATH, size=50)

    x_coordinate = 0
    for row in itertools.zip_longest(characters, choice_numbers):
        character, num = row[0], row[1]
        face_image_path = haircut_image_path = clothes_image_path = None
        if character.face:
            face_image_path = character.face.image_path
        if character.haircut:
            haircut_image_path = character.haircut.image_path
        if character.clothes:
            clothes_image_path = character.clothes.image_path
        character_image = create_character_image(
            skin_image_path=character.skin.image_path,
            face_image_path=face_image_path,
            haircut_image_path=haircut_image_path,
            clothes_image_path=clothes_image_path
        )
        background_image.paste(
            character_image,
            (x_coordinate, 119),
            character_image
        )
        draw_context.rectangle(
            (66 + x_coordinate, 18, 116 + x_coordinate, 68),
            fill='white',
            outline='black',
            width=3

        )
        draw_context.text(
            (81 + x_coordinate, 20),
            str(num),
            font=font,
            fill='black'
        )
        x_coordinate += 208
    return background_image
