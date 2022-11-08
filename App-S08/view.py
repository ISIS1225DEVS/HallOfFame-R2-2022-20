"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

from gettext import Catalog
from turtle import update
import config as cf
import sys
import controller as ct
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate
import controller as ct

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#-------------------------------------------------Apartado para interactuar con el usuario-------------------------------------------------#
def printMenu():
    print(" ╠═══════════════════════════ BIENVENIDO ═══════════════════════════╣ ")
    print("1- Cargar información en el catálogo")
    print("2- Listar las películas estrenadas en un periodo de tiempo")
    print("3- Listar programas de televisión agregados en un periodo de tiempo ")
    print("4- Encontrar contenido donde participa un actor")
    print("5- Encontrar contenido por un género especifico")
    print("6- Encontrar contenido producido en un país")
    print("7- Encontrar contenido con un director involucrado")
    print("8- Listar el TOP (N) de los géneros con más contenido")
    print("9- Listar el TOP (N) de los actores con más participaciones en contenido ")
    print("0- Salir")

catalogo = None

#---------------------------------------------Función que crea los dict para realizar los tabulate--------------------------------------------#
def TAD_a_dict(tad,columnas):
    """
    Función que crea el formato tabulate para cada TAD.
    ----------
    tad :
        El TAD a transformar a tabulate
    columnas:
        Lista con los titulos de cada columna.
    ---------
    Return:
        Diccionario de los datos.
    """
    lista = []
    dicc={}
    for i in lt.iterator(tad):
        lista.append(i)
    for c in columnas:
        dicc[c]=[]
        for diccionario in lista:
            for llaves in diccionario:
                if c == llaves:
                    dicc[c].append(diccionario[llaves])
    for valores in dicc.values():
        for pos in range(0,len(valores)):
            if valores[pos] == '':
                valores[pos] = "Unknown"
    return dicc
def dict_a_listas(diccionario):
    keys = []
    values = []
    for llaves in diccionario.keys():
        keys.append(llaves)
    for valores in diccionario.values():
        values.append(valores)
    return keys, values
#--------------------------------------------------------Menu Principal--------------------------------------------------------#
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if inputs[0] == "1":
        print("Cargando información de los archivos... ")
        print("Posibles tamaños: small, 5pct, 10pct, 20pct, 30pct, 50pct, 80pct y large")
        tamaño = input("Digite el tamaño de la muesta de datos que desea cargar: ")
        cond_medida_memoria = input("Digite 1  si desea medir la memoria usasada, 2 de lo contrario : ")
        cant, lista_p_u,catalogo, d_cantidades,delta_time, delta_memory= ct.carga_datos(tamaño,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("La cantidad de datos cargados fueron: " + str(cant))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        plataformas = ["Amazon Prime","Netflix","Hulu","Disney+"]
        cantidad = [d_cantidades["amazon"],d_cantidades["netflix"],d_cantidades["hulu"],d_cantidades["disney"]]
        print(tabulate({"Service name":plataformas,"Count":cantidad},headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias= ["show_id","stream_service","type","release_year","title","director","cast","country","date_added","rating","duration","listed_in","description"]
        dict_categorias = TAD_a_dict(lista_p_u,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 8, 8, 8, 8, 8, 22, 8, 8, 8, 8, 8, 25]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "2":
        año_consulta = input("Digite el año que desea consultar: ")
        cant_r1, lista_p_u_r1,delta_time, delta_memory= ct.consulta_año__estreno(catalogo,año_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("La cantidad de peliculas fueron: " + str(cant_r1))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["type","release_year","title","duration","stream_service","director","cast"]
        dict_categorias = TAD_a_dict(lista_p_u_r1,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8,12,8,12,8,22]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "3":
        fecha_consulta = input("Digite la fecha que desea consultar: ")
        cant_r2, lista_p_u_r2,delta_time, delta_memory= ct.consulta_fecha(catalogo,fecha_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("La cantidad de peliculas fueron: " + str(cant_r2))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["type","date_added","title","duration","stream_service","director","cast"]
        dict_categorias = TAD_a_dict(lista_p_u_r2,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8,12,8,12,8,22]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "4":
        actor_consulta = input("Digite el actor que desea consultar: ")
        cant_r3, lista_p_u_r3,delta_time, delta_memory= ct.consulta_actor(catalogo,actor_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        formato = ["Movie", "TV Show"]
        cantidad = lt.getElement(cant_r3, 1)["count: "] ,lt.getElement(cant_r3, 2)["count: "]
        print(tabulate({"Type":formato,"Count":cantidad},headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["release_year","title","duration","stream_service","director","type","cast","country","rating","listed_in","description"]
        dict_categorias = TAD_a_dict(lista_p_u_r3,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 8, 8, 8, 8, 8, 22, 8, 8, 8, 25]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "5":
        genero_consulta = input("Digite el genero que desea consultar: ")
        cant_r4, lista_p_u_r4,delta_time, delta_memory= ct.consulta_genero(catalogo,genero_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        formato = ["Movie", "TV Show"]
        cantidad = [cant_r4["Movies"],cant_r4["Tv_shows"]]
        print(tabulate({"Type":formato,"Count":cantidad},headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["release_year","title","duration","stream_service","director","type","cast","country","rating","listed_in","description"]
        dict_categorias = TAD_a_dict(lista_p_u_r4,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 8, 8, 8, 8, 8, 22, 8, 8, 8, 25]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "6":
        pais_consulta = input("Digite el país que desea consultar: ")
        cant_r5, lista_p_u_r5,delta_time, delta_memory= ct.consulta_pais(catalogo,pais_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        formato = ["Movie", "TV Show"]
        cantidad = [cant_r5["Movies"],cant_r5["Tv_shows"]]
        print(tabulate({"Type":formato,"Count":cantidad},headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["release_year","title","duration","stream_service","director","type","cast","country","rating","listed_in","description"]
        dict_categorias = TAD_a_dict(lista_p_u_r5,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 12, 8, 8, 8, 8, 22, 8, 8, 8, 25]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "7":
        director_consulta = input("Digite el director que desea consultar: ")
        cant_por_tipo_r6,cant_por_plataforma_r6,cant_por_genero_r6, lista_r6,delta_time, delta_memory = ct.consulta_director(catalogo,director_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        formato, cantidad = dict_a_listas(cant_por_tipo_r6)
        print(tabulate({"Type":formato,"Count":cantidad},headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        plataformas, cantidad = dict_a_listas(cant_por_plataforma_r6)
        print(tabulate({"Service name":plataformas,"Count":cantidad},headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        apartados = ["listed_in","count"]
        dict_apartados = TAD_a_dict(cant_por_genero_r6,apartados)
        print(tabulate(dict_apartados,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["release_year","title","duration","stream_service","director","type","cast","country","rating","listed_in","description"]
        dict_categorias = TAD_a_dict(lista_r6,categorias)
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 8, 8, 8, 8, 8, 22, 8, 8, 8, 25]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "8":
        top_consulta = int(input("Digite el el número (N) de generos a identificar: "))
        num_consulta,TAD_cantidad,TAD_top,delta_time, delta_memory = ct.consulta_top_generos(catalogo,top_consulta,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Fueron "+str(num_consulta)+" generos consultados para este top " + str(top_consulta))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        apartados = ["listed_in","count"]
        dict_apartados = TAD_a_dict(TAD_cantidad,apartados)
        print(tabulate(dict_apartados,headers="keys",tablefmt="fancy_grid",maxcolwidths=[25, 8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        categorias = ["rank","listed_in","count","type","stream_service"]
        dict_categorias = TAD_a_dict(TAD_top,categorias)
        tipo = dict_categorias["type"]
        servicio = dict_categorias["stream_service"]
        for pos in range(0,len(tipo)):
            dict_generos = tipo[pos]
            lista = []
            for generos in dict_generos.values():
                dict_nuevo = {}
                dict_nuevo["type"] = []
                dict_nuevo["count"] = []
                for categorias in generos.keys():
                    conteo = generos[categorias]
                    dict_nuevo["type"].append(categorias)
                    dict_nuevo["count"].append(conteo)
                lista.append(dict_nuevo)
        dict_categorias["type"] = lista
        for pos in range(0,len(servicio)):
            dict_generos = servicio[pos]
            lista = []
            for generos in dict_generos.values():
                dict_nuevo = {}
                dict_nuevo["type"] = []
                dict_nuevo["stream_service"] = []
                for categorias in generos.keys():
                    conteo = generos[categorias]
                    dict_nuevo["type"].append(categorias)
                    dict_nuevo["stream_service"].append(conteo)
                lista.append(dict_nuevo)
        dict_categorias["stream_service"] = lista
        tipo = dict_categorias["type"]
        servicio = dict_categorias["stream_service"]
        lista1 = []
        for pos in range(0,len(tipo)):
            conteo_genero = tipo[pos]
            tabla = tabulate(conteo_genero,headers="keys",maxcolwidths=[10,8])
            lista1.append(tabla)
        dict_categorias["type"] = lista1
        lista2 = []
        for pos in range(0,len(servicio)):
            conteo_genero = servicio[pos]
            tabla = tabulate(conteo_genero,headers="keys",maxcolwidths=[12,14])
            lista2.append(tabla)
        dict_categorias["stream_service"] = lista2
        print(tabulate(dict_categorias,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 15,8,18,30]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "9":
        Top_n = input("Digite el numero de actores que desea consultar en el top: ")
        genero= input("Digite el genero que desea consultar: ")
        num_actores,num_participaciones_actor,lista_cantidades,lista_videos, lista_colaboraciones,delta_time, delta_memory=ct.consulta_top_n_actores(catalogo,Top_n,genero,cond_medida_memoria)
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("La cantidad de actores que compiten en el top "+ Top_n + " son en total " + str(num_actores))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        titulos = ["cast","count"]
        dict_participaciones = TAD_a_dict(num_participaciones_actor,titulos)
        print(tabulate(dict_participaciones,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8, 8]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        titulos = ["cast","count stream service"]
        dict_cantidades = {}
        rank = []
        i = 1
        while i <= int(Top_n):
            rank.append(i)
            i += 1
        dict_cantidades["rank"] = rank
        dict_cantidades.update(TAD_a_dict(lista_cantidades,titulos))
        service = dict_cantidades["count stream service"]
        for pos in range(0,len(service)):
            diccionarios = service[pos]
            subtabulate = {"service":[],"type":[],"count":[]}
            list_service = subtabulate["service"]
            list_type = subtabulate["type"]
            list_count = subtabulate["count"]
            for keys in diccionarios.keys():
                list_service.append(keys)
                tipos = diccionarios[keys]
                if len(tipos) > 1:
                    list_service.append("L------>")
                for llaves in tipos.keys():
                    list_type.append(llaves)
                    conteo = tipos[llaves]
                    list_count.append(conteo)
            tabla = tabulate(subtabulate,headers="keys",maxcolwidths=[15,15,15])
            service[pos] = tabla
        print(tabulate(dict_cantidades,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,20,30]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        titulos = ["cast","Movies","Tv Show"]
        dict_videos = {}
        dict_videos["rank"] = rank
        dict_videos.update(TAD_a_dict(lista_videos,titulos))
        movies = dict_videos["Movies"]
        tv_shows = dict_videos["Tv Show"]
        for pos in range(0,len(movies)):
            tads = movies[pos]
            columnas = ["release_year","title","duration"]
            diccionarios = TAD_a_dict(tads,columnas)
            for listas in diccionarios.values():
                if listas == []:
                    listas = ["Is empty"]
            movies[pos] = tabulate(diccionarios,headers=["año","titulo","Dur."],maxcolwidths=[10,20,7])
        for pos in range(0,len(tv_shows)):
            tads = tv_shows[pos]
            columnas = ["release_year","title","duration"]
            diccionarios = TAD_a_dict(tads,columnas)
            for llaves in diccionarios.keys():
                listas = diccionarios[llaves]
                if listas == []:
                    diccionarios[llaves] = ["Is Empty"]
            tv_shows[pos] = tabulate(diccionarios,headers=["año","titulo","duración"],maxcolwidths=[12,25,15])
        print(tabulate(dict_videos,headers=["rank","cast","Movies","TV Shows"],tablefmt="fancy_grid",maxcolwidths=[8,10,35,42]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        titulos = ["cast","directors","actors"]
        dict_colaboraciones = {}
        dict_colaboraciones["rank"] = rank
        dict_colaboraciones.update(TAD_a_dict(lista_colaboraciones,titulos))
        director = dict_colaboraciones["directors"]
        actor = dict_colaboraciones["actors"]
        for pos in range(0,len(director)):
            lista = director[pos]
            tabla = {"directores":[]}
            lista1 = tabla["directores"]
            for valores in lt.iterator(lista):
                lista1.append(valores)
            tabla = tabulate(tabla,maxcolwidths=[18])
            director[pos] = tabla
        for pos in range(0,len(actor)):
            lista = actor[pos]
            tabla = {"actores":[]}
            lista1 = tabla["actores"]
            for valores in lt.iterator(lista):
                lista1.append(valores)
            tabla = tabulate(tabla,maxcolwidths=[18])
            actor[pos] = tabla
        print(tabulate(dict_colaboraciones,headers="keys",tablefmt="fancy_grid",maxcolwidths=[8,20,18,18]))
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("el tiempo de carga fue : " +str(delta_time))
        if delta_memory!= None:
            print("------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("la memoria usada fue: " + str(delta_memory))
    elif inputs[0] == "0":
        sys.exit(0)
    else:
        print("No es una opción válida.")
        sys.exit(0)
