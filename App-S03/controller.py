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

from model import count_by
import config as cf
import model
import csv
import time
import tracemalloc
import datetime as dt

csv.field_size_limit(2147483647)

# Inicialización del Catálogo 

def newController():
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control

# Carga de datos

def loadData(control,filesize, memflag=True):

    start_time = getTime()
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    data=loadelements(control,filesize)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return delta_time, delta_memory

    else:
        return delta_time
    
def loadNetflix(catalog,size):
    """
    Carga la información de las películas y shows de Netflix.
    """
    netflixfile = cf.data_dir + 'Streaming/netflix_titles-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(netflixfile, encoding='utf-8'))
    for element in input_file:
        element["platform"] = "Netflix"
        if element["release_year"] != "":
            element["release_year"]=int(element["release_year"])
        if element["date_added"] != "":
            element["date_added"]=dt.datetime.strptime(element["date_added"], "%B %d, %Y")
        model.addElement(catalog["model"], element)
        model.addElement_Platform(catalog["model"],element,"Netflix")
    return catalog

def loadHulu(catalog,size):
    """
    Carga la información de las películas y shows de Hulu.
    """
    hulufile = cf.data_dir + 'Streaming/hulu_titles-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(hulufile, encoding='utf-8'))
    for element in input_file:
        element["platform"] = "Hulu"
        if element["release_year"] != "":
            element["release_year"]=int(element["release_year"])
        if element["date_added"] != "":
            element["date_added"]=dt.datetime.strptime(element["date_added"], "%B %d, %Y")
        model.addElement(catalog["model"], element)
        model.addElement_Platform(catalog["model"],element,"Hulu")
    return catalog

def loadamazonprime(catalog,size):
    """
    Carga la información de las películas y shows de Amazon Prime.    
    """
    amazonfile =  cf.data_dir + 'Streaming/amazon_prime_titles-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(amazonfile, encoding='utf-8'))
    for element in input_file:
        element["platform"] = "Amazon Prime"
        if element["release_year"] != "":
            element["release_year"]=int(element["release_year"])
        if element["date_added"] != "":
            element["date_added"]=dt.datetime.strptime(element["date_added"], "%B %d, %Y")
        model.addElement(catalog["model"], element)
        model.addElement_Platform(catalog["model"],element,"Amazon Prime")
    return catalog

def loaddisneyplus(catalog,size):
    """
    Carga la información de las películas y shows de Disney plus.
    """
    disneyfile =  cf.data_dir + 'Streaming/disney_plus_titles-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(disneyfile, encoding='utf-8'))
    for element in input_file:
        element["platform"] = "Disney Plus"
        if element["release_year"] != "":
            element["release_year"]=int(element["release_year"])
        if element["date_added"] != "":
            element["date_added"]=dt.datetime.strptime(element["date_added"], "%B %d, %Y")
        model.addElement(catalog["model"],element)
        model.addElement_Platform(catalog["model"],element,"Disney Plus")
    return catalog

def loadelements(catalog,size):
    loadamazonprime(catalog,size)
    loaddisneyplus(catalog,size)
    loadHulu(catalog,size)
    loadNetflix(catalog,size)
    return catalog

# Tiempo y memoria

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

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory = delta_memory/1024.0
    return delta_memory

# Requerimiento 1

def getContentByYear(catalog,Year):
    Year = model.findyear(catalog,Year)
    return Year

# Requerimiento 2

def getContentByDate(catalog,Date):
    Date = model.finddate(catalog,Date)
    return Date
    
# Requerimiento 7

def topngenres(catalog, n):
    top = model.topngenres(catalog["generos"],n)
    count = []
    for i in range(n):
        genre = {}
        Netflix = model.count_by(top[i]["elements"],"Netflix","platform")
        genre["Netflix"]=Netflix
        Hulu = model.count_by(top[i]["elements"],"Hulu","platform")
        genre["Hulu"] = Hulu
        Disney_plus = model.count_by(top[i]["elements"],"Disney Plus","platform")
        genre["Disney Plus"] = Disney_plus
        Amazon_prime = model.count_by(top[i]["elements"],"Amazon Prime","platform")
        genre["Amazon Prime"] = Amazon_prime
        Movies = model.count_by(top[i]["elements"],"Movie","type")
        genre["Movies"] = Movies
        TV_shows = model.count_by(top[i]["elements"],"TV Show","type")
        genre["TV Shows"] = TV_shows
        count.append(genre)
    return top, count


# Funciones de consulta sobre el catálogo


def getContentByActor(catalog, ActorName, criteria = 'cast'):
    """
    Requerimiento 3: Encontrar el contenido donde participa un actor.
    """
    Actor = model.find_by(catalog, ActorName, criteria)
    return Actor

def getContentByGenre(catalog, Genre, criteria="generos"):
    """
    Requerimiento 4: Encontrar el contenido de un género.
    """
    Genre = model.find_by(catalog, Genre, criteria)
    return Genre

def getContentByCountry(catalog, Country, criteria="country" ):
    """
    Requerimiento 5: Encontrar el contenido producido en un país.
    """
    Country = model.find_by(catalog, Country, criteria)
    return Country

def getContentByDirector(catalog, DirectorName, criteria="director"):
    """
    Requerimiento 6: Encontrar el contenido con un director involucrado.
    """
    Director = model.find_by(catalog, DirectorName, criteria)
    return Director
