import os

# url site contendo http ou https
webSite = 'http://www.sempreupdate.com.br'

# Nome banco de dados
nomeDB = 'dataposts.db'

# Time zone
tzone = 'America/Sao_Paulo'

# Api key blogger
api_key = os.environ['API_BLOGGER']

# Token bot
token = os.environ['TOKEN_SUBOT']

# Mensagens
ajuda = """
    \n/receber_noticias - <code>Receba notícias assim que sairem no SU</code>\
    \n/ranking - <code>Visualize o ranking dos membros pontuados por colaborar</code>\
    \n/+1 @username - <code>Pontue um membro por lhe ajudar (Ex: /+1 @Illuminarch)</code>\
    \n\n<b>Administradores</b>\
    \n/rmponto @username (padrao=1) - <code>(Ex: /rmponto @Illuminarch)</code>\
    \n<code>É possível adicionar esse bot a outros groupos.</code>\
"""

modelopost = """
        \n[{0}]({1})\
        \n\n📆<b>Data:</b> {3}\
        \n✍<b>Autor:</b> {2}\
        \n📌<b>Tags:</b> {4}\
        \n🌐<b>Página inicial:</b> www.sempreupdate.com.br"""