from .bot_utils import main_keyboard, personal_data_keyboard

from beautyshop_bot.db_utils import get_salon_contacts, get_client_orders, get_speciality


def greet_user(update, context):
    chat_id = update.effective_chat.id
    with open('static/greting_salon.jpg', 'rb') as photo_file:
        context.bot.send_photo(chat_id=chat_id, photo=photo_file)
    welcome_message = 'Приветствуем в нашем боте. 🌹🌹🌹 Поможем выбрать услугу, записаться к мастеру в удобное для вас время.'
    update.message.reply_text(welcome_message, reply_markup=main_keyboard())


def welcome_pdf_user(update, context):
    chat_id = update.effective_chat.id
    with open('static/test.pdf', 'rb') as pdf_file:
        context.bot.send_document(chat_id=chat_id, document=pdf_file)
        welcome_pdf_message = 'Приветствуем в нашем боте. Перед использованием необходимо принять согласие на обработку ПД'
        update.message.reply_text(welcome_pdf_message, reply_markup=personal_data_keyboard())

def not_accept_personal_data(update, context):
    welcome_pdf_message = 'Извините без принятого согласия невозможно продолжить работу'
    update.message.reply_text(welcome_pdf_message, reply_markup=personal_data_keyboard())

def show_contacts(update, contex):
    contacts = get_salon_contacts()

    answer_message = f"У нас есть следующие салоны:\n\n"
    for salon in contacts:
        answer_message += f"Салон: {salon['name']}\n"
        answer_message += f"Адрес: {salon['address']}\n"
        answer_message += f"Телефон: {salon['phone']}\n"
        answer_message += f"\n"

    update.message.reply_text(answer_message, reply_markup=main_keyboard())


def show_my_orders(update, context):
    chat_id = update.message.chat_id

    orders = get_client_orders(chat_id)

    message = f'Ваши заказы:\n\n'
    for order in orders:
        message += f"Услуга: {order['speciality']}\n"
        message += f"Мастер: {order['master']}\n"
        message += f"Время: {order['time']}\n"
        message += f"\n"

    update.message.reply_text(message, reply_markup=main_keyboard())


def show_speciality(update, contex):
    specialitys_salon = get_speciality()

    message = f"У нас представлены следующие услуги:\n\n"
    for speciality in specialitys_salon:
        message += f"Услуга: {speciality['name']}\n"
        message += f"Описание: {speciality['description']}\n"
        message += f"\n"

    update.message.reply_text(message, reply_markup=main_keyboard())

