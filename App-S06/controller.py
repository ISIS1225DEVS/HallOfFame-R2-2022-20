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

from msilib.schema import Control
import time
import tracemalloc
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from datetime import datetime
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def newController():
    control = {
        'model': None,
    }
    control['model'] = model.newCatalog()
    return control

# Funciones para la carga de datos

def loadData(control, porcentaje_data, memflag = False):
    catalog = control['model']
    platforms = ['amazon_prime', 'disney_plus', 'hulu', 'netflix']
    total = {}
    elements = {}

    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    for platform in platforms:
        total[platform] = loadPlatform(catalog, porcentaje_data, platform)
        elements[platform] = lt.newList('ARRAY_LIST')
        for title in lt.iterator(catalog['total']):
            if title['platform'] == platform:
                lt.addLast(elements[platform], title)
    
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return total, elements, delta_time, delta_memory
    else:
        return total, elements, delta_time


def loadPlatform(catalog, porcentaje_data, platform):
    file = cf.data_dir + platform + "_titles-utf8-" + porcentaje_data + ".csv"
    input_file = csv.DictReader(open(file, encoding="utf-8"))
    count = 0
    for title in input_file:
        model.addTitle(catalog, title, platform)
        count += 1
    return count
    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getSix(list):
    return model.getSix(list)

def countplatforms(total):
    return model.countplatforms(total)

#======================
# REQUERIMIENTO 1
#======================

def getMoviesByYear(control, year, memflag = True):
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    titles = model.getMoviesByYear(control['model'], year)

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
        return titles, delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return titles, delta_time

#======================
# REQUERIMIENTO 3
#======================    
def getTitlesByActor(control, actor, memflag = True):
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    titles= model.getTitlesByActor(control["model"], actor)

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
        return titles, delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return titles, delta_time

#======================
# REQUERIMIENTO 4
#======================

def getTitlesByGenero(control, genero, memflag = True):
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    titles = model.getTitlesByGenero(control['model'], genero)

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
        return titles, delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return titles, delta_time

#======================
# REQUERIMIENTO 6
#======================

def getTitlesByDirector(control, director, memflag = True): 
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    titles, sorted_titles, mapa, mapa2 = model.getTitlesByDirector(control['model'], director)

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
        return [titles, sorted_titles, mapa, mapa2], delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return [titles, sorted_titles, mapa, mapa2], delta_time

#=======================
# REQUERIMIENTO 7
#======================

def getTopGeneros(control, rank, memflag=True):
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    top = model.getTopGenero(control['model'], rank)

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
        return top, delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return top, delta_time
    
#=======================
# REQUERIMIENTO 8
#======================

def getTopActor(control, genero, rank, memflag = True):
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    info_genero = model.getTitlesByGenero(control['model'], genero)
    info_actors = model.getActorGenero(info_genero[0])
    top = model.getTopActor(info_actors, rank)

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
        return [top, info_actors], delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return [top, info_actors], delta_time

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