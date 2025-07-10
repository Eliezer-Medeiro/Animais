from app import app
from flask import render_template, url_for, request, redirect
import sqlite3
import os

#camunho do bd, se o arquivo estiver fora da pasta app/
CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), '..', 'animais.db')


# pagina inicial, onde só tem um botao para ir para o /adicionar
@app.route("/", methods=["GET", "POST"])
def homepage():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais")
    animais = cursor.fetchall()
    conn.close()
    return render_template("home.html", animais=animais)

# pagina para add animal
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
	if request.method == "POST":
		nome = request.form["nome"]
		especie = request.form["especie"]
		raca = request.form["raca"]
		nascimento = request.form["nascimento"]
		descricao = request.form["descricao"]
		foto = request.form["foto"]

		
		#conexao com o bd
		conn = sqlite3.connect(CAMINHO_BANCO)
		cursor = conn.cursor()


		# Inserção dos dados
		cursor.execute('''
			INSERT INTO animais (nome, especie, raca, nascimento, descricao, foto)
			VALUES (?, ?, ?, ?, ?, ?)
			''', (nome, especie, raca, nascimento, descricao, foto))

		conn.commit()
		conn.close()

		return redirect("/")

	return render_template("adicionar.html")