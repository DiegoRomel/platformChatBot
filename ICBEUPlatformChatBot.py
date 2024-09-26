from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Este é o chatbot das plataformas do ICBEU. Digite o seu seu problema'
                                    '\none - NatGeo'
                                    '\ntwo - Cambridge'
                                    '\nthree - Pearson')


async def one(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('you chose cambridge')


app = ApplicationBuilder().token("7503805557:AAG1BZ3SBN8sdTKRLllgC-XH-WUYVR_Wmr4").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("one", one))
app.add_handler(CommandHandler(""))

app.run_polling()

