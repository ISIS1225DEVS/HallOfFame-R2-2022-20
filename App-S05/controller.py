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
import time
import tracemalloc
import config as cf
import model
import csv

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def newController():
    """
    Crea una instancia del modelo
    """
    control = {'model':None}
    control['model'] = model.newCatalog()

    return control

# Funciones para la carga de datos

def loadData(control, file_size='large', memflag=True):
    """
    carga los datos de los archivos y cargar los datos de la 
    estructura de datos
    """

    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    catalog = control['model']
    loadAmazon(catalog, file_size)
    loadDisney(catalog, file_size)
    loadHulu(catalog, file_size)
    loadNetflix(catalog, file_size)


    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return delta_time

def loadAmazon(catalog, file_size):
    """
    Carga los datos de los archivos y cargar los datos de la 
    estructura de datos
    """
    amazonfile = cf.data_dir + f'Streaming/amazon_prime_titles-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(amazonfile, encoding='utf-8'))
    for video in input_file:

        video['release_year'] = int(video['release_year'])
        video['service'] = 'Amazon Prime'

        model.addGenero(catalog, video)
        model.addGeneralVideoByService(catalog, video)
        model.addPais(catalog, video)
        model.addAno(catalog, video)
        model.addActor(catalog, video)
        model.addDirector(catalog,video)
        model.addFecha(catalog, video)

def loadDisney(catalog, file_size):
    """
    Carga los datos de los archivos y cargar los datos de la 
    estructura de datos
    """
    disneyfile = cf.data_dir + f'Streaming/disney_plus_titles-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(disneyfile, encoding='utf-8'))
    for video in input_file:
        video['release_year'] = int(video['release_year'])
        video['service'] = 'Disney Plus'

        model.addGenero(catalog, video)
        model.addGeneralVideoByService(catalog, video)
        model.addPais(catalog, video)
        model.addAno(catalog, video)
        model.addActor(catalog, video)
        model.addDirector(catalog,video)
        model.addFecha(catalog, video)

def loadHulu(catalog, file_size):
    """
    Carga los datos de los archivos y cargar los datos de la 
    estructura de datos
    """
    hulufile = cf.data_dir + f'Streaming/hulu_titles-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(hulufile, encoding='utf-8'))
    for video in input_file:
        video['release_year'] = int(video['release_year'])
        video['service'] = 'Hulu'

        model.addGenero(catalog, video)
        model.addGeneralVideoByService(catalog, video)
        model.addPais(catalog, video)
        model.addAno(catalog, video)
        model.addActor(catalog, video)
        model.addDirector(catalog,video)
        model.addFecha(catalog, video)

def loadNetflix(catalog, file_size):
    """
    Carga los datos de los archivos y cargar los datos de la 
    estructura de datos
    """
    netflixfile = cf.data_dir + f'Streaming/netflix_titles-utf8-{file_size}.csv'
    input_file = csv.DictReader(open(netflixfile, encoding='utf-8'))
    for video in input_file:
        video['release_year'] = int(video['release_year'])
        video['service'] = 'Netflix'

        model.addGenero(catalog, video)
        model.addGeneralVideoByService(catalog, video)
        model.addPais(catalog, video)
        model.addAno(catalog, video)
        model.addActor(catalog, video)
        model.addFecha(catalog, video)
        model.addDirector(catalog,video)
    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def topGeneros(control, num_top, memflag=True):
    """
    Encuentra los top N contenidos de un genero.

    parametros:
    control: catalogo de contenidos
    num_top: numero de elementos a retornar

    Retorna:
    Lista con los top N contenidos de un genero
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    #----------------------------------------------------------
    top_generos = model.topGeneros(control['model'], num_top)
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory, top_generos

    else:
        # respuesta sin medir memoria
        return delta_time, top_generos


def buscarPais(control, pais, memflag=True):
    """
    Encuentra los contenidos de un pais.

    parametros:
    control: catalogo de contenidos
    pais: pais

    Retorna:
    Lista con los contenidos listados en ese pais.
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    #----------------------------------------------------------
    contenido_pais = model.buscarPais(control['model'], pais)
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory, contenido_pais

    else:
        # respuesta sin medir memoria
        return delta_time, contenido_pais


def buscarGenero(control, genero):
    """
    Encuentra los contenidos de un genero.

    parametros:
    control: catalogo de contenidos
    genero: genero a buscar

    Retorna:
    Lista con los contenidos de un genero
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    tracemalloc.start()
    start_memory = getMemory()

    #----------------------------------------------------------
    generos = model.buscarGenero(control['model'], genero)
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    stop_memory = getMemory()
    tracemalloc.stop()
    # calcula la diferencia de memoria
    delta_memory = deltaMemory(stop_memory, start_memory)
    # respuesta con los datos de tiempo y memoria
    return delta_time, delta_memory, generos

def buscarAno(control, ano, type, memflag=True):
    """
    Encuentra los contenidos producidos en un año.

    parametros:
    control: catalogo de contenidos
    ano: año

    Retorna:
    Lista con los contenidos estrenados en ese año.
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    #----------------------------------------------------------
    contenido_pelis, conteo = model.buscarAno(control['model'], ano)
    contenido_typeano = model.getType(contenido_pelis, type)
    contenido_typeano = contenido_typeano, conteo
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory, contenido_typeano

    else:
        # respuesta sin medir memoria
        return delta_time, contenido_typeano


def buscarFecha(control, fecha, type, memflag=True):
    """
    Encuentra los contenidos de un pais.

    parametros:
    control: catalogo de contenidos
    pais: pais

    Retorna:
    Lista con los contenidos listados en ese pais.
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    #----------------------------------------------------------
    contenido_series, conteo = model.buscarFecha(control['model'], fecha)
    contenido_typeseries = model.getType(contenido_series, type)
    contenido_typeseries = contenido_typeseries, conteo
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory, contenido_typeseries

    else:
        # respuesta sin medir memoria
        return delta_time, contenido_typeseries


def generalServiceFirstLast(control):
    """
    """
    return model.generalServiceFirstLast(control['model'])

def buscarActor(control, actor):
    """
    Encuentra los contenidos de un actor espesifico.

    parametros:
    control: catalogo de contenidos
    actor: actor a buscar

    Retorna:
    Lista con los contenidos de un actor
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    tracemalloc.start()
    start_memory = getMemory()

    #----------------------------------------------------------
    dataActor = model.buscarActor(control['model'], actor)
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    stop_memory = getMemory()
    tracemalloc.stop()
    # calcula la diferencia de memoria
    delta_memory = deltaMemory(stop_memory, start_memory)
    # respuesta con los datos de tiempo y memoria
    return delta_time, delta_memory, dataActor

def buscarDirector(control, director):
    """
    Encuentra los contenidos de un director espesifico.

    parametros:
    control: catalogo de contenidos
    director: director a buscar

    Retorna:
    Lista con los contenidos de un director
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    tracemalloc.start()
    start_memory = getMemory()

    #----------------------------------------------------------
    dataDirector = model.buscarDirector(control['model'], director)
    #----------------------------------------------------------

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    stop_memory = getMemory()
    tracemalloc.stop()
    # calcula la diferencia de memoria
    delta_memory = deltaMemory(stop_memory, start_memory)
    # respuesta con los datos de tiempo y memoria
    return delta_time, delta_memory, dataDirector

# Funciones para medir tiempos de ejecución

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
