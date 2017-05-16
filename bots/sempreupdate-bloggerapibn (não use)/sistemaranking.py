import sqlite3 


class Ranking:
    """Manipula ranking"""
    def __init__(self):
        "Carrega ranking na memoria"
        self.nomeDB = 'dataposts.db'
        
    def __newuser(self, username, chat_id):
        """Cria um novo usuario para inserir pontos
        username: username do telegram
        chat_id: id do chat"""
        if not username or not chat_id:
            raise AttributeError

        conn = sqlite3.connect(self.nomeDB)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO ranking(username, chat_id, pontos) VALUES (?,?,?)
        """, (username, chat_id, 0))
        conn.commit()
        cursor.close()
        conn.close()
    
    def addscore(self, username, chat_id, count=1):
        """Adiciona pontos ao usuario
        username: username do telegram
        chat_id: id do chat
        count: quantidade (Padrao 1)
        Atualiza ranking
        """

        if not username or not chat_id:
            raise AttributeError
            
        if not self.exists(username, chat_id):
            self.__newuser(username, chat_id)
        
        conn = sqlite3.connect(self.nomeDB)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ranking
            SET pontos = pontos +?
            WHERE username LIKE ? AND chat_id=?
        """, (count, username, chat_id))
        conn.commit()
        cursor.close()
        conn.close()
        
    def removescore(self, username, chat_id, count=1):
        """Remove pontos do usuario
        username: username do telegram
        chat_id: id do chat
        count: quantidade (Padrao 1)"""
        if not username or not chat_id:
            raise AttributeError
        if not self.exists(username, chat_id):
            return False
        
        conn = sqlite3.connect(self.nomeDB)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ranking
            SET pontos = pontos -?
            WHERE username LIKE ? AND chat_id=?
        """, (count, username, chat_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    def getranking(self, chat_id):
        """Retorna uma lista do ranking
        chat_id: id do chat"""
        if not chat_id:
            raise AttributeError

        conn = sqlite3.connect(self.nomeDB)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT username, pontos FROM ranking WHERE chat_id=? AND pontos > 0 ORDER BY pontos DESC;
        """, (chat_id,))
        ranking = cursor.fetchall()
        cursor.close()
        conn.close()
        if ranking:
            return ranking
        else:
            return None

    def exists(self, username, chat_id):
        """Verifica se existe
        username: username do telegram
        chat_id: id do chat
        Retorna True ou False"""
        if not username or not chat_id:
            raise AttributeError
    
        conn = sqlite3.connect(self.nomeDB)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT username FROM ranking WHERE username LIKE ? AND chat_id=?
        """, (username, chat_id))
        response = cursor.fetchone()
        cursor.close()
        conn.close()
        if response:
            return username.lower() == response[0].lower()
        else:
            return False
