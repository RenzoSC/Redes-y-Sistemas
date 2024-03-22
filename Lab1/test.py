import requests
import random

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película de ID: ", id_pelicula, ", eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Obtener por genero
genero = "Drama"
response = requests.get(f'http://localhost:5000/peliculas/{genero}')
if response.status_code == 200:
    peliculas = response.json()
    print("Peliculas de género", genero,"obtenidas:")
    print(peliculas)
else:
    print("No se pudo obtener pelicula por género")
print()

# Obtener por filter
filter_tittle = "the"  # Filtro del titulo de la pelicula
response = requests.get(f'http://localhost:5000/peliculas/filter/{filter_tittle}')
if response.status_code == 200:
    peliculas = response.json()
    print("Peliculas filtradas por clave '",filter_tittle, "':")
    print(peliculas)
else:
    print("No se obtuvo peliculas con este filtro.")
print()

# Sugerir pelicula sin genero
response = requests.get(f'http://localhost:5000/peliculas/sugerir')
if response.status_code == 200:
    peli = response.json()["titulo"]
    print(f'Pelicula sugerida: {peli}')
else:
    print("Error: falló la sugerencia")
print()

# Sugerir pelicula con genero
genero = "Drama"
response = requests.get(f'http://localhost:5000/peliculas/sugerir/{genero}')
if response.status_code == 200:
    peli = response.json()["titulo"]
    print(f'Pelicula sugerida de genero {genero}: {peli}')
else:
    print("Error: falló la sugerencia")
print()

# Sugerir pelicula por feriado
genero = "Acción"
response = requests.get(f'http://localhost:5000/peliculas/sugerir-por-feriado/{genero}')
if response.status_code == 200:
    peli = response.json()["pelicula"]
    feriado =response.json()["feriado"]

    print(f'El proximo feriado es el {feriado["dia"]}/{feriado["mes"]} por motivo de {feriado["motivo"]} y recomiendo para ese dia la pelicula de {peli["genero"]}: {peli["titulo"]}')
else:
    print("Error: falló la sugerencia")
print()

#Faltaria el Test para fetch_holiday_by_type
