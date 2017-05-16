import telebot
from telebot import types

TOKEN = "SEU TOKEN DO BOT AQUI"


bot = telebot.TeleBot(TOKEN)

alarme = False

@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    """Receber resposta callback_data"""
    global alarme
    if 'on/off' in call.data and alarme:
        alarme = False
    else:
        alarme = True


def teclado():
    """Retornar um teclado inline"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    botao = types.InlineKeyboardButton(text='Ativar/Desativar', callback_data='on/off')
    markup.add(botao)
    return markup


@bot.message_handler(commands=['help'])
def helper(msg):
    """Retornar botao inline de ajuda"""
    bot.send_message(msg.chat.id, 'Pressione esse botão!', reply_markup=teclado())

@bot.message_handler(commands=['status'])
def status(msg):
    """Retornar o status atual do botao"""
    bot.send_message(msg.chat.id, 'O status atual do alarme é: {}.'.format(alarme))

print("Iniciando")
bot.polling()
