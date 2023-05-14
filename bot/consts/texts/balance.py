DEFAULT_BALANCE_TEXT = 'Ваші гроши: <b>{balance}</b>\n\nОбери розмір ставки:'

MENU_TEXT = '💵 Баланс:\n\n{balances}\n\nПоїхали?'
BALANCE_TEXT = '{icon}{name}: <b>{amount}</b>'
SETTING_TEXT = 'Вітаю у налаштуваннях!\n\nА ви вже налаштувались взяти баночку?'
LANGUAGE_TEXT = 'Обери потрібну мову:'
CABINET_MENU_TEXT = 'Дякую тобі мій мілорд за науку. Я створив цю затишну домівку для твоїх синів та моїх братів. \n' \
                    'StillNoWoman.'
REFERRAL_MENU_TEXT = 'Запрошуйте друзів та отримайте <b>до 15%</b> від всіх їх ставок. Виграшних та програшних.\n\n' \
                     'Кількість рефералів:\n' \
                     'Всього зароблено:\n' \
                     'Виведено на ігровий баланс:\n' \
                     'Ваш рівень:\n\n' \
                     'Посилання для запрошень: <code>{invite_link}</code>'
CHECK_REF_DENIED_TEXT = 'Невірне реферальне посилання. Уважніше.'
CHECK_REF_APPROVE_TEXT = '<a href="tg://user?id={id}">{name}</a> став вашим поддіваном'

WALLET_MENU_TEXT = '💸 <b>Мій гаманець</b> \n\n<b>Баланс</b>: \n\n{balances} \n\n<b>Курс</b>: {token_price}💎 = 1 TON\n\n' \
                   'Одноразовий платіж за ініціацію {init_pay_ton} TON'


DEMO_FUNDS_ICON = '🐠'
TON_FUNDS_ICON = '💎'

# withdraw

WITHDRAW_MENU_TEXT1 = '📤 Виведення • крок 1/3 \n\nВаш баланс: {general_balance} 💎\n' \
                      '⚠️ Мін. сума виведення: {min_withdraw} 💎 ({ton_amount} TON)\n\n' \
                      'Надішліть суму 💎 для виведення:'
WITHDRAW_MENU_TEXT2 = '📤 Виведення • крок 2/3 \n\nНадішліть адресу вашого гаманця:'
WITHDRAW_MENU_TEXT3 = '📤 Виведення • крок 3/3 \n\n<b>Ваш баланс:</b> {general_balance} 💎\n' \
                      'Сума: {user_withdraw_amount} 💎 ({user_withdraw_amount_ton} TON)\nАдрес:\n<code>{user_withdraw_address}</code>\n\n' \
                      'Підтвердіть або надішліть іншу кількість 💎 на виведення'

WITHDRAW_APPROVE = '✅ Заявка на виплату {user_withdraw_amount_ton} TON • {user_withdraw_amount} 💎 прийнята!\n\n' \
                   'Кошти будуть зараховані протягом 24 годин'

WITHDRAW_MANUAL_TX = '@{username} (id: {user_id}) хоче вивести купу грошей: {withdraw_amount}.'

ADMIN_APPROVE_TX = 'Адмін схвалив вашу транзу на виведення {amount} 💎! Очікуйте поповнення :)'
ADMIN_REJECT_TX = 'Транза відхилена адміном. Токени повернені на баланс'

WITHDRAW_DAILY_LIMIT = 'Досягнутий денний ліміт на вивід! Сьогодні ще можна вивести: {allowable_amount} 💎'
PREVIOUS_MANUAL_TX_IN_PROCESS = 'Дочекайтесь оброблення попередньої транзакції'
WITHDRAW_TOO_BIG = 'Максимальний денний ліміт - {daily_limit} 💎 ({daily_limit_token} TON)'

WITHDRAW_ERR_AMOUNT_TOO_SMALL = 'Мінімальна сума для виведення: {min_withdraw} 💎 ({ton_amount} TON)'
WITHDRAW_ERR_TON_TESTNET_ADDRESS = '❌ Голова, це тест-нетівська адреса, будь уважніше'
WITHDRAW_ERR_WRONG_ADDRESS = '❌ Невірно введено адресу'
WITHDRAW_ERR_INSUFFICIENT_FUNDS = '❌ Бажаної суми виводу нема на вашому рахунку'
WITHDRAW_ERR_INSUFFICIENT_FUNDS_MASTER = 'На мастер-рахунку не вистачає грошей. Токени повернені на баланс'

PAYMENT_CONFIRMED = '✅ Гроші ({ton_amount} TON) зараховані на ваш рахунок!'
PAYMENT_DENIED = '❌ Гроші ({ton_amount} TON) не зараховані, токени повернені на баланс.'
PAYMENT_LOST = 'Транзакція на вивід {ton_amount} TON загублена блокчейном, токени повернені на баланс. \n' \
               'Просто спробуйте ще раз :)'

# deposit

DEPOSIT_MENU_TEXT = '📥 <b>Поповнити Toncoin</b>\n\nПереведіть <b>Toncoin</b> на свою депозитну адресу в <b>The Open Network – TON</b>\n\n' \
                    '<b>Адреса</b>:\n<code>{wallet_address}</code>'

DEPOSIT_ACCOUNT_INITIATED = '✅ Одноразовиій платіж за ініціацію вашого особистого TON-гаманця ({init_pay_ton} TON) пройшов успішно :)\n\n' \
                            'З Вашого особистого рахунку було списано {init_pay_ton} TON'
DEPOSIT_INITIATION_ERROR = '❌ Недостатньо коштів!\n\nОдноразовий платіж за ініціацію вашого особистого TON-гаманця - {init_pay_ton} TON'

DEPOSIT_SUCCESSFUL = '✅ Баланс успішно поповнений на {amount}💎!\n\nВдалих спінів, друже 😉'
