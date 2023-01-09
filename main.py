import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler , filters , MessageHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

from bs4 import BeautifulSoup
import urllib
from urllib import request

API_key = '4aaebaffb00df78abf85103c3158b91d'
code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }



List = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Ii',
 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'C', 'Т': 'T', ' У': 'U', 'Ф': 'F',
 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Э': 'Ye', 'Ю': 'Yu', 'Я': 'Ya'}


def fun(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    p = 0
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            p += 1
    return (int(p / len(s1) * 100))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

async def Weather(update: Update , context: ContextTypes.DEFAULT_TYPE):
    URL =f"https://api.openweathermap.org/data/2.5/weather?q={update.message.text}&appid={API_key}&units=metric"
    try:
        r = requests.get(URL)
        data = r.json()
        # pprint(data)
        city_name = data["name"]
        description = data["weather"][0]["main"]  # описание
        citys_temp = data["main"]["temp"]  # температура
        feels_like = data["main"]["feels_like"]  # температура как чувствуется
        temp_max = data['main']['temp_max']
        temp_min = data["main"]['temp_min']
        humidity = data["main"]['humidity']  # влажность
        pressure = data['main']["pressure"]  # давление
        wind = data["wind"]['speed']

        if description in code_to_smile:
            wd = code_to_smile[description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        text = f" В городе {city_name}\n Погода {description} {wd} \n Температура {citys_temp}°C \n Ощущается как {feels_like}°C \n Максимальная температура {temp_max}°C \n Минимальная температура {temp_min}°C \n Влажность {humidity}\n Давление {pressure}"

        await context.bot.send_message(chat_id=update.effective_chat.id, text= text)
    except Exception as x:
        #Реализация поиска подходящего города
        copy = 0
        name = ''

        city = update.message.text
        letter_ru = city[0]
        letter_en = List[letter_ru]
        URL = f'https://www.1000mest.ru/city{letter_en}'
        html_page = urllib.request.urlopen(URL)
        soup = BeautifulSoup(html_page, 'html.parser')
        app = []
        list = soup.find_all('td')
        for link in list:
            app.append(link.text)

        for element in app:
            Copy = fun(city, element)
            if Copy > copy:
                copy = Copy
                name = element

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Возможно вы имели в виду город {name} \U0001F928?')
        #await context.bot.send_message(chat_id=update.effective_chat.id, text='Не найдено \U0001F625')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f' Добрый день, {name} \n Бот - "Погода" готов к работе \n Вам достаточно ввести город,\n а остальная работа с меня \U0001F609')

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id , text=update.message.text)

# async def caps(update: Update , contex: ContextTypes.DEFAULT_TYPE):
#     text_caps = ' '.join(contex.args).upper()
#     await contex.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     await context.bot.answer_inline_query(update.inline_query.id, results)

if __name__ =="__main__":
    application = ApplicationBuilder().token('5957926306:AAGuU391PDtiikb4xUqC8FAVd96Dtiq1UV8').build()

    start_handler = CommandHandler('start' , start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #caps_handler = CommandHandler('caps', caps)
    #inline_caps_handler = InlineQueryHandler(inline_caps)
    Weather_city = MessageHandler(filters.TEXT & (~filters.COMMAND), Weather)

    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(caps_handler)
    #application.add_handler(inline_caps_handler)
    application.add_handler(Weather_city)

    application.run_polling()