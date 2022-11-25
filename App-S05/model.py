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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from datetime import datetime
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    movies
    tvShows

    Retorna el catalogo inicializado.
    """
    catalog = {'general': None,
                'general_service': None,
               'generos': None,
               'paises': None,
               'años': None,
               "actores":None, 
               "directores":None,
               'fechas': None
               }

    catalog['general'] = lt.newList('ARRAY_LIST')
    catalog['general_service'] = mp.newMap(4,
                                            maptype='PROBING',
                                            loadfactor=0.1,
                                            comparefunction=cmpVideoService)
    
    mp.put(catalog['general_service'], 'Amazon Prime', lt.newList('ARRAY_LIST'))
    mp.put(catalog['general_service'], 'Disney Plus', lt.newList('ARRAY_LIST'))
    mp.put(catalog['general_service'], 'Hulu', lt.newList('ARRAY_LIST'))
    mp.put(catalog['general_service'], 'Netflix', lt.newList('ARRAY_LIST'))
    
    catalog['generos'] = mp.newMap(120,
                                      maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareGenres)
    catalog['paises'] = mp.newMap(500,
                                      maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareCountries)
    catalog['años'] = mp.newMap(150,
                                      maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareAno)                                    
    catalog['actores'] = mp.newMap(62443,
                                      maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareActores) 
    catalog['directores'] = mp.newMap(10899,
                                      maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareActores)
    catalog['fechas'] = mp.newMap(23000,
                                      maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareFecha)                               
    return catalog


def newGenero(genero_name, gen_type, gen_service):
    """
    Crea una nueva estructura para modelar los generos de los contenidos y la
    informacion de conteo de los generos. Se crea una lista para guardar los
    contenidos de un genero.
    """
    genero = {'name': "",
    'count': 0,
    'Movie': 0,
    'TV Show': 0,
    'Amazon Prime': 0,
    'Disney Plus': 0,
    'Hulu': 0,
    'Netflix': 0,
    "videos": None,
    }
    genero['name'] = genero_name
    genero['count'] = 1
    genero[f'{gen_type}']= 1
    genero[f'{gen_service}']= 1
    genero['videos'] = lt.newList('SINGLE_LINKED', compareGenres)
    return genero

def newPais(nombre_pais, pais_type, pais_service):
    """
    Crea una nueva estructura para modelar los paises de los contenidos y la
    informacion de conteo de los paises. Se crea una lista para guardar los
    contenidos de un pais.
    """
    pais = {'name': "",
    'count': 0,
    'Movie': 0,
    'TV Show': 0,
    'Amazon Prime': 0,
    'Disney Plus': 0,
    'Hulu': 0,
    'Netflix': 0,
    "videos": None,
    }
    pais['name'] = nombre_pais
    pais['count'] = 1
    pais[f'{pais_type}']= 1
    pais[f'{pais_service}']= 1
    pais['videos'] = lt.newList('SINGLE_LINKED', compareCountries)
    return pais


def newAno(nombre_ano, ano_type, ano_service):
    """
    Crea una nueva estructura para modelar los años de los contenidos y la
    informacion de conteo de los años. Se crea una lista para guardar los
    contenidos de un año.
    """
    ano = {'name': "",
    'count': 0,
    'Movie': 0,
    'TV Show': 0,
    'Amazon Prime': 0,
    'Disney Plus': 0,
    'Hulu': 0,
    'Netflix': 0,
    "videos": None,
    }
    ano['name'] = nombre_ano
    ano['count'] = 1
    ano[f'{ano_type}']= 1
    ano[f'{ano_service}']= 1
    ano['videos'] = lt.newList('SINGLE_LINKED', compareAno)
    return ano


def newFecha(nombre_fecha, fecha_type, fecha_service):
    """
    Crea una nueva estructura para modelar las fechas de adición de los contenidos y la
    informacion de conteo de las fechas. Se crea una lista para guardar los
    contenidos de una fecha.
    """
    fecha = {'name': "",
    'count': 0,
    'Movie': 0,
    'TV Show': 0,
    'Amazon Prime': 0,
    'Disney Plus': 0,
    'Hulu': 0,
    'Netflix': 0,
    "videos": None,
    }
    fecha['name'] = nombre_fecha
    fecha['count'] = 1
    fecha[f'{fecha_type}']= 1
    fecha[f'{fecha_service}']= 1
    fecha['videos'] = lt.newList('SINGLE_LINKED', compareFecha)
    return fecha


def newActor(actor_name, act_type, act_service):
    """
    Crea una nueva estructura para modelar los actores de los contenidos y la
    informacion de conteo de los actores. Se crea una lista para guardar los
    contenidos de un actor.
    """
    actor = {'name': "",
    'count': 0,
    'Movie': 0,
    'TV Show': 0,
    'Amazon Prime': 0,
    'Disney Plus': 0,
    'Hulu': 0,
    'Netflix': 0,
    "videos": None,
    }
    actor['name'] = actor_name
    actor['count'] = 1
    actor[f'{act_type}']= 1
    actor[f'{act_service}']= 1
    actor['videos'] = lt.newList('SINGLE_LINKED', compareActores)
    return actor

def newDirector(director_name, dire_type, dire_service):
    """
    Crea una nueva estructura para modelar los actores de los contenidos y la
    informacion de conteo de los actores. Se crea una lista para guardar los
    contenidos de un actor.
    """
    director = {'name': "",
    'count': 0,
    'Movie': 0,
    'TV Show': 0,
    'Amazon Prime': 0,
    'Disney Plus': 0,
    'Hulu': 0,
    'Netflix': 0,
    "videos": None,
    }
    director['name'] = director_name
    director['count'] = 1
    director[f'{dire_type}']= 1
    director[f'{dire_service}']= 1
    director['videos'] = lt.newList('SINGLE_LINKED', compareActores)
    return director

# Funciones para agregar informacion al catalogo

def addGeneralVideoByService(catalog, video):
    """
    Adiciona un video a la lista general de videos

    Parametros:
    catalog: catalogo de videos
    video: video a agregar
    """
    lt.addLast(catalog['general'], video)

    general_service = catalog['general_service']

    service = video['service']

    entry = mp.get(general_service, service)

    serviceList = me.getValue(entry)

    lt.addLast(serviceList, video)

    return catalog

def addGenero(catalog, video):
    """
    Agrega un genero al mapa de generos de el catalogo.

    Parametros:
    catalog: catalogo de contenidos
    video: informacion del video a agregar

    Retorna:
    Catalogo de contenidos con el genero agregado
    """
    generos = catalog['generos']

    genero_name = video['listed_in']
    genero_type = video['type']
    genero_service = video['service']

    genero_name = (genero_name.split(","))

    for genero in genero_name:

        gen_name = (genero.strip())
        gen_name = genero.strip(',')
        gen_name = gen_name.strip()

        existegenero = mp.contains(generos, gen_name)

        if existegenero:
            entry = mp.get(generos, gen_name)
            genero_info = me.getValue(entry)
            genero_info['count'] += 1
            genero_info[f'{genero_type}'] += 1
            genero_info[f'{genero_service}'] += 1
            lt.addLast(genero_info['videos'], video)
        else:
            genero_info = newGenero(gen_name, genero_type, genero_service)
            lt.addLast(genero_info['videos'], video)
            mp.put(generos, gen_name, genero_info)

    return catalog

def addPais(catalog, video):
    """
    Agrega un pais al mapa de paises de el catalogo.

    Parametros:
    catalog: catalogo de contenidos
    video: informacion del video a agregar

    Retorna:
    Catalogo de contenidos con el pais agregado
    """
    paises = catalog['paises']

    pais_name = video['country']
    pais_type = video['type']
    pais_service = video['service']

    pais_name = (pais_name.split(","))

    for pais in pais_name:
        pa_name = (pais.strip())
        pa_name = pais.strip(',')
        pa_name = pa_name.strip()

        existepais = mp.contains(paises, pa_name)

        if existepais:
            entry = mp.get(paises, pa_name)
            pais_info = me.getValue(entry)
            pais_info['count'] += 1
            pais_info[f'{pais_type}'] += 1
            pais_info[f'{pais_service}'] += 1
            lt.addLast(pais_info['videos'], video)
        else:
            pais_info = newPais(pais_name, pais_type, pais_service)
            lt.addLast(pais_info['videos'], video)
            mp.put(paises, pa_name, pais_info)

    return catalog

def addAno(catalog, video):
    """
    Agrega un año al mapa de años de el catalogo.

    Parametros:
    catalog: catalogo de contenidos
    video: informacion del video a agregar

    Retorna:
    Catalogo de contenidos con el año agregado
    """
    anos = catalog['años']

    ano_name = video['release_year']
    ano_type = video['type']
    ano_service = video['service']

    existeano = mp.contains(anos, ano_name)

    if existeano:
        entry = mp.get(anos, ano_name)
        ano_info = me.getValue(entry)
        ano_info['count'] += 1
        ano_info[f'{ano_type}'] += 1
        ano_info[f'{ano_service}'] += 1
        lt.addLast(ano_info['videos'], video)
    else:
        ano_info = newAno(ano_name, ano_type, ano_service)
        lt.addLast(ano_info['videos'], video)
        mp.put(anos, ano_name, ano_info)

    return catalog
    

def addFecha(catalog, video):
    """
    Agrega una fecha al mapa de fechas de el catalogo.

    Parametros:
    catalog: catalogo de contenidos
    video: informacion del video a agregar

    Retorna:
    Catalogo de contenidos con la fecha agregada
    """
    fechas = catalog['fechas']
    if video['date_added'] != '':
        video['date_added'] = datetime.strptime(video['date_added'], '%Y-%m-%d')
        fecha_name = video['date_added']
        fecha_type = video['type']
        fecha_service = video['service']

        existefecha = mp.contains(fechas, fecha_name)

        if existefecha:
            entry = mp.get(fechas, fecha_name)
            fecha_info = me.getValue(entry)
            fecha_info['count'] += 1
            fecha_info[f'{fecha_type}'] += 1
            fecha_info[f'{fecha_service}'] += 1
            lt.addLast(fecha_info['videos'], video)
        else:
            fecha_info = newFecha(fecha_name, fecha_type, fecha_service)
            lt.addLast(fecha_info['videos'], video)
            mp.put(fechas, fecha_name, fecha_info)

        return catalog
    else:
        return None


def addActor(catalog, video):
    """
    Agrega un actor al mapa de generos de el catalogo.

    Parametros:
    catalog: catalogo de contenidos
    video: informacion del video a agregar

    Retorna:
    Catalogo de contenidos con el genero agregado
    """
    actores = catalog['actores']

    actor_name = video['cast']
    actor_type = video['type']
    actor_service = video['service']

    actor_name = (actor_name.split(","))

    for actor in actor_name:

        act_name = (actor.strip())
        act_name = actor.strip(',')
        act_name = act_name.strip()

        existeactor = mp.contains(actores, act_name)

        if existeactor:
            entry = mp.get(actores, act_name)
            actor_info = me.getValue(entry)
            actor_info['count'] += 1
            actor_info[f'{actor_type}'] += 1
            actor_info[f'{actor_service}'] += 1
            lt.addLast(actor_info['videos'], video)
        else:
            actor_info = newActor(act_name, actor_type, actor_service)
            lt.addLast(actor_info['videos'], video)
            mp.put(actores, act_name, actor_info)

    return catalog

def addDirector(catalog, video):
    """
    Agrega un director al mapa de directores de el catalogo.

    Parametros:
    catalog: catalogo de contenidos
    video: informacion del video a agregar

    Retorna:
    Catalogo de contenidos con el genero agregado
    """
    directores = catalog['directores']

    director_name = video['director']
    director_type = video['type']
    director_service = video['service']

    director_name = (director_name.split(","))

    for director in director_name:

        dire_name = (director.strip())
        dire_name = director.strip(',')
        dire_name = dire_name.strip()

        existedirector = mp.contains(directores, dire_name)

        if existedirector:
            entry = mp.get(directores, dire_name)
            director_info = me.getValue(entry)
            director_info['count'] += 1
            director_info[f'{director_type}'] += 1
            director_info[f'{director_service}'] += 1
            lt.addLast(director_info['videos'], video)
        else:
            director_info = newDirector(dire_name, director_type, director_service)
            lt.addLast(director_info['videos'], video)
            mp.put(directores, dire_name, director_info)

    return catalog

# Funciones para creacion de datos

def getType(lista,type):
    """
    Filtra para un tipo de contenido
    """
    list = lt.newList('ARRAY_LIST')
    for i in lt.iterator(lista):
        if i['type'] == type:
            lt.addLast(list, i)
    return list

# Funciones de consulta

def topGeneros(catalog, num_top):
    """
    Encuentra los top N contenidos de un genero.

    Parametros:
    catalog: catalogo de contenidos
    num_top: numero de elementos a retornar

    Retorna:
    Lista con los top N contenidos de un genero
    """
    gen_top = lt.newList('ARRAY_LIST')
    generos = catalog['generos']
    
    for genero in lt.iterator(mp.keySet(generos)):
        entry = mp.get(generos, genero)
        genero_info = me.getValue(entry)
        lt.addLast(gen_top, genero_info)

    sorted_list = ms.sort(gen_top, cmpGenresByCount)
    top = lt.subList(sorted_list, 1, num_top)

    return top, lt.size(sorted_list)


def buscarPais(catalog, pais):
    """
    Busca un pais en el catalogo de contenidos

    Parametros:
    catalog: catalogo de contenidos
    pais: pais a buscar

    Retorna:
    Una lista con los contenidos del pais
    """
    paises = catalog['paises']
    pais_info_list = lt.newList('ARRAY_LIST')
    conteo = lt.newList('ARRAY_LIST')
    existepais = mp.contains(paises, pais)
    if existepais:
        entry = mp.get(paises, pais)
        pais_info = me.getValue(entry)

        for video in lt.iterator(pais_info['videos']):
            lt.addLast(pais_info_list, video)

        lt.addLast(conteo, pais_info['Movie'])
        lt.addLast(conteo, pais_info['TV Show'])

        sorted_pais_info = ms.sort(pais_info_list, cmpByReleaseYear)

        return sorted_pais_info, conteo
    return None


def buscarAno(catalog, ano):
    """
    Busca un año en el catalogo de contenidos

    Parametros:
    catalog: catalogo de contenidos
    ano: año a buscar

    Retorna:
    Una lista con los contenidos del año
    """
    anos = catalog['años']
    ano_info_list = lt.newList('ARRAY_LIST')
    conteo = lt.newList('ARRAY_LIST')
    existeano = mp.contains(anos, ano)
    if existeano:
        entry = mp.get(anos, ano)
        ano_info = me.getValue(entry)

        for video in lt.iterator(ano_info['videos']):
            lt.addLast(ano_info_list, video)

        lt.addLast(conteo, ano_info['Movie'])
        lt.addLast(conteo, ano_info['TV Show'])

        sorted_ano_info = ms.sort(ano_info_list, cmpByReleaseYear)

        return sorted_ano_info, conteo
    return None


def buscarFecha(catalog, fecha):
    """
    Busca una fecha en el catalogo de contenidos

    Parametros:
    catalog: catalogo de contenidos
    fecha: fecha a buscar

    Retorna:
    Una lista con los contenidos de la fecha
    """
    fechas = catalog['fechas']
    fecha_info_list = lt.newList('ARRAY_LIST')
    conteo = lt.newList('ARRAY_LIST')
    existefecha = mp.contains(fechas, fecha)
    if existefecha:
        entry = mp.get(fechas, fecha)
        fecha_info = me.getValue(entry)

        for video in lt.iterator(fecha_info['videos']):
            lt.addLast(fecha_info_list, video)

        lt.addLast(conteo, fecha_info['Movie'])
        lt.addLast(conteo, fecha_info['TV Show'])
        sorted_fecha_info = ms.sort(fecha_info_list, cmpByTitle)

        return sorted_fecha_info, conteo
    return None


def buscarGenero(catalog, genero):
    """
    Busca un genero en el catalogo de contenidos

    Parametros:
    catalog: catalogo de contenidos
    genero: genero a buscar

    Retorna:
    Una lista con los contenidos del genero
    """
    generos = catalog['generos']
    genero_info_list = lt.newList('ARRAY_LIST')
    conteo = lt.newList('ARRAY_LIST')
    existegenero = mp.contains(generos, genero)
    if existegenero:
        entry = mp.get(generos, genero)
        genero_info = me.getValue(entry)

        for video in lt.iterator(genero_info['videos']):
            lt.addLast(genero_info_list, video)

        lt.addLast(conteo, genero_info['Movie'])
        lt.addLast(conteo, genero_info['TV Show'])

        sorted_genero_info = ms.sort(genero_info_list, cmpGenresByReleaseYear)

        return sorted_genero_info, conteo
    return None

def buscarActor(catalog, actor):
    """
    Busca un actor en el catalogo de contenidos

    Parametros:
    catalog: catalogo de contenidos
    actor: actor a buscar

    Retorna:
    Una lista con los contenidos del actor
    """
    actores = catalog['actores']
    actor_info_list = lt.newList('ARRAY_LIST')
    conteo = lt.newList('ARRAY_LIST')
    existeactor = mp.contains(actores, actor)
    if existeactor:
        entry = mp.get(actores, actor)
        actor_info = me.getValue(entry)

        for video in lt.iterator(actor_info['videos']):
            lt.addLast(actor_info_list, video)

        lt.addLast(conteo, actor_info['Movie'])
        lt.addLast(conteo, actor_info['TV Show'])

        sorted_actor_info = ms.sort(actor_info_list, cmpGenresByReleaseYear)

        return sorted_actor_info, conteo
    return None

def buscarDirector(catalog, director):
    """
    Busca un director en el catalogo de contenidos

    Parametros:
    catalog: catalogo de contenidos
    director: director a buscar

    Retorna:
    Una lista con los contenidos del director
    """
    directores = catalog['directores']
    director_info_list = lt.newList('ARRAY_LIST')
    conteoType = lt.newList('ARRAY_LIST')
    conteoPlat=lt.newList('ARRAY_LIST')
    existedirector = mp.contains(directores, director)
    if existedirector:
        entry = mp.get(directores, director)
        director_info = me.getValue(entry)

        for video in lt.iterator(director_info['videos']):
            lt.addLast(director_info_list, video)

        lt.addLast(conteoType, director_info['Movie'])
        lt.addLast(conteoType, director_info['TV Show'])
        lt.addLast(conteoPlat, director_info['Amazon Prime'])
        lt.addLast(conteoPlat, director_info['Disney Plus'])
        lt.addLast(conteoPlat, director_info['Hulu'])
        lt.addLast(conteoPlat, director_info['Netflix'])
        sorted_director_info = ms.sort(director_info_list, cmpGenresByReleaseYear)

        generos={}
        listgen=lt.newList('ARRAY_LIST')
        for content in lt.iterator(director_info_list):
            generes=content["listed_in"].split(',')
            for genere in generes:
                genere = (genere.strip()).lower()
                if  genere in generos:
                    generos[genere] +=1
                else:
                    generos[genere] =0
                    generos[genere] =1
        for genere in generos:
            lt.addLast(listgen, [genere,generos[genere]])


        return sorted_director_info, conteoType, conteoPlat, listgen
    return None

def generalServiceFirstLast(catalog):
    """
    Retorna el primer y ultimo video de cada servicio
    """
    general_service = catalog['general_service']
    general_list = lt.newList('ARRAY_LIST')

    Amazon = mp.get(general_service, 'Amazon Prime')
    Amazon = me.getValue(Amazon)

    Disney = mp.get(general_service, 'Disney Plus')
    Disney = me.getValue(Disney)

    Hulu = mp.get(general_service, 'Hulu')
    Hulu = me.getValue(Hulu)

    Netflix = mp.get(general_service, 'Netflix')
    Netflix = me.getValue(Netflix)

    for video in lt.iterator(Amazon):
        lt.addLast(general_list, video)
    for video in lt.iterator(Disney):
        lt.addLast(general_list, video)
    for video in lt.iterator(Hulu):
        lt.addLast(general_list, video)
    for video in lt.iterator(Netflix):
        lt.addLast(general_list, video)

    general_list = ms.sort(general_list, cmpGenresByReleaseYear)

    First = lt.subList(general_list, 1, 3)
    Last = lt.subList(general_list, lt.size(general_list)-2, 3)

    return First, Last, lt.size(Amazon), lt.size(Disney), lt.size(Hulu), lt.size(Netflix)

# Funciones utilizadas para comparar elementos dentro de una lista

def compareGenres(genero1, genero2):
    """
    Devuelve 0 si los nombres de los generos son iguales,
    si el "genero1" es menor que el "genero2" retorna -1
    si el "genero1" es mayor que el "genero2" retorna 1

    Parametros:
    genero1: primer genero a comparar
    genero2: segundo genero a comparar
    """

    genero2 = me.getKey(genero2)
    genero1 = genero1.strip()

    if (genero1) == (genero2):
        return 0
    elif (genero1) > (genero2):
        return 1
    elif (genero1) < (genero2):
        return -1
    else:
        raise Exception

def compareCountries(pais1, pais2):
    """
    Devuelve 0 si los nombres de los paises son iguales,
    si el "pais1" es menor que el "pais2" retorna -1
    si el "genero1" es mayor que el "pais2" retorna 1

    Parametros:
    pais1: primer pais a comparar
    pais2: segundo pais a comparar
    """

    pais2 = me.getKey(pais2)
    pais1 = pais1.strip()

    if (pais1) == (pais2):
        return 0
    elif (pais1) > (pais2):
        return 1
    elif (pais1) < (pais2):
        return -1
    else:
        raise Exception

def compareAno(pais1, pais2):
    """
    Devuelve 0 si los nombres de los paises son iguales,
    si el "pais1" es menor que el "pais2" retorna -1
    si el "genero1" es mayor que el "pais2" retorna 1

    Parametros:
    pais1: primer pais a comparar
    pais2: segundo pais a comparar
    """
    pais1 = int(pais1)
    pais2 = int(me.getKey(pais2))                                  

    if (pais1) == (pais2):
        return 0
    elif (pais1) > (pais2):
        return 1
    elif (pais1) < (pais2):
        return -1
    else:
        raise Exception

def compareFecha(pais1, pais2):
    """
    Devuelve 0 si los nombres de los paises son iguales,
    si el "pais1" es menor que el "pais2" retorna -1
    si el "genero1" es mayor que el "pais2" retorna 1

    Parametros:
    pais1: primer pais a comparar
    pais2: segundo pais a comparar
    """
    pais1 = pais1
    pais2 = me.getKey(pais2)

    if (pais1) == (pais2):
        return 0
    elif (pais1) > (pais2):
        return 1
    elif (pais1) < (pais2):
        return -1
    else:
        raise Exception

def compareActores(actor1, actor2):
    """
    Devuelve 0 si los nombres de los actores son iguales,
    si el "actor1" es menor que el "actor2" retorna -1
    si el "actor1" es mayor que el "actor2" retorna 1

    Parametros:
    actor1: primer actor a comparar
    actor2: segundo actor a comparar
    """

    actor2 = me.getKey(actor2)
    actor1 = actor1.strip()

    if (actor1) == (actor2):
        return 0
    elif (actor1) > (actor2):
        return 1
    elif (actor1) < (actor2):
        return -1
    else:
        raise Exception

def cmpVideoService(service1, service2):
    """
    Compara dos servicios de streaming de videos

    Parametros:
    service1: primer id a comparar
    service2: segundo id a comparar
    """
    service2 = me.getKey(service2)

    if (service1) == (service2):
        return 0
    elif (service1) > (service2):
        return 1
    elif (service1) < (service2):
        return -1
    else: raise Exception

def cmpGenresByCount(video1, video2):
    """
    Devuelve verdadero (True) si los 'count' de video1 son menores que los de video2.
    De lo contrario deuelve falso (False).
    Parametros:
        video1: informacion del primer genero que incluye su valor 'count'
        video2: informacion del segundo genero que incluye su valor 'count'
    """
    return (float(video1['count']) > float(video2['count']))


def cmpGenresByReleaseYear(video1, video2):
    """
    Devuelve verdadero (True) si los 'release_year' de video1 son mayores que los de video2.
    Si son iguales compara los 'title' de los videos. Si ambos criterios son iguales tiene 
    en cuenta el 'duration' de los videos. De lo contrario deuelve falso (False).
    Parametros:
        video1: informacion del primer genero que incluye su valor 'release_year'
        video2: informacion del segundo genero que incluye su valor 'release_year'
    """
    if video1['release_year'] == '':
        video1['release_year'] = 0
    if video2['release_year'] == '':
        video2['release_year'] = 0
    if (float(video1['release_year']) > float(video2['release_year'])):
        return True
    elif (float(video1['release_year']) == float(video2['release_year'])):
        if (video1['title']) > (video2['title']): #AQUI ESTA AL REVES LOCO
            return True
        elif (video1['title']) == (video2['title']):
            if (video1['duration']) > (video2['duration']):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def cmpByReleaseYear(video1, video2):
    """
    Devuelve verdadero (True) si los 'release_year' de video1 son mayores que los de video2.
    Si son iguales compara los 'title' de los videos. Si ambos criterios son iguales tiene 
    en cuenta el 'duration' de los videos. De lo contrario deuelve falso (False).
    Parametros:
        video1: informacion del primer genero que incluye su valor 'release_year'
        video2: informacion del segundo genero que incluye su valor 'release_year'
    """
    if video1['release_year'] == '':
        video1['release_year'] = 0
    if video2['release_year'] == '':
        video2['release_year'] = 0
    if (float(video1['release_year']) > float(video2['release_year'])):
        return True
    elif (float(video1['release_year']) == float(video2['release_year'])):
        if (video1['title']) < (video2['title']):
            return True
        elif (video1['title']) == (video2['title']):
            if (video1['duration']) > (video2['duration']):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def cmpByTitle(video1, video2):
    """
    Devuelve verdadero (True) si los 'release_year' de video1 son mayores que los de video2.
    Si son iguales compara los 'title' de los videos. Si ambos criterios son iguales tiene 
    en cuenta el 'duration' de los videos. De lo contrario deuelve falso (False).
    Parametros:
        video1: informacion del primer genero que incluye su valor 'release_year'
        video2: informacion del segundo genero que incluye su valor 'release_year'
    """
    if (video1['title']) < (video2['title']):
        return True
    elif (video1['title']) == (video2['title']):
        if (video1['duration']) > (video2['duration']):
            return True
        else:
            return False
    else:
        return False

# Funciones de ordenamiento
