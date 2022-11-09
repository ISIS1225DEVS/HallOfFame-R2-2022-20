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

import config as cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from datetime import datetime
from tabulate import tabulate
from textwrap import wrap
import sys
import controller
from DISClib.ADT import list as lt
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def newController():
    control = controller.newController()
    return control

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar peliculas estrenadas en un año")
    print("3- Consultar contenido donde participa un actor")
    print("4- Consultar contenido por género")
    print("5- Encontrar el contenido con un director involucrado")
    print("6- Consultar top (N) géneros con más contenido")
    print("7- Consultar top (N) actores más populares por género")
    print("0- Salir")

def loadData(control, porcentaje_data, memflag=True):
    answer = controller.loadData(control, porcentaje_data, memflag)
    count_platforms = controller.countplatforms(answer[0])
    elements = answer[1]
    for element in elements.keys():
        elements[element]=controller.getSix(elements[element])
    count_total = lt.size(control['model']['total'])
    print('--------------------------------')
    print('Loaded streaming service info:')
    print('--------------------------------')
    print('Total loaded titles: ' + str(count_total))
    print('--------------------------------')
    table = tabulate(count_platforms['elements'], headers=["service_name", "count"], tablefmt='fancy_grid')
    print(table)
    for platform in elements.keys():
        print('--------------------------------------------------------------------------')
        print('Las 3 primeras y las 3 ultimas peliculas cargadas en ' +
              platform + ' fueron: ')
        print('--------------------------------------------------------------------------')
        imprimirTitulos(elements[platform])
    return answer

def imprimirTitulos(titulos):

    titulos_print = []
    for titulo in lt.iterator(titulos):
        titulo_print = titulo.copy()
        for key in titulo_print.keys():
            if type(titulo_print[key]) == list:
                titulo_print[key] = ', '.join(titulo_print[key])
            elif type(titulo_print[key]) == datetime:
                titulo_print[key] = datetime.strftime(
                    titulo_print[key], '%Y-%m-%d')
            if type(titulo_print[key]) == str:
                titulo_print[key] = '\n'.join(wrap(titulo_print[key], 16))
        titulos_print.append(titulo_print)
    print(tabulate(titulos_print, headers='keys', tablefmt='fancy_grid'))

#======================
# REQUERIMIENTO 3
#======================

def printTitlesByActor(author):
    if author == None:
        print("--------------------------")
        print("El autor no se encontro")
        print("--------------------------")
    else:
        total = lt.newList('ARRAY_LIST')
        tupla1 = ['Movies', lt.size(author[0]['movies'])]
        tupla2 = ['Tv_shows', lt.size(author[0]['tv_shows'])]
        lt.addLast(total, tupla1)
        lt.addLast(total, tupla2)
        table = tabulate(total['elements'], headers=["Type", "count"], tablefmt='fancy_grid')
        print(table)
        print('--------------------------------------------------------------------------')
        print('Los primero 3 y los ultimos 3 titulos cargados son: ')
        print('--------------------------------------------------------------------------')
        titles = controller.getSix(author[1])
        imprimirTitulos(titles)

#======================
# REQUERIMIENTO 4
#======================

def printTitlesByGenero(answer):
    total = lt.newList('ARRAY_LIST')
    tupla1 = ['Movies', lt.size(answer[0]['movies'])]
    tupla2 = ['Tv_shows', lt.size(answer[0]['tv_shows'])]
    lt.addLast(total, tupla1)
    lt.addLast(total, tupla2)
    table = tabulate(total['elements'], headers=["Type", "count"], tablefmt='fancy_grid')
    print(table)
    print('--------------------------------------------------------------------------')
    print('Los primero 3 y los ultimos 3 titulos cargados son: ')
    print('--------------------------------------------------------------------------')
    titles = controller.getSix(answer[1])
    imprimirTitulos(titles)

#======================
# REQUERIMIENTO 6
#======================

def printTitlesByDirector(author, director):
    if author == None:
        print("--------------------------")
        print("El autor no se encontro")
        print("--------------------------")
    else:
        total = lt.newList('ARRAY_LIST')
        tupla1 = ['Movies', lt.size(author[0]['movies'])]
        tupla2 = ['Tv_shows', lt.size(author[0]['tv_shows'])]
        lt.addLast(total, tupla1)
        lt.addLast(total, tupla2)
        table = tabulate(total['elements'], headers=["Type", "count"], tablefmt='fancy_grid')
        print('----------------------------------------------------------------------------')
        print('Para el director ' + director + ' existen los siguientes contenidos: ')
        print('----------------------------------------------------------------------------')
        print('Total por tipo: ')
        print('----------------------------------------------------------------------------')
        print(table)
        
        plataform = author[2]
        i = 1
        llaves =  mp.keySet(plataform)
        total2= lt.newList("ARRAY_LIST")
        while i <= lt.size(llaves):
            plataforma = lt.getElement(llaves, i)
            num = me.getValue(mp.get(plataform,plataforma))
            i+=1
            tupla3= [plataforma, str(num)]
            lt.addLast(total2, tupla3 )
        print('--------------------------------------------------------------------------')
        print('Total por plataforma: ')
        print('--------------------------------------------------------------------------')
        print(tabulate(total2['elements'],headers = ['Plataform', 'Count'], tablefmt='fancy_grid'))

        gender = author[3]
        i = 1
        llaves =  mp.keySet(gender)
        total3= lt.newList("ARRAY_LIST")
        while i <= lt.size(llaves):
            plataforma = lt.getElement(llaves, i)
            num = me.getValue(mp.get(gender,plataforma))
            i +=1
            tupla4= [plataforma, str(num)]
            lt.addLast(total3, tupla4 )
        print('--------------------------------------------------------------------------')
        print('Total por género: ')
        print('--------------------------------------------------------------------------')
        print(tabulate(total3['elements'],headers=['Genre','Count'],tablefmt='fancy_grid'))

        print('--------------------------------------------------------------------------')
        print('Los primero 3 y los ultimos 3 titulos cargados son: ')
        print('--------------------------------------------------------------------------')
        titles = controller.getSix(author[1])
        imprimirTitulos(titles)

#======================
# REQUERIMIENTO 8
#======================

def printTopActors(answer):
    top = answer[0]
    info_actors = answer[1]
    print(tabulate(top['elements'], headers=['Actor', 'Count'], tablefmt='fancy_grid'))

    for actor in lt.iterator(top):
        print('--------------------------------------------------------------')
        print('Imprimiendo información de ' + actor[0] + '...')
        print('--------------------------------------------------------------')
        titles_count = lt.newList('ARRAY_LIST')
        movies = me.getValue(mp.get(info_actors, actor[0]))['movies']
        tv_shows = me.getValue(mp.get(info_actors, actor[0]))['tv_shows']
        lt.addLast(titles_count, ['Total', actor[1]])
        lt.addLast(titles_count, ['Movies', lt.size(movies)])
        lt.addLast(titles_count, ['Tv shows', lt.size(tv_shows)])
        print('Total de peliculas y shows de televisión donde participo: ')
        print('--------------------------------------------------------------')
        print(tabulate(titles_count['elements'], headers=['Tyoe', 'Count'], tablefmt='fancy_grid'))
        if lt.size(movies) > 0:
            print('--------------------------------------------------------------')
            print('Peliculas donde participo (3 primeras y ultimas cargadas): ')
            print('--------------------------------------------------------------')
            movies_six = controller.getSix(movies)
            imprimirTitulos(movies_six)
        if lt.size(tv_shows) > 0:
            print('--------------------------------------------------------------')
            print('Tv shows donde participo (3 primeras y ultimas cargadas): ')
            print('--------------------------------------------------------------')
            shows_six = controller.getSix(tv_shows)
            imprimirTitulos(shows_six)
        directores = me.getValue(mp.get(info_actors, actor[0]))
        directores_names = directores['directores']
        directores_six = controller.getSix(directores_names)
        dir = []
        for direc in lt.iterator(directores_six):
            dir.append([direc])
        print('--------------------------------------------------------------')
        print('Directores con los que trabajo (3 primeras y ultimas cargadas): ')
        print('--------------------------------------------------------------')
        print(tabulate(dir, headers=['Name'], tablefmt='fancy_grid'))
        actores = me.getValue(mp.get(info_actors, actor[0]))
        actores_names = actores['cast']
        actores_six = controller.getSix(actores_names)
        cast = []
        for actor2 in lt.iterator(actores_six):
            cast.append([actor2])
        print('--------------------------------------------------------------')
        print('Actores con los que trabajo (3 primeras y ultimas cargadas): ')
        print('--------------------------------------------------------------')
        print(tabulate(cast, headers=['Name'], tablefmt='fancy_grid'))

def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if len(answer) > 3:
        print("Tiempo [ms]: ", f"{answer[2]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[3]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[2]:.3f}")

def printAnswerTimes(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if len(answer) > 2:
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[1]:.3f}")

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False  

porcentaje_data = "small"

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        opcion_data = int(input(
            'Ingrese el porcentaje de los datos a cargar (small: 0) (large: 100):'))
        if opcion_data == 100:
            porcentaje_data = 'large'
        elif opcion_data != 0:
            porcentaje_data = str(opcion_data) + "pct"
        print("Cargando información de los archivos ....")
        control = newController()
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = loadData(control, porcentaje_data, memflag=mem)
        printLoadDataAnswer(answer)
        
    elif int(inputs[0]) == 2:
        year = int(input('Ingrese el año que desea consultar: '))
        answer = controller.getMoviesByYear(control, year)
        print('----------------------------------------------------------')
        print('Se encontraron: ' + str(lt.size(answer[0])) + ' peliculas.')
        print('----------------------------------------------------------')
        imprimirTitulos(answer[0])
        printAnswerTimes(answer)

    elif int(inputs[0])== 3:
        actor = (input("ingrese el actor que desea buscar: "))
        answer = controller.getTitlesByActor(control, actor)
        printTitlesByActor(answer[0])
        printAnswerTimes(answer)

    elif int(inputs[0]) == 4:
        genero = input('Ingrese el genero que desea buscar: ')
        mem = input("Desea ver el uso de memoria?")
        mem = castBoolean(mem)
        answer = controller.getTitlesByGenero(control, genero, memflag=mem)
        printTitlesByGenero(answer[0])
        printAnswerTimes(answer)


    elif int(inputs[0]) == 5 :
        director = input("ingrese el director que desea buscar: ")
        answer  = controller. getTitlesByDirector(control, director)
        printTitlesByDirector(answer[0], director)
        printAnswerTimes(answer)

    elif int(inputs[0]) == 6:
        rank = int(input('Ingrese el top de generos que desea observar: '))
        mem = input("Desea ver el uso de memoria?")
        mem = castBoolean(mem)
        answer = controller.getTopGeneros(control, rank, memflag=mem)
        top = answer[0]
        print(tabulate(top['elements'], headers=['Genre', 'Count'], tablefmt='fancy_grid'))
        printAnswerTimes(answer)

    elif int(inputs[0]) == 7:
        genero = input('Ingrese el género que desea buscar: ')
        rank = int(input('Ingrese el top de actores que desea observar: '))
        mem = input("Desea ver el uso de memoria?")
        mem = castBoolean(mem)
        answer = controller.getTopActor(control, genero, rank, memflag=mem)
        printTopActors(answer[0])
        printAnswerTimes(answer)

    elif int(inputs[0]) == 0:
        sys.exit(0)
    else:
        print('Ingrese una opción valida.')
sys.exit(0)
