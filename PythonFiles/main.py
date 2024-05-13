from telebot import TeleBot, types
import telebot
import qrcode
import calendar
from datetime import datetime
import psycopg2

# Variables
BASO_03_23_BD = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', port='5432', password='1')
cursor = BASO_03_23_BD.cursor()
link = 'https://t.me/ConsyyyBot'
groups = []
BASO_03_23 = open('TextFiles/BASO-03-23.txt', 'r').readlines()
token = '6626509200:AAHbOZAM-dMXqEPhmJQcW_I1qaEJ4MF0orQ'
bot = TeleBot(token)
admin_id = 647011387
schedules = []
schedule_c = {
    '0': {
        '12:40': 'Иностранный язык⚙️',
        '14:20': 'Физика⚙️'
    },
    '1': {
        '10:40': 'Языки программирования⚙️',
        '12:40': 'Физ-ра⚙️',
        '14:20': 'Линейная алгебра и аналитическая геометрия⚙️',
        '16:20': 'Информатика⚙️'
    },
    '2': {
        '09:00': 'Линейная алгебра и аналитическая геометрия🎓',
        '10:40': 'Введение в профессиональную деятельность🎓',
        '12:40': 'Русский язык и культура речи🎓',
        '14:20': 'Математический анализ'
    },
    '3': {
        '10:40': 'Основы российской государственности🎓',
        '12:40': 'Основы российской государственности⚙️',
        '14:20': 'История России⚙️'
    },
    '4': {
        '12:40': 'Языки программирования🎓',
        '14:20': 'Математический анализ🎓',
        '16:20': 'Основы информационной безопасности🎓'
    },
    '5': {
        '12:40': 'Физика🎓',
        '14:20': 'Физика🎓'
    },
}
schedule_n = {
    '0': {
        '12:40': 'Иностранный язык⚙️',
        '14:20': 'Физика⚙️'
    },
    '1': {
        '10:40': 'Языки программирования⚙️',
        '12:40': 'Физ-ра⚙️',
        '14:20': 'Линейная алгебра и аналитическая геометрия⚙️',
        '16:20': 'Информатика⚙️'
    },
    '2': {
        '09:00': 'Линейная алгебра и аналитическая геометрия🎓',
        '10:40': 'Информатика🎓',
        '12:40': 'Русский язык и культура речи⚙️',
        '14:20': 'Математический анализ⚙️'
    },
    '3': {
        '09:00': 'История России🎓',
        '10:40': 'История России🎓',
        '12:40': 'Основы российской государственности⚙️',
        '14:20': 'История России⚙️'
    },
    '4': {
        '12:40': 'Языки программирования🎓',
        '14:20': 'Математический анализ🎓',
        '16:20': 'Основы информационной безопасности🎓'
    },
    '5': {
        '12:40': 'Основы информационной безопасности⚙️',
        '14:20': 'Основы информационной безопасности⚙️'
    },
}
schedules.append(schedule_c)
schedules.append(schedule_n)
list_header = ''
students = open('TextFiles/list.txt', 'r')
welcome_msg = open('TextFiles/welcome.txt', 'r').read()
lines = students.readlines()
current_datetime = datetime.now()
hours = current_datetime.hour
minutes = current_datetime.minute
current_weekday = calendar.weekday(current_datetime.year, current_datetime.month, current_datetime.day)
people = {}
names = []
admin_list = ''
password = '123'
user_name = ''
ru_weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

# Параметры запуска
param = int(input())
if param == 1:
    hours = 12
    minutes = 50

# Keyboards
sign_in_keyboard = types.InlineKeyboardMarkup()
registration_btn = types.InlineKeyboardButton(text="Зарегистрироваться👤", callback_data="registration")
sign_in_keyboard.add(registration_btn)

start_keyboard = types.InlineKeyboardMarkup()
s_btn = types.InlineKeyboardButton(text="Отметиться на паре🖋️", callback_data="start_bot")
start_keyboard.add(s_btn)

admin_keyboard = types.InlineKeyboardMarkup()
ad_btn1 = types.InlineKeyboardButton(text="Задать код доступа🔢", callback_data="create_code")
ad_btn2 = types.InlineKeyboardButton(text="Показать список📃", callback_data="show_list")
ad_btn3 = types.InlineKeyboardButton(text="Очистить список⏩", callback_data="clear_list")
admin_keyboard.add(ad_btn1)
admin_keyboard.add(ad_btn2)
admin_keyboard.add(ad_btn3)
admin_keyboard.add(s_btn)


# Функция запуска
@bot.message_handler(commands=['start'])
def start(m: types.Message):
    global cursor, user_name
    n = ''
    if check_person(m.from_user.id):
        if check_weekday():
            if current_pair():
                cursor.execute(""" SELECT * FROM users WHERE tg_id = %s """, (m.from_user.id,))
                name = cursor.fetchall()
                for row in name:
                    n = row[1]
                if m.from_user.id != admin_id:
                    tmp = f'Привет, <b>{n}</b>, самое время отметиться на паре!🧑‍🎓'
                    bot.send_message(m.chat.id, tmp, reply_markup=start_keyboard, parse_mode='html')
                else:
                    bot.send_message(m.chat.id, 'Доступ администратора😎', reply_markup=admin_keyboard)
            else:
                bot.send_message(m.chat.id, 'Сейчас перерыв, отметки отключены🕗')
        else:
            bot.send_message(m.chat.id, 'Сегодня пар нет, кайфуй!🌟')
    else:
        bot.send_message(m.chat.id, "Для начала зарегистрируйся👤", reply_markup=sign_in_keyboard)


def register_user(m):
    global user_name, BASO_03_23_BD
    tmp = list(m.text.split())
    id = 0
    n = ''
    # Проверка на то, чтобы были введены ровно 2 слова
    if len(tmp) != 2:
        msg = bot.send_message(m.chat.id, 'Неправильно введены имя или фамилия, попробуй ещё раз.❌')
        bot.register_next_step_handler(msg, register_user)
    cursor.execute("SELECT * FROM users WHERE first_name = %s AND last_name = %s", (tmp[0], tmp[1]))
    name = cursor.fetchall()
    for row in name:
        n = row[1]
        id = row[3]
    # Проверка на то, что пользователь уже зарегистрирован
    if id is not None:
        msg = bot.send_message(m.chat.id, 'Неправильно введены имя или фамилия, попробуй ещё раз.❌')
        bot.register_next_step_handler(msg, register_user)
    if n is None:
        msg = bot.send_message(m.chat.id, 'Неправильно введены имя или фамилия, попробуй ещё раз.❌')
        bot.register_next_step_handler(msg, register_user)
    else:
        update_query = "UPDATE users SET tg_id = %s WHERE first_name = %s AND last_name = %s"
        cursor.execute(update_query, (m.from_user.id, tmp[0], tmp[1]))
        BASO_03_23_BD.commit()
        msg = f'Привет {tmp[0]} самое время отметиться на паре!🧑‍🎓'
        bot.send_message(m.chat.id, msg, reply_markup=start_keyboard, parse_mode='html')


# Функция обработки кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_weekday, hours, minutes, admin_list, students, lines, people, names, list_header
    if call.message:
        # User commands
        if call.data == 'registration':
            msg = bot.send_message(call.message.chat.id, 'Введи полное имя и фамилию в формате <Имя Фамилия>')
            bot.register_next_step_handler(msg, register_user)
        if call.data == 'start_bot':
            if not current_pair():
                bot.send_message(call.message.chat.id, 'Сейчас перерыв, отметки отключены.🕗')
            else:
                list_header = current_pair()
                t = f'Сейчас идёт <b><i><u>{list_header}</u></i></b>. Введи код. Его ты получишь, отсканировав QR-код!🔑'
                msg = bot.send_message(call.message.chat.id, t, parse_mode='html')
                bot.register_next_step_handler(msg, check_password)
        # Administrator commands
        if call.data == 'create_code':
            msg = bot.send_message(call.message.chat.id, 'Задай код доступа.')
            bot.register_next_step_handler(msg, set_password)
        if call.data == 'show_list':
            global admin_list, names, students
            admin_list = f'{list_header}\n'
            lines = open('TextFiles/list.txt', 'r').readlines()
            for i in range(len(lines)):
                admin_list = admin_list + f'{i + 1}. {lines[i]}\n'
            try:
                bot.send_message(call.message.chat.id, admin_list)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(call.message.chat.id, 'Список пуст')
        if call.data == 'clear_list':
            msg = bot.send_message(call.message.chat.id, 'Список успешно очищен!✅')
            bot.register_next_step_handler(msg, clear_list)


# Функция задания кода доступа
def set_password(m):
    global password
    password = m.text
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(str(password))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_colour="white")
    img.save("qr.png")
    photo = open('qr.png', 'rb')
    bot.send_photo(m.chat.id, photo)
    bot.send_message(m.chat.id, f'Код доступа теперь <b>{password}</b>', parse_mode='html')


# Функция проверки правильности пароля
def check_password(m):
    global names
    if m.text == password:
        f = l = ''
        cursor.execute(""" SELECT * FROM users WHERE tg_id = %s """, (m.from_user.id,))
        name = cursor.fetchall()
        for row in name:
            f = row[1]
            l = row[2]
        people[str(m.from_user.id)] = f + ' ' + l
        names.append(f + ' ' + l)
        names.sort()
        open('TextFiles/list.txt', 'w').close()
        open('TextFiles/list.txt', 'w').writelines(names)
        bot.send_message(m.chat.id, 'Всё верно, ты отмечен на паре!✅')
    else:
        msg = bot.send_message(m.chat.id, 'Код неверный, попробуй ещё раз.❌')
        bot.register_next_step_handler(msg, check_password)


def check_person(tg_id):
    global cursor
    cursor.execute("SELECT tg_id FROM users WHERE tg_id = %s", (tg_id,))
    return cursor.fetchone() is not None


def check_weekday():
    global current_weekday
    return current_weekday != 6


def clear_list():
    global admin_list
    open('../TextFiles/BASO-03-23.txt', 'r').close()
    admin_list = ''


def check_name(s):
    a = []
    f, l = map(str, s.split())
    f = f[:1].upper() + f[1:]
    l = l[:1].upper() + l[1:]
    a.append(f)
    a.append(l)
    return a


def current_pair():
    global schedule_n, BASO_03_23_BD, cursor, current_weekday
    cursor.execute(""" SELECT * FROM schedule_odd WHERE  weekday = %s """, (ru_weekdays[current_weekday],))
    r = cursor.fetchall()
    for row in r:
        if int(row[3][3:]) + int(row[3][:2]) * 60 <= hours * 60 + minutes <= int(row[3][3:]) + int(
                row[3][:2]) * 60 + 90:
            if row[2] == 'l':
                p = row[1] + '🎓'
                return p
            else:
                p = row[1] + '⚙️'
                return p
    return False


def main():
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
