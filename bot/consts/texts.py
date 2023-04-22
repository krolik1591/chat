# TODO i18n

DEFAULT_BALANCE_TEXT = 'Ваші гроши: <b>{balance}</b>\n\nОбери розмір ставки:'

MENU_TEXT = '💵 Баланс:\n\n{balances}\n\nПоїхали?'
BALANCE_TEXT = '{icon}{name}: <b>{amount}</b>'

DEPOSIT_MENU_TEXT = '💸 <b>Мій гаманець</b> \n\n<b>Баланс</b>: \n\n{balances} \n\n<b>Курс</b>: {token_price}💎 = 1 TON\n\n' \
                    'Одноразовий платіж за ініціацію {init_pay_ton} TON'
REPLENISH_MENU_TEXT = '📥 <b>Поповнити Toncoin</b>\n\nПереведіть <b>Toncoin</b> на свою депозитну адресу в <b>The Open Network – TON</b>\n\n' \
                      '<b>Адреса</b>:\n<code>{wallet_address}</code>'
SUCCESSFUL_REPLENISH_MENU = '✅ Баланс успішно поповнений на {amount}💎!\n\nВдалих спінів, друже 😉'

WITHDRAW_MENU_TEXT1 = '📤 Виведення • крок 1/3 \n\n⚠️ Мін. сума виведення: {min_withdraw} 💎 ({ton_amount} TON)\n\nНадішліть суму 💎 для виведення:'
WITHDRAW_MENU_TEXT2 = '📤 Виведення • крок 2/3 \n\nНадішліть адресу вашого гаманця:'
WITHDRAW_MENU_TEXT3 = '📤 Виведення • крок 3/3 \n\nСума: {user_withdraw_amount} 💎 ({user_withdraw_amount_ton} TON)\nАдрес:\n{user_withdraw_address}\n\n' \
                      'Підтвердіть або надішліть іншу кількість 💎 на виведення'
WITHDRAW_APPROVE = '✅ Заявка на виплату {user_withdraw_amount_ton} TON • {user_withdraw_amount} 💎 прийнята!\n\n' \
                   'Кошти будуть зараховані напротязі 24 годин'
ADMIN_APPROVE_TX = 'Адмін схвалив вашу транзу на виведення {amount} 💎! Очікуйте поповнення :)'
WITHDRAW_MANUAL_TX = '@{username} (id: {user_id}) хоче вивести купу грошей: {withdraw_amount}.'
WITHDRAW_DAILY_LIMIT = 'Досягнутий денний ліміт на вивід! Сьогодні ще можна вивести: {allowable_amount} 💎'
PREVIOUS_MANUAL_TX_IN_PROCESS = 'Дочекайтесь оброблення попередньої транзакції'
WITHDRAW_TOO_BIG = 'Максимальний денний ліміт - {daily_limit} 💎 ({daily_limit_token} TON)'

WITHDRAW_ERR1 = 'Мінімальна сума для виведення: {min_withdraw} 💎 ({ton_amount} TON)'
WITHDRAW_ERR3 = '❌ Голова, це тест-нетівська адреса, будь уважніше'
WITHDRAW_ERR4 = '❌ Невірно введено адресу'
WITHDRAW_ERR5 = '❌ Бажаної суми виводу нема на вашому рахунку'
WITHDRAW_ERR6 = 'На мастер-рахунку не вистачає грошей. Токени повернені на баланс'
WITHDRAW_ERR7 = 'Транза відхилена адміном. Токени повернені на баланс'

DEPOSIT_ACCOUNT_INITIATED = '✅ Одноразовиій платіж за ініціацію вашого особистого TON-гаманця ({init_pay_ton} TON) пройшов успішно :)\n\n' \
                      'З Вашого особистого рахунку було списано {init_pay_ton} TON'
DEPOSIT_INITIATION_ERROR = '❌ Недостатньо коштів!\n\nОдноразовий платіж за ініціацію вашого особистого TON-гаманця - {init_pay_ton} TON'


PAYMENT_CONFIRMED = '✅ Гроші зараховані на ваш рахунок!'
PAYMENT_DENIED = '❌ Гроші не зараховані, токени повернені на баланс.'

DICE_ROLL_TEXT = "🍀 Успіхів!"
LOSE_TEXT = "Наступного разу пощастить!"
WIN_TEXT = 'Перемога! Ізі + {score_change} {token_icon}'

GAME_ERR_BET_NOT_SELECTED = '❌ Не обраний результат ставки!'
GAME_ERR_BET_TOO_BIG = '❌ Ставка більше балансу!'

CUBE_SETTINGS_TEXT = "Баланс: <b>{balance}</b> {token_icon}\nСума усіх ставок: {general_bet} \n\nОбери суму ставки та на що ставиш:"
CUBE_BET_BUTTON = "⚙️ Ставка • {bet} {token_icon}"
RESET_BET = 'Обнуляємось'

DARTS_BOWLING_BASKET_FOOTBALL_TEXT_1 = '😐 Мимо'
DARTS_OR_BOWLING_TEXT_2 = '🙄 Не пощастило'
DARTS_OR_BOWLING_TEXT_3 = '😲 Гарна спроба'

DARTS_TEXT_4 = '👌 <b>Непогано \n\n✅ Ви виграли {score_change}</b> {token_icon}'
DARTS_TEXT_5_OR_BASKET_4 = '👌 <b>Гарне влучання \n\n✅ Ви виграли {score_change}</b> {token_icon}'
DARTS_TEXT_6 = '🍎 <b>ПРЯМО В ЦІЛЬ! 🍏\n\n✅ Ви виграли {score_change}</b> {token_icon}'

BOWLING_TEXT_4 = '🤐 Без коментарів...'
# BOWLING_TEXT_5 = '👌 <b>Гарне влучання \n\n✅ Ви виграли {score_change}</b> {token_icon}'
BOWLING_TEXT_5 = 'СТРАААЙ...\n\nА ні, здалося)'
BOWLING_TEXT_6 = '🤑 <b>СТРАААЙК! 🤑\n\n✅ Ви виграли {score_change}</b> {token_icon}'

BASKET_TEXT_2 = '😲 Майже влучив'
BASKET_TEXT_3 = '😵 Застряг'
BASKET_TEXT_5 = '🤑 <b>ЧИСТЕ ВЛУЧАННЯ! 🤑\n\n✅ Ви виграли {score_change}</b> {token_icon}'

FOOTBALL_TEXT_LOSE = '🙄 Відскочив...'
FOOTBALL_TEXT_WIN = '🤑 <b>ГОООООООЛ! 🤑\n\n✅ Ви виграли {score_change}</b> {token_icon}'

CUBE_TEXT_0 = '{dice_number_emoji}\n\n✅ Ви виграли {score_change} {token_icon}'
CUBE_TEXT_1 = '{dice_number_emoji}\n\n🙄 На жаль, вам не пощастило'
CUBE_TEXT_2 = '{dice_number_emoji}\n\n🤐 Дідько, знов не пощастило'
CUBE_TEXT_3 = '{dice_number_emoji}\n\n🔥 Вже {cube_lose_streak} раз не щастить'

DEMO_FUNDS_ICON = '🐠'
TON_FUNDS_ICON = '💎'

DEFAULT_PLAY_TEXT = 'Грати'

FOOTBALL_PLAY_TEXT = "⚽ ️Kick"
DARTS_PLAY_TEXT = "🎯 ️Darts"
SLOTS_PLAY_TEXT = "🎰 ️Slots"
CUBE_PLAY_TEXT = "🎲 Кубісь"
