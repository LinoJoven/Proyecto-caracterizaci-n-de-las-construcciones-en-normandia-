# programa.py

# ---- 1. IMPORTACIONES ----
# Importamos las herramientas de Flask
from flask import Flask, render_template, request, jsonify
# Importamos el objeto 'db' que creamos en db.py
from db import db
# Importamos el modelo 'Marcador' que creamos en models.py
from models import Marcador

# ---- 2. CONFIGURACIÓN INICIAL ----
app = Flask(__name__)

# Le decimos a Flask dónde está nuestra base de datos
# 'sqlite:///marcadores.sqlite3' significa: usa SQLite y guarda la base de datos
# en un archivo llamado 'marcadores.sqlite3'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marcadores.sqlite3"

# Conectamos nuestra app con el objeto de la base de datos
db.init_app(app)


# ---- 3. DEFINICIÓN DE RUTAS (ENDPOINTS) ----

# Ruta principal ('/'): Sirve la página web con el mapa.
@app.route("/")
def index():
    # Busca el archivo 'index.html' en la carpeta 'templates' y lo muestra
    return render_template("index.html")

# Ruta API para obtener todos los marcadores ('/api/marcadores')
# Responde a peticiones GET
@app.route("/api/marcadores", methods=["GET"])
def get_marcadores():
    # 1. Pide a la base de datos TODOS los marcadores guardados
    marcadores = Marcador.query.all()
    # 2. Convierte la lista de objetos 'Marcador' a una lista de diccionarios
    lista_marcadores = [
        {"lat": m.lat, "lng": m.lng, "titulo": m.titulo, "descripcion": m.descripcion}
        for m in marcadores
    ]
    # 3. Devuelve esa lista en formato JSON, que JavaScript entiende muy bien
    return jsonify(lista_marcadores)

# Ruta API para guardar un nuevo marcador ('/api/marcadores')
# Responde a peticiones POST
@app.route("/api/marcadores", methods=["POST"])
def add_marcador():
    # 1. Obtiene los datos (lat, lng, titulo, etc.) que JavaScript envió en formato JSON
    data = request.get_json()

    # 2. Crea un nuevo objeto 'Marcador' usando el modelo que definimos en models.py
    nuevo_marcador = Marcador(
        lat=data['lat'],
        lng=data['lng'],
        titulo=data['titulo'],
        descripcion=data['descripcion']
    )

    # 3. Lo añade a la sesión de la base de datos y lo guarda permanentemente
    db.session.add(nuevo_marcador)
    db.session.commit()

    # 4. Responde a JavaScript con un mensaje de éxito
    return jsonify({"mensaje": "Marcador guardado con éxito"}), 201


# ---- 4. EJECUCIÓN DE LA APLICACIÓN ----
if __name__ == "__main__":
    # Esto se asegura de que la tabla 'marcadores' se cree en la base de datos
    # la primera vez que ejecutas el programa (si no existe ya)
    with app.app_context():
        db.create_all()

    # Pone en marcha el servidor web
    app.run(debug=True)
    