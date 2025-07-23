from datetime import datetime
from pprint import pprint
import requests

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from config import API_KEY
import messages
from regions_districts import REGIONS_AND_DISTRICTS

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
                [KeyboardButton('⛅️ Hozirgi ob-havo'), KeyboardButton("📍 Lokatsiya bo'yicha aniqlash", request_location=True)],
                [KeyboardButton("🕔 Soatlik ob-havo"), KeyboardButton("🗓 Haftalik ob-havo")],
                [KeyboardButton("📍 Hududni o'zgartirish")],
                [KeyboardButton("📞 Aloqa")]
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
        1: "Dushanba", 2: "Seshanba", 3: "Chorshanba",
        4: "Payshanba", 5: "Juma", 6: "Shanba", 7: "Yakshanba"
    }

    months = {
        1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel",
        5: "May", 6: "Iyun", 7: "Iyul", 8: "Avgust",
        9: "Sentabr", 10: "Oktyabr", 11: "Noyabr", 12: "Dekabr"
    }

    update.message.reply_html(
        messages.current_weather.format(
            week_day=week_days[now.isoweekday()],
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

def current_weather_request(update: Update, context: CallbackContext):
    regions = list(REGIONS_AND_DISTRICTS.keys())
    keyboard = [[KeyboardButton(region)] for region in regions]

    update.message.reply_text(
        "⛅ Hozirgi ob-havo uchun viloyatni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


def current_weather_by_district(update: Update, context: CallbackContext):
    district = update.message.text

    url = f"{BASE_URL}/current.json"
    params = {
        'key': API_KEY,
        'q': f"{district}, Uzbekistan"
    }

    response = requests.get(url, params=params)
    if not response.ok:
        update.message.reply_text("❌ Ob-havo topilmadi.")
        return

    data = response.json()
    now = datetime.now()

    update.message.reply_text(
        f" {data['location']['name']}, {data['location']['region']}\n"
        f" {data['current']['temp_c']}°C, {data['current']['condition']['text']}\n"
        f" Namlik: {data['current']['humidity']}%\n"
        f"🌬 Shamol: {data['current']['wind_kph']} km/soat"
    )
def hourly_weather(update: Update, context: CallbackContext):
    regions = list(REGIONS_AND_DISTRICTS.keys())
    keyboard = [[KeyboardButton(region)] for region in regions]

    update.message.reply_text(
        " Soatlik ob-havo uchun viloyatni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
def hourly_weather_select_district(update: Update, context: CallbackContext):
    region = update.message.text
    districts = REGIONS_AND_DISTRICTS.get(region)

    if not districts:
        update.message.reply_text("❌ Viloyat topilmadi.")
        return

    keyboard = [[KeyboardButton(d)] for d in districts]

    update.message.reply_text(
        f"{region} viloyatidagi tuman yoki shaharni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
def hourly_weather_by_district(update: Update, context: CallbackContext):
    district = update.message.text

    url = f"{BASE_URL}/forecast.json"
    params = {
        'key': API_KEY,
        'q': f"{district}, Uzbekistan",
        'days': 1
    }

    response = requests.get(url, params=params)
    if not response.ok:
        update.message.reply_text("❌ Ob-havo topilmadi.")
        return

    data = response.json()
    hours = data['forecast']['forecastday'][0]['hour']

    reply = f" {district} uchun 24 soatlik ob-havo:\n\n"
    for h in hours:
        reply += f"{h['time'].split()[1]} — {h['temp_c']}°C, {h['condition']['text']}\n"

    update.message.reply_text(reply)


def weekly_weather(update: Update, context: CallbackContext):
    regions = list(REGIONS_AND_DISTRICTS.keys())
    keyboard = [[KeyboardButton(region)] for region in regions]

    update.message.reply_text(
        " Haftalik ob-havo uchun viloyatni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
def weekly_weather_select_district(update: Update, context: CallbackContext):
    region = update.message.text
    districts = REGIONS_AND_DISTRICTS.get(region)

    if not districts:
        update.message.reply_text("❌ Viloyat topilmadi.")
        return

    keyboard = [[KeyboardButton(d)] for d in districts]

    update.message.reply_text(
        f"{region} viloyatidagi tuman/shaharni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
def weekly_weather_by_district(update: Update, context: CallbackContext):
    district = update.message.text

    url = f"{BASE_URL}/forecast.json"
    params = {
        'key': API_KEY,
        'q': f"{district}, Uzbekistan",
        'days': 7,
        'aqi': 'no',
        'alerts': 'no'
    }

    response = requests.get(url, params=params)
    if not response.ok:
        update.message.reply_text("❌ Ob-havo topilmadi.")
        return

    data = response.json()
    days = data['forecast']['forecastday']

    reply = f" {district} uchun 7 kunlik ob-havo:\n\n"
    for day in days:
        date = day['date']
        condition = day['day']['condition']['text']
        avg_temp = day['day']['avgtemp_c']
        max_temp = day['day']['maxtemp_c']
        min_temp = day['day']['mintemp_c']
        reply += f"{date}: {condition}, {min_temp}°C–{max_temp}°C (O'rtacha: {avg_temp}°C)\n"

    update.message.reply_text(reply)



