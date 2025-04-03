import telebot
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

token = '7715807749:AAGN9DavV4bBZskrnwGQx_7WMUIGZfeidRQ'
bot: TeleBot = telebot.TeleBot(token)

user_states = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_states[message.chat.id] = 0  # Состояние "0" при старте
    send_initial_message(message.chat.id)

def send_initial_message(chat_id):
    keyboard = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton("Далее", callback_data='next')
    keyboard.add(next_button)
    bot.send_message(chat_id,
                     "Онлайн-консультация — это удобный способ обсудить важные вопросы, не выходя из дома."
                     "Вы сможете: \n"
                     "🔹получить гипотезу о предварительном диагнозе; \n"
                     "🔹отправить результаты лабораторной и инструментальной диагностики для интерпретации врачом; \n"
                     "🔹узнать о возможных методах лечения по Вашему диагнозу; \n"
                     "🔹сформировать тактику дальнейшей диагностики; \n"
                     "🔹получить второе мнение о диагнозе, установленном другим врачом; \n"
                     "🔹обсудить лечение, назначенное другим врачом; \n"
                     "🔹поговорить об иных вопросах в рамках неврологии.\n",
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_state = user_states.get(chat_id, 0)  # Получаем текущее состояние пользователя

    if user_state == 0:
        next_button = InlineKeyboardButton("Далее", callback_data='next')
        keyboard = InlineKeyboardMarkup().add(next_button)
        bot.send_message(chat_id,
                         "В рамках действующего законодательства (статья 36.2 федерального закона N° 323) на онлайн-консультациях запрещено:\n"
                         "⛔️устанавливать окончательный диагноз;\n"
                         "⛔️назначать лечение с указанием конкретных препаратов, их дозировки и кратности приема;\n"
                         "⛔️выписывать рецепт на лекарственный препарат.\n\n"
                         "Онлайн-консультация – это информационная, а не медицинская услуга, которая не заменяет очный прием.",
                         reply_markup=keyboard)
        user_states[chat_id] = 1

    elif user_state == 1:
        next_button = InlineKeyboardButton("Далее", callback_data='next')
        keyboard = InlineKeyboardMarkup().add(next_button)
        bot.send_message(chat_id,
                         "Как проходит онлайн-консультация?\n"
                         "👩🏻‍⚕️Формат Вы выберете самостоятельно — аудио-звонок/видео-звонок/текстовые сообщения/голосовые сообщения.\n"
                         "👩🏻‍⚕️Длительность консультации 30 минут.\n"
                         "👩🏻‍⚕️Время консультации подбирается в личном чате с врачом.",
                         reply_markup=keyboard)
        user_states[chat_id] = 2

    elif user_state == 2:
        next_button = InlineKeyboardButton("Далее", callback_data='next')
        keyboard = InlineKeyboardMarkup().add(next_button)
        bot.send_message(chat_id,
                         "Стоимость:\n"
                         "💲Первичная консультация 2000₽;\n"
                         "💲Повторная консультация (не более трех месяцев с даты проведения первичной) 1500₽.",
                         reply_markup=keyboard)
        user_states[chat_id] = 3

    elif user_state == 3:
        keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Договор-оферта на проведение онлайн-консультаций",
                                       url='https://disk.yandex.ru/i/HsiBX7bGcs927A')
        button2 = InlineKeyboardButton("Политика обработки персональных данных",
                                       url='https://disk.yandex.ru/i/IT7jNVfOgIwBaA')
        button3 = InlineKeyboardButton("С документами ознакомлен(а)",
                                       callback_data='agree_to_terms')
        user_states[chat_id] = 4

        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)

        bot.send_message(chat_id, "Вам необходимо ознакомиться со следующими документами:", reply_markup=keyboard)

    elif call.data == 'agree_to_terms':
        user_states[chat_id] = 4  # Обновляем состояние для следующего шага
        keyboard = InlineKeyboardMarkup()
        pay_button = InlineKeyboardButton("Перейти к оплате", callback_data='pay_consultation')
        keyboard.add(pay_button)

        bot.send_message(chat_id,
                         "Ваше общение с доктором не будет являться медицинской услугой. Для постановки точного диагноза и назначения лечения необходимо записаться на очный прием. Нажимая «Перейти к оплате» Вы полностью принимаете все условия и берете ответственность на себя.",
                         reply_markup=keyboard)

    elif call.data == 'pay_consultation':
        user_states[chat_id] = 5  # Устанавливаем состояние ожидания подтверждения оплаты
        additional_numbers_message = "Оплатить онлайн-консультацию: 5536 9138 5057 9539\n\nПосле произведения оплаты, нажмите \"Далее\"."
        next_button = InlineKeyboardButton("Далее", callback_data='after_payment')
        keyboard = InlineKeyboardMarkup().add(next_button)
        bot.send_message(chat_id, additional_numbers_message, reply_markup=keyboard)

    elif call.data == 'after_payment':
        # Логика после нажатия "Далее" после оплаты
        bot.send_message(chat_id, "Спасибо за доверие к врачу-неврологу Горбачевой Анне Владимировне.\n\n"
                                  "Мы очень старались, чтобы процесс записи был комфортным и простым для Вас🫶🏻\n"
                                  "Ниже расположена кнопка для связи с Анной Владимировной👩🏻‍⚕️\n\n\n"
                                  "Вы можете начать чат в любой день недели в удобное для Вас время.\n\n"
                                  "В течение 24-х часов Анна Владимировна ответит Вам, вы вместе подберете удобные время и формат консультации.\n\n"
                                  "Пожалуйста, для начала общения с Анной Владимировной отправьте ей В ЛИЧНЫЙ ЧАТ следующие сведения:\n"
                                  "1️⃣ Квитанцию об оплате онлайн-консультации.\n"
                                  "2️⃣ Запрос, который Вы бы хотели обсудить с доктором.\n"
                                  "3️⃣ Фото имеющихся обследований, выписок, иных консультаций, относящихся к Вашему запросу.\n"
                                  "4️⃣ Список имеющихся хронических заболеваний и препаратов, принимаемых на постоянной основе.")
        button5 = InlineKeyboardButton("Личный чат с доктором", url='https://t.me/vpsanna')
        chat_keyboard = InlineKeyboardMarkup().add(button5)
        bot.send_message(chat_id, "Начать чат:", reply_markup=chat_keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)