import logging
import json
import requests

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PLATFORM, NATGEO, CAMBRIDGE, PEARSON = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation."""

    update.message.reply_text(
        'Select your platform:'
        '\n1 - natgeo'
        '\n2 - cambridge'
        '\n3 - pearson'
    )

    return PLATFORM


def platform(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for a description of the problem."""
    which_platform = update.message.from_user

    update.message.reply_text(
        'Ótimo!\n\n'
        'Agora pode me relatar o problema que está ocorrendo?\n'
    )
    if which_platform == 1:
        return NATGEO
    elif which_platform == 2:
        return CAMBRIDGE
    elif which_platform == 3:
        return PEARSON
    else:
        update.message.reply_text(
            'Esta não é uma opção válida.'
        )
        return ConversationHandler.END


def natgeo(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'natgeo'
    )


def cambridge(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'cambridge'
    )


def pearson(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'pearson'
    )

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("O usuário %s cancelou o chamado.", user.first_name)
    update.message.reply_text(
        'Chamado cancelado!\n\n'
        'Obrigado por usar o suporte do ICBEU pelo Telegram.\n'
        'Se desejar registrar um novo chamado, basta digitar /start.'
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("7503805557:AAG1BZ3SBN8sdTKRLllgC-XH-WUYVR_Wmr4")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NATGEO: [MessageHandler(Filters.text & ~Filters.command, natgeo)],
            CAMBRIDGE: [MessageHandler(Filters.text & ~Filters.command, cambridge)],
            PEARSON: [MessageHandler(Filters.text & ~Filters.command, pearson)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()