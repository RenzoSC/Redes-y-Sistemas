from flask import Flask, jsonify, request
import random
import json
app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles
    for i in peliculas:
        if i['id'] == id:
            return jsonify(peliculas[id-1])
    return jsonify({"error":"id de pelicula no encontrada"})


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    # Lógica para buscar la película por su ID y actualizar sus detalles
    for i in peliculas:
        if i['id'] == id:
            peliculas[id-1] = {"id":id,"titulo":request.json["titulo"], "genero":request.json["genero"]}
            return jsonify(peliculas[id-1])
    return jsonify({"error":"id de pelicula no encontrada"})


def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla
    for i in peliculas:
        if i["id"]==id:
            del peliculas[id-1]
            return jsonify({'mensaje': 'Película eliminada correctamente'})
    return jsonify({"error":"pelicula no existe"})

def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1

def obtener_por_genero(gender):
    peliculas_genero = []
    for i in peliculas:
        if i["genero"]== gender:
            peliculas_genero.append(i)
    return  jsonify({"error":"genero no encontrado"}) if peliculas_genero==[] else jsonify(peliculas_genero)

def obtener_filter (filter):
    peliculas_filter = []
    for i in peliculas:
        if filter.lower() in i['titulo'].lower():
            peliculas_filter.append(i)
    return jsonify({"error":"genero no encontrado"}) if peliculas_filter==[] else jsonify(peliculas_filter)

def sugerir_pelicula(gender=None):
    if gender == None:
        return jsonify(random.choice(peliculas))
    else:
        peliculas_gender=[]
        for i in peliculas:
            if i["genero"]==gender:
                peliculas_gender.append(i)
        return jsonify({"error":"genero no encontrado"}) if peliculas_gender==[] else jsonify(random.choice(peliculas_gender))
        
app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:gender>', 'obtener_por_genero', obtener_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/filter/<string:filter>', 'obtener_filter', obtener_filter, methods=['GET'])
app.add_url_rule('/peliculas/sugerir', 'sugerir_pelicula', sugerir_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<string:gender>', 'sugerir_pelicula', sugerir_pelicula, methods=['GET'])

if __name__ == '__main__':
    app.run()
