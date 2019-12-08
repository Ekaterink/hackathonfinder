import telebot
import json
import random
from bs4 import BeautifulSoup
import requests


telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'} # overcome blocking in telegram
bot = telebot.TeleBot('1069355156:AAGneWZ3wJUE9VKkI5HEuAUxOJLTH__63xg') # token

stickers = []

@bot.message_handler(commands=['start', 'help'])                    # how to use bot
def help(message):
    user = message.chat.id
    bot.send_message(user, "Команды: \n\n/russianearshort - короткий список ближайших хакатонов\n/russianear - поиск ближайших хакатонов в России\n/russiacalendarshort - короткий вывод календаря\n/russiacalendar - вывести календарь хакатонов\n/asiapacific2020 - календарь хакатонов в Азии\n/europenear2020 - календарь ближайших хакатонов в Европе\n/northamerica2020 - календарь хакатонов в Северной Америке")

@bot.message_handler(commands=['russianear'])                       # if command =='russianear'
def search_hack(message):
    page = requests.get('http://www.xn--80aa3anexr8c.xn--p1ai/')    # with requests save page to variable page
    soup = BeautifulSoup(page.text, 'html.parser')                  # with BeautifulSoup save html code to variable soup

    user = message.chat.id
    names_near = soup.findAll(class_='t776__title t-name t-name_xl js-product-name')  # save html code in all classes with such name
    dates_near = soup.findAll(class_='t776__descr t-descr t-descr_xxs')
    links_near = soup.findAll(class_='t776__col t-col t-col_3 t-align_left t-item t776__col_mobile-grid js-product')

    datesinfo = []
    linksinfo = []
    for i in range(len(names_near)):
        if dates_near[i].find('strong') is not None:  # find html code in tag <strong>
            datesinfo.append(dates_near[i].text)      # add in list text in tag

    for link in links_near:
        link = link.find('a').get('href')             # save links
        linksinfo.append(link)

    allnear = ""

    for i in range (len(names_near)):                 # beautiful output
        allnear += names_near[i].text
        allnear += "\n"
        allnear += datesinfo[i]
        allnear += "\n"
        allnear += linksinfo[i]
        allnear += "\n"
    bot.send_message(user, allnear)


@bot.message_handler(commands=['russianearshort'])
def search_hack(message):
    page = requests.get('http://www.xn--80aa3anexr8c.xn--p1ai/')
    soup = BeautifulSoup(page.text, 'html.parser')

    user = message.chat.id
    names_near = soup.findAll(class_='t776__title t-name t-name_xl js-product-name')
    dates_near = soup.findAll(class_='t776__descr t-descr t-descr_xxs')
    links_near = soup.findAll(class_='t776__col t-col t-col_3 t-align_left t-item t776__col_mobile-grid js-product')

    datesinfo = []
    linksinfo = []
    for i in range(len(names_near)):
        if dates_near[i].find('strong') is not None:
            datesinfo.append(dates_near[i].text)

    for link in links_near:
        link = link.find('a').get('href')
        linksinfo.append(link)

    allnear = ""

    for i in range (len(names_near)):
        allnear += names_near[i].text
        allnear += "\n"

        allnear += linksinfo[i]
        allnear += "\n"
    bot.send_message(user, allnear)

@bot.message_handler(commands=['russiacalendar'])
def search_calendar(message):
    page = requests.get('http://www.xn--80aa3anexr8c.xn--p1ai/')
    soup = BeautifulSoup(page.text, 'html.parser')

    user = message.chat.id
    names_calendar = soup.findAll(class_='t776__title t-name t-name_xs js-product-name')
    dates_calendar = soup.findAll(class_ = 't776__descr t-descr t-descr_xxs')
    links_near = soup.findAll(class_='t776__col t-col t-col_3 t-align_left t-item t776__col_mobile-grid js-product')
    
    linksinfo = []
    datescalinfo = []
    for i in range(len(dates_calendar)):
        if dates_calendar[i].find() is not None:
            datescalinfo.append(dates_calendar[i].text)

    for link in links_near:
        link = link.find('a').get('href')
        linksinfo.append(link)

    allcal = ""
    i = 0
    for i in range (len(names_calendar)):
        allcal += names_calendar[i].text
        allcal += "\n"

    for j in range (len(names_calendar)):
        bot.send_message(user, names_calendar[j].text)
        i = j+2
        bot.send_message(user, linksinfo[j])
        if ('russiacalendar'):
            bot.send_message(user, dates_calendar[i].text)

@bot.message_handler(commands=['russiacalendarshort'])
def search_calendar(message):
    page = requests.get('http://www.xn--80aa3anexr8c.xn--p1ai/')
    soup = BeautifulSoup(page.text, 'html.parser')

    user = message.chat.id
    names_calendar = soup.findAll(class_='t776__title t-name t-name_xs js-product-name')
    dates_calendar = soup.findAll(class_ = 't776__descr t-descr t-descr_xxs')
    links_near = soup.findAll(class_='t776__col t-col t-col_3 t-align_left t-item t776__col_mobile-grid js-product')
    
    linksinfo = []
    datescalinfo = []
    for i in range(len(dates_calendar)):
        if dates_calendar[i].find() is not None:
            datescalinfo.append(dates_calendar[i].text)

    for link in links_near:
        link = link.find('a').get('href')
        linksinfo.append(link)

    allcal = ""
    i = 0
    for i in range (len(names_calendar)):
        allcal += names_calendar[i].text
        allcal += "\n"

    for j in range (len(names_calendar)):
        bot.send_message(user, names_calendar[j].text)
        bot.send_message(user, linksinfo[j])
    

@bot.message_handler(commands=['northamerica2020'])
def search_hack(message):
    page = requests.get('https://mlh.io/seasons/na-2020/events')
    soup = BeautifulSoup(page.text, 'html.parser')
    user = message.chat.id
    names_near = soup.find_all(class_='event-name')
    all = ""
    k = 0
    for i in names_near:
        k += 1
        if k > 15:
            break
        all += i.text
        all += "\n"
    bot.send_message(user, all)

@bot.message_handler(commands=['asiapacific2020'])
def search_hackasia(message):
    page = requests.get('https://mlh.io/seasons/apac-2020/events')
    soup = BeautifulSoup(page.text, 'html.parser')
    user = message.chat.id
    names_near = soup.find_all(class_='event-name')
    all = ""
    k = 0
    for i in names_near:
        k += 1
        if k > 15:
            break
        all += i.text
        all += "\n"
    bot.send_message(user, all)

@bot.message_handler(commands=['europenear2020'])
def search_hack(message):
    page = requests.get('https://mlh.io/seasons/eu-2020/events')
    soup = BeautifulSoup(page.text, 'html.parser')
    user = message.chat.id
    names_near = soup.find_all(class_='event-name')
    all = ""
    k = 0
    for i in names_near:
        k += 1
        if k > 2:
            break
        all += i.text
        all += "\n"
    bot.send_message(user, all)

@bot.message_handler(content_types=['sticker'])
def process_sticker(message):
    if message.sticker.file_id not in stickers:
        stickers.append(message.sticker.file_id)
    bot.send_sticker(message.chat.id, random.choice(stickers))

# content_types=['text'] - сработает, если нам прислали текстовое сообщение
@bot.message_handler(content_types=['text'])
def echo(message):
    help(message)

bot.polling()           # permanent looking for message
