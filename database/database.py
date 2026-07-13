import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "legado.db"
)


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            honors INTEGER DEFAULT 0,
            messages INTEGER DEFAULT 0,
            god TEXT DEFAULT NULL,
            welcomed INTEGER DEFAULT 0
        )
    """)

    try:
        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN welcomed INTEGER DEFAULT 0
        """)
    except:
        pass

    conn.commit()
    conn.close()


# ==========================
# USUÁRIOS
# ==========================

def criar_usuario(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id)
        VALUES (?)
    """, (user_id,))

    conn.commit()
    conn.close()


def obter_usuario(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    usuario = cursor.fetchone()

    conn.close()

    return usuario


# ==========================
# XP
# ==========================

def adicionar_xp(user_id, xp):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET xp = xp + ?
        WHERE user_id = ?
    """, (xp, user_id))

    conn.commit()
    conn.close()


def atualizar_level(user_id, level):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET level = ?
        WHERE user_id = ?
    """, (level, user_id))

    conn.commit()
    conn.close()


# ==========================
# HONRAS
# ==========================

def adicionar_honra(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET honors = honors + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================
# MENSAGENS
# ==========================

def adicionar_mensagem(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET messages = messages + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================
# DEUS
# ==========================

def definir_deus(user_id, deus):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET god = ?
        WHERE user_id = ?
    """, (deus, user_id))

    conn.commit()
    conn.close()


def obter_deus(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT god
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado["god"]

    return None


def resetar_deus(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET god = NULL
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================
# BOAS-VINDAS
# ==========================

def recebeu_boas_vindas(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT welcomed
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado["welcomed"]

    return 0


def marcar_boas_vindas(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET welcomed = 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================
# RANKING
# ==========================

def top_usuarios(limit=10):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        ORDER BY level DESC, xp DESC
        LIMIT ?
    """, (limit,))

    ranking = cursor.fetchall()

    conn.close()

    return ranking


def posicao_ranking(user_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM users
        ORDER BY level DESC, xp DESC
    """)

    ranking = cursor.fetchall()

    conn.close()

    for posicao, usuario in enumerate(
        ranking,
        start=1
    ):
        if usuario["user_id"] == user_id:
            return posicao

    return "N/A"