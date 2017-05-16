+ Guia
	+ [Obtendo Token](#obtendo-o-token)
	+ [Protegendo o Token](#protegendo-o-token)
	+ [Entendendo o Telebot de forma resumida](#entendendo-o-telebot-de-forma-resumida)
	+ [Arquitetura do objeto messsage](#arquitetura-do-objeto-messsage)
	+ [Autenticação com o User ID Telegram](#autenticação-com-o-user-id-telegram)
	+ [Executando comando e capturando resposta](#executando-comando-e-capturando-resposta)
	+ [Tratando qualquer mensagem como comando](#tratando-qualquer-mensagem-como-comando)
	+ [Final](#final)

# Usando Telebot como SSH.


### Obtendo o Token
	
O token é obtido através do  [@BotFather](https://telegram.me/botfather) pelo próprio Telegram. Acessando esse bot, ele irá te pedir nome para o bot e em segundo, pedirá o nome que servirá como link para você e outras pessoas o acessarem, esse devendo ter a palavra "Bot".

No final você obterá uma hash, chamada de token pelo Telegram, algo como:

	123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

Esse token é uma identificação única para que você tenha acesso ao seu bot.


### Protegendo o Token

Para proteger o token de um erro humano, de ter compartilhado o token junto com seu codígo Python, eu adicionei o token em um arquivo txt, evitando de ter a hash exposta no próprio código.

```python
token = open('token.txt') #Abre o arquivo token.txt
hash = token.readline() #Lê a primeira linha e adiciona o valor a variável hash
bot = telebot.TeleBot(hash) #Cria uma instância do Telebot com a hash
token.close() #Fecha o arquivo token.txt
```

O token deverá ser adicionado na primeira linha do arquivo.


### Entendendo o Telebot de forma resumida
O código abaixo responde sempre que /meuid, /meuId, /id, /Id etc.., é enviado.
```python
@bot.message_handler(commands=['meuid','meuId','id','Id','myid','myId'])
def userId(message):
    bot.send_message(message.chat.id, '{} seu ID Telegram é: {}'.format(message.from_user.first_name,message.chat.id))
```


A linha abaixo, faz com que capture todas mensagens que cheguem.
```python
@bot.message_handler()	
```
Para adicionar uma ação para essas mensagens, precisa ser adicionada uma função logo a baixo.

```python
def acao(message):
```
Dentro dessa função podemos adicionar qualquer tipo de resposta válida no Telegram como, citar a mensagem, enviar contato, gif, videos, imagens etc. Exemplo:
```python
bot.send_message(message.chat.id, '{} seu ID Telegram é: {}'.format(message.from_user.first_name,mmessage.from_user.id))
```
```python
bot.send_message(message.chat.id, "Algo") #Envia uma mensagem para o Id do chat aberto no Telegram
message.from_user.first_name #Captura o primeiro nome do usuário
message.from_user.id #Captura o ID do usuário
``` 
No final o bot enviará uma mensagem com o ID e Primeiro nome do usuário para o chat aberto.

O código abaixo enviará uma mensagem para o chatId que foi recebido:
Poderia ser acessado como:
```encaminharMensagem('Olá usuário. Boa tarde!', 788546487)```
```python
def encaminharMensagem(mensagem, chatId):
    bot.send_message(chatId, '{}'.format(mensagem))
```
Ao final do script deve ser adicionado a linha: ```bot.polling()``` para que o bot entre em um loop, esperando contato.

### Arquitetura do objeto messsage

Abaixo você pode ver como o objeto message é formado.

```python
{
   'venue':None,
   'entities':[
      <telebot.types.MessageEntity object at 0x7f4cd6633c88>
   ],
   'edit_date':None,
   'sticker':None,
   'new_chat_photo':None,
   'caption':None,
   'from_user':{
      'id':98339387,
      'username':'Ftimoteo',
      'first_name':'Franklin',
      'last_name':'T.'
   },
   'photo':None,
   'group_chat_created':None,
   'text':'/status',
   'delete_chat_photo':None,
   'left_chat_member':None,
   'contact':None,
   'location':None,
   'reply_to_message':None,
   'date':1465965855,
   'chat':{
      'id':98339387,
      'title':None,
      'username':'Ftimoteo',
      'type':'private',
      'first_name':'Franklin💻',
      'last_name':'T.'
   },
   'content_type':'text',
   'forward_date':None,
   'migrate_to_chat_id':None,
   'audio':None,
   'forward_from_chat':None,
   'voice':None,
   'channel_chat_created':None,
   'new_chat_title':None,
   'message_id':76,
   'migrate_from_chat_id':None,
   'supergroup_chat_created':None,
   'forward_from':None,
   'pinned_message':None,
   'new_chat_member':None,
   'document':None,
   'video':None
}
```

Veja como é simples. Para acessar o tipo de conversa apenas use:
```python
message.chat.type # Isso será igual a private do tipo, string.
```

##### Para mais informações acesse:
* [Repositório do Telebot](https://github.com/eternnoir/pyTelegramBotAPI)
* [Telegram Bot API](https://core.telegram.org/bots/api)

### Autenticação com o User ID Telegram

Para que se obtenha acesso ao bot de forma gerenciada ou seja, só alguns usuários podem utilizar os comandos, caso contrário uma mensagem de "Você não tem permissão será gerada", pode-se utilizar o ID único de usuário do Telegram acessado atráves do ```message.from_user.id```

```python
idUser = 98339387 #Adicionado para ser uma variável global de fácil alteração
```

```python
def testarUsuario(usuarioId):
    global idUser
    if(idUser == usuarioId):
        return True
    else:
        return False
```
Assim podemos utilizar a função acima para verificar se a mensagem é recebida por um usuário autenticado. Lembre-se que o id chega em formato int.

### Executando comando e capturando resposta

Usada a função popen da biblioteca os. Vale lembrar que esse script é simples e a função popen nos dar algumas limitações quando usada atráves do Telegram Bot.
```python
def executarBash(comando):
    saidaComando = popen(comando).read() #Executa o comando e captura a saida adicionando a variável saidaComando atráves do .read()
    return(saidaComando) #Retorna a saida
```


Algumas limitações encontradas:
No script não foi adicionado um modo de enviar a senha logo após ser requisitado. Felizmente no linux há algumas maneiras de resolver isso como:
```
Editar o arquivo /etc/sudoers com o comando visudo
```
Adicionando a linha:
```
nomeusuario		ALL=(ALL)		NOPASSWORD: ALL
```
A linha acima fara com que o usuário não precise digitar sua própria senha para ter acesso administrativos, mas só funcionará se o usuário estiver no grupo que permita ter esse acesso. No ubuntu você precisará adicionar o usuário. Já em outras distribuições o usuário já vem adicionado ao grupo com privilégio administrador. Ou seja sempre que for enviado um comando com sudo este usuário não precisará digitar sua senha.

### Tratando qualquer mensagem como comando

Se nenhuma das opções acima for utilizada o script trata a mensagem como sendo um comando para ser utilizado na função ```popen```, algo como:
```python
@bot.message_handler() #Se nenhum função acima for utilizada, o bot chegará até aqui.
def bash(message): #Repassa o objeto message para essa função
    if(testarUsuario(message.from_user.id) == True): #Testa se o usuário está autorizado
        try:
            entradaComando = executarBash(message.text) #Envia o comando e recebe a saida
            encaminharMensagem(entradaComando, message.chat.id) #Encaminha a saida para o usuário            
        except Exception: #Caso qualquer coisa de errado, é enviada uma mensagem para o usuário.(Aqui geranalizei com Exception, você pode filtrar melhor)
            entradaComando = "Algo errado."
            encaminharMensagem(entradaComando, message.chat.id) #Envia a mensagem para o usuário            
    else:
        bot.send_message(message.chat.id, 'Você não tem permissão para utilizar esse bot!') #Se o usuário não tem autorização, receberá essa mensagem.
```
### Final
Vale citar que existem outras bibliotecas para utilizar ao lugar do os.popen.

Por fim, deixo meu Telegram @ftimoteo para eventuais dúvidas e sugestões.

