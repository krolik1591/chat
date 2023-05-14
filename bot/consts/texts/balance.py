DEFAULT_BALANCE_TEXT = 'Ваші гроши: <b>{balance}</b>\n\nОбери розмір ставки:'

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


PAYMENT_CONFIRMED = '✅ Гроші ({ton_amount} TON) зараховані на ваш рахунок!'
PAYMENT_DENIED = '❌ Гроші ({ton_amount} TON) не зараховані, токени повернені на баланс.'
PAYMENT_LOST = 'Транзакція на вивід {ton_amount} TON загублена блокчейном, токени повернені на баланс. \n' \
               'Просто спробуйте ще раз :)'
