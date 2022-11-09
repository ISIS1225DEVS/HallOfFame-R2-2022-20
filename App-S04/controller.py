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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def newController(estructura, can_netflix, can_amazon, can_disney, can_hulu):
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog(estructura, can_netflix, can_amazon, can_disney, can_hulu)
    
    return control

# Funciones para la carga de datos

def loadData(control, tamanio):

    control = control['model']

    loadNetflix(control, tamanio)
    loadAmazon(control, tamanio)
    loadDisney(control, tamanio)
    loadHulu(control, tamanio)



def loadNetflix(control, tamanio):

    netflixfile = cf.data_dir + "Streaming/netflix_titles-utf8-" + tamanio + ".csv"
    input_file = csv.DictReader(open(netflixfile, encoding='utf-8'))
    for program in input_file:
        program["stream_service"] = "netflix"
        model.addNetflix(control, program)
        loadProgram(control, program)


def loadAmazon(control, tamanio):
    
    amazonfile = cf.data_dir + "Streaming/amazon_prime_titles-utf8-" + tamanio + ".csv"
    input_file = csv.DictReader(open(amazonfile, encoding='utf-8'))
    for program in input_file:
        program["stream_service"] = "amazon"
        model.addAmazon(control, program)
        loadProgram(control, program)


def loadDisney(control, tamanio):
    
    disneyfile = cf.data_dir + "Streaming/disney_plus_titles-utf8-" + tamanio + ".csv"
    input_file = csv.DictReader(open(disneyfile, encoding='utf-8'))
    for program in input_file:
        program["stream_service"] = "disney"
        model.addDisney(control, program)
        loadProgram(control, program)


def loadHulu(control, tamanio):
    
    hulufile = cf.data_dir + "Streaming/hulu_titles-utf8-" + tamanio + ".csv"
    input_file = csv.DictReader(open(hulufile, encoding='utf-8'))
    for program in input_file:
        program["stream_service"] = "hulu"
        model.addHulu(control, program)
        loadProgram(control, program)

def loadProgram(control, program):

    model.addProgram(control, program)
    model.addGeneros(control, program)
    model.addPaises(control, program)
    model.addDirectores(control, program)
    model.addActores(control, program)
    model.addAnios(control,program)
    model.addDadeAdded(control, program)

def carga_datos(control):
    
    carga = model.cargar_datos(control["model"])

    return carga

# Funciones de ordenamiento


# Funciones de consulta sobre el catálogo
def req_1 (catalog, anio):

    return model.req_1(catalog["model"], anio)

def req_2 (catalog, anio):

    return model.req_2(catalog["model"], anio )

def req_3(catalog, Actor):

    return model.req_3(catalog["model"],Actor)

def req_4(catalog, genero):

    return model.req_4(catalog["model"], genero)

def req_5(catalog, pais):

    return model.req_5(catalog["model"], pais)

def req_6(catalog, director):

    return model.req_6(catalog["model"], director)

def req_7(catalog, rank):

    return model.req_7(catalog["model"], rank)

def req_8(catalog, genero, rank):

    return model.req_8(catalog["model"], genero, rank)

def netflixSize(control):

    return model.netflixSize(control)

def amazonSize(control):

    return model.amazonSize(control)


def disneySize(control):

    return model.disneySize(control)

def huluSize(control):

    return model.huluSize(control)

def programSize(control):

    return model.programSize(control)

# Funciones para medir tiempos de ejecucion

def getTime():

    return float(time.perf_counter()*1000)


def deltaTime(end, start):

    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada

def getMemory():

    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):

    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
