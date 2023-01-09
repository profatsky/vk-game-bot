from io import BytesIO
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from database.models_representations import Character


def create_choice_image(characters: list[Character], choice_numbers: list[int]) -> Image:
    if 1 < len(characters) < 3:
        raise ValueError('На одном изображении может находиться не менее 1 и не более 3 персонажей')
    if len(choice_numbers) != len(characters):
        raise ValueError('Количество номеров для выбора должно быть равно количеству персонажей на изображении')
    background_image = Image.new('RGB', (600, 300), color='#FFC700')
    draw_context = ImageDraw.Draw(background_image)
    font = ImageFont.truetype("app/assets/fonts/Fifaks10DEV1.ttf", size=50)

    x_coordinate = 0
    for index, character in enumerate(characters):
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
            (66 + x_coordinate, 43, 116 + x_coordinate, 93),
            fill='white',
            outline='black',
            width=3

        )
        draw_context.text(
            (81 + x_coordinate, 45),
            str(choice_numbers[index]),
            font=font,
            fill='black'
        )
        x_coordinate += 208
    return background_image


def create_character_image(
        skin_image_path: str,
        face_image_path: Optional[str] = None,
        haircut_image_path: Optional[str] = None,
        clothes_image_path: Optional[str] = None
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


def open_image(image_path: str):
    return Image.open(f'app/assets/img/{image_path}')


def convert_image_to_bytes_io(img: Image, image_path: str = 'img') -> BytesIO:
    bio = BytesIO()
    bio.name = image_path
    img.save(bio, 'png')
    bio.seek(0)
    return bio
