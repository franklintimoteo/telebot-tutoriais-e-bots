import time
import logging
import sys

from sistemaranking import Ranking
import dbmod
import config
import telebot


# Autentica e cria aliase para message_handler
bot = telebot.TeleBot(config.token)
handler = bot.message_handler
ranking = Ranking() # Instancia sistema de ranking

def modo_debug():
    # Ativa o modo debug
    
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)
    
def formatar_post(post):
    # Formatar um post
    
    telebot.logger.info('Formatando post.')
    data = post[1]
    url = post[2]
    autor = post[3]
    etiquetas = post[4]
    titulo = post[5]

    postformatado = config.modelopost.format(titulo, url, autor, data, etiquetas)
    return postformatado


@handler(commands=['ajuda', 'help'])
def ajuda(msg):
    # Enviar mensagem de ajuda
    
    telebot.logger.info('Enviando mensagem de ajuda.')
    bot.send_message(msg.chat.id, config.ajuda, parse_mode='HTML')


@handler(commands=['receber_noticias'])
def adicionar_grupo(msg):
    dbmod.salvar_grupo(msg.chat.id)
    bot.send_chat_action(msg.chat.id, 'typing')
    time.sleep(3)
    text = "<b>A partir de agora você estará recebendo posts do Sempre Update</b>"
    bot.send_message(msg.chat.id, text, parse_mode='HTML')


@handler(commands=['ranking'])
def mostrar_ranking(msg):
    # Buscar ranking, formatar e enviar

    text = """🔝 <b>Ranking</b> 🔝\n\n"""
    ranklist = ranking.getranking(msg.chat.id)
    if msg.chat.type not in "supergroup group":
        bot.send_message(msg.chat.id, "Precisa me colocar em um grupo para esse comando funcionar.")
    elif not ranklist:
        bot.reply_to(msg, "Parece que ninguém do grupo foi pontuado por ajudar outro membro.😔")
    else:
        text += "".join(['✨  {} <b>+{}</b>\n'.format(user[0], user[1]) for user in ranklist])
        telebot.logger.info("Ranking formatado {}".format(text))
        bot.send_message(msg.chat.id, text, parse_mode='HTML')


@handler(commands=['+1'])
def adicionar_ponto(msg):
    # Adicionar ponto ao username salvo

    text = msg.text.split()
    if msg.chat.type not in "supergroup group":
        bot.send_message(msg.chat.id, "Me adicione em um grupo para esse comando funcionar")
    elif len(text) <= 1:
        bot.reply_to(msg, "Tente /+1 @username.")
    elif ('@'+msg.from_user.username).lower() == text[1].lower():
        bot.send_message(msg.chat.id, "Você não pode votar em si mesmo.")
    elif not text[1].startswith('@'):
        bot.reply_to(msg, "Um username precisa conter @ no início.")
    else:
        bot.send_chat_action(msg.chat.id, 'typing')
        time.sleep(3)
        ranking.addscore(text[1], msg.chat.id)
        title = msg.chat.title
        bot.send_message(msg.chat.id, "{0} agradece você, {1} por ajudar o {2}.😄👏".format(title ,text[1], msg.from_user.first_name))


@handler(commands=['rmponto'])
def remover_pontos(msg):
    # Remover ponto do username

    text = msg.text.split()
    telebot.logger.info("Removendo ponto com texto: {}".format(text))

    if msg.chat.type in "supergroup group":
        adminlist = [admin.user.id for admin in bot.get_chat_administrators(msg.chat.id)]
    if msg.chat.type not in "supergroup group":
        return bot.send_message(msg.chat.id, "Esse comando só funciona em um grupo.")
    elif msg.from_user.id not in adminlist:
        bot.reply_to(msg, "Você precisa ser um admin para usar este comando.")
    elif len(text) < 2:
        bot.reply_to(msg, "Tente /rmponto @username.")
    else:
        if ranking.removescore(text[1], msg.chat.id):
            bot.reply_to(msg, "Ponto removido! ")
        else:
            bot.reply_to(msg, "Usuário não encontrado")


if __name__ == '__main__':
    if sys.argv[-1] in "--debug":
        modo_debug()

    print("SUBOT Executando...")
    bot.polling()