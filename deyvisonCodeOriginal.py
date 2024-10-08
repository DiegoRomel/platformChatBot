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

NOME, LOCAL, DESCRICAO, CHAMADO = range(4)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""

    update.message.reply_text(
        'Olá! Bem vindo ao suporte do ICBEU, eu sou o TETI e irei te ajudar a registrar o chamado!\n'
        'Para começar, digite o seu nome e sobrenome:\n'
        '\nVocê pode enviar a qualquer momento /cancel para cancelar o chamado ou se desejar registrar um novo chamado em outro momento, basta digitar\n/start.'
        
    )
    return NOME


def nome(update: Update, context: CallbackContext) -> int:
    """Stores the name and asks the location."""
    user = update.message.from_user

    arquivo = open('%s.txt' % user.id, 'w')
    arquivo.write(str(update.message.text) + ', ')
    arquivo.close()
    
    logger.info("O usuário %s informou que seu nome é: %s", user.first_name, update.message.text)
    
    update.message.reply_text(
        'Obrigado!\n\n'
        'Agora pode me dizer onde você está?\nPor exemplo: Sala 23, Galeria, etc.'
    )

    return LOCAL


def local(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for a description of the problem."""
    user = update.message.from_user

    arquivo = open('%s.txt' % user.id, 'a')
    arquivo.write(str(update.message.text) + ', ')
    arquivo.close()
    
    logger.info("A localização do usuário %s é: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Ótimo!\n\n'
        'Agora pode me relatar o problema que está ocorrendo?\n'
    )

    return DESCRICAO


def descricao(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user

    arquivo = open('%s.txt' % user.id, 'a')
    arquivo.write(str(update.message.text))
    arquivo.close()
    
    logger.info("O usuário %s informou o problema: %s", user.first_name, update.message.text)
    
    update.message.reply_text(
        'Ok! Já estamos finalizando.\n\n'
        'Por favor, confirme a criação do seu chamado digitando /criarchamado.\n'
    )

    return CHAMADO

def chamado(update: Update, context: CallbackContext) -> int:
    
    user = update.message.from_user
    
    logger.info("O usuário %s CRIOU O CHAMADO!", user.first_name)
    
    update.message.reply_text(
        'Chamado registrado!\n\n'
        'Em breve um dos nossos técnicos do suporte irá entrar em contato com você.\n'
        'Obrigado por usar o suporte do ICBEU pelo Telegram.'
    )
    
    
    arquivo = open('%s.txt' % user.id, 'r')
    infos = arquivo.readlines()
    arquivo.close()
    
    info_geral = infos[0]

    base_url = 'http://192.168.0.42/apirest.php/'
    init_uri = 'initSession'
    ticket_uri = 'Ticket'
    kill_uri = 'killSession'
    app_token = 'UXayBCPeREbFLGNGkotIQJqYZbHaWkDg4ac3VZZw'
    user_token = 'm2uLdOQK1IqEJMtXiSaWB37F0ljizyAbhgDYWZEY'


    try:
        response = requests.get(
            url="{}{}".format(base_url,init_uri),
            params={
                "app_token": app_token,
                "user_token": user_token
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(content=response.content))

        resp_json = response.json()
        session_token = resp_json['session_token']
        print(session_token)

        headers = {"Session-Token":session_token, "App-Token":app_token, "Content-Type": "application/json"}
   
        ticket_input = {"input": {"name": info_geral, "content": info_geral, "requesttypes_id": "7"}}

        post_ticket = requests.post(url="{}{}".format(base_url,ticket_uri), headers=headers, data=json.dumps(ticket_input))
        print(post_ticket.content)
        
        kill_headers = {"Session-Token":session_token, "App-Token":app_token, "Content-Type": "application/json"}
        kill_session = requests.get(url="{}{}".format(base_url,kill_uri), headers=kill_headers)
    
    except requests.exceptions.RequestException as err:
        print('HTTP Request failed: ', err)
    
    
    return ConversationHandler.END


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
    updater = Updater("1914804837:AAFa_vIrVx-1v4dModk6Jw2wz_bdOadlvIg")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NOME: [MessageHandler(Filters.text & ~Filters.command, nome)],
            LOCAL: [MessageHandler(Filters.text & ~Filters.command, local)],
            DESCRICAO: [MessageHandler(Filters.text & ~Filters.command, descricao)],
            CHAMADO: [CommandHandler('criarchamado', chamado)]
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