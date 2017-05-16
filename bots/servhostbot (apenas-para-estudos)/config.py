import os

def token():
    if "TOKEN_SERVHOST" not in os.environ:
        exit("Adicione a variavel global TOKEN_SERVHOST no sistema.")
    return os.environ['TOKEN_SERVHOST']

dias_renovar = 172800 # Dias em segundos para renovação
dias_experimental = 172800 # Dias em segundos para experimentar
senha_sudo = ""