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
from tabulate import tabulate
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Examinar películas estrenadas en un año")
    print("3- Examinar programas de televisión agregados en un año")
    print("4- Encontrar contenido donde participa un actor")
    print("5- Encontrar contenido por un genero particular")
    print("6- Encontrar contenido producido en un país")
    print("7- Encontrar el contenido con un director involucrado")
    print("8- Listar TOP (N) de los géneros con más contenido")
    print("9- Listar TOP (N) de actores más populares para un género específico")

def printLoad(catalog):
    print_list = [["service_name","count"],["amazon",lt.size(catalog["amazon_prime"])],
    ["netflix",lt.size(catalog["netflix"])],["hulu",lt.size(catalog["hulu"])],["disney",lt.size(catalog["disney_plus"])]]
    total = lt.size(catalog["disney_plus"])+lt.size(catalog["netflix"])+lt.size(catalog["hulu"])+lt.size(catalog["amazon_prime"])
    print("Total de titulos cargados:",str(total)+".")
    print(tabulate(print_list,tablefmt="grid"))
    for i in ("amazon_prime","netflix","hulu","disney_plus"):
        print("Primeros y últimos 3 titulos cargados de",i+".")
        print_list = [["show_id","stream_service","type","release_year","title","director","cast",
                        "country","date_added","rating","duration","listed_in","description"]]
        first = lt.subList(catalog[i],1,3)
        last = lt.subList(catalog[i],lt.size(catalog[i])-2,3)
        for e in lt.iterator(first):
            print_list.append([e["show_id"],e["streaming_service"],e["type"],e["release_year"],
            e["title"],e["director"],e["cast"],e["country"],e["date_added"],e["rating"],e["duration"],
            e["listed_in"],e["description"][0:100]])
        for e in lt.iterator(last):
            print_list.append([e["show_id"],e["streaming_service"],e["type"],e["release_year"],
            e["title"],e["director"],e["cast"],e["country"],e["date_added"],e["rating"],e["duration"],
            e["listed_in"],e["description"][0:100]])
        print(tabulate(print_list,tablefmt="grid",maxcolwidths=17))

def printreq1(catalog,year):
    list = controller.MoviesInYear(catalog,year)
    printlist = [["type","release_year","title","duration","streaming_service","director","cast"]]
    if lt.size(list) <= 6:
        for i in lt.iterator(list):
            append_list = []
            for e in printlist[0]:
                append_list.append(i[e])
            printlist.append(append_list)
    else:
        first = lt.subList(list,1,3)
        last = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(first):
            append_list = []
            for e in printlist[0]:
                append_list.append(i[e])
            printlist.append(append_list)
        for i in lt.iterator(last):
            append_list = []
            for e in printlist[0]:
                append_list.append(i[e])
            printlist.append(append_list)
    print("Hay",str(lt.size(list)),"fechas en el año",year+".")
    print(tabulate(printlist,tablefmt="grid"))
def printreq2(catalog,date):
    list = controller.ShowsInDate(catalog,date)
    printlist = [["type","date_added","release_year","title","duration","streaming_service","director","cast"]]
    if lt.size(list) <= 6:
        for i in lt.iterator(list):
            append_list = []
            for e in printlist[0]:
                append_list.append(i[e])
            printlist.append(append_list)
    else:
        first = lt.subList(list,1,3)
        last = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(first):
            append_list = []
            for e in printlist[0]:
                append_list.append(i[e])
            printlist.append(append_list)
        for i in lt.iterator(last):
            append_list = []
            for e in printlist[0]:
                append_list.append(i[e])
            printlist.append(append_list)
    print("Hay",str(lt.size(list)),"shows en la fecha",date+".")
    print(tabulate(printlist,tablefmt="grid"))
def printreq3(catalog,actor):
    list,movies,shows = controller.ContentByActor(catalog,actor)
    print_list = [["type","count"]]
    if movies != 0:
        print_list.append(["Movies",movies])
    if shows != 0:
        print_list.append(["TV Shows",shows])
    print(tabulate(print_list,tablefmt="grid"))
    print_list = [["release_year","title","duration","director","stream_service","type",
    "cast","country","rating","listed_in","description"]]
    if lt.size(list) < 6:
        print("\nHay menos de 6 participaciones de",actor,"en el catálogo.")
        for i in lt.iterator(list):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["director"],i["streaming_service"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
    else:
        print("\nEstas son las primeras y últimas 3 participaciones de",actor+".")
        first3 = lt.subList(list,1,3)
        last3 = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(first3):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["director"],i["streaming_service"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
        for i in lt.iterator(last3):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["director"],i["streaming_service"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
    print(tabulate(print_list,tablefmt="grid",maxcolwidths=20))

def printreq4(catalog, genre):
    list, movies, shows = controller.ContentByGenre(catalog, genre)
    print_list = [["type","count"]]
    if movies != 0:
        print_list.append(["Movies",movies])
    if shows != 0:
        print_list.append(["TV Shows",shows])
    print(tabulate(print_list,tablefmt="grid"))
    print_list = [["release_year","title","duration","stream_service","director","type",
    "cast","country","rating","listed_in","description"]]
    if lt.size(list) <= 6:
        print("\nHay menos de 6 videos del género ",genre,"en el catálogo.")
        for i in lt.iterator(list):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["streaming_service"],i["director"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
    else:
        print("\nEstas son los primeros y últimos 3 videos del género",genre+".")
        first3 = lt.subList(list,1,3)
        last3 = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(first3):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["streaming_service"],i["director"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
        for i in lt.iterator(last3):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["streaming_service"],i["director"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
    print(tabulate(print_list,tablefmt="grid",maxcolwidths=20))
def printreq5(catalog,country):
    list,movies,shows = controller.ContentByCountry(catalog,country)
    print_list = [['type','count']]
    if movies != 0:
        print_list.append(["Movies",movies])
    if shows != 0:
        print_list.append(["TV Shows",shows])
    print(tabulate(print_list,tablefmt="grid"))
    print_list = [["release_year","title","duration","director","stream_service","type",
    "cast","country","rating","listed_in","description"]]
    if lt.size(list) < 6:
        print("\nHay menos de 6 participaciones de",country,"en el catálogo.")
        for i in lt.iterator(list):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["director"],i["streaming_service"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
    else:
        print("\nEstos son los primeros y últimos 3 contenidos producidos en",country+":")
        first3 = lt.subList(list,1,3)
        last3 = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(first3):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["director"],i["streaming_service"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
        for i in lt.iterator(last3):
            print_list.append([i["release_year"],i["title"],i["duration"],
            i["director"],i["streaming_service"],i["type"],i["cast"],i["country"],
            i["rating"],i["listed_in"],i["description"][0:100]])
    print(tabulate(print_list,tablefmt="grid",maxcolwidths=20))
def printreq6(catalog,director):
    DirectorList,type,service_name,listed_in = controller.TitlesByDirector(catalog,director)
    printlist1 = [["type","count"]]
    printlist2 = [["service_name","Movie","TV Show"]]
    printlist3 = [["listed_in","count"]]
    printlist4 = [["release_year","title","duration","director","streaming_service","type",
                    "cast","country","rating","listed_in","description"]]
    for i in ("Movie","TV Show"):
        printlist1.append([i,type[i]])
    for i in service_name:
        printlist2.append([i,service_name[i]["Movie"],service_name[i]["TV Show"]])
    for i in listed_in:
        printlist3.append([i,listed_in[i]])
    for i in lt.iterator(DirectorList):
        list_ = []
        for e in printlist4[0]:
            if e != "description":
                list_.append(i[e])
            else:
                list_.append(i[e][0:100])
        printlist4.append(list_)
    print(tabulate(printlist1,tablefmt="grid"))
    print(tabulate(printlist2,tablefmt="grid"))
    print(tabulate(printlist3,tablefmt="grid"))
    print(tabulate(printlist4,tablefmt="grid",maxcolwidths=17))
def printreq7(catalog,N):
    genreList = controller.TopNGenres(catalog,N)
    rank = 1
    print_list1 = [["listed_in","count"]]
    print_list2 = [["rank","listed_in","count","type","stream_service"]]
    for i in lt.iterator(genreList):
        str1 = tabulate([["type","count"],["Movies",i["type"]["Movie"]],["TV Shows",i["type"]["TV Show"]]],tablefmt="plain")
        str2_list = [["stream_service","count"]]
        for key in i["stream"]:
            if i["stream"][key] > 0:
                str2_list.append([key,i["stream"][key]])
        str2 = tabulate(str2_list,tablefmt="plain")
        print_list1.append([i["genre"],i["size"]])
        print_list2.append([rank,i["genre"],i["size"],str1,str2])
        rank += 1
    print(tabulate(print_list1,tablefmt="grid"))
    print(tabulate(print_list2,tablefmt="grid"))

def printreq8(catalog,genre,N):
    Info_list = controller.TopNActorByGenre(catalog,genre,N)
    printlist1 = [["Name","Movies","TV Shows","streaming_platform"]]
    printlist2 = [["Name","Cast","Directors"]]
    printlist3 = [['Name', 'Movies', 'TV Shows']]
    for i in lt.iterator(Info_list):
        name,service_name, type, directorList, castList = i
        service_list = [["Service","count"]]
        for key in service_name:
            service1_list = [["type","count"]]
            for key1 in service_name[key]:
                service1_list.append([key1,service_name[key][key1]])
            table1 = tabulate(service1_list,tablefmt="plain")
            service_list.append([key,table1])
        table2 = tabulate(service_list,tablefmt="plain")
        printlist1.append([name,lt.size(type["Movie"]),lt.size(type["TV Show"]),table2])
        CastString = ""
        if lt.size(castList) < 6:
            for cast in lt.iterator(castList):
                CastString += cast + ", "
        else:
            first_cast = lt.subList(castList,1,3)
            last_cast = lt.subList(castList,lt.size(castList)-2,3) 
            for cast in lt.iterator(first_cast):
                CastString += cast + ", "
            for cast in lt.iterator(last_cast):
                CastString += cast + ", "
        DirectorString = ""
        if lt.size(directorList) < 6:
            for director in lt.iterator(directorList):
                DirectorString += director + ", "
        else:
            first_director = lt.subList(directorList,1,3)
            last_director = lt.subList(directorList,lt.size(directorList)-2,3) 
            for director in lt.iterator(first_director):
                DirectorString += director + ", "
            for director in lt.iterator(last_director):
                DirectorString += director + ", "
        printlist2.append([name,CastString,DirectorString])
        if lt.size(type['Movie']) <= 6:
            movie_list = [["release_year","title","director"]]
            for title in lt.iterator(type["Movie"]):
                movie_list.append([title["release_year"],title["title"],title["director"]])
            movie_table = tabulate(movie_list,tablefmt="plain")
        else:
            movie_list = [["release_year","title","director"]]
            first_movies = lt.subList(type['Movie'], 1, 3)
            last_movies = lt.subList(type['Movie'], lt.size(type['Movie']) - 2, 3)        
            for title in lt.iterator(first_movies):
                movie_list.append([title["release_year"],title["title"],title["director"]])
            for title in lt.iterator(last_movies):
                movie_list.append([title["release_year"],title["title"],title["director"]])
            movie_table = tabulate(movie_list,tablefmt="plain")
        if lt.size(type['TV Show']) <= 6:
            shows_list = [["release_year","title","director"]]
            for title in lt.iterator(type["TV Show"]):
                shows_list.append([title["release_year"],title["title"],title["director"]])
            show_table = tabulate(shows_list,tablefmt="plain")
        else:
            shows_list = [["release_year","title","director"]]
            first_shows = lt.subList(type['TV Show'], 1, 3)
            last_shows = lt.subList(type['TV Show'], lt.size(type['TV Show']) - 2, 3)        
            for title in lt.iterator(first_shows):
                shows_list.append([title["release_year"],title["title"],title["director"]])
            for title in lt.iterator(last_shows):
                shows_list.append([title["release_year"],title["title"],title["director"]])
            show_table = tabulate(shows_list,tablefmt="plain")
        printlist3.append([name,movie_table,show_table])
    print('Actor, Movies, TV Shows, Streaming')
    print(tabulate(printlist1, tablefmt='grid'))
    print('Actor, Cast, Directors')
    print(tabulate(printlist2,tablefmt="grid"))
    print('Actor, Movies, TV Shows')
    print(tabulate(printlist3,tablefmt="grid"))
catalog = None
size = "-large"
type = "PROBING"
FC = 0.5
print('Tipo:', type, 'Factor de carga:', FC)
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        if catalog == None:
            catalog = controller.newController(type,FC)
        time,memory = controller.loadData(catalog,size)
        print("Tiempo de ejecución:",str(time),"ms.")
        print("Memoria Usada:",str(memory),"kb.")
        printLoad(catalog["model"])
    elif int(inputs[0]) == 2:
        year = input("Ingrese el año: ")
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq1(catalog,year)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs[0]) == 3:
        date = input("Ingrese la fecha: ")
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq2(catalog,date)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs[0]) == 4:
        actor = input("Ingrese el nombre del actor: ")
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq3(catalog,actor)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs[0]) == 5:
        genre = input('Ingrese el género que desea consultar:')
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq4(catalog,genre)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs[0]) == 6:
        country = input("Ingrese el nombre del pais a consultar: ")
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq5(catalog,country)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs) == 7:
        director = input("Ingrese el nombre del director: ")
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq6(catalog,director)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs) == 8:
        N = int(input("Ingrese el número N para el top: "))
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq7(catalog,N)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    elif int(inputs) == 9:
        genre = input('Ingrese el género que desea consultar: ')
        N = int(input('Ingrese el número N: '))
        time1 = controller.getTime()
        memory1 = controller.getMemory()
        printreq8(catalog, genre, N)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria usada:', str(deltamemory), 'kb.')
    else:
        sys.exit(0)
sys.exit(0)
