# -*- coding: UTF-8 -*
#!/usr/bin/python3

import telebot
from os import popen
###############################
token = open('token.txt')
hash = token.readline()
bot = telebot.TeleBot(hash)
token.close()
###############################

idUser = 98339387

################################################################################
def testarUsuario(usuarioId):
    global idUser
    if(idUser == usuarioId):
        return True
    else:
        return False
      
def executarBash(comando):
    saidaComando = popen(comando).read()
    return(saidaComando)
  
def encaminharMensagem(mensagem, chatId):
    bot.send_message(chatId, '{}'.format(mensagem))
    
@bot.message_handler(commands=['meuid','meuId','id','Id','myid','myId'])
def userId(message):
    bot.send_message(message.chat.id, '{} seu ID Telegram é: {}'.format(message.from_user.first_name,message.chat.id))

@bot.message_handler()
def bash(message):
    if(testarUsuario(message.from_user.id) == True):
        try:
            entradaComando = executarBash(message.text)
            encaminharMensagem(entradaComando, message.chat.id)            
        except Exception:
            entradaComando = "Algo errado."
            encaminharMensagem(entradaComando, message.chat.id)            
    else:
        bot.send_message(message.chat.id, 'Você não tem permissão para utilizar esse bot!')
    
#################################################################################   
print("Bot iniciado!")
bot.polling()