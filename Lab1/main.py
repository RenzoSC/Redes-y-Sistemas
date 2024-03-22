from flask import Flask, jsonify, request
import random
from proximo_feriado import NextHoliday


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

NUM = len(peliculas)


def get_by_gender(gender):
    """Auxiliar function to get all movies by gender"""

    peliculas_genero = []
    for i in peliculas:
        if i['genero'] == gender:
            peliculas_genero.append(i)
    return peliculas_genero

def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles
    for i in peliculas:
        if i["id"] == id:
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
    for pelicula in peliculas:
        if pelicula['id'] == id:
            peliculas[id-1] = {"id":id,"titulo":request.json["titulo"], "genero":request.json["genero"]}
            return jsonify(pelicula)
    return jsonify({"error":"id de Película no encontrada"})


def eliminar_pelicula(id):
    for index,pelicula in enumerate(peliculas):
        if pelicula["id"] == id:
            del peliculas[index]
            return jsonify({'mensaje': 'Película eliminada correctamente'})
        
    return jsonify({"error":"Pelicula no existe"})

def obtener_por_genero (gender):
    peliculas_filtradas = get_by_gender(gender)
    return jsonify({"error":"genero no encontrado"}) if peliculas_filtradas==[] else jsonify(peliculas_filtradas) 

def obtener_filter (filter):
    peliculas_filter = []
    for pelicula in peliculas:
        if filter.lower() in pelicula['titulo'].lower():
            peliculas_filter.append(pelicula)
    return jsonify({"error":"genero no encontrado"}) if peliculas_filter==[] else jsonify(peliculas_filter) 


def sugerir_pelicula(gender=None):
    if gender == None:
        return jsonify(random.choice(peliculas))
    else:
        peliculas_filtradas = get_by_gender(gender)
        return jsonify({"error":"genero no encontrado"}) if peliculas_filtradas==[] else random.choice(peliculas_filtradas)
        
def obtener_nuevo_id():
    global NUM
    NUM+=1
    return NUM

def sugerir_pelicula_por_feriado(gender):
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    holiday = next_holiday.holiday
    peliculas_filtradas = get_by_gender(gender)
    return jsonify({"feriado": holiday, "pelicula":random.choice(peliculas_filtradas)})


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:gender>', 'obtener_por_genero', obtener_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/filter/<string:filter>', 'obtener_filter', obtener_filter, methods=['GET'])
app.add_url_rule('/peliculas/sugerir', 'sugerir_pelicula', sugerir_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<string:gender>', 'sugerir_pelicula', sugerir_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/sugerir-por-feriado/<string:gender>', 'sugerir_pelicula_por_feriado', sugerir_pelicula_por_feriado, methods=['GET'])

if __name__ == '__main__':
    app.run()
