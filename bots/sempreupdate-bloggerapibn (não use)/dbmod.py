import json
import sqlite3
import time
import config
import logging

from telebot import logger
import bloggerapi

nomeDB = config.nomeDB
webSite = config.webSite
api_key = config.api_key

class BancoDados:
    """Instanciar sqlite para usar no 'with'"""

    logger.info("Entrando na classe BancoDados")
    def __init__(self, nomeDB):
        self.db_name = nomeDB

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_value:
            raise

def status_postado(idPost):
    """Checar se o id do post foi postado
    :param idPost: id do post capturado pela bloggerapi"""

    logger.info("Verificando se foi postado com id post: {}".format(idPost))
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT publicado FROM publicacoes WHERE idPost=?", (idPost,))
        resposta = cursor.fetchone()
        cursor.close()
        if resposta:
            return 1 in resposta


def existe_id(idPost):
    """Checar se o id do post existe do Banco de dados
    :param idPost: id do post capturado pela bloggerapi"""

    logger.info("Verificando se existe idpost com o id: {}".format(idPost))
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT idPost FROM publicacoes WHERE idPost=?;
            """, (idPost,))
        resposta = cursor.fetchone()
        cursor.close()
        if resposta:
            return idPost in resposta


def atualizar_db():
    """Atualizar banco de dados buscando 5 posts"""

    posts = bloggerapi.get_posts_blog(webSite, api_key, num=5)
    posts = json.loads(posts)

    logger.info('Atualizando db com os posts:\n {}'.format(posts))
    for post in posts.get('items'):
        idPost = int(post['id'])
        data = post['published'][0:10]
        url = post['url']
        autor = post['author']['displayName']
        etiquetas = ', '.join(post['labels'])
        titulo = post['title']
        publicado = 0
        if not existe_id(idPost):
            with BancoDados(nomeDB) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO publicacoes
                    (data_publicacao, url, autor, etiquetas, titulo, publicado, idPost)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                               (data, url, autor, etiquetas, titulo, publicado, idPost))
                conn.commit()
                cursor.close()

    logger.info("Banco de dados atualizado")


def atualizar_status(idPost):
    """Atualizar status do post para 1(postado)
    :param idPost: id do post capturado pela bloggerapi"""

    logger.info("Atualizando status para postado com o id: {}".format(idPost))
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE publicacoes SET publicado=1 WHERE idPost=?;""", (idPost,))
        conn.commit()
        cursor.close()

def buscar_posts():
    """Buscar posts no banco de dados com a data atual"""

    logger.info("Buscando posts no banco de dados por data.")
    dataHoje = time.strftime('%Y-%m-%d')
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM publicacoes WHERE data_publicacao=?", (dataHoje,))
        resposta = cursor.fetchall()
        cursor.close()
        if resposta:
            return resposta

def ultimo_post(limit=10):
    """Buscar ultimos posts adicionados no banco de dados
    :param limit: quantidade de posts retornados"""

    logger.info("Buscando ultimos posts no banco de dados.")
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM publicacoes ORDER BY id DESC limit ?;", (limit,))
        resposta = cursor.fetchall()
        cursor.close()
        if resposta:
            return resposta

##### Controle de grupos
def salvar_grupo(idgrupo):
    """Salvar o id do grupo na tabela grupos"""
    
    if type(idgrupo) != int:
        raise TypeError('Grupo id deve ser do tipo inteiro')
    logger.info("Salvando id grupo: {}".format(idgrupo))
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT OR IGNORE INTO grupos(idgrupo)
		VALUES(?)""", (idgrupo,))
        conn.commit()
        cursor.close()

def apagar_grupo(idgrupo):
    """Apagar id go grupo"""

    logger.info("Apagando id grupo {}".format(idgrupo))
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grupos WHERE idgrupo=?",(idgrupo,))
        conn.commit(())
        cursor.close()

def buscar_grupos():
    """Retornar os ids dos grupos salvos"""

    logger.info("Buscando id dos grupos salvos.")
    with BancoDados(nomeDB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT idgrupo FROM grupos")
        resposta = cursor.fetchall()
        cursor.close()
        if resposta:
            return resposta[0]
