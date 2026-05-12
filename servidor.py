from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("tareas.db")

app = Flask(__name__)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena_hash TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                completada INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
            """
        )
        conn.commit()


@app.route("/")
def index():
    return "Sistema de Gestión de Tareas con API Flask y SQLite"


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    contrasena = datos.get("contraseña", "")

    if not usuario or not contrasena:
        return jsonify({"estado": "error", "mensaje": "Debe enviar usuario y contraseña."}), 400

    contrasena_hash = generate_password_hash(contrasena, method="pbkdf2:sha256")

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
                (usuario, contrasena_hash),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"estado": "error", "mensaje": "El usuario ya existe."}), 409

    return jsonify({"estado": "success", "mensaje": "Usuario registrado correctamente."}), 201


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    contrasena = datos.get("contraseña", "")

    if not usuario or not contrasena:
        return jsonify({"estado": "error", "mensaje": "Debe enviar usuario y contraseña."}), 400

    with get_connection() as conn:
        fila = conn.execute(
            "SELECT id, usuario, contrasena_hash FROM usuarios WHERE usuario = ?",
            (usuario,),
        ).fetchone()

    if fila is None or not check_password_hash(fila["contrasena_hash"], contrasena):
        return jsonify({"estado": "error", "mensaje": "Credenciales inválidas."}), 401

    return jsonify({
        "estado": "success",
        "mensaje": "Inicio de sesión correcto.",
        "usuario_id": fila["id"],
        "usuario": fila["usuario"],
    })


@app.route("/tareas", methods=["GET"])
def tareas_bienvenida():
    return """
    <html>
        <head><title>Sistema de Tareas</title></head>
        <body>
            <h1>Bienvenido al Sistema de Gestión de Tareas</h1>
            <p>API Flask funcionando correctamente.</p>
            <p>Endpoints disponibles: POST /registro, POST /login y GET /tareas.</p>
        </body>
    </html>
    """


# Endpoints de tareas para que el cliente de consola 
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    datos = request.get_json(silent=True) or {}
    usuario_id = datos.get("usuario_id")
    titulo = datos.get("titulo", "").strip()

    if not usuario_id or not titulo:
        return jsonify({"estado": "error", "mensaje": "Debe enviar usuario_id y titulo."}), 400

    with get_connection() as conn:
        usuario = conn.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
        if usuario is None:
            return jsonify({"estado": "error", "mensaje": "Usuario inexistente."}), 404
        cursor = conn.execute(
            "INSERT INTO tareas (usuario_id, titulo) VALUES (?, ?)",
            (usuario_id, titulo),
        )
        conn.commit()

    return jsonify({"estado": "success", "mensaje": "Tarea creada.", "tarea_id": cursor.lastrowid}), 201


@app.route("/tareas/<int:usuario_id>", methods=["GET"])
def listar_tareas(usuario_id):
    with get_connection() as conn:
        filas = conn.execute(
            "SELECT id, titulo, completada FROM tareas WHERE usuario_id = ? ORDER BY id",
            (usuario_id,),
        ).fetchall()

    tareas = [dict(fila) for fila in filas]
    return jsonify({"estado": "success", "tareas": tareas})


@app.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"estado": "error", "mensaje": "Tarea inexistente."}), 404

    return jsonify({"estado": "success", "mensaje": "Tarea eliminada."})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
