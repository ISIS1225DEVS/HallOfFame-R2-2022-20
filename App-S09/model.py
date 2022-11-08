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


from asyncio import streams
from email.errors import NoBoundaryInMultipartDefect
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
import time
from datetime import datetime
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Sorting import quicksort as quick
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog= {"Amazon": None, "Disney": None, "Hulu": None, "Netflix":None, "Total":None, "Actores": None, "Generos":None, "Years": None, "Dates":None,"Directors":None}
    catalog["Amazon"] = lt.newList("ARRAY_LIST")
    catalog["Disney"] = lt.newList("ARRAY_LIST")
    catalog["Hulu"] = lt.newList("ARRAY_LIST")
    catalog["Netflix"] = lt.newList("ARRAY_LIST")
    catalog["Total"]= lt.newList("ARRAY_LIST")
    catalog["Generos"]=mp.newMap(120,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=comparegeneros)
    catalog["Actores"]=mp.newMap(62534,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=compareactores)
    catalog["Years"]=mp.newMap(101,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=compareanios)
    catalog["Dates"]=mp.newMap(1442,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=comparedates)
    catalog["Country"]=mp.newMap(129,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction=comparecountry)
    catalog["Directors"] =mp.newMap(10899,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=comparecountry)
            
    return catalog



# Funciones para agregar informacion al catalogo
def addAmazon(catalog, programaA):
    a = newAmazon(programaA["show_id"], programaA["type"], programaA["title"],
                  programaA["director"], programaA["cast"], programaA["country"], programaA["date_added"], programaA["release_year"], 
                  programaA["rating"], programaA["duration"], 
                  programaA["listed_in"], programaA["description"])
    lt.addLast(catalog["Amazon"], a)   
    lt.addLast(catalog["Total"], a)
    generos=a["listed_in"]
    actores= a["cast"]
    anio= a["release_year"]
    countries = a["country"]
    directors = a["director"]

    if a["date_added"] != "":
        date= time.strptime(a["date_added"],"%B %d, %Y")
    else:
        date = None
    for genero in generos:
        gen=genero.strip()
        AddGenero(catalog,gen, a)
    for actor in actores:
        AddActor(catalog,actor, a)
    if a["type"]=="Movie":
        AddYear(catalog, anio, a)
    elif a["type"]=="TV Show":
        AddDate(catalog, date , a)
    for country in countries:
        country = country.strip()
        AddCountry(catalog,country, a)
    for director in directors:
        director = director.strip()
        AddDirector(catalog,director,a)
    """"
    if a["type"]=="Movie":
        lt.addLast(catalog["Peliculas"],a)
    else:
        lt.addLast(catalog["ProgramasTV"],a)
    
    for actor in a["cast"]:
        lt.addLast(catalog["Actores"], actor)
    """
    return catalog


def addDisney(catalog, programaD):
    d = newDisney(programaD["show_id"], programaD["type"], programaD["title"],
                  programaD["director"], programaD["cast"], programaD["country"], programaD["date_added"], programaD["release_year"], 
                  programaD["rating"], programaD["duration"], 
                  programaD["listed_in"], programaD["description"])
    lt.addLast(catalog["Disney"], d)   
    lt.addLast(catalog["Total"], d)
    generos=d["listed_in"]
    actores= d["cast"]
    anio= d["release_year"]
    countries = d["country"]
    directors = d["director"]
    if d["date_added"] != "":
        date= time.strptime(d["date_added"],"%B %d, %Y")
    else:
        date = None
    for genero in generos:
        gen=genero.strip()
        AddGenero(catalog,gen, d)
    for actor in actores:
        AddActor(catalog,actor, d)
    if d["type"]=="Movie":
        AddYear(catalog, anio, d)
    elif d["type"]=="TV Show":
        AddDate(catalog, date, d)
    for country in countries:
        country = country.strip()
        AddCountry(catalog,country, d)
    for director in directors:
        director = director.strip()
        AddDirector(catalog,director,d)    
    
    return catalog


def addHulu(catalog, programaH):
    h = newHulu(programaH["show_id"], programaH["type"], programaH["title"],
                  programaH["director"], programaH["cast"], programaH["country"], programaH["date_added"], programaH["release_year"], 
                  programaH["rating"], programaH["duration"], 
                  programaH["listed_in"], programaH["description"])
    lt.addLast(catalog["Hulu"], h)  
    lt.addLast(catalog["Total"], h)
    generos=h["listed_in"]
    actores= h["cast"]
    anio= h["release_year"]
    countries = h["country"]
    directors = h["director"]
    if h["date_added"] != "":
        date= time.strptime(h["date_added"],"%B %d, %Y")
    else:
        date = None
    for genero in generos:
        gen=genero.strip()
        AddGenero(catalog,gen, h)
    for actor in actores:
        AddActor(catalog,actor, h)
    if h["type"]=="Movie":
        AddYear(catalog, anio, h)
    elif h["type"]=="TV Show":
        AddDate(catalog, date, h)
    for country in countries:
        country = country.strip()
        AddCountry(catalog,country, h)
    for director in directors:
        director = director.strip()
        AddDirector(catalog,director,h)
    return catalog
    

def addNetflix(catalog, programaN):
    n = newNetflix(programaN["show_id"], programaN["type"], programaN["title"],
                  programaN["director"], programaN["cast"], programaN["country"], programaN["date_added"], programaN["release_year"], 
                  programaN["rating"], programaN["duration"], 
                  programaN["listed_in"], programaN["description"])
    lt.addLast(catalog["Netflix"], n)   
    lt.addLast(catalog["Total"], n)
    generos=n["listed_in"]
    actores= n["cast"]
    anio= n["release_year"]
    countries = n["country"]
    directors = n["director"]
    if n["date_added"] != "":
        date= time.strptime(n["date_added"],"%B %d, %Y")
    else:
        date = None
    for genero in generos:
        gen=genero.strip()
        AddGenero(catalog,gen, n)
    for actor in actores:
        AddActor(catalog,actor, n)
    if n["type"]=="Movie":
        AddYear(catalog, anio, n)
    elif n["type"]=="TV Show":
        AddDate(catalog, date, n)
    for country in countries:
        country = country.strip()
        AddCountry(catalog,country, n)
    for director in directors:
        director = director.strip()
        AddDirector(catalog,director,n)
        
    return catalog

def AddGenero(catalog, genero, show):
    geners = catalog['Generos']
    if mp.contains(geners,genero) == False:
        list = lt.newList("ARRAY_LIST")
        mp.put(geners, genero, list)
    act = me.getValue(mp.get(geners, genero))
    lt.addLast(act, show)
    return catalog

def AddActor(catalog, actor, show):
    try:
        actors = catalog['Actores']
        existactor= mp.contains(actors, actor)
        if existactor:
            entry = mp.get(actors, actor)
            act = me.getValue(entry)
        else:
            act = newactor(actor)
            mp.put(actors, actor, act)
        lt.addLast(act['shows'], show)
    except Exception:
        return None

def AddYear(catalog, year, show):
    try:
        years = catalog['Years']
        existyear = mp.contains(years, year)
        if existyear:
            entry = mp.get(years, year)
            anio = me.getValue(entry)
        else:
            anio = newyear(year)
            mp.put(years, year, anio)
        lt.addLast(anio['shows'], show)
    except Exception:
        return None

def AddDate(catalog, date, show):
    try:
        dates = catalog['Dates']
        existdate = mp.contains(dates, date)
        if existdate:
            entry = mp.get(dates, date)
            dat = me.getValue(entry)
        else:
            dat = newdate(date)
            mp.put(dates, date, dat)
        lt.addLast(dat['shows'], show)
    except Exception:
        return None

def AddCountry(catalog, country, show):
    countries = catalog['Country']
    existactor= mp.contains(countries, country)
    if existactor == False:
        list = lt.newList("ARRAY_LIST")
        mp.put(countries, country, list)
    act = me.getValue(mp.get(countries, country))
    lt.addLast(act, show)
    return catalog
def AddDirector(catalog,director,show):
    directors = catalog["Directors"]
    existdirector = mp.contains(directors,director)
    if existdirector == False:
        list = lt.newList("ARRAY_LIST")
        mp.put(directors, director, list)
    act = me.getValue(mp.get(directors, director))
    lt.addLast(act,show)
#Funciones para la creación de datos

def newAmazon(show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
    
    Amazon = {
        "show_id": "",
        "type": "",
        "title": "",
        "director": list,
        "cast": list,
        "country": list,
        "date_added":"",
        "release_year": int,
        "rating": "",
        "duration": int,
        "duracionstr":str,
        "listed_in": list,
        "description":"",
        "stream_service": "Amazon"
    }
    Amazon["show_id"] = show_id
    Amazon["type"] = type
    Amazon["title"] = str(title)
    Amazon["director"] = director.split(",")
    Amazon["cast"] = cast.split(", ")
    Amazon["country"] = country.split(",")
    Amazon["date_added"] = str(date_added)
    Amazon["release_year"] = int(release_year)
    Amazon["rating"] = rating
    Amazon["duration"] =duration.split(" ")[0]
    Amazon["duracionstr"]=duration
    #generos=listed_in.replace(" & ",", ")
    Amazon["listed_in"] =listed_in.split(", ")

    Amazon["description"] = description


    return Amazon


def newDisney(show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
    
    Disney = {
        "show_id": "",
        "type": "",
        "title": "",
        "director": list,
        "cast": list,
        "country": list,
        "date_added":"",
        "release_year": int,
        "rating": "",
        "duration": int,
        "duracionstr":str,
        "listed_in": list,
        "description":"",
        "stream_service": "Disney plus"
    }
    Disney["show_id"] = show_id
    Disney["type"] = type
    Disney["title"] = str(title)
    Disney["director"] = director.split(",")
    Disney["cast"] = cast.split(", ")
    Disney["country"] = country.split(",")
    Disney["date_added"] = str(date_added)
    Disney["release_year"] = int(release_year)
    Disney["rating"] = rating
    Disney["duration"] = duration.split(" ")[0]
    Disney["duracionstr"]=duration
    #generos=listed_in.replace(" & ",", ")
    Disney["listed_in"] =listed_in.split(", ")
    Disney["description"] = description
    return Disney



def newHulu(show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
    
    Hulu = {
        "show_id": "",
        "type": "",
        "title": "",
        "director": list,
        "cast": list,
        "country": list,
        "date_added":"",
        "release_year": int,
        "rating": "",
        "duration": int,
        "duracionstr":str,
        "listed_in": list,
        "description":"",
        "stream_service":"Hulu"
    }
    Hulu["show_id"] = show_id
    Hulu["type"] = type
    Hulu["title"] = str(title)
    Hulu["director"] = director.split(",")
    Hulu["cast"] = cast.split(", ")
    Hulu["country"] = country.split(",")
    Hulu["date_added"] = str(date_added)
    Hulu["release_year"] = int(release_year)
    Hulu["rating"] = rating
    Hulu["duration"] = duration.split(" ")[0]
    Hulu["duracionstr"]=duration
    #generos=listed_in.replace(" & ",", ")
    Hulu["listed_in"] =listed_in.split(", ")
    Hulu["description"] = description
    return Hulu


def newNetflix(show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description):
    
    Netflix = {
        "show_id": "",
        "type": "",
        "title": "",
        "director": list,
        "cast": list,
        "country": list,
        "date_added":"",
        "release_year": int,
        "rating": "",
        "duration": int,
        "duracionstr":str,
        "listed_in": list,
        "description":"",
        "stream_service": "Netflix"
    }
    Netflix["show_id"] = show_id
    Netflix["type"] = type
    Netflix["title"] = str(title)
    Netflix["director"] = director.split(",")
    Netflix["cast"] = cast.split(", ")
    Netflix["country"] = country.split(",")
    Netflix["date_added"] = str(date_added)
    Netflix["release_year"] = int(release_year)
    Netflix["rating"] = rating
    Netflix["duration"] = duration.split(" ")[0]
    Netflix["duracionstr"]=duration
    #generos=listed_in.replace(" & ",", ")
    Netflix["listed_in"] =listed_in.split(", ")
    Netflix["description"] = description


    return Netflix

def newGenero(genero):
    """
    Esta funcion crea la estructura de shows asociados
    a un género.
    """
    entry = {'genero': "", "shows": None}
    entry['genero'] = genero
    entry['shows'] = lt.newList('ARRAY_LIST')
    return entry

def newactor(actor):
    """
    Esta funcion crea la estructura de shows asociados
    a un actor.
    """
    entry = {'actor': "", "shows": None}
    entry['actor'] = actor
    entry['shows'] = lt.newList('ARRAY_LIST')
    return entry

def newyear(year):
    """
    Esta funcion crea la estructura de shows asociados
    a un anio.
    """
    entry = {'year': "", "shows": None}
    entry['year'] = str(year)
    entry['shows'] = lt.newList('ARRAY_LIST')
    return entry

def newdate(date):
    """
    Esta funcion crea la estructura de shows asociados
    a una fecha.
    """
    entry = {'date': "", "shows": None}
    entry['date'] = str(date)
    entry['shows'] = lt.newList('ARRAY_LIST')
    return entry

def newcountry(country):
    """
    Esta funcion crea la estructura de shows asociados
    a un actor.
    """
    entry = {'country': "", "shows": None}
    entry['country'] = country
    entry['shows'] = lt.newList('ARRAY_LIST')
    return entry

#Funciones de consulta
def AmazonSize(catalog) -> int:
    return lt.size(catalog["Amazon"])

def DisneySize(catalog) -> int:
    return lt.size(catalog["Disney"])

def HuluSize(catalog) -> int:
    return lt.size(catalog["Hulu"])

def NetflixSize(catalog) -> int:
    return lt.size(catalog["Netflix"])

def TotalSize(catalog)->int:
    return lt.size(catalog["Total"])

def GenerosSize(catalog):
    return lt.size(mp.keySet(catalog["Generos"]))

def ActoresSize(catalog):
    return lt.size(mp.keySet(catalog["Actores"]))

def YearSize(catalog):
    return lt.size(mp.keySet(catalog["Years"]))

def DatesSize(catalog):
    return lt.size(mp.keySet(catalog["Dates"]))

def CountrySize(catalog):
    return lt.size(mp.keySet(catalog["Country"]))




#Funciones de comparación
def cmpMoviesByReleaseYear(movie1,movie2):
    
    if movie1["release_year"]>movie2["release_year"]:
        return True
    elif movie1["release_year"]<movie2["release_year"]:
        return False
    else:
        if movie1["title"].lower()<movie2["title"].lower():
            return True
        elif movie1["title"].lower()>movie2["title"].lower():
            return False
        else:
            if movie1["duration"]<movie2["duration"]:
                return True
            elif movie1["duration"]>movie2["duration"]:
                return False
            else:
                return False

def cmpShowsbyaniotitle(movie1, movie2):
    if movie1["release_year"]>movie2["release_year"]:
        return True
    elif movie1["release_year"]<movie2["release_year"]:
        return False
    else:
        if movie1["title"].lower()<movie2["title"].lower():
            return True
        elif movie1["title"].lower()>movie2["title"].lower():
            return False
        else:
            return False

def cmpshowsbycantidad(show1, show2):
    return show1["cantidad"]>show2["cantidad"]

def cmpMoviesByTitle(movie1,movie2):
    if movie1["title"].lower()<movie2["title"].lower():
            return True
    elif movie1["title"].lower()>movie2["title"].lower():
            return False
    else:
        if movie1["release_year"]>movie2["release_year"]:
            return True
        elif movie1["release_year"]<movie2["release_year"]:
            return False
        else:
            if movie1["duration"]<movie2["duration"]:
                return True
            elif movie1["duration"]>movie2["duration"]:
                return False
            else:
                return False

def cmpMoviesByanio(movie1,movie2):
    if movie1["title"].lower()<movie2["title"].lower():
        return True
    elif movie1["title"].lower()>movie2["title"].lower():
        return False
    else:
        if movie1["duration"]<movie2["duration"]:
            return True
        elif movie1["duration"]>movie2["duration"]:
            return False
        else:
            return False

def cmpreq2(title1,title2):
    if time.strptime( title1["date_added"],"%Y-%m-%d") >= time.strptime( title2["date_added"],"%Y-%m-%d"):
        return True
    elif time.strptime( title1["date_added"],"%Y-%m-%d") == time.strptime( title2["date_added"],"%Y-%m-%d"):
        if title1["title"] < title2["title"]:
            return True
        elif title1["title"] == title2["title"]:
            if title1["duration"] < title2["duration"]:
                return True
    else:
        return False

def cmpreq4(title1,title2):
    
    if title1["release_year"] > title2["release_year"]:
        return True
    elif title1["release_year"] == title2["release_year"]:
        if title1["title"].lower() < title2["title"].lower():
            return True
        elif title1["title"].lower() == title2["title"].lower():
            if int(title1["duration"]) < int(title2["duration"]):
                return True
    else:
        return False


def cmpreq5(title1,title2):
    
    if title1["release_year"] > title2["release_year"]:
        return True
    elif title1["release_year"] == title2["release_year"]:
        if title1["title"].lower() < title2["title"].lower():
            return True
        elif title1["title"].lower() == title2["title"].lower():
            if int(title1["duration"]) < int(title2["duration"]):
                return True
    else:
        return False

def cmpeq6(title1,title2):
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
def cmpreq7(title1,title2):
    if lt.size(title1["titles"]) > lt.size(title2["titles"]):
        return True
    else:
        False
def comparegeneros(gen, gener):
    g = me.getKey(gener)
    if (str(gen).lower() == str(g).lower()):
        return 0
    elif (str(gen).lower() > str(g).lower()):
        return 1
    else:
        return -1

def compareactores(act, actor):
    a = me.getKey(actor)
    if (str(act).lower() == str(a).lower()):
        return 0
    elif (str(act).lower() > str(a).lower()):
        return 1
    else:
        return -1

def compareanios(anio, year):
    y = me.getKey(year)
    if (int(anio)== int(y)):
        return 0
    elif (int(anio) > int(y)):
        return 1
    else:
        return -1

def comparedates(dat, date):
    d= me.getKey(date)
    if (dat == d):
        return 0
    elif (dat > d):
        return 1
    else:
        return -1

def comparecountry(p, c):
    c = me.getKey(c)
    if c == p:
        return 0
    elif p > c:
        return 1
    else:
        return -1


#Funciones de consulta

# REQUERIMIENTO 1
def peliculasbyanio(catalog, anio):
    pelispresent=lt.newList("ARRAY_LIST")
    NoPeliculaspresentes= 0
    exist=mp.contains(catalog["Years"], anio)
    if exist:
        year=mp.get(catalog["Years"], anio)
        shows_year= me.getValue(year)["shows"]
        NoPeliculaspresentes=lt.size(shows_year)
        pelispresent= sortPeliculasbyanio(shows_year)
    return NoPeliculaspresentes, pelispresent

# REQUERIMIENTO 2
def Show_by_time(catalog,date1):
    date1 = time.strptime(date1,"%B %d, %Y")
    list1 = lt.newList("ARRAY_LIST")
    exist=mp.contains(catalog["Dates"], date1)
    if exist:
        date=mp.get(catalog["Dates"], date1)
        shows_date= me.getValue(date)["shows"]
        list1= sortPeliculasbyanio(shows_date)
    return list1


# REQUERIMIENTO 3
def Shows_by_Actor(catalog, actor_name):
    shows_act= lt.newList("ARRAY_LIST")
    Num_peliculas= 0
    Num_programas= 0
    exist=mp.contains(catalog["Actores"], actor_name)
    if exist:
        actor=mp.get(catalog["Actores"], actor_name)
        shows_actor= me.getValue(actor)["shows"]
        for show in lt.iterator(shows_actor):
            if show["type"]=="Movie":
                Num_peliculas+=1
            else:
                Num_programas+=1
        shows_act= sortShowsbyTitle(shows_actor)
    return shows_act, Num_peliculas, Num_programas

# REQUERIMIENTO 4
def ContentbyGenero(catalog,genero):
    """
    Filtra el contenido por shows y peliculas que sean sobre un genero en especifico.
    """

    genContent= lt.newList("ARRAY_LIST")
    peliculas= 0
    shows= 0
    exist=mp.contains(catalog["Generos"], genero)
    if exist:
        g=mp.get(catalog["Generos"], genero)
        shows_generos= me.getValue(g)
        for show in lt.iterator(shows_generos):
            if show["type"]=="Movie":
                peliculas +=1
            else:
                shows +=1
        genContent= SortGeneros(shows_generos)
    return genContent, peliculas, shows

# REQUERIMIENTO 5

def MoviesByCountry(catalog,country):
    """
    Filtra el contenido por shows y peliculas del mismo pais que el ingresado por parametro.
    """
    country_list= lt.newList("ARRAY_LIST")
    movies= 0
    tv_show= 0
    exist=mp.contains(catalog["Country"], country)
    if exist:
        c=mp.get(catalog["Country"], country)
        shows_country= me.getValue(c)
        for show in lt.iterator(shows_country):
            if show["type"]=="Movie":
                movies +=1
            else:
                tv_show +=1
        country_list= SortCountry(shows_country)
    return country_list, movies, tv_show
    

# REQUERIMIENTO 6
def Shows_by_director(catalog, director_name):
    director_map = catalog["Directors"]
    type_dict = {}
    service_dict = {}
    listed_in_dict = {}
    titles_list = lt.newList()
    exist = mp.contains(director_map, director_name)
    if exist:
        titles_list = me.getValue(mp.get(director_map,director_name))
        for i in lt.iterator(titles_list):
            if i["type"] not in type_dict:
                type_dict[i["type"]] = 1
            else:
                type_dict[i["type"]] += 1
            if i["stream_service"] not in service_dict:
                service_dict[i["stream_service"]] = {"Movie":0,"TV Show":0}
            service_dict[i["stream_service"]][i["type"]] += 1
            for e in i["listed_in"]:
                if e not in listed_in_dict:
                    listed_in_dict[e] = 1
                else:
                    listed_in_dict[e] += 1
        sortShowsbydirector(titles_list)
    return titles_list,type_dict,service_dict,listed_in_dict

# REQUERIMIENTO 7
def TOP_genero(catalog,N):
    list = lt.newList("ARRAY_LIST")
    keys = mp.keySet(catalog["Generos"])
    for i in lt.iterator(keys):
        lt.addLast(list,{"genre":i,"titles":me.getValue(mp.get(catalog["Generos"],i))})
    mer.sort(list,cmpreq7)
    sublist = lt.subList(list,1,N)
    for a in lt.iterator(sublist):
        Movie = 0
        shows = 0
        amazon = 0
        netflix = 0
        hulu = 0
        disney = 0
        for i in lt.iterator(a["titles"]):
            if i["type"] == "Movie":
                Movie += 1
            else:
                shows += 1
            if i["stream_service"] == "Hulu":
                hulu += 1
            elif i["stream_service"] == "Disney plus":
                disney += 1
            elif i["stream_service"] == "Netflix":
                netflix += 1
            else:
                amazon += 1
        a["count"] = (Movie,shows,amazon,netflix,hulu,disney)
    return sublist
   
#Funciones de ordenamiento
def sortShowsbyReleaseyear(lista):
    return mer.sort(lista, cmpShowsbyaniotitle)

def sortPeliculasbyperiodo(lista):
    return mer.sort(lista, cmpMoviesByReleaseYear)

def sortPeliculasbyanio(lista):
    return mer.sort(lista, cmpMoviesByanio)

def sortShowsbydirector(lista):
    return mer.sort(lista, cmpMoviesByReleaseYear)

def sortgenerosbycantidad(lista):
    return mer.sort(lista, cmpshowsbycantidad)

def sortShowsbyTitle(catalog):
    #Ordena los albumes por fecha de lanzamiento
    return mer.sort(catalog, cmpMoviesByReleaseYear)

def sortShowsbydateaded(lista):
    return  mer.sort(lista,cmpreq2)

def SortCountry(lista):
    return  mer.sort(lista,cmpreq5)

def SortGeneros(lista):
    return mer.sort(lista,cmpreq4)



# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
