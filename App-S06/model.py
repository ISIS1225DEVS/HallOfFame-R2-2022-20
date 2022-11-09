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

from ast import Return
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
from datetime import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {
        'total': None,
        'movies': None,
        'tv_programs': None,
        "director": None,
        "cast": None,
        'release_year' : None,
        'listed_in': None        
    }

    catalog["total"]= lt.newList('ARRAY_LIST', cmpfunction = cmpMoviesByReleaseYear)
    catalog['movies'] = lt.newList('SINGLE_LINKED', cmpfunction = cmpMoviesByReleaseYear)
    catalog['tv_programs'] = lt.newList('SINGLE_LINKED', cmpfunction = cmpMoviesByReleaseYear)
    catalog["director"]= mp.newMap(50,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapdirector)
    catalog['cast'] = mp.newMap(50,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareMapcast)
    catalog['release_years'] = mp.newMap(50,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareMapYear)
    catalog['listed_in'] = mp.newMap(100,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction= compareMapListedIn)
    return catalog

# Funciones para agregar informacion al catalogo

def addTitle(catalog, title, platform):

    if title['director'] == '':
        title['director'] = 'Unknown'
    else:
        title['director'] = title['director'].split(', ')
    if title['cast'] == '':
        title['cast'] = 'Unknown'
    else:
        title['cast'] = title['cast'].split(', ')

    if title['country'] == '':
        title['country'] = 'Unknown'
    else:
        title['country'] = title['country'].split(', ')
    if title['date_added'] == '':
        title['date_added'] = 'Unknown'
    title['release_year'] = int(title['release_year'])
    title['listed_in'] = title['listed_in'].split(', ')
    title['platform'] = platform

    """Agregar información a la lista de peliculas y shows"""
    if title['type'] == 'Movie':
        lt.addLast(catalog['movies'], title)
    else:
        lt.addLast(catalog['tv_programs'], title)
    lt.addLast(catalog["total"],title)

    """Agregar información al mapa de director"""
    for director in title["director"]:
        addTitledirector(catalog, director.strip(),title)

    """Agregar información al mapa de cast"""
    if title['cast'] != 'Unknown':
        for actor in title["cast"]:
            addTitleActor(catalog, actor.strip(), title)

    """Agregar información al mapa de generos"""
    for genero in title['listed_in']:
        addTitleGenero(catalog, genero.strip(), title)

    addTitleYear(catalog, title)

    return catalog

#--------------------------------------------------
#Función para adherir un titulo al mapa de director
#--------------------------------------------------

def addTitledirector(catalog, directorname, title):

    try:

        directores = catalog['director']
        existdirector = mp.contains(directores, directorname)

        if existdirector:
            entry = mp.get(directores, directorname)
            director=me.getValue(entry)

        else:
            director = newdirector(directorname)
            mp.put(directores, directorname, director)

        if title['type'] == 'Movie':
            lt.addLast(director['movies'], title)

        else:
            lt.addLast(director['tv_shows'], title)
        
        lt.addLast(director['titles'], title)
        director['total'] += 1

    except Exception:
        return None

#--------------------------------------------------
#Función para adherir un titulo al mapa de cast
#--------------------------------------------------

def addTitleActor(catalog, actorname, title):

    try:

        actors = catalog['cast']
        existactor = mp.contains(actors, actorname)

        if existactor:
            entry = mp.get(actors, actorname)
            actor=me.getValue(entry)

        else:
            actor = newActor(actorname)
            mp.put(actors, actorname, actor)

        if title['type'] == 'Movie':
            lt.addLast(actor['movies'], title)

        else:
            lt.addLast(actor['tv_shows'], title)

        lt.addLast(actor['titles'], title)
        actor['total'] += 1

    except Exception:
        return None

#------------------------------------------------------
#Función para adherir un titulo al mapa de release year
#------------------------------------------------------

def addTitleYear(catalog, title):
    try:
        years = catalog['release_years']
        if (title['release_year'] != ''):
            pubyear = title['release_year']
            pubyear = int(float(pubyear))
        else:
            pubyear = None
        existyear = mp.contains(years, pubyear)
        if existyear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        if title['type'] == 'Movie':
            lt.addLast(year['movies'], title)
        else:
            lt.addLast(year['tv_shows'], title)
        lt.addLast(year['titles'], title)
        year['total'] += 1
    except Exception:
        return None

#--------------------------------------------------
#Función para adherir un titulo al mapa de generos
#--------------------------------------------------

def addTitleGenero(catalog, generoname, title):

    try:

        generos = catalog['listed_in']
        existgenero = mp.contains(generos, generoname)

        if existgenero:
            entry = mp.get(generos, generoname)
            genero = me.getValue(entry)

        else:
            genero = newGenero(generoname)
            mp.put(generos, generoname, genero)

        if title['type'] == 'Movie':
            lt.addLast(genero['movies'], title)

        else:
            lt.addLast(genero['tv_shows'], title)

        lt.addLast(genero['titles'], title)
        genero['total'] += 1

    except Exception:
        return None

# Funciones para creacion de datos

#-----------------------------------------------------
#Función para crear una nueva llave en el map director
#-----------------------------------------------------

def newdirector(pubdirector):
    entry = {'date': "", 
            "titles": None,
            'movies': None,
            'tv_shows': None,
            'total': 0}

    entry['date'] = pubdirector
    entry['titles'] = lt.newList('SINGLE_LINKED', cmpTitulos)
    entry['movies'] = lt.newList('SINGLE_LINKED', cmpTitulos)
    entry['tv_shows'] = lt.newList('SINGLE_LINKED', cmpTitulos)
    return entry

#-----------------------------------------------------
#Función para crear una nueva llave en el map cast
#-----------------------------------------------------

def newActor(name):
    actor = {'name':"",
              'titles': None,
              'movies': None,
              'tv_shows': None,
              'total': 0,
              'directores': None,
              'cast': None
    }
    actor['name'] = name
    actor['titles'] = lt.newList('SINGLE_LINKED', compareMapListedIn)
    actor['movies'] = lt.newList('SINGLE_LINKED', compareMapListedIn)
    actor['tv_shows'] = lt.newList('SINGLE_LINKED', compareMapListedIn)
    actor['directores'] = lt.newList('ARRAY_LIST', compareMapListedIn)
    actor['cast'] = lt.newList('ARRAY_LIST', compareMapListedIn)
    return actor

#---------------------------------------------------------
#Función para crear una nueva llave en el map release year
#---------------------------------------------------------

def newYear(pubyear):
    entry = {'year': "", 
            "titles": None,
            'movies': None,
            'tv_shows': None,
            'total': 0}

    entry['year'] = pubyear
    entry['titles'] = lt.newList('SINGLE_LINKED', cmpTitulos)
    entry['movies'] = lt.newList('SINGLE_LINKED', cmpTitulos)
    entry['tv_shows'] = lt.newList('SINGLE_LINKED', cmpTitulos)
    return entry

#-----------------------------------------------------
#Función para crear una nueva llave en el map genero
#-----------------------------------------------------

def newGenero(name):
    genero = {'name':"",
              'titles': None,
              'movies': None,
              'tv_shows': None,
              'total': 0
    }
    genero['name'] = name
    genero['titles'] = lt.newList('SINGLE_LINKED', compareMapListedIn)
    genero['movies'] = lt.newList('SINGLE_LINKED', compareMapListedIn)
    genero['tv_shows'] = lt.newList('SINGLE_LINKED', compareMapListedIn)
    return genero
    
# Funciones de consulta

def getSix(list):
    if lt.size(list)>= 6: 
        first = lt.subList(list, 1, 3)
        last = lt.subList(list, lt.size(list) - 2, 3)
        six = lt.newList('ARRAY_LIST')
        for elem in lt.iterator(first):
            lt.addLast(six, elem)
        for elem in lt.iterator(last):
            lt.addLast(six, elem)
    else:
        six = list
    return six

def countplatforms(total):
    movies_total = lt.newList('ARRAY_LIST', cmpfunction= cmpTitulos)   
    count = 0
    for platform in total.keys():
        dupla = [platform, total[platform]]
        lt.addLast(movies_total, dupla)
    return movies_total

# ==============================
# REQUERIMIENTO 1 
# ==============================

def getMoviesByYear(catalog, year):
    year = mp.get(catalog['release_years'], year)
    if year:
        titles = me.getValue(year)['movies']
        return mer.sort(titles, cmpTitulos)  
    return None

# ==============================
# REQUERIMIENTO 3
# ==============================   

def getTitlesByActor(catalog, actor): 
    actor =mp.get(catalog["cast"], actor)
    if actor:
        titles=  me.getValue(actor)
        titles_total= sortByReleaseYear(titles['titles'])
        return titles, titles_total
    return None 

# ==============================
# REQUERIMIENTO 4
# ==============================

def getTitlesByGenero(catalog, genero):
    genero = mp.get(catalog['listed_in'], genero)
    if genero:
        titles = me.getValue(genero)
        titles_total = sortByReleaseYear(titles['titles'])
        return titles, titles_total
    return None

# ==============================
# REQUERIMIENTO 6
# ==============================

def getTitlesByDirector(catalog, director):
    director = mp.get(catalog['director'], director)
    if director:
        titles = me.getValue(director)
        titles_total = sortByReleaseYear(titles['titles'])
        i = 1

        plataformas= mp.newMap()

        while i <= lt.size(titles_total):
            title = lt.getElement(titles_total, i)
            plataforma = title["platform"]
            esta = mp.contains(plataformas,plataforma)
            if not esta:
                mp.put(plataformas, plataforma, 0)
            num = me.getValue(mp.get(plataformas, plataforma))
            num += 1
            mp.put(plataformas, plataforma, num)
            i += 1


        i=1
        generos =mp.newMap()

        for title in lt.iterator(titles_total):
            generos2 = title["listed_in"]
            for genero in generos2:
                esta = mp.contains(generos,genero)
                if not esta:
                    mp.put(generos, genero, 0)
                num = me.getValue(mp.get(generos, genero))
                num += 1
                mp.put(generos, genero, num)
            i += 1

        return titles, titles_total, plataformas, generos
    return None

# ==============================
# REQUERIMIENTO 7
# ==============================
def getTopGenero(catalog, rank):
    generos = mp.keySet(catalog['listed_in'])
    lista_genero = lt.newList('ARRAY_LIST')
    for genero in lt.iterator(generos):
        entry = mp.get(catalog['listed_in'], genero)
        tupla = [genero, me.getValue(entry)['total']]
        lt.addLast(lista_genero, tupla)
    
    lista_genero = mer.sort(lista_genero, cmpCantidadGenero)
    top = lt.subList(lista_genero, 1, rank)
    return top
    
# ==============================
# REQUERIMIENTO 8
# ==============================

def getActorGenero(info_genero):
    titles = info_genero['titles']
    info = {'cast': None}
    info['cast'] = mp.newMap()
    for title in lt.iterator(titles):
        if title['cast'] != 'Unknown':
            for actor in title['cast']:
                addTitleActor(info, actor, title)
                directores = me.getValue(mp.get(info['cast'], actor))
                directores = directores['directores']
                for director in title['director']:
                    if not director in directores['elements']:
                        lt.addLast(directores, director)
                actores2 = me.getValue(mp.get(info['cast'], actor))
                actores2 = actores2['cast']
                for actor2 in title['cast']:
                    if actor2 != actor:
                       if not actor2 in actores2['elements']:
                        lt.addLast(actores2, actor2)
    actores = mp.keySet(info['cast'])
    for actor in lt.iterator(actores):
        count = me.getValue(mp.get(info['cast'], actor))
        count['movies'] = sortByReleaseYear(count['movies'])
        count['tv_shows'] = sortByReleaseYear(count['tv_shows'])
        count['directores'] = mer.sort(count['directores'], cmpByName)
        count['cast'] = mer.sort(count['cast'], cmpByName)
    return info['cast']

def getTopActor(actors, rank):
    
    actores = mp.keySet(actors)
    actor_list = lt.newList('ARRAY_LIST')
    for actor in lt.iterator(actores):
        count = me.getValue(mp.get(actors, actor))
        count['movies'] = sortByReleaseYear(count['movies'])
        count['tv_shows'] = sortByReleaseYear(count['tv_shows'])
        lt.addLast(actor_list, [actor, count['total']])
    
    actor_list = mer.sort(actor_list, cmpCantidadGenero)
    top = lt.subList(actor_list,1 , rank)
    return top

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpMoviesByReleaseYear(movie1, movie2):
    if movie1['release_year'] == movie2['release_year']:
        if movie1['title'] == movie2['title']:
            return movie1['duration'] > movie2['duration']
        return movie1['title'] < movie2['title']
    return movie1['release_year'] > movie2['release_year']

def cmpTitulos(titulo1, titulo2):
    return titulo1['title'] < titulo2['title']

def compareMapListedIn(genero, entry):
    #print(entry)
    genentry = me.getKey(entry)
    if (genero == genentry):
        return 0
    elif (genero > genentry):
        return 1
    else:
        return -1

def compareMapYear(year, title):
    #print(title)
    #print(year)
    titlentry = me.getKey(title)
    if (year == titlentry):
        return 0
    elif (year > titlentry):
        return 1
    else:
        return -1

def compareMapdate(date, title):
    titlentry = me.getKey(title)
    if (date == titlentry):
        return 0
    elif (date > titlentry):
        return 1
    else:
        return -1

def compareMapActors(actor, title):
    actentry = me.getKey(title)
    if (actor == actentry):
        return 0
    elif (actor > actentry):
        return 1
    else:
        return -1
        
def compareMapdirector(director,title):
    titlentry = me.getKey(title)
    if (director == titlentry):
        return 0
    elif (director > titlentry):
        return 1
    else:
        return -1


def compareMapcast(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    #print(author)
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def cmpByName(name1, name2):
    return name1<name2

def cmpCantidadGenero(genero1,genero2):
    if genero1[1] == genero2[1]:
        return genero1[0] < genero2[0]
    return genero1[1] > genero2[1]

# Funciones de ordenamiento

def sortByReleaseYear(titles):
    return mer.sort(titles, cmpMoviesByReleaseYear)