from datetime import datetime
from pprint import pprint

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from config import API_KEY
import messages
import requests

BASE_URL = 'http://api.weatherapi.com/v1'


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    
    update.message.reply_html(
        messages.welcome_text.format(full_name=user.full_name)
    )

    update.message.reply_html(
        messages.select_category,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton('⛅️ Hozirgi ob-havo'), KeyboardButton('📍 Lokatsiya bo''yicha aniqlash', request_location=True)],
                [KeyboardButton('🕔 Soatlik ob-havo'), KeyboardButton('🗓 Haftalik ob-havo')],
                [KeyboardButton('📍 Hududni o\'zgartirish')],
                [KeyboardButton('📞 Aloqa')]
            ],
            resize_keyboard=True
        )
    )

def send_weather_by_location(update: Update, context: CallbackContext):
    location = update.message.location

    url = f"{BASE_URL}/current.json"
    payload = {
        'key': API_KEY,
        'q': f'{location.latitude},{location.longitude}'
    }
    response = requests.get(url, params=payload)

    data = response.json()

    pprint(data)

    now = datetime.now()

    week_days = {
        1: "Dushanba",
        2: "Seshanba",
        3: "Chorshanba",
        4: "Payshanba",
        5: "Juma",
        6: "Shanba",
        7: "Yakshanba",
    }

    months = {
        1: "Yanvar",
        2: "Fevfral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentabr",
        10: "Obkabr",
        11: "Noyabr",
        12: "Dekabr",
    }

    update.message.reply_html(
        messages.current_weather.format(
            week_day=week_days[now.weekday() + 1],
            day=now.day,
            month=months[now.month],
            city=data['location']['region'],
            district=data['location']['name'],
            temp_c=data['current']['temp_c'],
            feelslike_c=data['current']['feelslike_c'],
            cloud=data['current']['cloud'],
            humidity=data['current']['humidity'],
            wind_mph=data['current']['wind_mph'],
            pressure_mb=data['current']['pressure_mb']
        )
    )
    