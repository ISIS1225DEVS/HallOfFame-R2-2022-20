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
from DISClib.Algorithms.Sorting import mergesort as m
import datetime as dt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """
    Inicializa el catálogo general que guarda todos los elementos en todas las plataformas. 
    Una lista que contenga todas las películas, otra que contenga todos los tv shows, y una por cada plataforma.
    """
    catalog = {'content': None,
               'Movies': None,
               'TV-shows': None,
               "generos": None, 
               "date_added": None,
               "release_year": None,
               "cast":None,
               "country":None,
               "director":None,
               'Netflix': None,
               'Hulu': None,
               'Amazon Prime': None,
               'Disney Plus': None
               }

    """
    Estas listas contienen todos los contenidos encontrados en 
    los archivos de carga. No están ordenados por ningun criterio. 
    Son referenciados por los indices creados a continuacion.
    """
    catalog["content"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    catalog["Movies"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    catalog["TV-shows"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    catalog["Netflix"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    catalog["Hulu"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    catalog["Amazon Prime"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    catalog["Disney Plus"]=lt.newList("ARRAY_LIST",cmpfunction=cmpByReleaseYear)
    """
    A continuacion se crean índices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """
    catalog["generos"] = mp.newMap(120,maptype="PROBING", loadfactor=0.5)
    catalog["date_added"] = mp.newMap(22000, maptype="PROBING", loadfactor=0.5,comparefunction=compareMap)
    catalog["release_year"] = mp.newMap(22000, maptype="PROBING",loadfactor= 0.5,comparefunction=compareMap)
    catalog["cast"] = mp.newMap(22000,maptype= "PROBING", loadfactor=0.5)
    catalog["country"] = mp.newMap(195,maptype= "PROBING",loadfactor= 0.5)
    catalog["director"] = mp.newMap(22000, maptype="PROBING", loadfactor=0.5)
    
    return catalog

# Agregar al catálogo
def addElement(catalog,element):
    """
    Agrega un elemento a la lista de todo el contenido y 
    a su lista correspondiente dependiendo de si es película o show.
    Además se agrega en el map de todas las otras categorías que se tienen crenado un link
    entre la película y sus valores asociados
    """
    lt.addLast(catalog["content"],element)
    if element["type"]=="Movie":
        lt.addLast(catalog["Movies"],element)
    else:
        lt.addLast(catalog["TV-shows"],element)
    genres = element["listed_in"].split(",")
    cast = element["cast"].split(",")
    countries = element["country"].split(",")
    directors = element["director"].split(",")
    for genre in genres:
        addgenre(catalog,genre.strip(),element)
    for country in countries:
        addcountry(catalog,country.strip(),element)
    for actor in cast:
        addactor(catalog,actor.strip(),element)
    for director in directors:
        adddirector(catalog,director.strip(),element)
    addyeardded(catalog,element)
    addyearestrenado(catalog,element)
    
    return catalog

# Crear elementos
def newgenre(genero):
    genre={"genero": None,
            "elements":None}
    genre["genero"]=genero
    genre["elements"]=lt.newList("ARRAY_LIST")
    return genre

def newyear(año):
    year={"year":None,"elements":None}
    year["year"]=año
    year["elements"]=lt.newList("ARRAY_LIST")
    return year

def newactor(actor):
    cast={"actor":None,"elements":None}
    cast["actor"]=actor
    cast["elements"]=lt.newList("ARRAY_LIST")
    return cast

def newcountry(pais):
    country={"country":None,"elements":None}
    country["country"]=pais
    country["elements"]=lt.newList("ARRAY_LIST")
    return country

def newdirector(director):
    dir={"director":None,"elements":None}
    dir["director"]=director
    dir["elements"]=lt.newList("ARRAY_LIST")
    return dir

# Agregar elementos
def addElement_Platform(catalog,element,platform):
    """
    Agrega un elemento a la lista de su plataforma correspondiente.
    """
    lt.addLast(catalog[platform],element) 
    return catalog

def addgenre(catalog,genre,element):
    genres = catalog["generos"]
    if mp.contains(genres,genre):
        entry = mp.get(genres,genre)
        genero = me.getValue(entry)
    else:
        genero=newgenre(genre)
        mp.put(genres,genre,genero)
    lt.addLast(genero["elements"],element)
    return None 

def addyeardded(catalog,element):
    years=catalog["date_added"]
    if element["type"]=="TV Show":
        if element["date_added"]!="":
            addyear=element["date_added"]
            if mp.contains(years,addyear):
                entry=mp.get(years,addyear)
                year=me.getValue(entry)
            else:
                year=newyear(addyear)
                mp.put(years,addyear,year)
            lt.addLast(year["elements"],element)
    return None

def addyearestrenado(catalog,element):
    years=catalog["release_year"]
    if element["type"]=="Movie":
        if element["release_year"]!="":
            relyear=element["release_year"]
        else:
            relyear=2020
        if mp.contains(years,relyear):
            entry=mp.get(years,relyear)
            year=me.getValue(entry)
        else:
            year=newyear(relyear)
            mp.put(years,relyear,year)
        lt.addLast(year["elements"],element)
    return None

def addcountry(catalog,country,element):
    countries = catalog["country"]
    if mp.contains(countries,country):
        entry = mp.get(countries,country)
        pais = me.getValue(entry)
    else:
        pais=newgenre(country)
        mp.put(countries,country,pais)
    lt.addLast(pais["elements"],element)
    return None 

def addactor(catalog,actor,element):
    cast = catalog["cast"]
    if mp.contains(cast,actor):
        entry = mp.get(cast,actor)
        act = me.getValue(entry)
    else:
        act=newgenre(actor)
        mp.put(cast,actor,act)
    lt.addLast(act["elements"],element)
    return None 

def adddirector(catalog,director,element):
    directors = catalog["director"]
    if mp.contains(directors,director):
        entry = mp.get(directors,director)
        dir = me.getValue(entry)
    else:
        dir=newgenre(director)
        mp.put(directors,director,dir)
    lt.addLast(dir["elements"],element)
    return None 

# Funciones por requerimiento

# TODO: Requerimientos 1 y 2
def findyear(catalog,Year):
    map = catalog["release_year"]
    if mp.contains(map , Year):
        entry = mp.get(map, Year)
        value = me.getValue(entry)                                  
        return mergesort(value["elements"], cmpByTRD)
    else: 
        return ("No hay peliculas estrenadas ese año")

def finddate(catalog,Date):
    map = catalog["date_added"]
    if mp.contains(map , Date):
        entry = mp.get(map, Date)
        value = me.getValue(entry)
        return mergesort(value["elements"], cmpByTRD)
    else: 
        return ("No hay TV SHOWS estrenados ese año")

#Función general: Requerimientos 3, 4, 5 y 6.

def find_by(catalog, Name, criteria):
    """
    Retorna los títulos con las características solicitadas por usuario,
    puede ser por actor, género, país de producción, director.

    Args:
        catalog: El diccionario del catálogo general con la información de los títulos.
        Name: String que el controller recibió para comparar con las llaves del índice de interés.
        criteria: Índice del catálogo en el que se está buscando.
    Returns:
        Los contenidos con los detalles que busca el usuario, junto al tamaño de la lista.
    """
    map = catalog[criteria]
    if mp.contains(map, Name):
        entry = mp.get(map, Name)
        value = me.getValue(entry)
        return mergesort(value["elements"], cmpByReleaseYear)
    else: 
        return None


def findDirector():
    pass
   

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpByReleaseYear(title1, title2):
    """
    Devuelve verdadero (True) si el release_year de title1 es menor que el
    de title2, en caso de que sean iguales tenga en cuenta el titulo y en caso de que
    ambos criterios sean iguales tenga en cuenta la duración, de lo contrario devuelva
    falso (False).
    Args:
    title1: informacion de la primera pelicula que incluye sus valores 'release_year',
    'title' y 'duration'
    title2: informacion de la segunda pelicula que incluye su valor 'release_year',
    'title' y 'duration'
    """
    if int(title1["release_year"])!=int(title2["release_year"]):
        return int(title1["release_year"])>int(title2["release_year"])
    elif title1["title"]!=title2["title"]:
        return title1["title"].lower()>title2["title"].lower()
    else: 
        title1["duration"] = title1["duration"][:len(title1["duration"])-4]
        title2["duration"] = title2["duration"][:len(title2["duration"])-4]
        return title1["duration"]>title2["duration"]

def cmpByTRD(title1, title2):
    """
    Devuelve verdadero (True) si el title de title1 es menor que el
    de title2, en caso de que sean iguales tenga en cuenta el release_year y en caso de que
    ambos criterios sean iguales tenga en cuenta el director, de lo contrario devuelva
    falso (False).
    Args:
    title1: informacion de la primera pelicula que incluye sus valores 'release_year',
    'title' y 'director'
    title2: informacion de la segunda pelicula que incluye su valor 'release_year',
    'title' y 'director'
    """
    if title1["title"]!=title2["title"]:
        return title1["title"].lower()<title2["title"].lower()   
    elif int(title1["release_year"])!=int(title2["release_year"]):
        return int(title1["release_year"])<int(title2["release_year"])
    else: 
        return title1["director"].lower()<title2["director"].lower()
    
def compareMap(year, elem):
    entry = me.getKey(elem)
    if (year == entry):
        return 0
    elif (year > entry):
        return 1
    else:
        return -1


def cmpgenre(genre1, genre2):
    size1 = genre1["elements"]["size"]
    size2 = genre2["elements"]["size"]
    if size1 != size2:
        return size1 > size2


# Ordenmiento de datos

def mergesort(list,cmpfunction):
    """
    Ordena una lista de datos con base en la fecha de lanzamiento 
    por medio del método recursivo de ordenamiento mergesort.
    """
    return m.sort(list,cmpfunction)

# Requerimiento 7

def topngenres(map,n):
    lista = mp.valueSet(map)
    lista = mergesort(lista,cmpgenre)
    top = []
    for i in range(n):
        top.append(lista["elements"][i])
    return top

def count_by (lista, valor, criteria):
    count = 0
    for i in range(lista["size"]):
        element = lista["elements"][i]
        if element[criteria]!="":
            if element[criteria]==valor:
                count+=1
    return count
