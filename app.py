from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "tareas.db"

# --- Crear base de datos si no existe ---
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE tareas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        descripcion TEXT,
                        estado TEXT DEFAULT 'Pendiente'
                    )''')
        conn.commit()
        conn.close()

# --- Página principal: lista de tareas ---
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tareas")
    tareas = c.fetchall()
    conn.close()
    return render_template_string('''
        <html>
        <head>
            <title>Gestor de Tareas Flask</title>
            <style>
                body { font-family: Arial; background: #f9f9f9; padding: 20px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
                th { background: #ffb74d; }
                h1 { color: #ff6f00; }
                form { margin-top: 20px; }
                input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
                button { background: #ff9800; color: white; border: none; padding: 10px 15px; cursor: pointer; border-radius: 5px; }
                button:hover { background: #fb8c00; }
            </style>
        </head>
        <body>
            <h1>📋 Gestor de Tareas Flask</h1>
            <form method="POST" action="/agregar">
                <input type="text" name="titulo" placeholder="Título de la tarea" required>
                <textarea name="descripcion" placeholder="Descripción"></textarea>
                <button type="submit">Agregar tarea</button>
            </form>
            <table>
                <tr><th>ID</th><th>Título</th><th>Descripción</th><th>Estado</th><th>Acciones</th></tr>
                {% for t in tareas %}
                <tr>
                    <td>{{t[0]}}</td>
                    <td>{{t[1]}}</td>
                    <td>{{t[2]}}</td>
                    <td>{{t[3]}}</td>
                    <td>
                        <a href="/completar/{{t[0]}}">✅</a> |
                        <a href="/eliminar/{{t[0]}}">🗑️</a>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
    ''', tareas=tareas)

# --- Agregar tarea ---
@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)", (titulo, descripcion))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Completar tarea ---
@app.route('/completar/<int:id>')
def completar(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tareas SET estado='Completada' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- Eliminar tarea ---
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tareas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
