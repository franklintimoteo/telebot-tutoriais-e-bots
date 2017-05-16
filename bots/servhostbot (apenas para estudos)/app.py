import os, time
from random import randint
import telebot
import dbmod
import sshmod
import config

os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

token = '311791154:AAHSuE4nhUI0sgBVk8DUoAmRhGfvgyZQhEk'
bot = telebot.TeleBot(token)

config.senha_sudo = input("Digite a senha sudo:\n-->")
grupo = -1001076315011

def gerar_senha():
    letras = "abcdefghjkmnpqrstuvxywzABCDEFGHJKMNPQRSTUVXYWZ"
    senha = ""
    n = len(letras)
    for e in range(8):
        senha += letras[randint(0,n)]
    return senha

def reply(msg, texto, font=None, parse_mode=None):
    if font:
        if 'italic' in font:
            texto = '<i>'+str(texto)+'</i>'
        elif 'bold' in font:
            texto = '<b>'+str(texto)+'</b>'
        else:
            pass
        parse_mode="HTML"
    bot.reply_to(msg, texto, parse_mode=parse_mode)

def send_msg(msg, texto, font=None, parse_mode=None):
   if font:
       if 'italic' in font:
           texto = '<i>'+str(texto)+'</i>'
       elif 'bold' in font:
           texto = '<b>'+str(texto)+'</b>'
       else:
           pass
       parse_mode="HTML"
   bot.send_message(msg.chat.id, texto, parse_mode=parse_mode)
 
 
@bot.message_handler(commands=['cadastrar'])
def cadastrar(msg):
    
    texto = msg.text.split(maxsplit=1)
    
    if msg.chat.id != grupo:
        send_msg(msg, "Esse Robô não funciona aqui.")
    elif dbmod.existe(msg.from_user.id):
        reply(msg, "Você já está cadastrado.", font='italic')
    elif len(texto) <= 1:
        reply(msg, "Tente /cadastrar seunome.", font='italic')
    elif not texto[1].isalpha():
        reply(msg, "O usuário deve conter somente letras.", font='italic')
    else:
        username = texto[1]
        senha = gerar_senha()
        vencimento = time.time() + config.dias_experimental
        if sshmod.useradd(username, senha):
            dbmod.cadastrar(msg.from_user.id, senha, vencimento)
            send_msg(msg, """{} cadastrado com sucesso!
                    \nATENÇÃO: Somente no nome de usuário, use apenas letras minusculas.
                    \nNa senha utilize de acordo com o que foi fornecido.
                    \nFale comigo no privado, e digite /senha para receber a sua senha.""".format(texto[1]), font='bold')
        else:
            send_msg(msg, "Usuário {} já existe.".format(texto[1]))

@bot.message_handler(commands=['renovar'])
def renovar(msg):
    
    atraso = 1800
    vencer = time.time() + (config.dias_experimental - atraso)
    
    if msg.chat.id != grupo:
        send_msg(msg, "Esse Robô não funciona aqui.")
    # Verifica se o plano irá vencer em 30 minutos ou já venceu
    elif not dbmod.venceu(msg.from_user.id, vencer):
        reply(msg, "Seu plano ainda não venceu.", font='italic')
    else:
        if dbmod.existe(msg.from_user.id):
            data_atual = time.time() 
            vencimento = data_atual + config.dias_experimental
            if dbmod.renovar(msg.from_user.id, vencimento):
                send_msg(msg, "Renovado com sucesso!", font='bold')
            else:
                send_msg(msg, "Ocorreu algum problema ao renovar seu cadastro.", font='bold')
        else:
            reply(msg, "Você ainda não está cadastrado.", font='italic')


@bot.message_handler(commands=['senha'])
def enviar_senha(msg):
    
    if msg.chat.type != 'private':
        send_msg(msg, "Solicite sua senha no privado comigo.", font='italic')
    elif not dbmod.existe(msg.from_user.id):
        send_msg(msg, "Cadastro não encontrado.", font='italic')
    else:
        senha = dbmod.senha(msg.from_user.id)
        if senha:
            send_msg(msg, "Sua senha é {}.".format(senha), font='bold')
        else:
            send_msg(msg, "Ocorreu algum problema ao procurar sua senha.", font='italic')

@bot.message_handler(commands=['id'])
def identifcar_grupo(msg):
    send_msg(msg, "ID chat: {}".format(msg.chat.id), font='bold')

print('Executando...')
bot.polling()