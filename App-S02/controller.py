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
import tracemalloc
import time
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController(type,FC):
    """
    Crea una instancia del modelo
    """
    control = {
        'model': model.newCatalog(type,FC)
    }
    tracemalloc.start()
    return control
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
def loadData(control,size):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    time1 = getTime()
    memory1 = getMemory()
    loadContentData(catalog,size,"amazon_prime")
    loadContentData(catalog,size,"disney_plus")
    loadContentData(catalog,size,"hulu")
    loadContentData(catalog,size,"netflix")
    time2 = getTime()
    memory2 = getMemory()
    return deltaTime(time2,time1),deltaMemory(memory2,memory1)
def loadContentData(catalog,size,platform):
    file = 'Streaming/'+platform+'_titles-utf8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        content["streaming_service"] = platform
        for key in content:
            if content[key] == "":
                content[key] = "unknown"
        model.add_content(catalog, content)
    return catalog
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def MoviesInYear(catalog,year): #Requerimiento 1
    return model.MoviesInYear(catalog["model"],year)
def ShowsInDate(catalog,date):  #Requerimiento 2
    return model.ShowsInDate(catalog["model"],date)
def ContentByActor(catalog,actor): #Requerimiento 3
    return model.ContentByActor(catalog["model"],actor)
def ContentByGenre(catalog,genre): #Requerimiento 4
    return model.contentByGenre(catalog['model'],genre)
def ContentByCountry(catalog,country): #Requerimiento 5
    return model.ContentbyCountry(catalog["model"],country)
def TitlesByDirector(catalog,director): #Requerimiento 6
    return model.TitlesByDirector(catalog["model"],director)
def TopNGenres(catalog,N): #Requerimiento 7
    return model.TopNGenres(catalog["model"],N)
def TopNActorByGenre(catalog, genre, N): #Requerimiento 8
    return model.TopNActorsByGenre(catalog["model"], genre, N)