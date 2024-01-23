import telebot
import time
import re
from telebot import types, TeleBot

admin = '5261885864'
admin1 = '642500259'

bot = TeleBot("6670581865:AAFfkWdbZm9z9usHMSz_F9k4zfDYlTPA_iA")

# bot.set_my_commands(telebot.types.BotCommand("/start", "Начать"))

requests = {}

@bot.message_handler(commands=["start"])
def start(message):
    kb = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Отправить заявку", callback_data="add_request")
    kb.add(button)
    photo = open('main.jpg', 'rb')
    bot.send_photo(chat_id=message.chat.id, caption='''<b>Получите приглашение на выпуск карты банка Казахстана</b>. 🇰🇿

Заявки принимаются и обрабатываются в этот же день. Если у вас нету ИИН (налоговый номер Казахстана), то ниже есть контакт менеджера для получения. 

По ссылке на регистрацию, вам нужно пройти верификацию с загранпаспортом, открыть счет, далее заказать карту на адрес проживания. Получить карту сможете ТОЛЬКО ВЫ лично в руки. 
В среднем доставка занимает 3-4 дня.    

<b>Для заявки потребуются</b> следующие данные:
- ФИО
- Дата рождения
- Номер телефона
- Номер ИИН Казахстана (если его у вас нету, наш менеджер поможет вам его оформить @PFL2024)
- Адрес электронной почты''', reply_markup=kb, parse_mode="html", photo=photo)

@bot.callback_query_handler(func= lambda call: call.data == "add_request")
def get_fio(call):
    requests[call.message.chat.id] = {}
    requests[call.message.chat.id]["delete"] = []
    bot.send_message(call.message.chat.id, '''<b>> Введите ФИО</b>
<i>Иванов Иван Иванович</i>''', parse_mode="html")
    bot.register_next_step_handler(call.message, get_date)
    
def get_date(message):
    # for msg in requests[message.chat.id]["delete"]:
    #     bot.delete_message(msg, message_id=msg)
    if len(message.text) != 1:
        requests[message.chat.id]["fio"] = message.text
        bot.send_message(message.chat.id, '''<b>> Введите дату рождения</b>
<i>чч.мм.гггг</i>''', parse_mode="html")
        requests[message.chat.id]["delete"] = []
        bot.register_next_step_handler(message, get_phone)
    else:
        for msg in requests[message.chat.id]["delete"]:
            bot.delete_message(message.chat.id, message_id=msg)
        msg1 = bot.send_message(message.chat.id, "<u>Неправильный формат ФИО</u>", parse_mode="html")
        msg2 = bot.send_message(message.chat.id, '''<b>> Введите ФИ</b>
<i>Иванов Иван Иванович</i>''', parse_mode="html")
        requests[message.chat.id]["delete"] = [msg1.id, msg2.id]
        bot.register_next_step_handler(message, get_date)

def get_phone(message):
    # for msg in requests[message.chat.id]["delete"]:
    #     bot.delete_message(message.chat.id, message_id=msg)
    result = re.match(r'\d\d.\d\d.\d{4}', message.text)
    if bool(result):
        requests[message.chat.id]["date"] = message.text
        bot.send_message(message.chat.id, '''><b>Введите номер телефона</b>
7номербезпробелов''', parse_mode="html")
        requests[message.chat.id]["delete"] = []
        bot.register_next_step_handler(message, get_inn)
    else:
        for msg in requests[message.chat.id]["delete"]:
            bot.delete_message(message.chat.id, message_id=msg)
        msg1 = bot.send_message(message.chat.id, "<u>Неправильный формат даты рождения</u>", parse_mode="html")
        msg2 = bot.send_message(message.chat.id, '''<b>> Введите дату рождения</b>
<i>чч.мм.гггг</i>''', parse_mode="html")
        requests[message.chat.id]["delete"] = [msg1.id, msg2.id]
        bot.register_next_step_handler(message, get_phone)

def get_inn(message):
    result = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', message.text)
    if bool(result):
        requests[message.chat.id]["phone"] = message.text
        bot.send_message(message.chat.id, '''<b>> Введите номер ИИН</b>''', parse_mode="html")
        requests[message.chat.id]["delete"] = []
        bot.register_next_step_handler(message, get_email)
    else:
        for msg in requests[message.chat.id]["delete"]:
            bot.delete_message(message.chat.id, message_id=msg)
        msg1 = bot.send_message(message.chat.id, "<u>Неправильный формат телефона</u>", parse_mode="html")
        msg2 = bot.send_message(message.chat.id, '''<b>> Введите номер телефона</b>
<i>7номербезпробелов</i>''', parse_mode="html")
        requests[message.chat.id]["delete"] = [msg1.id, msg2.id]
        bot.register_next_step_handler(message, get_inn)

def get_email(message):
    if len(message.text) == 12 or re.search(r'\w', message.text) == None:
        requests[message.chat.id]["inn"] = message.text
        bot.send_message(message.chat.id, '''<b>> Введите адрес электронной почты</b>''', parse_mode="html")
        requests[message.chat.id]["delete"] = []
        bot.register_next_step_handler(message, validate)
    else:
        for msg in requests[message.chat.id]["delete"]:
            bot.delete_message(message.chat.id, message_id=msg)
        msg1 = bot.send_message(message.chat.id, "<u>Неправильный формат ИИН</u>", parse_mode="html")
        msg2 = bot.send_message(message.chat.id, '''<b>> Введите номер ИИН</b>''', parse_mode="html")
        requests[message.chat.id]["delete"] = [msg1.id, msg2.id]
        bot.register_next_step_handler(message, get_email)

def validate(message):
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

    if re.match(pattern, message.text) is not None:
        requests[message.chat.id]["delete"] = []
        requests[message.chat.id]["email"] = message.text
        kb = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="Все верно!", callback_data="send_request")
        button2 = types.InlineKeyboardButton(text="Ввести заново", callback_data="add_request")
        kb.add(button1, button2)
        bot.send_message(message.chat.id, f'''<b>ПРОВЕРКА</b>

❗️Внимательно проверьте корректность введенных ранее данных:

ФИО: {requests[message.chat.id]["fio"]}
Телефон: {requests[message.chat.id]["phone"]}
ИИН: {requests[message.chat.id]["inn"]}
Email: {requests[message.chat.id]["email"]}

Если обнаружили ошибку, нажмите кнопку "Ввести заново"''', reply_markup=kb ,parse_mode="html")
    else:
        for msg in requests[message.chat.id]["delete"]:
            bot.delete_message(message.chat.id, message_id=msg)
        msg1 = bot.send_message(message.chat.id, "<u>Неправильный формат email</u>")
        msg2 = bot.send_message(message.chat.id, '''<b>> Введите адрес электронной почты</b>''')
        requests[message.chat.id]["delete"] = [msg1.id, msg2.id]
        bot.register_next_step_handler(message, validate)

@bot.callback_query_handler(func= lambda call: call.data == "send_request")
def send_request(call):
    bot.send_message(admin, f'''<b>Пришла новая заявка!</b>
ФИО: {requests[call.message.chat.id]["fio"]}
Дата рождения: {requests[call.message.chat.id]["date"]}
Телефон: {requests[call.message.chat.id]["phone"]}
ИИН: {requests[call.message.chat.id]["inn"]}
Email: {requests[call.message.chat.id]["email"]}''', parse_mode="html")
#     bot.send_message(admin1, f'''<b>Пришла новая заявка!</b>
# ФИО: {requests[call.message.chat.id]["fio"]}
# Дата рождения: {requests[call.message.chat.id]["date"]}
# Телефон: {requests[call.message.chat.id]["phone"]}
# ИИН: {requests[call.message.chat.id]["inn"]}
# Email: {requests[call.message.chat.id]["email"]}''', parse_mode="html")
    bot.send_message(call.message.chat.id, f'''<b>ЗАЯВКА ОТПРАВЛЕНА</b>

Ожидайте приглашение в виде СМС на номер <b>{requests[call.message.chat.id]["phone"]}</b>
''', parse_mode="html")
    del requests[call.message.chat.id]

bot.polling()

