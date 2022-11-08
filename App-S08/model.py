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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
"""


#-------------------------------------------------Imports necesarios para el reto-------------------------------------------------#
from ast import Lt
from inspect import getargvalues
from tracemalloc import start
from DISClib.ADT.stack import top
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sh
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as mrg
from DISClib.Algorithms.Sorting import quicksort as qck
from DISClib.Algorithms.Sorting import selectionsort as sel
import time
from datetime import datetime
assert cf
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
#-----------------------------------Funciones que nos permiten calcular la complejidad temporal----------------------------------#
def getTime():
    """
    Devuelve el instante tiempo de procesamiento en milisegundos
    Retorno
    -------
    float:
        El contador de tiempo
    """
    return float(time.perf_counter()*1000)

def deltaTime(start, end):
    """
    Función que determina la diferencia entre tiempos
    Parámetros
    ----------
    start :
        Tiempo inicial
    end :
        Tiempo final
    Retorno
    -------
    float:
        Tiempo final - Tiempo inicial
    """
    elapsed = float(end - start)
    return elapsed

# Construccion de modelos

def nuevo_catalogo():
    """
    Función que crea el catalogo con la información de cada pelicula.
    ----------
    Return:
        Un diccionario de diccionarios con las listas de cada apartado de las plataformas.
    """
    catalogo={}
    catalogo["l_videos"]=lt.newList(datastructure='ARRAY_LIST')
    datos = ["show_id","type","director","cast","country","release_year","listed_in","date_added","stream_service"]
    for dato in datos:
        catalogo[dato]=mp.newMap(maptype='CHAINING',loadfactor=8.00)
    return catalogo

# Funciones para agregar informacion al catalogo
def añadir_video(catalogo, video):
    lista_videos=catalogo["l_videos"]
    lt.addLast(lista_videos,video)
    mp.put(catalogo["show_id"],video["show_id"],video)
    nosplit = ["type","country","release_year","date_added","stream_service"]
    split = ["listed_in","director","cast"]
    for dato in nosplit:
        añadir(catalogo,video,dato)
    for dato in split:
        añadir_con_split(catalogo,video,dato)

def añadir(catalogo, video, categoria):
    if not mp.contains(catalogo[categoria],video[categoria]):
        lista_type=lt.newList()
        lt.addLast(lista_type,video)
        mp.put(catalogo[categoria],video[categoria] ,lista_type)
    else:
        entry=mp.get(catalogo[categoria],video[categoria])
        lista_a_cambiar =me.getValue(entry)
        lt.addLast(lista_a_cambiar,video)
        mp.put(catalogo[categoria],video[categoria],lista_a_cambiar)

def añadir_con_split(catalogo, video, categoria):
    lista_elementos=video[categoria].split(",")
    for elemento in lista_elementos:
        if not mp.contains(catalogo[categoria],elemento):
            lista_nueva=lt.newList()
            lt.addLast(lista_nueva,video)
            mp.put(catalogo[categoria],elemento ,lista_nueva)
        else:
            entry=mp.get(catalogo[categoria],elemento)
            lista_a_cambiar =me.getValue(entry)
            lt.addLast(lista_a_cambiar,video)
            mp.put(catalogo[categoria],elemento,lista_a_cambiar)




# Funciones para creacion de datos

def p_u(lista):
    if lt.size(lista)>6:
        lista_p_u=lt.newList()
        p=1
        while p<=3:
            peli=lt.getElement(lista,p)
            lt.addLast(lista_p_u,peli)
            p+=1
        p2=lt.size(lista)-2
        while p2<=lt.size(lista):
            peli=lt.getElement(lista,p2)
            lt.addLast(lista_p_u,peli)
            p2+=1
        return lista_p_u
    else:
        return lista

def primeros_n(lista,n):
    lista_primeros_n=lt.newList()
    p=1
    while p<=n:
        elemento=lt.getElement(lista,p)
        lt.addLast(lista_primeros_n,elemento)
        p+=1
    return lista_primeros_n

# Funciones de consulta

#req 1
def año_estreno(catalogo,año_consulta):
    mapa_año=catalogo["release_year"]
    entry=mp.get(mapa_año,año_consulta)
    año_solicitado=me.getValue(entry)
    lista_peli=lt.newList()
    for video in lt.iterator(año_solicitado):
        if video["type"]=="Movie":
            lt.addLast(lista_peli,video)
    cantidad=lt.size(lista_peli)
    return lista_peli, cantidad

def fecha(catalogo,fecha_consulta):
    mapa_fecha=catalogo["date_added"]
    entry=mp.get(mapa_fecha,fecha_consulta)
    fecha_solicita=me.getValue(entry)
    lista_tv=lt.newList()
    for video in lt.iterator(fecha_solicita):
        if video["type"]!="Movie":
            lt.addLast(lista_tv,video)
    cantidad=lt.size(lista_tv)
    return lista_tv, cantidad

def actor(catalogo, actor_consulta):
    mapa_actor = catalogo["cast"]
    programas = 0
    peliculas = 0
    entry = mp.get(mapa_actor,actor_consulta)
    actor_solicitado = me.getValue(entry)
    listado = lt.newList()
    for video in lt.iterator(actor_solicitado):
        if actor_consulta in video["cast"]:
            lt.addFirst(listado,video)
            if video["type"] == "Movie":
                peliculas += 1
            else:
                programas += 1
    lista_de_cantidades=lt.newList()
    lt.addLast(lista_de_cantidades,{"type":"Movies","count: ":peliculas})
    lt.addLast(lista_de_cantidades,{"type":"Tv Show","count: ":programas})
    return  lista_de_cantidades, listado

def genero(catalogo,genero_consulta):
    mapa_genero=catalogo["listed_in"]
    generos_en_mapa=mp.keySet(mapa_genero)
    lista_generos_consultados=lt.newList()
    for genero in lt.iterator(generos_en_mapa):
        if genero_consulta in genero:
            lt.addLast(lista_generos_consultados,genero)
    lista_retorno=lt.newList()
    c_m=0
    c_tv=0
    for genero in lt.iterator(lista_generos_consultados):
        entry=mp.get(mapa_genero,genero)
        lista_genero=me.getValue(entry)
        for video in lt.iterator(lista_genero):
            lt.addLast(lista_retorno,video)
            if video["type"]=="Movie":
                c_m+=1
            else:
                c_tv+=1
    d_cantidad = {}
    d_cantidad["Movies"]=c_m
    d_cantidad["Tv_shows"]=c_tv
    return lista_retorno, d_cantidad
def pais(catalogo,pais_consulta):
    lista=lt.newList()
    cantidad={}
    movies=0
    tv_show=0
    mapa_pais=catalogo["country"]
    paises_en_mapa=mp.keySet(mapa_pais)
    lista_pais_consultados=lt.newList()
    for pais in lt.iterator(paises_en_mapa):
        if pais_consulta in pais:
            lt.addLast(lista_pais_consultados,pais)
    for pais in lt.iterator(lista_pais_consultados):
        lista_pais=me.getValue(mp.get(mapa_pais,pais))
        for video in lt.iterator(lista_pais):
            lt.addLast(lista,video)
            if video["type"]=="Movie":
                movies+=1
            else:
                tv_show+=1
    cantidad["Movies"]=movies
    cantidad["Tv_shows"]=tv_show
    return lista, cantidad

def director(catalogo,director_consulta):
    mapa_directores=catalogo["director"]
    entry=mp.get(mapa_directores,director_consulta)
    lista_director=me.getValue(entry)
    cant_por_tipo={}
    cant_por_plataforma={}
    cant_por_genero={}
    generos_presentes=lt.newList()
    for video in lt.iterator(lista_director):
        if video["type"] not in cant_por_tipo:
            cant_por_tipo[video["type"]]=1
        elif video ["type"] in cant_por_tipo:
            cant_por_tipo[video["type"]]+=1
        if video["stream_service"] not in cant_por_plataforma:
            cant_por_plataforma[video["stream_service"]]=1
        elif video["stream_service"] in cant_por_plataforma:
            cant_por_plataforma[video["stream_service"]]+=1
        generos=video["listed_in"].split(",")
        for genero in generos:
            if genero not in cant_por_genero.keys():
                cant_por_genero[genero]=1
                lt.addLast(generos_presentes,genero)
            else:
                cant_por_genero[genero]+=1
    lista_cant_genero=lt.newList()
    for genero in lt.iterator(generos_presentes):
        genero_como_elem={}
        genero_como_elem["listed_in"]=genero
        genero_como_elem["count"]=cant_por_genero[genero]
        lt.addLast(lista_cant_genero,genero_como_elem)
    return cant_por_tipo,cant_por_plataforma, lista_cant_genero, lista_director

def añadir_bono(mapa,llave,elemento):
    if not mp.contains(mapa,llave):
        lista_type=lt.newList()
        lt.addLast(lista_type,elemento)
        mp.put(mapa,llave ,lista_type)
    else:
        entry=mp.get(mapa,llave)
        lista_a_cambiar =me.getValue(entry)
        lt.addLast(lista_a_cambiar,elemento)
        mp.put(mapa,llave,lista_a_cambiar)

def grupo_n_actores(catalogo,genero_consulta):
    mapa_actores=catalogo["cast"]
    lista_actores=mp.keySet(mapa_actores)
    nuevo_mapa_actores=mp.newMap()
    lista_num_participaciones=lt.newList("ARRAY_LIST")
    for actor in lt.iterator(lista_actores):
        entry=mp.get(mapa_actores,actor)
        lista_videos_actor=me.getValue(entry)
        c=0
        for video in lt.iterator(lista_videos_actor):
            if genero_consulta in video["listed_in"]:
                añadir_bono(nuevo_mapa_actores,actor,video)
                c+=1
        if c>0:
            cantidad_actor_elem={}
            cantidad_actor_elem["cast"]=actor 
            cantidad_actor_elem["count"]=c 
            lt.addLast(lista_num_participaciones,cantidad_actor_elem)   
    cantidad_participantes= mp.size(nuevo_mapa_actores)
    return cantidad_participantes,lista_num_participaciones ,nuevo_mapa_actores

def listas_bono(lista_top_n,nuevo_mapa_actores):
    lista_cantidades=lt.newList()
    lista_videos=lt.newList()
    lista_colaboraciones=lt.newList()
    for actor in lt.iterator(lista_top_n):
        nombre_actor=actor["cast"]
        entry=mp.get(nuevo_mapa_actores,nombre_actor)
        lista_actor=me.getValue(entry)
        elem_listas_cantidades={}
        elem_lista_videos={}
        elem_lista_colaboraciones={}
        elem_listas_cantidades["cast"]=nombre_actor
        elem_lista_videos["cast"]=nombre_actor
        elem_lista_colaboraciones["cast"]=nombre_actor
        count_type={}
        lista_peliculas=lt.newList()
        lista_tv=lt.newList()
        lista_directores=lt.newList()
        lista_actores=lt.newList()
        for video in lt.iterator(lista_actor):
            if video["type"]=="Movie":
                    lt.addLast(lista_peliculas,video) 
            if video["type"]!="Movie":
                lt.addLast(lista_tv,video)
            if video["stream_service"] not in count_type:          
                count_type[video["stream_service"]]={video["type"]:1}
            elif video["type"] not in count_type[video["stream_service"]]:
                dict_asociado=count_type[video["stream_service"]]
                dict_asociado[video["type"]]=1
            else: 
                dict_asociado=count_type[video["stream_service"]]
                dict_asociado[video["type"]]+=1
            
            
            directores=video["director"].split(",")
            for director in directores:
                if not lt.isPresent(lista_directores,director):
                    lt.addLast(lista_directores,director)
            actores_colab=video["cast"].split(",")
            for actor_colab in actores_colab:
                if not lt.isPresent(lista_actores,actor_colab):
                    lt.addLast(lista_actores,actor_colab)
        orden_año_titulo_duracion(lista_peliculas)
        orden_año_titulo_duracion(lista_tv) 
        orden_nombres_bono(lista_directores)
        orden_nombres_bono(lista_actores)
        lista_peliculas_p_u=p_u(lista_peliculas)
        lista_tv_p_u=p_u(lista_tv)
        lista_directores_p_u=p_u(lista_directores)
        lista_actores_p_u=p_u(lista_actores)
        elem_listas_cantidades["count stream service"]=count_type
        elem_lista_videos["Movies"]=lista_peliculas_p_u
        elem_lista_videos["Tv Show"]=lista_tv_p_u
        elem_lista_colaboraciones["directors"]=lista_directores_p_u
        elem_lista_colaboraciones["actors"]=lista_actores_p_u
        lt.addLast(lista_cantidades,elem_listas_cantidades)
        lt.addLast(lista_videos,elem_lista_videos)
        lt.addLast(lista_colaboraciones,elem_lista_colaboraciones)

    return lista_cantidades,lista_videos, lista_colaboraciones
        
def top_generos(catalogo):
    TAD_conteo = lt.newList()
    list_generos = []
    TAD_generos = lt.newList()
    mapa_genero=catalogo["listed_in"]
    mapa_peliculas = catalogo["stream_service"]
    ll_filmes = mp.valueSet(mapa_peliculas)
    generos = mp.keySet(mapa_genero)
    for generos_sep in lt.iterator(generos):
        for genero in generos_sep.split(", "):
            if genero not in list_generos:
                list_generos.append(genero)
    for pos in range(0,len(list_generos)):
        genero = list_generos[pos]
        if genero[0] == " ":
            genero1 = genero[1:]
            list_generos[pos] = genero1
    list_generos1 = []
    for genero in list_generos:
        if genero not in list_generos1:
            list_generos1.append(genero)
    conteo_generos = {}
    for genero in list_generos1:
        conteo_generos[genero] = 0
        lt.addLast(TAD_generos,genero)
    for genero in conteo_generos:
        for l_filmes_genero in lt.iterator(ll_filmes):
            for filmes in lt.iterator(l_filmes_genero):
                generos = filmes["listed_in"].split(", ")
                for genero1 in generos:
                    if genero == genero1:
                        conteo_generos[genero] += 1
    for genero in lt.iterator(TAD_generos):
        tabla_genero={}
        tabla_genero["listed_in"]=genero
        tabla_genero["count"]=conteo_generos[genero]
        lt.addLast(TAD_conteo,tabla_genero)
    return len(list_generos1), TAD_conteo

def TAD_top(top_genero,catalogo):
    tad_conteo = lt.newList()
    mapa_servicios = catalogo["stream_service"]
    ll_filmes = mp.valueSet(mapa_servicios)
    tipo = {}
    plataforma = {}
    for top in lt.iterator(top_genero):
        genero = top["listed_in"]
        tipo[genero] = {}
        plataforma[genero] = {}
    for l_filmes in lt.iterator(ll_filmes):
        for filmes in lt.iterator(l_filmes):
            l_generos = filmes["listed_in"].split(", ")
            for generos in l_generos:
                for top in lt.iterator(top_genero):
                    genero = top["listed_in"]
                    tag1 = tipo[genero]
                    tag2 = plataforma[genero]
                    if genero in generos:
                        tipe1 = filmes["type"]
                        plataforma1 = filmes["stream_service"]
                        if tipe1 in tag1:
                            tag1[tipe1] += 1
                        else:
                            tag1[tipe1] = 1
                        if plataforma1 in tag2:
                            tag2[plataforma1] += 1
                        else:
                            tag2[plataforma1] = 1
    rank = 1
    for top in lt.iterator(top_genero):
        tabla_genero = {}
        genero = top["listed_in"]
        count = top["count"]
        tabla_genero["rank"] = rank
        tabla_genero["listed_in"] = genero
        tabla_genero["count"] = count
        tabla_genero["type"] = tipo
        tabla_genero["stream_service"] = plataforma
        lt.addLast(tad_conteo,tabla_genero)
        rank +=1
    return tad_conteo

# Funciones utilizadas para comparar elementos dentro de una lista

def condicion_orden_año_titulo(objeto1,objeto2):
    r=False
    if int(objeto1["release_year"]) > int(objeto2["release_year"]):
        r=True
    elif int(objeto1["release_year"]) == int(objeto2["release_year"]) and objeto1["title"].lower() > objeto2["title"].lower() :
        r=True
    return r

def condicion_orden_titulo_duracion(objeto1,objeto2):
    r=False
    if objeto1["title"].lower() < objeto2["title"].lower():
        r=True
    elif objeto1["title"].lower() < objeto2["title"].lower() and objeto1["duration"] < objeto2["duration"] :
        r=True
    return r

def condicion_pelicula_añoestreno_titulo_duracion(objeto1,objeto2):
    r=False
    if int(objeto1["release_year"]) > int(objeto2["release_year"]):
        r=True
    elif int(objeto1["release_year"]) == int(objeto2["release_year"]) and objeto1["title"].lower() < objeto2["title"].lower() :
        r=True
    elif int(objeto1["release_year"]) == int(objeto2["release_year"]) and objeto1["title"] == objeto2["title"] and objeto1["duration"]<objeto2["duration"]:
        r=True
    return r

def condicion_actor(objeto1,objeto2):

    r = False

    if objeto1["title"] < objeto2["title"]:
        r = True
    elif objeto1["title"] == objeto2["title"] and objeto1["release_year"] < objeto2["release_year"]:
        r = True
    elif objeto1["title"] == objeto2["title"] and objeto1["release_year"] == objeto2["release_year"] and objeto1["duration"] < objeto2["duration"]:
        r = True


    return r

def condicion_cant(objeto1,objeto2):
    r=False
    if objeto1["count"]>objeto2["count"]:
        r=True
    return r

def condicion_cant_bono(objeto1,objeto2):
    r=False
    if objeto1["count"]>objeto2["count"]:
        r=True
    elif objeto1["count"]==objeto2["count"] and objeto1["cast"].lower() < objeto2["cast"].lower():
        r=True
    return r
def condicion_nombre_bono(objeto1,objeto2):
    r=False
    if objeto1.lower() < objeto2.lower():
        r=True
    return r
def condicion_cant_por_genero(objeto1,objeto2):
    r=False
    if objeto1["count"]>objeto2["count"]:
        r=True
    return r

# Funciones de ordenamiento

def orden_año_titulo(lista):
    mrg.sort(lista,condicion_orden_año_titulo)

def orden_titulo_duracion(lista):
    mrg.sort(lista,condicion_orden_titulo_duracion)

def orden_actor(lista):
    mrg.sort(lista, condicion_actor)

def orden_año_titulo_duracion(lista):
    mrg.sort(lista,condicion_pelicula_añoestreno_titulo_duracion)

def orden_cant(lista):
    mrg.sort(lista,condicion_cant)

def orden_cant_bono(lista):
    mrg.sort(lista,condicion_cant_bono)
def top_cant_genero(lista,top_consulta):
    if lt.size(lista)>top_consulta:
        lista1 = lt.newList()
        while lt.size(lista1) != top_consulta:
            elemento = lt.removeFirst(lista)
            lt.addLast(lista1,elemento)
        return lista1
    else:
        return lista

def orden_nombres_bono(lista):
    mrg.sort(lista,condicion_nombre_bono)

def orden_cant_por_genero(cant_por_genero):
    mrg.sort(cant_por_genero,condicion_cant_por_genero)