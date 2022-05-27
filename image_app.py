from io import BytesIO

from PIL import Image, ImageFont, ImageDraw

from blueprints.admin import check_status


# Преобразование изображения с типом Image в изображение с типом BytesIO
async def get_img_to_send(img: Image, file_name: str = 'img') -> BytesIO:
    bio = BytesIO()
    bio.name = file_name
    img.save(bio, 'png')
    bio.seek(0)
    return bio


# Создание персонажа
async def create_character(skin: int, face: int = None, haircut: int = None, clothes: int = None) -> Image:
    shape_img = Image.open("files/images/contour.png")  # изображение с контуром персонажа
    skin_img = Image.open(f"files/images/skin/skin{skin}.png")  # изображние тела
    skin_img.paste(shape_img, (0, 0), shape_img)
    if face is not None:
        face_img = Image.open(f"files/images/face/face{face}.png")
        skin_img.paste(face_img, (0, 0), face_img)
    if haircut is not None:
        haircut_img = Image.open(f"files/images/haircut/haircut{haircut}.png")
        skin_img.paste(haircut_img, (0, 0), haircut_img)
    if clothes is not None:
        clothes_img = Image.open(f"files/images/clothes/clothes{clothes}.png")
        skin_img.paste(clothes_img, (0, 0), clothes_img)

    skin_img = skin_img.resize((181, 181), Image.ANTIALIAS)

    return skin_img


# Создание фона
async def create_background(nums: tuple = (1, 2, 3)) -> Image:
    # Шрифт
    font = ImageFont.truetype("files/Fifaks10DEV1.ttf", size=50)

    # Создание фона
    background_img = Image.new('RGB', (600, 300), color='#FFC700')

    # Объект для рисования
    draw = ImageDraw.Draw(background_img)

    # Рисование белых квадратов
    draw.rectangle((66, 43, 116, 93), fill='white', outline='black', width=3)
    draw.rectangle((274, 43, 324, 93), fill='white', outline='black', width=3)
    draw.rectangle((483, 43, 533, 93), fill='white', outline='black', width=3)

    # Рисуование цифр на белых квадратах
    draw.text((81, 45), str(nums[0]), font=font, fill='black')
    draw.text((288, 45), str(nums[1]), font=font, fill='black')
    draw.text((497, 45), str(nums[2]), font=font, fill='black')

    return background_img


# Создание изображения для выбора лица при регистрации
async def create_face(skin: int) -> BytesIO:
    # Создание фона
    img = await create_background()

    first_character = await create_character(skin=skin, face=1)
    second_character = await create_character(skin=skin, face=2)
    third_character = await create_character(skin=skin, face=3)

    # Размещение изображения персонажей на фоне
    img.paste(first_character, (0, 119), first_character)
    img.paste(second_character, (208, 119), second_character)
    img.paste(third_character, (417, 119), third_character)

    # Сохраняние полученного изображение
    return await get_img_to_send(img)


async def create_haircut(skin: int, face: int) -> BytesIO:
    # Создание фона
    img = await create_background()

    first_character = await create_character(skin=skin, face=face, haircut=1)
    second_character = await create_character(skin=skin, face=face, haircut=2)
    third_character = await create_character(skin=skin, face=face, haircut=3)

    # Размещение изображения персонажей на фоне
    img.paste(first_character, (0, 119), first_character)
    img.paste(second_character, (208, 119), second_character)
    img.paste(third_character, (417, 119), third_character)

    # Сохранение полученного изображения
    return await get_img_to_send(img)


async def create_profile(user_info: dict, vk_user) -> BytesIO:
    # Создание фон
    img = Image.new('RGB', (600, 300), color='#FFC700')

    # Шрифт
    font = ImageFont.truetype("files/Fifaks10DEV1.ttf", size=35)

    # Создание объекта для рисования
    draw = ImageDraw.Draw(img)

    # Рисование текста на изображении
    draw.text((55, 20), 'Имя:', font=font, fill='black')
    draw.text((55, 65), 'Ник:', font=font, fill='black')
    draw.text((55, 110), 'Банк:', font=font, fill='black')
    draw.text((55, 155), 'Статус:', font=font, fill='black')

    draw.text((140, 20), f"{vk_user.first_name} {vk_user.last_name}", font=font, fill='black')
    draw.text((140, 65), f"{user_info['nickname']}", font=font, fill='black')
    draw.text((158, 110), f"${user_info['balance']:,}".replace(",", "."), font=font, fill='black')
    draw.text((193, 155), f"{await check_status(vk_user.id)}", font=font, fill='black')

    # Сохранение изображений видеокарт в переменные
    slot_1 = Image.open(f"files/images/video_cards/{user_info['slot_1']}.png")
    slot_2 = Image.open(f"files/images/video_cards/{user_info['slot_2']}.png")
    slot_3 = Image.open(f"files/images/video_cards/{user_info['slot_3']}.png")

    # Размещение видеокарт на основном изображении
    img.paste(slot_1, (55, 200), slot_1)
    img.paste(slot_2, (160, 200), slot_2)
    img.paste(slot_3, (265, 200), slot_3)

    # Создание изображения персонажа с атрибутами внешнего вида, сохраненными у пользователя
    character_img = await create_character(
        skin=user_info["skin"],
        face=user_info["face"],
        haircut=user_info["haircut"],
        clothes=user_info["clothes"]
    )
    # Размещение персонажа на основном изображении
    img.paste(character_img, (404, 119), character_img)

    return await get_img_to_send(img)


# Создание изображения с тремя персонажами для магазина
async def create_shop_page(user_attributes: dict, attribute_type: str,
                           prices: tuple, nums: tuple) -> BytesIO:
    # Шрифты
    font_50 = ImageFont.truetype("files/Fifaks10DEV1.ttf", size=50)
    font_40 = ImageFont.truetype("files/Fifaks10DEV1.ttf", size=40)

    # Создаем фон
    img = Image.new('RGB', (600, 300), color='#FFC700')

    draw = ImageDraw.Draw(img)

    # Рисование трех белых квадратов
    draw.rectangle((66, 18, 116, 68), fill='white', outline='black', width=3)
    draw.rectangle((274, 18, 324, 68), fill='white', outline='black', width=3)
    draw.rectangle((483, 18, 533, 68), fill='white', outline='black', width=3)

    # Рисование номеров указанных атрибутов внешнего вида на белых квадратах
    draw.text((81, 20), str(nums[0]), font=font_50, fill='black')
    draw.text((288, 20), str(nums[1]), font=font_50, fill='black')
    draw.text((497, 20), str(nums[2]), font=font_50, fill='black')

    # Отрисовка трех персонажей
    x = 0
    for count, dict_attributes in enumerate((user_attributes, user_attributes, user_attributes)):
        for key, value in dict_attributes.items():
            if key == attribute_type:
                dict_attributes[key] = nums[count]
        character = await create_character(
            skin=dict_attributes["skin"],
            face=dict_attributes["face"],
            haircut=dict_attributes["haircut"],
            clothes=dict_attributes["clothes"]
        )
        img.paste(character, (x, 119), character)
        x += 208

    # Цены
    draw.text((81 - 12 * len(str(prices[0])), 79), f"${prices[0]:,}".replace(",", "."), font=font_40, fill='black')
    draw.text((288 - 12 * len(str(prices[1])), 79), f"${prices[1]:,}".replace(",", "."), font=font_40, fill='black')
    draw.text((497 - 12 * len(str(prices[2])), 79), f"${prices[2]:,}".replace(",", "."), font=font_40, fill='black')

    return await get_img_to_send(img)
