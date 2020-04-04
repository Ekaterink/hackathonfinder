import telebot
import json
import random
from bs4 import BeautifulSoup
import requests
from telebot import types

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}  # overcome blocking in telegram
bot = telebot.TeleBot('TOKEN')  # token

stickers = []


@bot.message_handler(commands=['start', 'help'])  # how to use bot, main buttons
def help(message):
    user = message.chat.id

    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="North America", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Europe", callback_data="button2")
    button3 = types.InlineKeyboardButton(text="Asia Pacific", callback_data="button3")
    button4 = types.InlineKeyboardButton(text="Online", callback_data="button4")
    button5 = types.InlineKeyboardButton(text="In-person", callback_data="button5")
    keyboard.add(button1, button2, button3)
    keyboard.add(button4, button5)

    bot.send_message(message.chat.id, "Hi there!\nI am bot and I can find some cool hackathons for you :)", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)  # при нажатии на кнопку
def callback_inline(call):
    keyboard = types.InlineKeyboardMarkup()
    if call.message:
        if call.data == "button1":
            search(call.message, "america")
        elif call.data == "button2":
            search(call.message, "europe")
        elif call.data == "button3":
            search(call.message, "asia")

        elif call.data == "button4":
            online_deadline = types.InlineKeyboardButton(text="Sort by deadline", callback_data="online_deadline")
            online_prize = types.InlineKeyboardButton(text="Sort by prize amount", callback_data="online_prize")
            keyboard.add(online_deadline, online_prize)
            bot.send_message(call.message.chat.id, "Online hackathons: ", reply_markup=keyboard)

        elif call.data == "button5":
            inperson_deadline = types.InlineKeyboardButton(text="Sort by deadline", callback_data="inperson_deadline")
            inperson_prize = types.InlineKeyboardButton(text="Sort by prize amount", callback_data="inperson_prize")
            keyboard.add(inperson_deadline, inperson_prize)
            bot.send_message(call.message.chat.id, "In-person hackathons: ", reply_markup=keyboard)

        elif call.data == "online_deadline" or call.data == "online_prize" or call.data == "inperson_deadline" or call.data == "inperson_prize":
            search_online(call.message, call.data)


def search_online(message, text):
    if text == "online_deadline":
        page = requests.get('https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=online&sort_by=Submission+Deadline')
    elif text == "online_prize":
        page = requests.get('https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=online&sort_by=Prize+Amount')
    elif text == "inperson_deadline":
        page = requests.get('https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=in-person&sort_by=Submission+Deadline')
    else:        #elif text == "inperson_prize":
        page = requests.get('https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=in-person&sort_by=Prize+Amount')

    soup = BeautifulSoup(page.text, 'html.parser')
    user = message.chat.id

    html = soup.find_all(class_='title')
    names = []
    hrefs = []
    for i in html:
        names.append(i.text)
    html = soup.find_all(class_='clearfix')
    for i in html:
        if i.get('href') is not None:
            hrefs.append(i.get('href'))

    j = 0
    for i in names:
        if j > 4:
            break
        all = ''
        all += i + hrefs[j]
        j += 1
        bot.send_message(user, all)

    help(message) # вызов клавиатуры

# @bot.message_handler(commands=['northamerica2020'])
def search(message, text):
    if text == "america":
        page = requests.get('https://mlh.io/seasons/na-2020/events')
    elif text == "europe":
        page = requests.get('https://mlh.io/seasons/eu-2020/events')
    else: #elif text == "asia":
        page = requests.get('https://mlh.io/seasons/apac-2020/events')
    soup = BeautifulSoup(page.text, 'html.parser')
    user = message.chat.id
    html = soup.find_all(class_='row') # находит первое соответствие то есть апкаминг
    upcoming = html[1]

    #'=========================== event_names ==================================')
    event_names = upcoming.find_all('h3')
    names = []
    for i in event_names[1:]:
        names.append(i.text)
    #'=========================== event_dates ==================================')
    event_dates = upcoming.find_all('p')
    dates = []
    for i in event_dates:
        dates.append(i.text)
    #'=========================== event_locations ==================================')
    event_locations = upcoming.find_all(class_='event-location')
    locations = []
    for i in event_locations:
        locations.append(i.text)
    #'=========================== href ==================================')
    event_hrefs = upcoming.find_all('a')
    hrefs = []
    for i in event_hrefs:
        hrefs.append(i.get('href'))

    i = 0
    for j in names:
        if i > 4:
            break
        all = ""
        all += names[i] + "\n" + dates[i] + locations[i] + hrefs[i]
        i += 1
        bot.send_message(user, all)

    help(message)  # вызов клавиатуры

@bot.message_handler(content_types=['sticker'])
def process_sticker(message):
    if message.sticker.file_id not in stickers:
        stickers.append(message.sticker.file_id)
    bot.send_sticker(message.chat.id, random.choice(stickers))


# content_types=['text'] - сработает, если нам прислали текстовое сообщение
@bot.message_handler(content_types=['text'])
def echo(message):
    help(message)


bot.polling()  # permanent looking for message