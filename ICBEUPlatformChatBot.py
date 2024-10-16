from telegram import Update
from telegram.ext import ConversationHandler, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters 
import requests


CENGAGE, ANSWER_HANDLING, CAMBRIDGE, PEARSON, FOWARD_MESSAGE = range(5)

# start func
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Este é o chat de suporte às plataformas do ICBEU Manaus.\n'
                                    'Com qual plataforma você precisa de ajuda?\n'
                                    '1 - Cengage\n'
                                    '2 - Cambridge\n'
                                    '3 - Pearson\n')
    return ANSWER_HANDLING



async def forward_message(bot_token, source_chat_id, target_chat_id, message_id):
    url = f"https://api.telegram.org/bot{bot_token}/forwardMessage"
    data = {
        "chat_id": target_chat_id,
        "from_chat_id": source_chat_id,
        "message_id": message_id
    }
    response = requests.post(url, json=data)
    return response.json()


# answer_handling
async def answer_handling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    print(user_input)
    if user_input == "1":
        print("verificacao certa natgeo")
        await update.message.reply_text('Qual seu problema na plataforma Cengage?\n'
                                        '1 - Esqueci minha senha.\n'
                                        '2 - Ainda não estou em uma turma.\n'
                                        '3 - Código do livro rasurado/inexistente.\n'
                                        '4 - Não sei meu username.\n'
                                        '5 - Meu problema não é nenhum desses/meu problema não foi resolvido.\n')
        return CENGAGE
    elif user_input == "2":
        print("verificacao certa natgeo")
        await update.message.reply_text('Qual seu problema na plataforma da Cambridge?\n'
                                        '1 - Esqueci minha senha.\n'
                                        '2 - Ainda não estou em uma turma.\n'
                                        '3 - Não sei meu username/email.\n'
                                        '4 - Perdi acesso ao meu email com o qual acessava a plataforma.\n'
                                        '5 - Não estou na turma/turma errada.\n'
                                        '6 - Sou aluno repetente.\n'
                                        '7 - Meu problema não é nenhum desses/meu problema não foi resolvido.\n')
        return CAMBRIDGE
    elif user_input == "3":
        await update.message.reply_text('Qual seu problema na plataforma da Pearson?\n'
                                        '1 - Perdi acesso ao meu email com o qual acessava a plataforma.\n'
                                        '2 - Não estou na turma/turma errada.\n'
                                        '3 - Sou aluno repetente.\n'
                                        '4 - Meu problema não é nenhum desses/meu problema não foi resolvido.\n')
        return PEARSON
    else:
        await update.message.reply_text('not a valid option')
        return ConversationHandler.END


# platforms funcs
async def cengage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    if user_input == "1":
        await update.message.reply_text('Se Icbeu123 não funcionar, nos envie o nome do student completo, nome do(a) teacher, dia e horário e em breve a senha será resetada para Icbeu123.')
    elif user_input == "2":
        await update.message.reply_text('Cheque o código da turma no grupo do WhatsApp e insira no campo "course key".')
    elif user_input == "3":
        await update.message.reply_text('Tire uma foto da página do código rasurado e envie o nome completo do(a) student, nome do(a) teacher e horário da aula. Encaminhe tudo para o teacher.')
    elif user_input == "4":
        await update.message.reply_text('Se não estiver na capa do seu livro insira o nome completo do(a) student, nome do(a) teacher e horário da aula, retornaremos o username para o seu contato assim que possível.')
    elif user_input == "5":
        try:
            response = forward_message("7503805557:AAG1BZ3SBN8sdTKRLllgC-XH-WUYVR_Wmr4", "7503805557", "1189922892", "1189922892")
            print(response)
        except requests.exceptions.RequestException as err:
            print('HTTP Request failed: ', err)


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
    await update.message.reply_text('Encerrando conversa.')
    return ConversationHandler.END
#app builder
app = ApplicationBuilder().token("7503805557:AAG1BZ3SBN8sdTKRLllgC-XH-WUYVR_Wmr4").build()

# main func
def main() -> None:
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ANSWER_HANDLING: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handling)],
            CENGAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cengage)],
            CAMBRIDGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cambridge)],
            PEARSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, pearson)],
            FOWARD_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conversation_handler)
    app.run_polling()


if __name__ == '__main__':
    main()



# app.add_handler(CommandHandler('start', start))
# app.run_polling()