from vkbottle.tools import Keyboard, KeyboardButtonColor, Text

# Клавиатура главного меню
main_menu_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text('📄 Профиль', payload={'main_menu': 'profile'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('☎ Поддержка', payload={'main_menu': 'help'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('🎮 Игры', payload={'main_menu': 'games'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('⛏ Заработок', payload={'main_menu': 'income'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🏬 Магазин', payload={'main_menu': 'shop'}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
)

shop_menu_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text('✏ Кастомизация персонажа', payload={'shop_menu': 'customize'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('📼 Видеокарты', payload={'mining_menu': 'buy_cards'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
        .get_json()
)

# Клавиатура списка игр
games_menu_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('👋 Цуефа', payload={'games': 'tsuefa'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🃏 Blackjack', payload={'games': 'blackjack'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🦅 Монетка', payload={'games': 'coinflip'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
        .get_json()
)

income_menu_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('🔆 Ежедневный бонус', payload={'income_menu': 'bonus'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🖥 Майнинг', payload={'income_menu': 'mining'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'main_menu': 'back'}))
        .get_json()
)


register_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text('1️⃣', payload={'choice': 1}))
        .add(Text('2️⃣', payload={'choice': 2}))
        .add(Text('3️⃣', payload={'choice': 3}))
        .get_json()
)

back_keyboard = (
    Keyboard(one_time=False, inline=False)
        .add(Text('◀ В главное меню', payload={"main_menu": "back"}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
)