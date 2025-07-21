from config import TOKEN
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
import handlers


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # command hanlers
    dispatcher.add_handler(CommandHandler('start', handlers.start))

    # message handler
    dispatcher.add_handler(MessageHandler(Filters.location, handlers.send_weather_by_location))

    # start bot
    updater.start_polling()
    updater.idle()

main()
