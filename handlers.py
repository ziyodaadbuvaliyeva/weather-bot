from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_html(
        f'Assalomu Alaykum <b>{user.full_name}!</b>\n\n<i>OB HAVO ANIQLOCHI BOTGA XUSH KELIBSIZ.</i>'
    )

    update.message.reply_html(
        'Botdan foydalanish uchun <u>kerakli bo\'lim</u>ni tanlang:',
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

