import time
import sqlite3
import config

db_name = config.dbname

class BancoDados:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def __enter__(self):
        self.conn = sqlite3.connect(db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_value:
            print('Erro ao fechar conexão com ', db_name)
            raise

# Classe Cliente
class TicketCliente:
    """Classe ticket cliente"""
    def __init__(self):
        pass
    
    def salvar(self, id_user, nome, texto, data):
        """Salvar ticket
        :param int id_user      : id usuario Telegram
        :param str nome         : username Telegram
        :param str texto        : texto do ticket
        :param int data         : data em segundos
        """
        
        status = 1 # Status 1: enviado
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO tickets_salvos(id_user, nome_user, texto, data_envio, status)
            VALUES (?,?,?,?,?);""", (id_user, nome, texto, data, status))
            conn.commit()
            cursor.close()
    
    def buscar(self, id_user, num=10):
        """Busca ticket - retorna uma lista com tuplas
        :param int num          : Quantidade de tickets
        :param int id_user      : id usuario Telegram
        """
        
        status = 2 # Status 2: respondido
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT resposta, nome_admin, data_respondido, id_ticket
                FROM tickets_salvos
                WHERE id_user=? AND status=? ORDER BY id_ticket DESC LIMIT ?
                """, (id_user, status, num))
            resposta = cursor.fetchall()
            cursor.close()
        if resposta: 
            return resposta

    def buscarid(self, id_ticket, id_user):
        """Buscar ticket atraves do id_ticket
        :param int id_ticket:   :id ticket a buscar
        :param int id_user      :id usuario Telegram
        """

        status = 2 # Status 2: respondido
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT resposta, nome_admin, data_respondido, id_ticket
            FROM tickets_salvos
            WHERE id_ticket=? AND id_user=? AND status=?
            """, (id_ticket, id_user, status))
            resposta = cursor.fetchall()
            cursor.close()
            if resposta:
                return resposta

            
    def pendente(self, id_user):
        """Verificar ticket pendente
            retorna bool
        :param int id_user      : id usuario Telegram
        """
        status = 1 # Status 1: enviado
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT status FROM tickets_salvos
                WHERE id_user=? AND status=?
            """, (id_user, status))
            resposta = cursor.fetchone()
            cursor.close()
            if resposta:
                return True
                
class TicketAdmin:
    """Classe ticket admin"""
    
    def __init__(self):
        pass
    
    def atualizar(self, texto, data, username, id_ticket):
        """Atualizar/responder ticket criado
        :param str texto        : texto do ticket
        :param int data         : data em segundos
        :param str username     : username Telegram
        :param int id_ticket    : id ticket a responder
        """
        
        status = 2 # Status 2: respondido
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tickets_salvos
                SET resposta=?, data_respondido=?, nome_admin=?, status=?
                WHERE id_ticket=?
                """, (texto, data, username, status, id_ticket))
            conn.commit()
            cursor.close()

    def ativos(self, num=3):
        """Retorna tickets pendentes
        :param int num          : Quantidade de tickets
        """
        
        status = 1 # Status 1: enviado
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_ticket, texto, nome_user, data_envio
                FROM tickets_salvos 
                WHERE status=? LIMIT ?
            """, (status,num))
            resposta = cursor.fetchall()
            cursor.close()
            if resposta:
                return resposta

    def existe(self, id_ticket):
        """Verificar existencia de ticket"""

        status = 1 # Status 1: enviado
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT status FROM tickets_salvos
                WHERE id_ticket=? AND status=?
            """, (id_ticket, status))
            resposta = cursor.fetchone()
            cursor.close()
            if resposta:
                return True