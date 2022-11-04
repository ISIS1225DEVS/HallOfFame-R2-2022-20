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
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as merg
import time
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog(type,FC):
    catalog = {"MapReleaseYear":mp.newMap(maptype=type,loadfactor=FC),
                "MapDateAdded":mp.newMap(maptype=type,loadfactor=FC),
                "MapActor":mp.newMap(maptype=type,loadfactor=FC),
                "MapListedIn":mp.newMap(maptype=type,loadfactor=FC),
                "MapCountry":mp.newMap(maptype=type,loadfactor=FC),
                "MapDirector":mp.newMap(maptype=type,loadfactor=FC),
                "amazon_prime":lt.newList("ARRAY_LIST"),
                "disney_plus":lt.newList("ARRAY_LIST"),
                "hulu":lt.newList("ARRAY_LIST"),
                "netflix":lt.newList("ARRAY_LIST")}
    return catalog
# Funciones para agregar informacion al catalogo
def add_content(catalog,content):
    if content["type"] == "Movie":
        if content["release_year"] != "unknown":
            if (mp.contains(catalog["MapReleaseYear"],content["release_year"]) == True):
                lt.addLast(me.getValue(mp.get(catalog["MapReleaseYear"],content["release_year"])),content)
            else:
                mp.put(catalog["MapReleaseYear"],content["release_year"],lt.newList("ARRAY_LIST"))
                lt.addLast(me.getValue(mp.get(catalog["MapReleaseYear"],content["release_year"])),content)
    elif content["type"] == "TV Show":
        if content["date_added"] != "unknown":
            year = date_parser(content["date_added"])
            content["date_added"] = year
            if (mp.contains(catalog["MapDateAdded"],year) == True):
                lt.addLast(me.getValue(mp.get(catalog["MapDateAdded"],year)),content)
            else:
                mp.put(catalog["MapDateAdded"],year,lt.newList("ARRAY_LIST"))
                lt.addLast(me.getValue(mp.get(catalog["MapDateAdded"],year)),content)
    for actor in content["cast"].split(","):
        actor = actor.strip()
        if mp.contains(catalog["MapActor"],actor) == True:
            lt.addLast(me.getValue(mp.get(catalog["MapActor"],actor)),content)
        else:
            mp.put(catalog["MapActor"],actor,lt.newList("SINGLE_LINKED"))
            lt.addLast(me.getValue(mp.get(catalog["MapActor"],actor)),content)
    content["listed_in"] = content["listed_in"].replace("&",',')
    for genre in content["listed_in"].split(","):
        genre = genre.strip()
        if mp.contains(catalog["MapListedIn"],genre) == True:
            lt.addLast(me.getValue(mp.get(catalog["MapListedIn"],genre)),content)
        else:
            mp.put(catalog["MapListedIn"],genre,lt.newList("SINGLE_LINKED"))
            lt.addLast(me.getValue(mp.get(catalog["MapListedIn"],genre)),content)
    for country in content["country"].split(","):
        country = country.strip()
        if mp.contains(catalog["MapCountry"],country) == True:
            lt.addLast(me.getValue(mp.get(catalog["MapCountry"],country)),content)
        else:
            mp.put(catalog["MapCountry"],country,lt.newList("ARRAY_LIST"))
            lt.addLast(me.getValue(mp.get(catalog["MapCountry"],country)),content)
    for director in content["director"].split(","):
        director = director.strip()
        if mp.contains(catalog["MapDirector"],director) == True:
            lt.addLast(me.getValue(mp.get(catalog["MapDirector"],director)),content)
        else:
            mp.put(catalog["MapDirector"],director,lt.newList("ARRAY_LIST"))
            lt.addLast(me.getValue(mp.get(catalog["MapDirector"],director)),content)
    lt.addLast(catalog[content["streaming_service"]],content)
    return catalog
def date_parser(date): #Función para procesar fechas en formato "%B %d, %Y"
    result = time.strptime(date, "%B %d, %Y")
    year = str(result.tm_year)
    month = str(result.tm_mon) 
    if len(month) == 1:
        month = "0"+month
    day = str(result.tm_mday)
    if len(day) == 1:
        day = "0"+day
    return year + "-" + month + "-" + day
# Funciones para creacion de datos
def MoviesInYear(catalog,year): #Función Principal Requerimiento 1
    yearMap = catalog["MapReleaseYear"]
    yearlist = me.getValue(mp.get(yearMap,year))
    merg.sort(yearlist,CMPMoviesInYear)
    return yearlist

def ShowsInDate(catalog,date): #Función Principal Requerimiento 2
    if mp.contains(catalog["MapDateAdded"],date) == True:
        DateList = me.getValue(mp.get(catalog["MapDateAdded"],date))
        merg.sort(DateList,CMPShowsInDate)
    else:
        DateList = lt.newList("ARRAY_LIST")
    return DateList
def ContentByActor(catalog,actor): #Función Principal Requerimiento 3
    ActorMap = catalog["MapActor"]
    movies = 0
    shows = 0
    if mp.contains(ActorMap,actor) == True:
        ActorList = me.getValue(mp.get(ActorMap,actor))
    else:
        ActorList = lt.newList("ARRAY_LIST")
    for i in lt.iterator(ActorList):
        if i["type"] == "Movie":
            movies += 1
        else:
            shows += 1
    merg.sort(ActorList,CMPContentByActor)
    return ActorList,movies,shows

def contentByGenre(catalog, genre): #Función Principal Requerimiento 4
    GenreMap = catalog['MapListedIn']
    movies = 0
    shows = 0
    if mp.contains(GenreMap, genre) == True:
        GenreList = me.getValue(mp.get(GenreMap,genre))
    else:
        GenreList = lt.newList('ARRAY_LIST')
    for video in lt.iterator(GenreList):
        if video['type'] == 'Movie':
            movies+=1
        else:
            shows+=1
    merg.sort(GenreList, CMPContentByActor)
    return GenreList, movies, shows
    
def ContentbyCountry(catalog,country): #Función Principal Requerimiento 5
    CountryMap = catalog["MapCountry"]
    movies = 0
    shows = 0
    if mp.contains(CountryMap,country):
        CountryList = me.getValue(mp.get(CountryMap,country))
    else:
        CountryList = lt.newList("ARRAY_LIST")
    for i in lt.iterator(CountryList):
        if i["type"] == "Movie":
            movies += 1
        else:
            shows += 1
    merg.sort(CountryList,CMPContentByCountry)
    return CountryList,movies,shows
def TitlesByDirector(catalog,director): #Función Principal Requerimiento 6
    type = {"Movie":0,"TV Show":0}
    service_name = {"amazon_prime":{"Movie":0,"TV Show":0},"disney_plus":{"Movie":0,"TV Show":0},
        "hulu":{"Movie":0,"TV Show":0},"netflix":{"Movie":0,"TV Show":0}}
    listed_in = {}
    if mp.contains(catalog["MapDirector"],director) == True:
        DirectorList = me.getValue(mp.get(catalog["MapDirector"],director))
        for i in lt.iterator(DirectorList):
            type[i["type"]] += 1
            service_name[i["streaming_service"]][i["type"]] += 1
            for e in i["listed_in"].split(","):
                e = e.strip()
                if e not in listed_in:
                    listed_in[e] = 1
                else:
                    listed_in[e] += 1
        merg.sort(DirectorList,CMPTitlesByDirector)
        return DirectorList,type,service_name,listed_in
    else:
        return lt.newList("ARRAY_LIST"),type,service_name,listed_in
def TopNGenres(catalog,N): #Función Principal Requerimiento 7
    GenresMap = catalog["MapListedIn"]
    GenresList = mp.keySet(GenresMap)
    GenreSizeList = lt.newList("ARRAY_LIST")
    for genre in lt.iterator(GenresList):
        type_dict = {"Movie":0,"TV Show":0}
        stream_dict = {"amazon_prime":0,"disney_plus":0,"hulu":0,"netflix":0}
        title = me.getValue(mp.get(GenresMap,genre))
        for i in lt.iterator(title):
            type_dict[i["type"]] += 1
            stream_dict[i["streaming_service"]] += 1
        lt.addLast(GenreSizeList,{"genre":genre,"size":lt.size(title),"type":type_dict,"stream":stream_dict})
    merg.sort(GenreSizeList,CMPTopGenres)
    return lt.subList(GenreSizeList,1,N)

def TopNActorsByGenre(catalog, genre, N): #Función Principal Requerimiento 8
    dictActores = {}
    GenreMap = catalog["MapListedIn"]
    Titles = me.getValue(mp.get(GenreMap,genre))
    ActorList = lt.newList("ARRAY_LIST")
    for video in lt.iterator(Titles):
        for actor in video["cast"].split(","):
            actor = actor.strip()
            if actor not in dictActores:
                dictActores[actor] = lt.newList("ARRAY_LIST")  
            lt.addLast(dictActores[actor],video)
    count = 0
    while count < N:
        max_ = None
        name = None
        for key in dictActores:
            if max_ == None:
                name = key
                max_ = dictActores[key]
            elif lt.size(dictActores[key]) > lt.size(max_):
                name = key
                max_ = dictActores[key]
            elif lt.size(dictActores[key]) == lt.size(max_):
                if key < name:
                    name = key
                    max_ = dictActores[key]
        lt.addLast(ActorList,{"name":name,"titles":max_})
        dictActores.pop(name)
        count += 1
    Info_list = lt.newList("ARRAY_LIST")
    for i in lt.iterator(ActorList):
        lt.addLast(Info_list,infoActor(i))
    return Info_list
def infoActor(ActorMap):
    service_name = {"amazon_prime":{"Movie":0,"TV Show":0},"disney_plus":{"Movie":0,"TV Show":0},
        "hulu":{"Movie":0,"TV Show":0},"netflix":{"Movie":0,"TV Show":0}}
    type = {"Movie":lt.newList("ARRAY_LIST"),"TV Show":lt.newList('ARRAY_LIST')}
    directorList = lt.newList("ARRAY_LIST")
    castList = lt.newList("ARRAY_LIST")
    name = ActorMap["name"]
    titles = ActorMap["titles"]
    for i in lt.iterator(titles):
        lt.addLast(type[i["type"]],i)
        service_name[i["streaming_service"]][i["type"]] += 1
        for director in i["director"].split(","):
            director = director.strip()
            if (lt.isPresent(directorList,director) == 0) and (director != "unknown"):
                lt.addLast(directorList,director)
        for actor in i["cast"].split(","):
            actor = actor.strip()
            if (lt.isPresent(castList,actor) == 0) and (actor != name):
                lt.addLast(castList,actor)
    merg.sort(type['Movie'],CMPShowsAndSeries)
    merg.sort(type['TV Show'],CMPShowsAndSeries)
    merg.sort(directorList, CMPByAlphabet)
    merg.sort(castList, CMPByAlphabet)
    tuple = (name,service_name, type, directorList, castList)
    return tuple
        


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def CMPMoviesInYear(title1,title2): #CMP Requerimiento 1
    if title1["title"] < title2["title"]:
        return True
    elif title1["title"] == title2["title"]:
        if title1["duration"] < title2["duration"]:
            return True
    else:
        return False
def CMPShowsInDate(title1,title2): #CMP Requerimiento 2
    if title1["title"] < title2["title"]:
        return True
    elif title1["title"] == title2["title"]:
        if title1["duration"] < title2["duration"]:
            return True
    else:
        return False
def CMPContentByActor(title1,title2): #CMP Requerimiento 3
    if title1["release_year"] > title2["release_year"]:
        return True
    elif title1["release_year"] == title2["release_year"]:
        if title1["title"] < title2["title"]:
            return True
        elif title1["title"] == title2["title"]:
            if title1["duration"] < title2["duration"]:
                return True
    else:
        return False
def CMPContentByCountry(title1,title2): #CMP Requerimiento 5
    if title1["release_year"] > title2["release_year"]:
        return True
    elif title1["release_year"] == title2["release_year"]:
        if title1["title"] < title2["title"]:
            return True
        elif title1["title"] == title2["title"]:
            if title1["duration"] < title2["duration"]:
                return True
    else:
        return False
def CMPTitlesByDirector(title1,title2): #CMP Requerimiento 6
    if title1["release_year"] < title2["release_year"]:
        return True
    elif title1["release_year"] == title2["release_year"]:
        if title1["title"] < title2["title"]:
            return True
        elif title1["title"] == title2["title"]:
            if title1["duration"] < title2["duration"]:
                return True
    else:
        return False

def CMPTopGenres(title1,title2): #CMP Requerimiento 7
    if title1["size"] > title2["size"]:
        return True
    else:
        return False

def CMPByAlphabet(title1,title2):
    if title1 < title2:
        return True
    else:
        return False
def CMPShowsAndSeries(title1,title2):
    if title1["release_year"] < title2["release_year"]:
        return True
    elif title1["release_year"] == title2["release_year"]:
        if title1["title"] < title2["title"]:
            return True
        elif title1["title"] == title2["title"]:
            if title1["duration"] < title2["duration"]:
                return True
    else:
        return False