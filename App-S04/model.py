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


from sqlite3 import Date
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as se
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(estructura, can_netflix, can_amazon, can_disney, can_hulu):

    catalog = {"netflix": None,
               'amazon': None,
               'disney': None,
               "hulu" : None,
               "program": None,
               'generos': None,
               'directores': None,
               'actores': None,
               'country':None,
               'años':None}

    if estructura == "CHAINING":
        factor_carga = 4
    elif estructura == "PROBING":
        factor_carga = 0.5
    can_total = can_netflix + can_amazon + can_disney + can_hulu

    catalog["program"] = lt.newList("ARRAY_LIST")

    catalog["netflix"] = lt.newList("ARRAY_LIST")

    catalog["amazon"] = lt.newList("ARRAY_LIST")

    catalog["disney"] = lt.newList("ARRAY_LIST")

    catalog["hulu"] = lt.newList("ARRAY_LIST")

    catalog['date_added'] = mp.newMap(200,
                                maptype=estructura,
                                loadfactor=factor_carga)

    catalog['generos'] = mp.newMap(can_disney,
                                maptype=estructura,
                                loadfactor=factor_carga)

    catalog['directores'] = mp.newMap(can_total,
                                maptype=estructura,
                                loadfactor=factor_carga)
    
    catalog['actores'] = mp.newMap(can_total*3,
                                maptype=estructura,
                                loadfactor=factor_carga)
    catalog['country'] = mp.newMap(300,
                                maptype=estructura,
                                loadfactor=factor_carga)
    catalog['anio'] = mp.newMap(200,
                                maptype=estructura,
                                loadfactor=factor_carga)
    return catalog

# Funciones para agregar informacion al catalogo

def addProgram(catalog, program):

    existentes = lt.newList("ARRAY_LIST")
    present = lt.isPresent(existentes, program["show_id"])
    if present == 0:
        lt.addLast(catalog["program"], program)
        lt.addLast(existentes, program["show_id"])

    return catalog

def addNetflix(catalog, program):

    lt.addLast(catalog["netflix"], program)

    return catalog

def addAmazon(catalog, program):

    lt.addLast(catalog["amazon"], program)

    return catalog

def addDisney(catalog, program):

    lt.addLast(catalog["disney"], program)

    return catalog

def addHulu(catalog, program):

    lt.addLast(catalog["hulu"], program)

    return catalog

def addDadeAdded(catalog, program):

    date = program["date_added"]
    if date != "" and program["type"] == "TV Show":
        date_list = date.split(", ")
        anio = date_list[1]
        if mp.contains(catalog["date_added"], anio):
            anterior_tupla = mp.get(catalog["date_added"], anio)
            if anterior_tupla:
                    anterior = me.getValue(anterior_tupla)

            lt.addLast(anterior, program)
            mp.put(catalog['date_added'], anio, anterior)

        else:
            program_list = lt.newList("ARRAY_LIST")
            lt.addLast(program_list, program)

            mp.put(catalog['date_added'], anio, program_list)
        
        return catalog

def addGeneros(catalog, program):
    
    gen_1 = program["listed_in"].split(" & ")
    gen_2 = (", ").join(gen_1)
    generos = gen_2.split(", ")
    
    for genero in generos:
        if mp.contains(catalog["generos"], genero):
            anterior_tupla = mp.get(catalog["generos"], genero)
            if anterior_tupla:
                    anterior = me.getValue(anterior_tupla)

            lt.addLast(anterior, program)
            mp.put(catalog['generos'], genero, anterior)

        else:
            program_list = lt.newList("ARRAY_LIST")
            lt.addLast(program_list, program)

            mp.put(catalog['generos'], genero, program_list)

    return catalog

def addDirectores(catalog, program):

    director = program["director"]
    if mp.contains(catalog["directores"], director):
        anterior_tupla = mp.get(catalog["directores"], director)
        if anterior_tupla:
                anterior = me.getValue(anterior_tupla)

        lt.addLast(anterior, program)
        mp.put(catalog['directores'], director, anterior)

    else:
        program_list = lt.newList("ARRAY_LIST")
        lt.addLast(program_list, program)

        mp.put(catalog['directores'], director, program_list)
    
    return catalog

def addActores(catalog, program):
    
    actores = program["cast"].split(", ")
    
    for actor in actores:
        if mp.contains(catalog["actores"], actor):
            anterior_tupla = mp.get(catalog["actores"], actor)
            if anterior_tupla:
                    anterior = me.getValue(anterior_tupla)
            lt.addLast(anterior, program)
            mp.put(catalog['actores'], actor, anterior)

        else:
            program_list = lt.newList("ARRAY_LIST")
            lt.addLast(program_list, program)

            mp.put(catalog['actores'], actor, program_list)
        
    return catalog

def addPaises(catalog, program):

    Paises = program["country"]
    if mp.contains(catalog["country"], Paises):
        last_tp = mp.get(catalog["country"], Paises)
        if last_tp:
                l = me.getValue(last_tp)

        lt.addLast(l, program)
        mp.put(catalog['country'], Paises, l)

    else:
        program_list = lt.newList("ARRAY_LIST")
        lt.addLast(program_list, program)

        mp.put(catalog['country'], Paises, program_list)
    
    return catalog

def addAnios (catalog, program):
    
    anio = program["release_year"]
    if program["type"] == "Movie":
        if mp.contains(catalog["anio"], anio):
            anterior_tupla = mp.get(catalog["anio"], anio)
            if anterior_tupla:
                    anterior = me.getValue(anterior_tupla)

            lt.addLast(anterior, program)
            mp.put(catalog['anio'], anio, anterior)

        else:
            program_list = lt.newList("ARRAY_LIST")
            lt.addLast(program_list, program)

            mp.put(catalog['anio'], anio, program_list)
    
    return catalog

# Funciones para creacion de datos

# Funciones de consulta

def cargar_datos(catalog):

    sorted_list_netflix = ordenamiento(catalog["netflix"], compareYearTittle)
    pos_final_neflix = catalog["netflix"]["size"] - 2
    first_netflix = lt.subList(sorted_list_netflix, 1, 3)
    last_netflix = lt.subList(sorted_list_netflix, pos_final_neflix, 3)

    sorted_list_amazon = ordenamiento(catalog["amazon"], compareYearTittle)
    pos_final_amazon = catalog["amazon"]["size"] - 2
    first_amazon = lt.subList(sorted_list_amazon, 1, 3)
    last_amazon = lt.subList(sorted_list_amazon, pos_final_amazon, 3)

    sorted_list_disney = ordenamiento(catalog["disney"], compareYearTittle)
    pos_final_disney = catalog["disney"]["size"] - 2
    first_disney = lt.subList(sorted_list_disney, 1, 3)
    last_disney = lt.subList(sorted_list_disney, pos_final_disney, 3)

    sorted_list_hulu = ordenamiento(catalog["hulu"], compareYearTittle)
    pos_final_hulu = catalog["hulu"]["size"] - 2
    first_hulu = lt.subList(sorted_list_hulu, 1, 3)
    last_hulu = lt.subList(sorted_list_hulu, pos_final_hulu, 3)

    resultado_netflix = lt.newList("ARRAY_LIST")
    resultado_amazon = lt.newList("ARRAY_LIST")
    resultado_disney = lt.newList("ARRAY_LIST")
    resultado_hulu = lt.newList("ARRAY_LIST")

    print(last_netflix)
    i = 0
    j = 0
    while i < 6:
        if i < 3:
            lt.addLast(resultado_netflix, first_netflix["elements"][i])
            lt.addLast(resultado_amazon, first_amazon["elements"][i])
            lt.addLast(resultado_disney, first_disney["elements"][i])
            lt.addLast(resultado_hulu, first_hulu["elements"][i])
            
            
        elif i >= 3:
            lt.addLast(resultado_netflix, last_netflix["elements"][j])
            lt.addLast(resultado_amazon, last_amazon["elements"][j])
            lt.addLast(resultado_disney, last_disney["elements"][j])
            lt.addLast(resultado_hulu, last_hulu["elements"][j])
            j += 1
        i += 1

    return catalog["program"], resultado_netflix, resultado_amazon, resultado_disney, resultado_hulu


def req_1 (catalog, anio):

    date = mp.get(catalog["anio"], anio)
    if date:
        program_list = me.getValue(date)

    sorted_list = ordenamiento(program_list, compareTittleDuration)

    resultado = lt.newList("ARRAY_LIST")
    
    if sorted_list["size"] < 7:
        for program in lt.iterator(sorted_list):
            
            prom = {"title": program["title"],
                        "duration": program["duration"],
                        "stream_service": program["stream_service"],
                        "director": program["director"],
                        "cast": program["cast"]}
            lt.addLast(resultado, prom)

    else:
        pos_final = sorted_list["size"] - 2
        first = lt.subList(sorted_list, 1, 3)  
        last = lt.subList(sorted_list, pos_final, 3)

        i = 0
        j = 0
        while i < 6:
            if i < 3:
                add = first["elements"][i]
                prom = {"release_year": add["release_year"],
                        "title": add["title"],
                        "duration": add["duration"],
                        "stream_service": add["stream_service"],
                        "director": add["director"],
                        "cast": add["cast"]}
                lt.addLast(resultado, prom)
                
            elif i >= 3: 
                add = last["elements"][j]
                prom = {"title": add["title"],
                        "duration": add["duration"],
                        "stream_service": add["stream_service"],
                        "director": add["director"],
                        "cast": add["cast"]}
                lt.addLast(resultado, prom)
                j += 1
            i += 1

    cantidad = sorted_list["size"]

    return resultado, cantidad

def req_2 (catalog, anio):

    date = mp.get(catalog["date_added"], anio)
    if date:
        program_list = me.getValue(date)

    sorted_list = ordenamiento(program_list, compareTittleDuration)

    resultado = lt.newList("ARRAY_LIST")
    
    if sorted_list["size"] < 7:
        for program in lt.iterator(sorted_list):
            
            prom = {"title": program["title"],
                        "duration": program["duration"],
                        "stream_service": program["stream_service"],
                        "director": program["director"],
                        "cast": program["cast"]}
            lt.addLast(resultado, prom)

    else:
        pos_final = sorted_list["size"] - 2
        first = lt.subList(sorted_list, 1, 3)  
        last = lt.subList(sorted_list, pos_final, 3)

        i = 0
        j = 0
        while i < 6:
            if i < 3:
                add = first["elements"][i]
                prom = {"title": add["title"],
                        "duration": add["duration"],
                        "stream_service": add["stream_service"],
                        "director": add["director"],
                        "cast": add["cast"]}
                lt.addLast(resultado, prom)
                
            elif i >= 3: 
                add = last["elements"][j]
                prom = {"title": add["title"],
                        "duration": add["duration"],
                        "stream_service": add["stream_service"],
                        "director": add["director"],
                        "cast": add["cast"]}
                lt.addLast(resultado, prom)
                j += 1
            i += 1

    cantidad = sorted_list["size"]

    return resultado, cantidad

def req_3(catalog,Actor):

    Actores = mp.get(catalog["actores"],Actor)
    if Actores:
        program_list=me.getValue(Actores)

    sorted_list = ordenamiento(program_list, compareYearTittleDuration)
    if sorted_list["size"]<7:
        resultado= sorted_list
    else:
        pos_final = sorted_list["size"] - 2
        first = lt.subList(sorted_list, 1, 3)  #cambio de 1 ,3 a 0,2
        last = lt.subList(sorted_list, pos_final, 3)

        resultado = lt.newList("ARRAY_LIST")
        i = 0
        j = 0
        while i < 6:
            if i < 3:
                lt.addLast(resultado, first["elements"][i])
                
            elif i >= 3: 
                lt.addLast(resultado, last["elements"][j])
                j += 1
            i += 1
    
    can_movie = 0
    can_tv = 0
    for valor in sorted_list["elements"]:
        if valor["type"] == "Movie":
            can_movie += 1
        elif valor["type"] == "TV Show":
            can_tv += 1

    return resultado, can_movie, can_tv, sorted_list

def req_4(catalog, genero):

    generos = mp.get(catalog["generos"], genero)
    if generos:
        program_list = me.getValue(generos)

    sorted_list = ordenamiento(program_list, compareYearTittleDuration)

    if sorted_list["size"] < 7:
        resultado = sorted_list
    else:
        pos_final = sorted_list["size"] - 2
        first = lt.subList(sorted_list, 1, 3)
        last = lt.subList(sorted_list, pos_final, 3)

        resultado = lt.newList("ARRAY_LIST")
        i = 0
        j = 0
        while i < 6:
            if i < 3:
                lt.addLast(resultado, first["elements"][i])
                
            elif i >= 3: 
                lt.addLast(resultado, last["elements"][j])
                j += 1
            i += 1
    
    can_movie = 0
    can_tv = 0
    for valor in sorted_list["elements"]:
        if valor["type"] == "Movie":
            can_movie += 1
        elif valor["type"] == "TV Show":
            can_tv += 1

    return resultado, can_movie, can_tv, sorted_list

def req_5(catalog, pais):

    Paises = mp.get(catalog["country"], pais)
    if Paises:
        program_list = me.getValue(Paises)

    sorted_list = ordenamiento(program_list, compareYearTittleDuration)

    if sorted_list["size"] < 7:
        resultado = sorted_list
    else:
        pos_final = sorted_list["size"] - 2
        first = lt.subList(sorted_list, 1, 3)
        last = lt.subList(sorted_list, pos_final, 3)

        resultado = lt.newList("ARRAY_LIST")
        i = 0
        j = 0
        while i < 6:
            if i < 3:
                lt.addLast(resultado, first["elements"][i])
                
            elif i >= 3: 
                lt.addLast(resultado, last["elements"][j])
                j += 1
            i += 1
    
    can_movie = 0
    can_tv = 0
    for valor in sorted_list["elements"]:
        if valor["type"] == "Movie":
            can_movie += 1
        elif valor["type"] == "TV Show":
            can_tv += 1

    return resultado, can_movie, can_tv, sorted_list

def req_6(catalog, director):

    directores = mp.get(catalog["directores"], director)
    if directores:
        program_list = me.getValue(directores)

    sorted_list = ordenamiento(program_list, compareYearTittleDuration)

    resultado = lt.newList("ARRAY_LIST")
    
    if sorted_list["size"] <= 6:
        resultado = sorted_list
    else:
        pos_final = sorted_list["size"] - 2
        first = lt.subList(sorted_list, 1, 3)
        last = lt.subList(sorted_list, pos_final, 3)
         
        i = 0
        j = 0
        while i < 6:
            if i < 3:
                lt.addLast(resultado, first["elements"][i])
                
            elif i >= 3:
                lt.addLast(resultado, last["elements"][j])
                j += 1
            i += 1
    
    can_movie = 0
    can_tv = 0
    can_streams = {"netflix": 0, "amazon": 0, "disney": 0, "hulu": 0}
    can_generos = {}
    for valor in sorted_list["elements"]:
        if valor["type"] == "Movie":
            can_movie += 1
        elif valor["type"] == "TV Show":
            can_tv += 1
        
        can_streams[valor["stream_service"]] += 1

        gen_1 = valor["listed_in"].split(" & ")
        gen_2 = (", ").join(gen_1)
        generos = gen_2.split(", ")
        for genero in generos:
            if genero in can_generos:
                can_generos[genero] += 1
            else:
                can_generos[genero] = 1


    return resultado, can_movie, can_tv, can_streams, can_generos

def req_7(catalog, rank):

    lista_generos = mp.keySet(catalog["generos"])
    lista_generos_total = lt.newList("ARRAY_LIST")
    geners = {}
    for genero in lt.iterator(lista_generos): 
            tupla_generos = mp.get(catalog["generos"], genero)
            if tupla_generos:
                lista_generos = me.getValue(tupla_generos)
                lt.addLast(lista_generos, genero)
                lt.addLast(lista_generos_total, lista_generos["elements"])

    sorted_list = ordenamiento(lista_generos_total, compareCantidadNombre)
    resultado = lt.subList(sorted_list, 1, rank)

    for generos in lt.iterator(resultado):
        nom = generos[-1]
        list_cantidad = {"TV Show": 0, "Movie": 0}
        list_streams = {"netflix": 0, "amazon": 0, "disney": 0, "hulu": 0}
        geners[nom]={"cantidad":0, "list_cantidad":list_cantidad, "list_streams":list_streams}

        size = len(generos)-1
        geners[nom]["cantidad"] = len(generos)-1
        
        for i in range(0, size):
            prom = generos[i]

            geners[nom]["list_cantidad"][prom["type"]] += 1
            geners[nom]["list_streams"][prom["stream_service"]] += 1

    return geners     

def req_8(catalog, genero, rank):

    list_genero = req_4(catalog, genero)[3]

    lista_actores_total = lt.newList("ARRAY_LIST")

    for program in lt.iterator(list_genero):
        actores = program["cast"].split(", ")
        for actor in actores:
            tupla_actores = mp.get(catalog["actores"], actor)
            if tupla_actores:
                lista_actores = me.getValue(tupla_actores)
                if lt.getElement(lista_actores, lista_actores["size"]) != actor:
                    lt.addLast(lista_actores, actor)
                lt.addLast(lista_actores_total, lista_actores["elements"])

    sorted_list = ordenamiento(lista_actores_total, compareCantidadNombre)

    resultado = lt.newList("ARRAY_LIST")

    actores = {}

    if sorted_list["size"] <= rank :
        resultado = sorted_list
    else:
        resultado = lt.subList(sorted_list, 1, rank)
        
    for actor in range(0, rank):
        size = len(resultado["elements"][actor]) - 1
        nom_actor = resultado["elements"][actor][-1]
        actores[nom_actor] = {}
        valor_actor = actores[nom_actor]

        valor_actor["cantidad"] = size 
        valor_actor["can_streams"] = {"TV Show": 0, "Movie": 0}
        
        valor_actor["program_stream"] = {"TV Show": None, "Movie": None}
        valor_actor["program_stream"]["TV Show"] = lt.newList("ARRAY_LIST")
        valor_actor["program_stream"]["Movie"] = lt.newList("ARRAY_LIST")

        valor_actor["plataform"] = {"netflix": 0, "amazon": 0, "disney": 0, "hulu": 0}

        valor_actor["directores"] = lt.newList("ARRAY_LIST")

        valor_actor["actores"] = lt.newList("ARRAY_LIST")

        for program in range(0, size):

            prom = resultado["elements"][actor][program]
            
            añadir = {"title": prom["title"],
                    "release_year": prom["release_year"],
                    "duration": prom["duration"],
                    "type" : prom["type"]}

            valor_actor["can_streams"][prom["type"]] += 1
            
            lt.addLast(valor_actor["program_stream"][prom["type"]], añadir)

            valor_actor["plataform"][prom["stream_service"]] += 1

            if lt.isPresent(valor_actor["directores"], prom["director"]) == 0:
                lt.addLast(valor_actor["directores"], prom["director"])

            rep_1 =  prom["cast"].split(nom_actor + ", ")
            rep_2 = ("").join(rep_1)
            reparto = rep_2.split(", ")
            for cast in reparto:
                if lt.isPresent(valor_actor["actores"], cast) == 0:
                    lt.addLast(valor_actor["actores"], cast)

        valor_actor["program_stream"]["TV Show"] = ordenamiento(valor_actor["program_stream"]["TV Show"], compareYearTittleDuration)
        valor_actor["program_stream"]["Movie"] = ordenamiento(valor_actor["program_stream"]["Movie"], compareYearTittleDuration)
        valor_actor["actores"] = ordenamiento(valor_actor["actores"], compereAlfabet)
        valor_actor["directores"] = ordenamiento(valor_actor["directores"], compereAlfabet)

    return resultado, actores


def netflixSize(catalog):

    return lt.size(catalog["model"]['netflix'])

def amazonSize(catalog):

    return lt.size(catalog["model"]['amazon'])

def disneySize(catalog):

    return lt.size(catalog["model"]['disney'])

def huluSize(catalog):

    return lt.size(catalog["model"]['hulu'])


def programSize(catalog):

    return lt.size(catalog["model"]['program'])

# Funciones utilizadas para comparar elementos dentro de una lista

def compareCantidadNombre(program_1, program_2):

    if len(program_1) > len(program_2):
        return True
    elif len(program_1) == len(program_2):
        if program_1[-1] < program_2[-1]:
            return True
    else:
        return False

def compareTittleDuration(program_1, program_2):

    if program_1["title"].lower() < program_2["title"].lower():
            return True
    elif program_1["title"].lower() == program_2["title"].lower():
        if program_1["type"] == program_2["type"] and len(program_1["duration"]) != 0 and len(program_2["duration"]) != 0:
            duration_1 = program_1["duration"].split(" ")
            can_duration_1 = float(duration_1[0])
            duration_2 = program_2["duration"].split(" ")
            can_duration_2 = float(duration_2[0])

            if can_duration_1 < can_duration_2:
                return True
    else:
        return False

def compareYearTittle(program_1, program_2):
    
    if int(program_1['release_year']) > int(program_2['release_year']):
        return True
    
    elif int(program_1['release_year']) == int(program_2['release_year']):
        if program_1["title"].lower() > program_2["title"].lower():
            return True
    else:
        return False

def compareYearTittleDuration(program_1, program_2):

    if int(program_1['release_year']) > int(program_2['release_year']):
        return True
    
    elif int(program_1['release_year']) == int(program_2['release_year']):
        if program_1["title"].lower() < program_2["title"].lower():
            return True
        elif program_1["title"].lower() == program_2["title"].lower():
             if program_1["type"] == program_2["type"] and len(program_1["duration"]) != 0 and len(program_2["duration"]) != 0:
                duration_1 = program_1["duration"].split(" ")
                can_duration_1 = float(duration_1[0])
                duration_2 = program_2["duration"].split(" ")
                can_duration_2 = float(duration_2[0])
        
                if can_duration_1 < can_duration_2:
                    return True
    else:
        return False

def compereAlfabet(program_1, program_2):

    if program_1.lower() < program_2.lower():
        return True
    else:
        return False

# Funciones de ordenamiento

def ordenamiento(catalog, cmpfunction):

    catalog_sorted = se.sort(catalog, cmpfunction)

    return catalog_sorted

