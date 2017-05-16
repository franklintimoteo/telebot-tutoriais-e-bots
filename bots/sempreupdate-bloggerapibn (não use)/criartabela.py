import sqlite3
import config

# Arquivo para criar tabela

nomeDB = config.nomeDB
conn = sqlite3.connect(nomeDB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE publicacoes(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data_publicacao DATE NOT NULL,
    url TEXT NOT NULL,
    autor TEXT,
    etiquetas TEXT,
    titulo TEXT NOT NULL,
    publicado BIT NOT NULL,
    idPost BIGINT NOT NULL
);
""")
conn.commit()
cursor.close()
conn.close()