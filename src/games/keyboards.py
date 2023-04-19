from vkbottle import Keyboard, Text, KeyboardButtonColor


games_menu_keyboard = (
    Keyboard(one_time=True, inline=False)
        .add(Text('👋 Цуефа', payload={'games': 'tsuefa'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🃏 Blackjack', payload={'games': 'blackjack'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('🦅 Монетка', payload={'games': 'coinflip'}), color=KeyboardButtonColor.PRIMARY)
        .row()
        .add(Text('◀ В главное меню', payload={'menu': 'back'}))
        .get_json()
)


blackjack_action_keyboard = (
    Keyboard(one_time=True)
    .add(Text('➕ Еще', payload={'blackjack': 'take_more'}), color=KeyboardButtonColor.POSITIVE)
    .add(Text('⛔ СТОП', payload={'blackjack': 'stop_game'}), color=KeyboardButtonColor.NEGATIVE)
)

bet_keyboard = (
    Keyboard(one_time=True)
    .add(Text('Без ставки'), color=KeyboardButtonColor.PRIMARY)
    .add(Text('◀ К списку игр'), color=KeyboardButtonColor.PRIMARY)
)

blackjack_choice_keyboard = (
    Keyboard(one_time=True)
    .add(Text('Играть'), color=KeyboardButtonColor.POSITIVE)
    .add(Text('◀ К списку игр'), color=KeyboardButtonColor.NEGATIVE)
)

tsuefa_keyboard = (
    Keyboard(one_time=True)
    .add(Text('👊Камень', payload={'tsuefa': 'Камень'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('✌Ножницы', payload={'tsuefa': 'Ножницы'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('✋Бумага', payload={'tsuefa': 'Бумага'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ К списку игр', payload={'tsuefa': 'back'}))
)

coin_flip_keyboard = (
    Keyboard(one_time=True)
    .add(Text('🦅Орёл', payload={'coin_flip': 'Орел'}), color=KeyboardButtonColor.PRIMARY)
    .add(Text('💰Решка', payload={'coin_flip': 'Решка'}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text('◀ К списку игр', payload={'coin_flip': 'back'}))
)
