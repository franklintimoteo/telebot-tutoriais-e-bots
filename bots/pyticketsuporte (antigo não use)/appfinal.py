import time
import telebot
from telebot import types
import ticketfinal
import config


bot = telebot.TeleBot(config.token)
cmd = bot.message_handler
admintc = ticketfinal.TicketAdmin()
clientetc = ticketfinal.TicketCliente()

def criar_teclado(numtickets):
    """Criar teclado com o id dos tickets"""

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for num in numtickets:
        markup.add(types.KeyboardButton('/ticket '+ str(num)))
    return markup

@cmd(commands=['help', 'ajuda'])
def helper(msg):
    # Enviar mensagem de ajuda
    if msg.from_user.id not in config.admins:
        texto = config.ajuda
    else:
        texto = config.ajudaadmin

    bot.send_message(msg.chat.id, texto, parse_mode='Markdown')

@cmd(commands=['criarticket'])
def criar_ticket(msg):
    # Criar ticket com texto da mensagem
    
    texto = msg.text.split(maxsplit=1)
    if msg.chat.type not in 'private':
        bot.send_message(msg.chat.id, config.erro['naoprivado'])
    elif len(texto) <= 1:
        bot.send_message(msg.chat.id, config.erro['faltatexto'])
    else:
        texto = texto[1]
        userid = msg.from_user.id
        username = '@'+str(msg.from_user.username)
        data = time.time()
        if not clientetc.pendente(userid):
            clientetc.salvar(userid, username, texto, data)
            bot.send_message(msg.chat.id, config.sucesso['criado'])
            bot.send_message(config.gruposuporte[0], 'Novo ticket registrado por '+ username)
        else:
            bot.send_message(msg.chat.id, config.erro['pendente'])

@cmd(commands=['meuticket'])
def meu_ticket(msg):
    # Visualiza tickets
    
    userid = msg.from_user.id
    if msg.chat.type not in 'private':
        bot.send_message(msg.chat.id, config.erro['naoprivado2'])
    elif clientetc.pendente(userid):
        bot.send_message(msg.chat.id, config.erro['pendente'])
    elif not clientetc.buscar(userid, num=10):
        bot.send_message(msg.chat.id, config.erro['naoexiste'])
    else:
        listaticket = clientetc.buscar(userid)
        numtickets = [num for _,_,_,num in listaticket]
        bot.send_message(msg.chat.id, 'Escolha um ticket: ', reply_markup=criar_teclado(numtickets))

@cmd(commands=['ticket'])
def buscar_ticket(msg):
    # Buscar ticket pelo numero Ex: /ticket 1

    userid = msg.from_user.id
    texto = msg.text.split(maxsplit=1)
    if msg.chat.type not in 'private':
        bot.send_message(msg.chat.id, config.erro['naoprivado'])
    elif len(texto) <= 1:
        bot.send_message(msg.chat.id, config.erro['faltanumero'])
    elif not clientetc.buscar(userid, num=1):
        bot.send_message(msg.chat.id, config.erro['naoexiste'])
    elif not texto[1].isnumeric():
        bot.send_message(msg.chat.id, config.erro['faltanumero'])
    else:
        texto = texto[1]
        listaticket = clientetc.buscarid(texto, userid)
        if listaticket:
            resposta, nomeadmin, data, _ = listaticket[0]
            data = time.strftime('%d/%m/%Y %X', time.localtime(data))
            texto = '''
            *{adm} {data}*
            ``` {texto}```
            '''.format(adm=nomeadmin, data=data, texto=resposta)
            bot.send_message(msg.chat.id, texto, parse_mode='Markdown')
        else:
            bot.send_message(msg.chat.id, config.erro['naoexiste'])

@cmd(commands=['responder'])
def responder_ticket(msg):
    # Responder ticket sendo admin

    texto = msg.text.split(maxsplit=2)
    if msg.from_user.id not in config.admins:
        return
    elif msg.chat.id not in config.gruposuporte:
        return
    elif len(texto) <= 1 or not texto[1].isnumeric():
        bot.send_message(msg.chat.id, config.erro['faltanumero'])
    elif len(texto) <= 2:
        bot.send_message(msg.chat.id, config.erro['faltatexto2'])
    elif not admintc.existe(texto[2]):
        bot.send_message(msg.chat.id, config.erro['naoexisteidticket'])
    else:
        id_ticket = texto[1]
        texto = texto[2]
        data = time.time()
        username = '@' + msg.from_user.username
        admintc.atualizar(texto, data, username, id_ticket)
        bot.send_message(msg.chat.id, config.sucesso['respondido'])

@cmd(commands=['listar'])
def listar_tickets(msg):
    # Listar tickets ativos

    if msg.from_user.id not in config.admins:
        return
    elif msg.chat.id not in config.gruposuporte:
        return
    else:
        listatickets = admintc.ativos()
        if listatickets:
            for tck in listatickets:
                id_ticket, texto, nomeuser, dataenvio = tck
                dataenvio = time.strftime('%d/%m/%Y %X', time.localtime(dataenvio))
                texto = """
                *ID:* {id}
                \n*Usuário*: {user}
                \n*Data de envio:* {data}
                \n``` {texto}```
                """.format(id=id_ticket, user=nomeuser, data=dataenvio, texto=texto)
                bot.send_message(msg.chat.id, texto,parse_mode='Markdown')
        else:
            bot.send_message(msg.chat.id, config.erro['nenhumpendente'])


print('Executando...')
bot.polling(none_stop=True, timeout=30)