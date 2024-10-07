from telegram import Update
from telegram.ext import ConversationHandler, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters 


NATGEO, ANSWER_HANDLING, CAMBRIDGE, PEARSON = range(4)

# start func
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Este é o chat de suporte às plataformas do ICBEU Manaus.\n'
                                    'Com qual plataforma você precisa de ajuda?\n'
                                    '1 - Natgeo\n'
                                    '2 - Cambridge\n'
                                    '3 - Pearson\n')
    return ANSWER_HANDLING


# answer_handling
async def answer_handling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    print(user_input)
    if user_input == "1":
        print("verificacao certa natgeo")
        await update.message.reply_text('chose natgeo. Select your problem:\n'
                                        '1 - I have forgotten my password.\n'
                                        '2 - I am not in a class.\n'
                                        '3 - I have a scratched code.\n')
        return NATGEO
    elif user_input == "2":
        print("verificacao certa natgeo")
        await update.message.reply_text('1 - I have lost my email\n'
                                        '2 - I have switched classes\n'
                                        '3 - I am a repeat student\n')
        return CAMBRIDGE
    elif user_input == "3":
        return PEARSON
    else:
        await update.message.reply_text('not a valid option')
        return ConversationHandler.END


# platforms funcs
async def natgeo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    if user_input == "1":
        await update.message.reply_text('Remember it.')
    elif user_input == "2":
        await update.message.reply_text('join one.')
    elif user_input == "3":
        await update.message.reply_text('get a new.')

async def cambridge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    if user_input == "1":
        await update.message.reply_text('Find it.')
    elif user_input == "2":
        await update.message.reply_text('join your new class using the class code.')
    elif user_input == "3":
        await update.message.reply_text('get a new.')


async def pearson(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('user chose pearson')
    await update.message.reply_text('chose pearson')

#cancel func
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ConversationHandler.END
#app builder
app = ApplicationBuilder().token("7503805557:AAG1BZ3SBN8sdTKRLllgC-XH-WUYVR_Wmr4").build()

# main func
def main() -> None:
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ANSWER_HANDLING: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handling)],
            NATGEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, natgeo)],
            CAMBRIDGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cambridge)],
            PEARSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, pearson)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conversation_handler)
    app.run_polling()


if __name__ == '__main__':
    main()



# app.add_handler(CommandHandler('start', start))
# app.run_polling()