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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import datetime as dt
from tabulate import tabulate
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

# ===================================
# Funciones para imprimir resultados
# ===================================

def tabla_corta(title):
    report_table = []
    report_table.append(['Title',title['title']])
    report_table.append(['Release year',title['release_year']]) 
    report_table.append(['Director',title['director']])
    report_table.append(['Streaming Platform',title['platform']])
    report_table.append(['Duration',title['duration']]) 
    report_table.append(['Country',title['country']])
    report_table.append(['Genre',title['listed_in']]) 
    report_table.append(['Country',title['cast']])
    report = tabulate(report_table,tablefmt='fancy_grid')
    return report


def tabla_largos(titles):
    Headers = ['Título','Director','Fecha de estreno','Duración','Plataforma','Reparto']
    table = [[titles[0]['title'],titles[0]['director'],titles[0]['release_year'],titles[0]['duration'],titles[0]['platform'],titles[0]['cast']],
             [titles[1]['title'],titles[1]['director'],titles[1]['release_year'],titles[1]['duration'],titles[1]['platform'],titles[1]['cast']],
             [titles[2]['title'],titles[2]['director'],titles[2]['release_year'],titles[2]['duration'],titles[2]['platform'],titles[2]['cast']],
             ['...',              '...',                 '...',                     '...',                 '...',                 '...'],
             [titles[-3]['title'],titles[-3]['director'],titles[-3]['release_year'],titles[-3]['duration'],titles[-3]['platform'],titles[-3]['cast']],
             [titles[-2]['title'],titles[-2]['director'],titles[-2]['release_year'],titles[-2]['duration'],titles[-2]['platform'],titles[-2]['cast']],
             [titles[-1]['title'],titles[-1]['director'],titles[-1]['release_year'],titles[-1]['duration'],titles[-1]['platform'],titles[-1]['cast']]]
    return tabulate(table,headers=Headers,tablefmt='fancy_grid')

def printActor(consulta):
    get = controller.getContentByActor(catalog,consulta)
    if get:
        titles = get['elements']
        Shows = 0
        Movies = 0
        headers = ['Type','Count']
        if len(titles)<=7:
            for title in titles:

                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
                print(tabla_corta(title))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

        else:
            for title in titles:
                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
            
            print(tabla_largos(titles))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

    else:
        print(f'No hay resultados para: {consulta}')

def printGenre(consulta):
    get = controller.getContentByGenre(catalog,consulta)
    if get:
        titles = get['elements']
        Shows = 0
        Movies = 0
        headers = ['Type','Count']
        if len(titles)<=7:
            for title in titles:

                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
                print(tabla_corta(title))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

        else:
            for title in titles:
                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
            
            print(tabla_largos(titles))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

    else:
        print(f'No hay resultados para: {consulta}')

def printCountry(consulta):
    get = controller.getContentByCountry(catalog,consulta)
    if get:
        titles = get['elements']
        Shows = 0
        Movies = 0
        headers = ['Type','Count']
        if len(titles)<=7:
            for title in titles:

                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
                print(tabla_corta(title))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

        else:
            for title in titles:
                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
            
            print(tabla_largos(titles))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

    else:
        print(f'No hay resultados para: {consulta}')

def printGenre(consulta):
    get = controller.getContentByGenre(catalog,consulta)
    if get:
        titles = get['elements']
        Shows = 0
        Movies = 0
        headers = ['Type','Count']
        if len(titles)<=7:
            for title in titles:

                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
                print(tabla_corta(title))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

        else:
            for title in titles:
                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
            
            print(tabla_largos(titles))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

    else:
        print(f'No hay resultados para: {consulta}')

def printDirector(consulta):
    get = controller.getContentByDirector(catalog,consulta)
    if get:
        titles = get['elements']
        Shows = 0
        Movies = 0
        headers = ['Type','Count']
        if len(titles)<=7:
            for title in titles:

                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
                print(tabla_corta(title))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

        else:
            for title in titles:
                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
            
            print(tabla_largos(titles))
            print(tabulate([['Movies', Movies],
                            ['TV shows', Shows],
                            ['TOTAL',Movies+Shows]],headers = headers,tablefmt='fancy_grid'))

    else:
        print(f'No hay resultados para: {consulta}')

# Menu de opciones

def printMenu():
    print("Bienvenido")
    print("0-  Cargar información en el catálogo")
    print("1-  Películas estrenadas en un año")
    print("2-  Programas de televisión agregados en un año")
    print("3-  Contenido en el que participa un actor")
    print("4-  Contenido por género")
    print("5-  Contenido producido en un país")
    print("6-  Contenido con un director")
    print("7-  Top (N) géneros con más contenido")
    print("8-  Top (N) actores más populares para un género específico")
    print("9-  EXIT")

catalog = None

"""
Menu principal
"""
while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:

        filesize = input("Ingrese el tamaño del archivo que desea cargar: ")
        memory = castBoolean(input("¿Desea observar el uso de memoria? (True/False): "))
        control = newController()
        catalog = control["model"]

        print("\nCargando información de los archivos ....")
        data= controller.loadData(control,filesize,memory)

        total_size = catalog["content"]["size"]
        Amazon_size = catalog["Amazon Prime"]["size"]
        Disney_size = catalog["Disney Plus"]["size"]
        Hulu_size = catalog["Hulu"]["size"]
        Netflix_size = catalog["Netflix"]["size"]

        headers_1 = ['Streaming Service','Total Titles']
        table_1 = [['Amazon Prime Video',Amazon_size],
                   ['Disney+',Disney_size],
                   ['Hulu',Hulu_size],
                   ['Netflix',Netflix_size],
                   ['TOTAL',total_size]]

        Overall = tabulate(table_1,headers=headers_1,tablefmt='fancy_grid')

        if memory:
            print('\nContenido cargado con éxito al catálogo.')
            print("Time elapsed:",data[0])
            print("Memory used:",data[1])
            print()
            print(Overall)
        else:
            print('\nContenido cargado con éxito al catálogo.')
            print("Time elapsed:",data)
            print()
            print(Overall)
        

    elif int(inputs[0]) == 1:
        year = int(input("Ingrese el año para realizar la busqueda (AAAA): \n"))
        start = time.time()
        anio = controller.getContentByYear(catalog,year)
        if anio != "No hay peliculas estrenadas ese año":
            titles = anio["elements"]
            partido = []
            for i in range(len(titles)):
                txt = ""
                actores = titles[i]["cast"].split(",")
                for i in range(len(actores)):
                    if len(txt) == 0:
                        txt += " " + str(actores[i])
                    else:
                        txt += "\n" + str(actores[i])
                partido.append(txt)

            Headers_1 = [f'Número de peliculas estrenadas en: {year}']
            General_report = [['Películas',len(titles)]]
            if 6 >= len(titles):
                print("Hay menos de 6 peliculas estrenadas en " + str(year))
            Headers_2 = ['Fecha de lanzamiento','Titulo','Duración','Plataforma',"Director",'Actores']
            if len(titles) >= 6:
                Specific_report = [[titles[0]['release_year'],titles[0]['title'],titles[0]['duration'],titles[0]['platform'],titles[0]['director'],partido[0]],
                            [titles[1]['release_year'],titles[1]['title'],titles[1]['duration'],titles[1]['platform'],titles[1]['director'],partido[1]],
                            [titles[2]['release_year'],titles[2]['title'],titles[2]['duration'],titles[2]['platform'],titles[2]['director'],partido[2]],
                            ['...','...','...','...','...','...','...','...','...'],
                            [titles[-3]['release_year'],titles[-3]['title'],titles[-3]['duration'],titles[-3]['platform'],titles[-3]['director'],partido[-3]],
                            [titles[-2]['release_year'],titles[-2]['title'],titles[-2]['duration'],titles[-2]['platform'],titles[-2]['director'],partido[-2]],
                            [titles[-1]['release_year'],titles[-1]['title'],titles[-1]['duration'],titles[-1]['platform'],titles[-1]['director'],partido[-1]]]
            else:
                Specific_report = []
                for i in range(len(titles)):
                    Specific_report.append([titles[i]['release_year'],titles[i]['title'],titles[i]['duration'],titles[i]['platform'],titles[i]['director'],partido[i]])
                    
            print(tabulate(General_report,headers=Headers_1,tablefmt='fancy_grid'))
            print(tabulate(Specific_report,headers=Headers_2,tablefmt='fancy_grid'))
        else:
            print(anio)
        stop = time.time()
        print(f'Elapsed time: {stop-start}')
    
    elif int(inputs[0]) == 2:
        date = input("Indique la fecha inferior para realizar la busqueda (Month %B day %d, year %Y): \n")
        start = time.time()
        fecha_real = dt.datetime.strptime(date,"%B %d, %Y")
        fecha = controller.getContentByDate(catalog,fecha_real)
        if fecha != "No hay TV SHOWS estrenados ese año":
            titles = fecha["elements"]
            jecha = []
            for i in range(len(titles)):
                fechitas = str(titles[i]["date_added"]).replace("00:00:00","")
                jecha.append(fechitas)
                if str(titles[i]["director"]) == "":
                    titles[i]["director"] = "Desconocido"
                if str(titles[i]["cast"]) == "":
                    titles[i]["cast"] = "Desconocido"
            partido = []
            for i in range(len(titles)):
                txt = ""
                actores = titles[i]["cast"].split(",")
                for i in range(len(actores)):
                    if len(txt) == 0:
                        txt += " " + str(actores[i])
                    else:
                        txt += "\n" + str(actores[i])
                partido.append(txt)
            Headers_1 = [f'Número de series estrenadas en: {fecha_real}']
            General_report = [['Series',len(titles)]]
            if 6 >= len(titles):
                print("Hay menos de 6 peliculas estrenadas en " + str(fecha_real))
            Headers_2 = ['Fecha de carga a la plataforma','Titulo','Duración','Plataforma',"Director",'Actores']
            if len(titles) >= 6:
                Specific_report = [[jecha[0],titles[0]['title'],titles[0]['duration'],titles[0]['platform'],titles[0]['director'],partido[0]],
                            [jecha[1],titles[1]['title'],titles[1]['duration'],titles[1]['platform'],titles[1]['director'],partido[1]],
                            [jecha[2],titles[2]['title'],titles[2]['duration'],titles[2]['platform'],titles[2]['director'],partido[2]],
                            ['...','...','...','...','...','...','...','...','...'],
                            [jecha[-3],titles[-3]['title'],titles[-3]['duration'],titles[-3]['platform'],titles[-3]['director'],partido[-3]],
                            [jecha[-2],titles[-2]['title'],titles[-2]['duration'],titles[-2]['platform'],titles[-2]['director'],partido[-2]],
                            [jecha[-1],titles[-1]['title'],titles[-1]['duration'],titles[-1]['platform'],titles[-1]['director'],partido[-1]]]
            else:
                Specific_report = []
                for i in range(len(titles)):
                    Specific_report.append([jecha[i],titles[i]['title'],titles[i]['duration'],titles[i]['platform'],titles[i]['director'],partido[i]])
                    
            print(tabulate(General_report,headers=Headers_1,tablefmt='fancy_grid'))
            print(tabulate(Specific_report,headers=Headers_2,tablefmt='fancy_grid'))
        else:
            print(fecha)
        stop = time.time()
        print(f'Elapsed time: {stop-start}')

    elif int(inputs[0]) == 3:
        Consulta = input('Digite el nombre del actor que desea consultar:\n')
        start = time.time()
        printActor(Consulta)
        stop = time.time()
        print(f'Elapsed time: {stop-start}')

    elif int(inputs[0]) == 4:
        genre = input("Ingrese el género para el que desea concoer el contenido:\n")
        start = time.time()
        printGenre(genre)
        stop = time.time()
        print(f'Elapsed time: {stop-start}')

    elif int(inputs[0]) == 5:
        country = input("Ingrese el país para el que desea conocer el contenido:\n")
        start = time.time()
        printCountry(country)
        stop = time.time()
        print(f'Elapsed time: {stop-start}')

    elif int(inputs[0]) == 6:
        Director = input("Ingrese el nombre del director cuyos títulos desea consultar:\n")
        start = time.time()
        get = controller.getContentByDirector(catalog,Director)
        if get:
            Movies = 0
            Shows = 0
            titles = get['elements']
            for title in titles:
                if title['type']=='Movie':
                    Movies += 1
                elif title['type']=='TV Show':
                    Shows += 1
            print()
            print(f'{Director} ha dirigido: {len(titles)} títulos.')
            print(f'Movies: {Movies}')
            print(f'TV Shows: {Shows}')
            print()
            print(printDirector(Director))

        else:
            print(f'No hay resultados para {Director}')
        stop = time.time()
        print(f'Elapsed time: {stop-start}')

    elif int(inputs[0]) == 7:
        N = int(input("Indique la cantidad de títulos que quiere que aparezcan en el top: \n"))
        start = time.time()
        tp, ct = controller.topngenres(catalog,N)
        print("El top "+str(N)+" géneros con más contenido son: \n")
        for i in range(N):
            print(tp[i]["genero"]+":",tp[i]["elements"]["size"])
            print("\n")
        print("La cantidad de títulos por plataforma por cada género son: \n")
        for i in range(N):
            print((tp[i]["genero"]).upper())
            print("Netflix: ",ct[i]["Netflix"])
            print("Hulu: ",ct[i]["Hulu"])
            print("Disney Plus: ",ct[i]["Disney Plus"])
            print("Amazon Prime: ",ct[i]["Amazon Prime"])
            print("\n")
        print("La cantidad de títuos por tipo de contenido por cada género son: \n")
        for i in range(N):
            print((tp[i]["genero"]).upper())
            print("Movies: ",ct[i]["Movies"])
            print("TV Shows: ",ct[i]["TV Shows"])
            print("\n")
        stop = time.time()
        print(f'Elapsed time: {stop-start}')

    elif int(inputs[0]) == 8:
        print('Pa la próxima te hacemos este bono mi rey')

    else:
        sys.exit(0)
sys.exit(0)
