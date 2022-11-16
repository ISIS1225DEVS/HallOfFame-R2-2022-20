"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from datetime import datetime
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de contenido digital
def newController():
    """
    Crea una instancia del modelo
    """
    control = model.newCatalog('ARRAY_LIST')
    return control

# Inicialización del Catálogo de libros
# Funciones para la carga de datos
def loadData(catalog, memflag=True):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    loadPlatform(catalog, 'netflix')
    loadPlatform(catalog, 'amazon')
    loadPlatform(catalog, 'disney')
    loadPlatform(catalog, 'hulu')
    model.sortTitles(catalog, model.compareLoadData)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        times = delta_time, delta_memory
    else:
        # respuesta sin medir memoria
        times = delta_time
    return catalog['generalInformation'], times

def loadPlatform(catalog, platform):
    if platform == 'amazon':
        platformT = platform + '_prime'
    elif platform == 'disney':
        platformT = platform + '_plus'
    else:
        platformT = platform
    contentFile = cf.data_dir + 'Streaming/' + str(platformT) + '_titles-utf8-large.csv'
    input_file = csv.DictReader(open(contentFile, encoding='utf-8'))
    for title in input_file:
        title['streame_service'] = platform
        model.addTitle(catalog, title, platform)

# Funciones de ordenamiento
def firstAndLastThreeTitles(lista):
    return model.firstAndLastThreeTitles(lista)

def sortDataAmounts(lista):
    model.sortDataAmounts(lista)

# Funciones de consulta sobre el catálogo
def getMoviesByYear(catalog, year):
    return model.getMoviesByYear(catalog, year)

def getTVShowsByDate(catalog, date):
    date = datetime.strptime(date, '%B %d, %Y')
    year = date.year
    return model.getTVShowsByDate(catalog, year, date)

def getTitlesByActor(catalog, actor): 
    actor = actor.title()
    return model.getTitlesByActor(catalog, actor)

def getTitlesByGenre(catalog, genre):
    genre = genre.title()
    return model.getTitlesByGenre(catalog, genre)

def getTitlesByCountry(catalog, country):
    country = country.title()
    return model.getTitlesByCountry(catalog, country)

def getTitlesByDirector(catalog, director):
    director = director.title()
    return model.getTitlesByDirector(catalog, director)

def getTopNByGenre(catalog, N):
    return model.getTopNByGenre(catalog, N)

def getTopNByActorInGenre(catalog, N, genre):
    genre = genre.title()
    return model.getTopNByActorInGenre(catalog, N, genre)

# Funciones para medir tiempos de ejecucion
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Funciones para medir la memoria utilizada
def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory