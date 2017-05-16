### TOKEN ###
token = 'SEU TOKEN AQUI'

## DATA BASE ##
dbname = 'tickets.db'

## MENSAGENS ##
erro = {'naoprivado': 'Para criar um ticket, fale comigo no privado.',
        'naoprivado2': 'Esse comando só funciona no privado.',
        'faltatexto': 'Preciso de um texto para encaminhar ao suporte.',
        'pendente': 'Já existe um ticket pendente! Aguarde até ser respondido.',
        'naoexiste': 'Não encontrei nenhum ticket em meu sistema.',
        'naoexisteidticket': 'Não encontrei nenhum ticket com esse número.',
        'faltanumero': 'Tente /meuticket 10.',
        'faltatexto2': 'Preciso de um texto para responder ao usuário.',
        'nenhumpendente': 'Nenhum ticket pendente.'}

sucesso = {'criado': 'Ticket enviado! Aguarde nosso retorno no prazo de 24 horas.',
           'respondido': 'Ticket respondido com sucesso!'}
ajuda = '''
    \n/criarticket ``` Forneça seu login APENAS. Digite toda sua dúvida apenas nessa mensagem que irá junto com o comando.```
    \n/help ``` Exibe mensagem de ajuda```
    \n/meuticket ``` Utilize esse comando para verificar se há uma resposta ao seu ticket```
    *Atenção: Nosso bot tentará enviar-lhe uma resposta assim que o status do ticket or alterado.\
    Se por algum motivo o bot não te enviar uma mensagem em 24 horas, acesse o comando /meuticket.*
    '''
ajudaadmin = '''
    \n/responder 10 ``` Responder o ticket número 10```
    \n/listar ``` Listar tickets ativos```
''' + ajuda

### ADMINS ###
admins = [265159574, 98339387, 274456415]

## GRUPO SUPORTE ##
gruposuporte = [-1001073560805]