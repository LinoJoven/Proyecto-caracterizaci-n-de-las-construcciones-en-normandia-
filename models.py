# models.py
from db import db # Importamos el objeto 'db' de nuestro archivo db.py

# Definimos la clase Marcador que representa nuestra tabla en la base de datos
class Marcador(db.Model):
    # Le damos un nombre a la tabla
    __tablename__ = "marcadores"

    # Definimos las columnas (los campos de la tabla)
    id = db.Column(db.Integer, primary_key=True) # Llave primaria, se autoincrementa
    lat = db.Column(db.Float, nullable=False)    # Latitud, no puede estar vacía
    lng = db.Column(db.Float, nullable=False)    # Longitud, no puede estar vacía
    titulo = db.Column(db.String(100), nullable=False) # Título, no puede estar vacío
    descripcion = db.Column(db.String(250))      # Descripción, puede estar vacía

    # Este es el constructor. Se llama cuando creamos un nuevo marcador.
    def __init__(self, lat, lng, titulo, descripcion):
        self.lat = lat
        self.lng = lng
        self.titulo = titulo
        self.descripcion = descripcion