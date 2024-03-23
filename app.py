from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Función para establecer la conexión con la base de datos
def get_db_connection():
    conn = sqlite3.connect('iecadr.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para obtener todos los usuarios
# Función para establecer la conexión con la base de datos
def get_db_connection():
    conn = sqlite3.connect('iecadr.db')
    conn.row_factory = sqlite3.Row
    return conn

# Función para establecer la conexión con la base de datos
def get_db_connection():
    conn = sqlite3.connect('iecadr.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para autenticar usuarios
@app.route('/usuarios', methods=['POST'])
def autenticar_usuario():
    # Obtener datos de la solicitud
    datos_solicitud = request.json
    nombre = datos_solicitud.get('nombre')
    contraseña = datos_solicitud.get('contraseña')

    # Comprobar si el usuario y la contraseña coinciden con los de la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?", (nombre, contraseña))
    usuario_autenticado = cur.fetchone()
    conn.close()

    if usuario_autenticado:
        return jsonify({"mensaje": "Usuario autenticado correctamente"})
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401


# Ruta para obtener todas las sedes
@app.route('/sedes', methods=['GET'])
def obtener_sedes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sedes")
    sedes = cur.fetchall()
    conn.close()
    return jsonify([dict(sede) for sede in sedes])

# Ruta para obtener todos los proyectos
@app.route('/proyectos', methods=['GET'])
def obtener_proyectos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM proyectos")
    proyectos = cur.fetchall()
    conn.close()
    return jsonify([dict(proyecto) for proyecto in proyectos])

# Función para establecer la conexión con la base de datos
def get_db_connection():
    conn = sqlite3.connect('iecadr.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para agregar una nueva noticia
@app.route('/noticias', methods=['POST'])
def agregar_noticia():
    # Obtener datos de la solicitud
    datos_solicitud = request.form
    titulo = datos_solicitud.get('titulo')
    descripcion = datos_solicitud.get('descripcion')
    imagen = request.files['imagen']

    # Guardar la imagen en la carpeta IMG/noticias
    ruta_imagen = os.path.join('IMG/noticias', imagen.filename)
    imagen.save(ruta_imagen)

    # Guardar la URL de la imagen en la base de datos
    url_imagen = '/' + ruta_imagen.replace('\\', '/')  # Cambiar las barras invertidas por barras normales
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO noticias (titulo, descripcion, imagen) VALUES (?, ?, ?)", (titulo, descripcion, url_imagen))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Noticia agregada correctamente"})

# Ruta para obtener las últimas 5 noticias
@app.route('/noticias', methods=['GET'])
def obtener_ultimas_noticias():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM noticias ORDER BY id DESC LIMIT 5")
    noticias = cur.fetchall()
    conn.close()

    noticias_lista = []
    for noticia in noticias:
        noticia_dict = dict(noticia)
        noticia_dict['imagen'] = request.host_url + noticia_dict['imagen'].lstrip('/')
        noticias_lista.append(noticia_dict)

    return jsonify(noticias_lista)


# Ruta para obtener todos los docentes
@app.route('/docentes', methods=['GET'])
def obtener_docentes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM docentes")
    docentes = cur.fetchall()
    conn.close()
    return jsonify([dict(docente) for docente in docentes])

# Ruta para obtener el consejo
@app.route('/consejo', methods=['GET'])
def obtener_consejo():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM consejo")
    consejo = cur.fetchall()
    conn.close()
    return jsonify([dict(miembro) for miembro in consejo])

# Ruta para obtener la agenda
@app.route('/agenda', methods=['GET'])
def obtener_agenda():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM agenda")
    agenda = cur.fetchall()
    conn.close()
    return jsonify([dict(evento) for evento in agenda])

# Ruta para obtener información sobre la organización
@app.route('/about', methods=['GET'])
def obtener_about():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM about")
    about = cur.fetchone()
    conn.close()
    return jsonify(dict(about))

if __name__ == '__main__':
    app.run(debug=True)
