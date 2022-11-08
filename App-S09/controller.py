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

from heapq import merge
from App.model import cmpMoviesByTitle
import time
import tracemalloc
import config as cf
import model
import csv


csv.field_size_limit(2147483647)
from typing import Callable

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController():
    """
    Crea una instancia del modelo
    """
    control = {'model': None}
    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos
def loadData(control,memflag=True):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    loadAmazon(catalog)
    loadDisney(catalog)
    loadHulu(catalog)
    loadNetflix(catalog)
    sortShowsbyReleaseYear(catalog["Amazon"])
    sortShowsbyReleaseYear(catalog["Disney"])
    sortShowsbyReleaseYear(catalog["Hulu"])
    sortShowsbyReleaseYear(catalog["Netflix"])
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    ama = model.AmazonSize(catalog)
    dis = model.DisneySize(catalog)
    hulu = model.HuluSize(catalog)
    net = model.NetflixSize(catalog)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return ama, dis, hulu, net, delta_time, delta_memory
    else:
        return ama, dis, hulu, net, delta_time
    



def loadAmazon(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    Amazonfile = cf.data_dir + 'Challenge-RETO2/Streaming/amazon_prime_titles-utf8-large.csv'
    input_file = csv.DictReader(open(Amazonfile, encoding='utf-8'))
    for programaA in input_file:     
        model.addAmazon(catalog, programaA)
    sortShowsbyReleaseYear(catalog["Amazon"])
    return model.AmazonSize(catalog)

def loadDisney(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    Disneyfile = cf.data_dir + 'Challenge-RETO2/Streaming/disney_plus_titles-utf8-large.csv'
    input_file = csv.DictReader(open(Disneyfile, encoding='utf-8'))
    for programaD in input_file:
        model.addDisney(catalog, programaD)
    sortShowsbyReleaseYear(catalog["Disney"])
    return model.DisneySize(catalog)

def loadHulu(catalog):
    """
    Carga la información que asocia tags con libros.
    """
    Hulufile = cf.data_dir + 'Challenge-RETO2/Streaming/hulu_titles-utf8-large.csv'
    input_file = csv.DictReader(open(Hulufile, encoding='utf-8'))
    for programaH in input_file:
        model.addHulu(catalog, programaH)
    sortShowsbyReleaseYear(catalog["Hulu"])
    return model.HuluSize(catalog)

def loadNetflix(catalog) -> int:
    Netflixfile = cf.data_dir + 'Challenge-RETO2/Streaming/netflix_titles-utf8-large.csv'
    input_file = csv.DictReader(open(Netflixfile, encoding="utf-8"))
    for programaN in input_file:
        model.addNetflix(catalog, programaN)
    sortShowsbyReleaseYear(catalog["Netflix"])
    return model.NetflixSize(catalog)

def SizeTotal(control)->int:
    catalog=control["model"]
    return model.TotalSize(catalog)

#Funciones de consulta

#REQUERIMIENTO 1

def peliculasbyanio(control, anio, memflag):
    """
    Consulta las peliculas estrenadas en un anio.
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()

    Nopeliculas,listapeliculas=model.peliculasbyanio(control["model"],anio)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return Nopeliculas, listapeliculas,delta_time, delta_memory

    else: 
        return Nopeliculas, listapeliculas, delta_time

# REQUIRIMIENTO 2
def Show_by_time(catalog,date1, memflag):
    """
     Consulta los shows de television agregados  en un rango de fechas.
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()
    x = model.Show_by_time(catalog["model"],date1)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return x, delta_time, delta_memory
    else:
        return x, delta_time
# REQUERIMIENTO 3
def Shows_by_Actor(control, actor_name, memflag):
    """
    Filtra el contenido en el  que participa un actor especifico.
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()
    lista_actor, num_movies, num_programs= model.Shows_by_Actor(control["model"], actor_name)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return lista_actor, num_movies, num_programs, delta_time, delta_memory
    else: 
        return lista_actor, num_movies, num_programs, delta_time


# REQUERIMIENTO 4
def contentbyGenero(contenido, genero, memflag):
    """
    Filtra contenido por un genero en especifico.
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()

    genContent, Peliculas, Shows= model.ContentbyGenero(contenido["model"], genero)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return genContent,Peliculas, Shows, delta_time, delta_memory
    else:
        return genContent, Peliculas, Shows, delta_time
    

# REQUERIMIENTO 5

def MoviesByCountry(control,country,memflag):
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()

    country_list, movies, tv_show = model.MoviesByCountry(control["model"],country)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return country_list, movies, tv_show, delta_time, delta_memory
    else:
        return country_list, movies, tv_show, delta_time

    

# REQUERIMIENTO 6
def Shows_by_director(control, director_name, memflag):
    """
    Filtra conenido en el que participa un director en especifico.
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()

    titles_list,type_dict,service_dict,listed_in_dict = model.Shows_by_director(control["model"],director_name)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return titles_list,type_dict,service_dict,listed_in_dict,delta_time,delta_memory
    else:
        return titles_list,type_dict,service_dict,listed_in_dict, delta_time

    

# REQUIRIMIENTO 7
def TOP_genero(control,N,memflag):
    """
    Ordena contenido respecto a los generos que tengan mas apariciones en las plataformas.
    """
    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory= getMemory()
    x = model.TOP_genero(control["model"],N)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return x, delta_time,delta_memory
    else:
        return x, delta_time


    

#Funciones de ordenamiento
def sortShowsbyReleaseYear(lista):
    """
    Ordena los shows por release_year
    """
    return model.sortShowsbyReleaseyear(lista)

def sortShowsbyTitle(catalog): 
    return merge.sort(catalog,cmpMoviesByTitle)

#Funciones para saber el tamanio de los archivos
def GenerosSize(control):
    return model.GenerosSize(control["model"])

def ActoresSize(control):
    return model.ActoresSize(control["model"])

def YearSize(control):
    return model.YearSize(control["model"])

def DatesSize(control):
    return model.DatesSize(control["model"])

def CountrySize(control):
    return model.CountrySize(control["model"])


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

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

