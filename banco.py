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
	print("Banco criado com sucesso!")
"""
import sqlite3
conn = sqlite3.connect("animais.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM animais WHERE nome='lua'")
conn.commit()
cursor.execute("SELECT * FROM animais")
print(cursor.fetchall())
conn.close()
