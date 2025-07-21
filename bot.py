from config import TOKEN
from telegram.ext import (
    Updater,
    CommandHandler,
)
import handlers


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # command hanlers
    dispatcher.add_handler(CommandHandler('start', handlers.start))

    # start bot
    updater.start_polling()
    updater.idle()

main()
