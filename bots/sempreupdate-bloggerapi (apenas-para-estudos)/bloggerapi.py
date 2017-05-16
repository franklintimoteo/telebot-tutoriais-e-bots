import json
import logging
import requests
from requests import HTTPError
from telebot import logger


def get_id_blog(url, api_key):
    """Retorna id do blog atraves da URL
    :param url: link com http ou https"""

    logger.info("get_id_blog\nurl={}\napi_key={}".format(url, api_key))

    try:
        url = 'https://www.googleapis.com/blogger/v3/blogs/byurl?url='+url+\
            '&view=READER&fields=id&key='+api_key
        resposta = requests.get(url).content.decode('utf-8')
        blogID = json.loads(resposta)
        if blogID:
            return blogID.get('id')

    except HTTPError:
        return None

def get_posts_blog(url, api_key, num=1):
    """Retorna entidade post
    :param url: link com http ou https
    :param api_key: chave api google blogger
    :param num: quantidade de posts"""

    logger.info("get_posts_blog\nurl={}\napi_key={}\nnum={}".format(url, api_key, num))

    if 'http' not in url:
        raise KeyError('A url precisa conter http ou https')
    blogID = get_id_blog(url, api_key)
    resposta = None
    num = str(num)
    if blogID is not None:
        try:
            url = 'https://www.googleapis.com/blogger/v3/blogs/'\
                            +blogID+'/posts?fetchBodies=false&fetch\
                            Images=false&maxResults=' + num + '&orderBy=published&\
                            status=live&view=READER&key='+api_key
            resposta = requests.get(url).content.decode('utf-8')

            logger.info("Resposta ao buscar posts {}".format(resposta))
            if resposta:
                return resposta
        except HTTPError:
            return None

