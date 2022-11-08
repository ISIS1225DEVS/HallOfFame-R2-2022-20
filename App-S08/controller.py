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


import config as cf
import model as m
import csv
import os
import time
import tracemalloc
csv.field_size_limit(2147483647)
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def carga_datos(tamaño:str,condicion_memoria):

    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    catalogo=m.nuevo_catalogo()
    cant_a=carga_plataforma(catalogo,tamaño,"amazon_prime")
    cant_d=carga_plataforma(catalogo,tamaño,"disney_plus")
    cant_h=carga_plataforma(catalogo,tamaño,"hulu")
    cant_n=carga_plataforma(catalogo,tamaño,"netflix")
    cant= cant_a+cant_d+cant_h+cant_n
    d_cantidades={}
    d_cantidades["amazon"]=cant_a
    d_cantidades["netflix"]=cant_n
    d_cantidades["hulu"]=cant_h
    d_cantidades["disney"]=cant_d
    m.orden_año_titulo(catalogo["l_videos"])
    lista_p_u=m.p_u(catalogo["l_videos"])
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return cant, lista_p_u, catalogo, d_cantidades, delta_time, delta_memory

def carga_plataforma(catalogo,tamaño,plataforma:str):
    
    archivo= os.path.join(cf.data_dir + "Streaming/" + plataforma +"_titles-utf8-" + tamaño +".csv")
    archivo_lectura=  csv.DictReader(open(archivo,encoding="utf-8"))
    p=0
    for video in archivo_lectura:
        video["stream_service"]=plataforma
        m.añadir_video(catalogo,video)
        p+=1
    return p

def orden(catalogo,tipo_de_sort):
    t1=m.ordenar(catalogo["amazon_prime"],tipo_de_sort)
    t2=m.ordenar(catalogo["disney_plus"],tipo_de_sort)
    t3=m.ordenar(catalogo["hulu"],tipo_de_sort)
    t4=m.ordenar(catalogo["netflix"],tipo_de_sort)
    t5=m.ordenar(catalogo["general"],tipo_de_sort)
    return t1+t2+t3+t4+t5 


# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def consulta_año__estreno(catalogo,año_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    lista, cantidad =m.año_estreno(catalogo,año_consulta)
    m.orden_titulo_duracion(lista)
    lista_final=m.p_u(lista)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return cantidad, lista_final,delta_time, delta_memory

def consulta_fecha(catalogo,fecha_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    lista, cantidad =m.fecha(catalogo,fecha_consulta)
    m.orden_titulo_duracion(lista)
    lista_final=m.p_u(lista)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return cantidad, lista_final, delta_time, delta_memory

def consulta_actor (catalogo, actor_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    cantidad, lista = m.actor(catalogo,actor_consulta)
    m.orden_actor(lista)
    lista_final = m.p_u(lista)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)


    return cantidad, lista_final, delta_time, delta_memory

def consulta_genero(catalogo,genero_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    lista, d_cantidad= m.genero(catalogo,genero_consulta)
    m.orden_año_titulo_duracion(lista)
    lista_final=m.p_u(lista)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return d_cantidad, lista_final, delta_time, delta_memory

def consulta_director(catalogo,director_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    cant_por_tipo,cant_por_platagorma,cant_por_genero, lista=m.director(catalogo,director_consulta)
    m.orden_año_titulo_duracion(lista)
    lista_return=m.p_u(lista)
    m.orden_cant(cant_por_genero)
    cant_por_genero_return=m.p_u(cant_por_genero)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return cant_por_tipo, cant_por_platagorma, cant_por_genero_return, lista_return, delta_time, delta_memory

def consulta_pais(catalogo,pais_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    lista, d_cantidad= m.pais(catalogo,pais_consulta)
    m.orden_año_titulo_duracion(lista)
    lista_final=m.p_u(lista)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return d_cantidad, lista_final, delta_time, delta_memory

def consulta_top_n_actores(catalogo,Top_n,genero,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    cantidad_participantes,lista_cant_actores, nuevo_mapa_actores=m.grupo_n_actores(catalogo,genero)
    m.orden_cant_bono(lista_cant_actores)
    lista_top_n=m.primeros_n(lista_cant_actores,int(Top_n))
    lista_cantidades,lista_videos, lista_colaboraciones=m.listas_bono(lista_top_n,nuevo_mapa_actores)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)


    return cantidad_participantes, lista_top_n, lista_cantidades,lista_videos, lista_colaboraciones, delta_time, delta_memory



def consulta_top_generos(catalogo,top_consulta,condicion_memoria):
    memflag=False
    if int(condicion_memoria) == 1:
        memflag=True 
    
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    num_consulta, cantidad = m.top_generos(catalogo)
    m.orden_cant_por_genero(cantidad)
    top_genero = m.top_cant_genero(cantidad,top_consulta)
    top = m.TAD_top(top_genero,catalogo)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)
    delta_memory=None

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)

    return num_consulta, top_genero, top, delta_time, delta_memory

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