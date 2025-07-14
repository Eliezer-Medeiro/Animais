from app import app
from flask import render_template, url_for, request, redirect, session, flash
import sqlite3
import os

# Caminho do banco de dados
CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), '..', 'animais.db')


# Página inicial
@app.route("/", methods=["GET", "POST"])
def homepage():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais WHERE arquivado = 0")
    animais = cursor.fetchall()

    cursor.execute("SELECT DISTINCT nome FROM animais WHERE arquivado = 0")
    nomes = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template("home.html", animais=animais, nomes=nomes)


# Filtro por nome
@app.route("/filtro/<nome>")
def filtro_por_nome(nome):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais WHERE nome = ? AND arquivado = 0", (nome,))
    animais = cursor.fetchall()

    cursor.execute("SELECT DISTINCT nome FROM animais WHERE arquivado = 0")
    nomes = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template("home.html", animais=animais, nomes=nomes)


# Registrar novo usuário
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        apelido = request.form["apelido"]

        conn = sqlite3.connect(CAMINHO_BANCO)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, apelido) VALUES (?, ?, ?, ?)",
                (nome, email, senha, apelido)
            )
            conn.commit()
            flash("Usuário registrado com sucesso!")
        except:
            flash("Erro: e-mail já existe.")
        finally:
            conn.close()
        return redirect("/login")

    return render_template("registrar.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = sqlite3.connect(CAMINHO_BANCO)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session["usuario_id"] = usuario[0]
            session["usuario_nome"] = usuario[1]

            conn = sqlite3.connect(CAMINHO_BANCO)
            cursor = conn.cursor()
            cursor.execute("SELECT apelido FROM usuarios WHERE id = ?", (usuario[0],))
            apelido = cursor.fetchone()[0]
            conn.close()

            return redirect(f"/perfil/{apelido}")

        else:
            flash("Login inválido.")

    return render_template("login.html")



# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Adicionar novo animal
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if "usuario_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        nome = request.form["nome"]
        especie = request.form["especie"]
        raca = request.form["raca"]
        nascimento = request.form["nascimento"]
        descricao = request.form["descricao"]
        foto = request.form["foto"]
        usuario_id = session["usuario_id"]

        conn = sqlite3.connect(CAMINHO_BANCO)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO animais (nome, especie, raca, nascimento, descricao, foto, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, especie, raca, nascimento, descricao, foto, usuario_id))
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("adicionar.html")


# Ver arquivados
@app.route("/arquivados")
def ver_arquivados():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais WHERE arquivado = 1")
    animais = cursor.fetchall()
    conn.close()
    return render_template("arquivados.html", animais=animais)


# Arquivar animal (só dono)
@app.route("/arquivar/<int:id>")
def arquivar(id):
    if "usuario_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT usuario_id FROM animais WHERE id = ?", (id,))
    dono = cursor.fetchone()

    if dono and dono[0] == session["usuario_id"]:
        cursor.execute("UPDATE animais SET arquivado = 1 WHERE id = ?", (id,))
        conn.commit()

    conn.close()
    return redirect("/")


# Desarquivar animal (só dono)
@app.route("/desarquivar/<int:id>")
def desarquivar(id):
    if "usuario_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT usuario_id FROM animais WHERE id = ?", (id,))
    dono = cursor.fetchone()

    if dono and dono[0] == session["usuario_id"]:
        cursor.execute("UPDATE animais SET arquivado = 0 WHERE id = ?", (id,))
        conn.commit()

    conn.close()
    return redirect("/arquivados")


# Excluir animal (só dono)
@app.route("/excluir/<int:id>")
def excluir(id):
    if "usuario_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT usuario_id FROM animais WHERE id = ?", (id,))
    dono = cursor.fetchone()

    if dono and dono[0] == session["usuario_id"]:
        cursor.execute("DELETE FROM animais WHERE id = ?", (id,))
        conn.commit()

    conn.close()
    return redirect("/arquivados")


@app.route("/perfil/<apelido>")
def perfil(apelido):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    # Busca o usuário pelo apelido
    cursor.execute("SELECT id, nome FROM usuarios WHERE apelido = ?", (apelido,))
    usuario = cursor.fetchone()

    if not usuario:
        conn.close()
        return "Usuário não encontrado", 404

    usuario_id = usuario[0]
    nome = usuario[1]

    # Pega só os animais desse usuário que não estão arquivados
    cursor.execute("SELECT * FROM animais WHERE usuario_id = ? AND arquivado = 0", (usuario_id,))
    animais = cursor.fetchall()
    conn.close()

    return render_template("home.html", animais=animais, nomes=[], perfil_nome=apelido, perfil_apelido=apelido)

