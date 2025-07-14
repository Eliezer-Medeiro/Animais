#script para criar o banco
"""
import sqlite3

def criar_banco():
	conn = sqlite3.connect('animais.db')
	cursor = conn.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS animais(
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			nome TEXT NOT NULL,
			especie TEXT NOT NULL,
			raca TEXT,
			nascimento TEXT,
			descricao TEXT,
			foto TEXT
		)
	''')

	conn.commit()
	conn.close()


if __name__ == "__main__":
	criar_banco()


import sqlite3
conn = sqlite3.connect("animais.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM animais WHERE nome='lua'")
conn.commit()
cursor.execute("SELECT * FROM animais")
print(cursor.fetchall())
conn.close()


import sqlite3
conn = sqlite3.connect("animais.db")
cursor = conn.cursor()
cursor.execute("ALTER TABLE animais ADD COLUMN arquivado INTERGER default 0;")
conn.commit()
"""

import sqlite3

def criar_banco():
    conn = sqlite3.connect('animais.db')  # usa o mesmo banco do projeto
    cursor = conn.cursor()

    # Cria tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            apelido TEXT NOT NULL
        )
    ''')

    # Tenta adicionar o campo usuario_id à tabela animais
    try:
        cursor.execute("ALTER TABLE animais ADD COLUMN usuario_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Campo já existe

    conn.commit()
    conn.close()
    print("Banco atualizado com sucesso!")

if __name__ == "__main__":
    criar_banco()
