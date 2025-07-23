from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import handlers
from config import TOKEN


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    
    dp.add_handler(CommandHandler('start', handlers.start))

    
    dp.add_handler(MessageHandler(Filters.location, handlers.send_weather_by_location))

    
    dp.add_handler(MessageHandler(Filters.regex("⛅️ Hozirgi ob-havo"), handlers.current_weather_request))

    
    dp.add_handler(MessageHandler(Filters.regex("🕔 Soatlik ob-havo"), handlers.hourly_weather))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handlers.hourly_weather_by_district))

    
    dp.add_handler(MessageHandler(Filters.regex("🗓 Haftalik ob-havo"), handlers.weekly_weather))

    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handlers.weekly_weather_select_district))

    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handlers.weekly_weather_by_district))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
