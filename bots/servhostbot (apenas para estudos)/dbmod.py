import sqlite3

db_name = 'cadastros.db'

class BancoDados:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def __enter__(self):
        self.conn = sqlite3.connect(db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_value:
            raise


def existe(id_user):
    try:
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id_user FROM usuarios WHERE id_user=?
            """, (id_user,))
            resposta = cursor.fetchone()
            cursor.close()
            if resposta:
                return id_user in resposta
                
    except Exception as erro:
        print("Erro ao verificar existência de id_user no banco de dados")
        raise erro


def cadastrar(id_user, senha, vencimento):
    try:
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO usuarios(id_user, senha, vencimento)
            VALUES(?,?,?)
            """,(id_user, senha, vencimento))
            conn.commit()
            cursor.close()
    except Exception:
        return False
    return True


def renovar(id_user, vencimento):
    try:
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE usuarios
            SET vencimento=?
            WHERE id_user=?""",(vencimento, id_user))
            conn.commit()
            cursor.close()
    except Exception:
        return False
    return True


def senha(id_user):
    try:
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT senha FROM usuarios WHERE id_user=?
            """, (id_user,))
            senha = cursor.fetchone()            
            cursor.close()
            if senha:
                return senha[0]
    except Exception as erro:
        print("Erro ao buscar senha no banco de dados.")
        raise erro


def venceu(id_user, plano):
    """plano deve ser dado em segundos"""
    try:
        with BancoDados(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT vencimento FROM usuarios
            WHERE id_user=? AND vencimento <=?
            """, (id_user, plano))
            resposta = cursor.fetchone()
            cursor.close()
            if resposta:
                return True
    except Exception as erro:
        print("Erro ao buscar vencimento no banco de dados.")
        raise erro

def expirados(plano):
    pass

#1483297616.0153427 expira a dois dias
#1483122001.6389558 hoje