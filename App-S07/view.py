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

from platform import platform
from re import A
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def imprimirReqParticipations(data, headers):
    table = []
    for info in lt.iterator(data):
        infoActorMovies = []
        infoActorShows = []
        movies = lt.newList()
        shows = lt.newList()
        for title in lt.iterator(info['titles']):
            if title['type'] == 'Movie':
                lt.addLast(movies, title)
            else:
                lt.addLast(shows, title)
        movies = controller.firstAndLastThreeTitles(movies)
        shows = controller.firstAndLastThreeTitles(shows)
        for movie in lt.iterator(movies):
            infoActorMovies.append([movie['release_year'], movie['title'], movie['duration']])
        for show in lt.iterator(shows):
            infoActorShows.append([show['release_year'], show['title'], show['duration']])
        tableInfoActorMovies = [tabulate(infoActorMovies, tablefmt="plain")]
        tableInfoActorShows = [tabulate(infoActorShows, tablefmt="plain")]
        if info['actor'] == '':
            actorName = 'Unknown'
        else:
            actorName = info['actor']
        if len(tableInfoActorMovies[0]) == 0:
            tableInfoActorMovies = ['Unknown']
        if len(tableInfoActorShows[0]) == 0:
            tableInfoActorShows = ['Unknown']
        table.append([info['rank'], actorName, tabulate([tableInfoActorMovies], tablefmt="plain"), tabulate([tableInfoActorShows], tablefmt="plain")])
    print(tabulate(table, headers, tablefmt="grid"))

def imprimirReqColborations(data, headers):
    table = []
    for info in lt.iterator(data):
        infoActor = []
        for dicType in info['streame_service'].values():
            infoPlatform = []
            for key, value in dicType.items():
                if type(value) != str:
                    if value > 0:
                        countType = [key, value]
                        infoPlatform.append(countType)
            tablePlatform = [dicType['name'], tabulate(infoPlatform, tablefmt="plain")]
            infoActor.append(tablePlatform)
            tableStreameService = tabulate(infoActor, ['count type\n'], tablefmt="plain")
        if info['actor'] == '':
            actorName = 'Unknown'
        else:
            actorName = info['actor']
        tableActor = [info['rank'], actorName, tabulate([['Movies', info['movies']], ['TV Shows', info['TVShows']]], tablefmt="plain"), tableStreameService]
        table.append(tableActor)
    print(tabulate(table, headers, tablefmt="grid"))

def printGeneralInformation(data, headers, simple=False):
    """
    Organiza las plataformas de acuerdo a la cantidad de titulos cargados de mayor a menor
    """
    lista = lt.newList()
    for key, value in data.items():
        if value > 0:
            lt.addLast(lista, {'name': key, 'amount': value})
    controller.sortDataAmounts(lista)
    table = []
    for element in lt.iterator(lista):
        name = element['name']
        amount = element['amount']
        table.append([name, amount])
    if simple:
        return table
    else:
        print(tabulate(table, headers, tablefmt="grid"))

def printTabulatedData(filteredTitles, headers, req= False):
    if req:
        imprimirReqColborations(filteredTitles[0], headers[0])
        imprimirReqParticipations(filteredTitles[1], headers[1])
    else:
        size = lt.size(filteredTitles)
        table = []
        if len(headers) >= 12:
            width = 10
        elif len(headers) >= 10:
            width = 15
        else:
            width = 22
        if size:
            for filteredTitle in lt.iterator(filteredTitles):
                fields = []
                for header in headers:
                    if type(filteredTitle[header]) == dict:
                        info = printGeneralInformation(filteredTitle[header], [header, 'count'], simple=True)
                        fields.append(tabulate(info, ['count ' + header[:4]], tablefmt="plain"))
                    else:
                        if filteredTitle[header] == '':
                            fields.append('Unknown')
                        else:
                            fields.append(filteredTitle[header])
                table.append(fields)
            print(tabulate(table, headers, tablefmt="grid", maxcolwidths=width))
        else:
            print('\nNo se encontró contenido con este criterio de busqueda')

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Examinar películas estrendas en un año")
    print("2- Examinar los programas de televisión estrenados en un año")
    print("3- Encontrar el contenido donde participa un actor")
    print("4- Encontrar el contenido por un género particular")
    print("5- Encontrar el contenido producido en un país")
    print("6- Encontrar el contenido con un director involucrado")
    print("7- Listar el top (N) de los géneros con más contenido")
    print("8- Listar el Top (N) de actores más populares para un género especifico")

catalog = None

# Se crea el controlador asociado a la vista
control = newController()

def loadData(control, memflag):
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    generalInformation = controller.loadData(control, memflag)
    return generalInformation

def printLoadDataTimes(times):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(times, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{times[0]:.3f}", "||",
              "Memoria [kB]: ", f"{times[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{times:.3f}")

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("\n\nCargando información de los archivos ....")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        generalInformation, times = loadData(control, memflag=mem)
        print('-'*52)
        print('Total loaded streaming service info:')
        print('Total loaded titles: ' + str(lt.size(control)))
        print('Total loaded features: ' + str(generalInformation['features']))
        print('-'*52)
        del generalInformation['features']
        headers = ["service_name", "count"]
        printGeneralInformation(generalInformation, headers)
        filtered = controller.firstAndLastThreeTitles(control)
        headers = ['show_id', 'streame_service', 'type', 'release_year', 'title', 'director', 'cast', 'country', 'date_added', 'rating', 'duration', 'listed_in', 'description']
        print('\nThe first 3 and last 3 titles in content range are...')
        print('Contentet sorted by release year / title:')
        printTabulatedData(filtered, headers)
        printLoadDataTimes(times)

    elif int(inputs[0]) == 1:
        year = input('year: ')
        startTime = controller.getTime()
        filtered = controller.getMoviesByYear(control, year)
        print('\n\n' + '='*15 + 'Req No. 1 Inputs' + '='*15)
        print('Movies released in the year: ' + year)
        print('\n' + '='*15 + 'Req No. 1 Answer' + '='*15)
        print('There are only ' + str(lt.size(filtered)) + " IPs (Intelectual Properties) in 'Movie' type released in the year: " + year)
        filtered = controller.firstAndLastThreeTitles(filtered)
        headers = ['type', 'release_year', 'title', 'duration', 'streame_service', 'director', 'cast']
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    elif int(inputs[0]) == 2:
        date = input('Date: ')
        startTime = controller.getTime()
        filtered = controller.getTVShowsByDate(control, date)
        print('\n\n' + '='*15 + 'Req No. 2 Inputs' + '='*15)
        print('TV Shows released in the date: ' + date)
        print('\n' + '='*15 + 'Req No. 2 Answer' + '='*15)
        print('There are only ' + str(lt.size(filtered)) + " 'TV Shows' in the date: " + date)
        filtered = controller.firstAndLastThreeTitles(filtered)
        headers = ['type', 'date_added', 'title', 'duration', 'release_year', 'streame_service', 'director', 'cast']
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)
    
    elif int(inputs[0]) == 3: 
        actor = input('Actor: ')
        startTime = controller.getTime()
        filtered, details = controller.getTitlesByActor(control, actor)
        size = lt.size(filtered)
        print('\n\n' + '='*15 + 'Req No. 3 Inputs' + '='*15)
        print("The content with " + actor + "in the 'cast'")
        print('\n' + '='*15 + 'Req No. 3 Answer' + '='*15)
        print('-'*6 + "'" + actor + "' cast participation count" + '-'*6)
        headers = ["type", "count"]
        printGeneralInformation(details, headers)
        print('\n' + '-'*6 + ' Participation details ' + '-'*6)
        if size < 6:
            print("There are less than 6 participations of '" + actor + "' on record")
        else:
            print("There are " + str(size) + " participations of " + actor + " on record")
        filtered = controller.firstAndLastThreeTitles(filtered)
        headers = ['release_year', 'title', 'duration', 'director', 'streame_service', 'type', 'cast', 'country', 'rating', 'listed_in', 'description']
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    elif int(inputs[0]) == 4:
        genre = input('Genre: ')
        startTime = controller.getTime()
        filtered, details = controller.getTitlesByGenre(control, genre)
        print('\n\n' + '='*15 + 'Req No. 4 Inputs' + '='*15)
        print("The content in 'listed_in' " + genre)
        print('\n' + '='*15 + 'Req No. 4 Answer' + '='*15)
        print('-'*6 + "'" + genre + "' content type production count" + '-'*6)
        headers = ["type", "count"]
        printGeneralInformation(details, headers)
        print('\n' + '-'*6 + ' Content details ' + '-'*6)
        print('There are ' + str(lt.size(filtered)) + " IPs (Intelectual Properties) with the '" + genre + "' label.")
        print('The first 3 and last 3 IPs in range are:')
        filtered = controller.firstAndLastThreeTitles(filtered)
        headers = ['release_year', 'title', 'duration', 'streame_service', 'director', 'cast', 'country', 'rating', 'listed_in', 'description']
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    elif int(inputs[0]) == 5:
        country = input('Ingrese el país: ')
        startTime = controller.getTime()
        filtered, details = controller.getTitlesByCountry(control, country)
        size = lt.size(filtered)
        print('\n\n' + '='*15 + 'Req No. 5 Inputs' + '='*15)
        print("The content produced in '" + str(country) + "'")
        print('\n' + '='*15 + 'Req No. 5 Answer' + '='*15)
        print('-'*6 + "'" + str(country) + "' content type production count" + '-'*6)
        headers = ["type", "count"]
        printGeneralInformation(details, headers)
        print('\n' + '-'*6 + ' Content details ' + '-'*6)
        print('There are only ' + str(size) + " IPs (Intelectual Properties) produced in '" + str(country) + "'.")
        filtered = controller.firstAndLastThreeTitles(filtered)
        headers = ['release_year', 'title', 'director', 'streame_service', 'duration', 'type', 'cast', 'country', 'listed_in', 'description']
        printTabulatedData(filtered, headers)
        endTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(endTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    elif int(inputs[0]) == 6:
        director = input('Director: ')
        startTime = controller.getTime()
        filtered, details = controller.getTitlesByDirector(control, director)
        print('\n\n' + '='*15 + 'Req No. 6 Inputs' + '='*15)
        print("Find the content with '" + director + "' as 'director'")
        print('\n' + '='*15 + 'Req No. 6 Answer' + '='*15)
        print('-'*6 + " '" + director + "' content type count " + '-'*6)
        headers = ["type", "count"]
        printGeneralInformation(details[0], headers)
        print('\n' + '-'*6 + " '" + director + "' Streaming content type  count " + '-'*6)
        headers = ["service_name", "count"]
        printGeneralInformation(details[1], headers)
        print('\n' + '-'*6 + " '" + director + "' listed in count " + '-'*6)
        genres = details[2]
        print('There are only ' + str(lt.size(genres)) + " tags in 'listed_in'")
        genres = controller.firstAndLastThreeTitles(genres)
        headers = ["listed_in", "count"]
        printTabulatedData(genres, headers)
        print('\n' + '-'*6 + " '" + director + "' content details " + '-'*6)
        print('There are only ' + str(lt.size(filtered)) + " IPs (Intelectual Properties) with '" + director + "' as 'director'")
        headers = ['release_year', 'title', 'duration', 'streame_service', 'type', 'cast', 'country', 'rating', 'listed_in', 'description']
        filtered = controller.firstAndLastThreeTitles(filtered)
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    elif int(inputs[0]) == 7:
        N = int(input('Top N: '))
        startTime = controller.getTime()
        filtered, tags = controller.getTopNByGenre(control, N)
        print('\n\n' + '='*15 + 'Req No. 7 Inputs' + '='*15)
        print('The TOP ' + str(N) + " in 'listed_in' are:")
        print('\n' + '='*15 + 'Req No. 7 Answer' + '='*15)
        print("Ther are '" + str(tags) + "' tags participating in TOP '" + str(N) + "' genres for 'listed_in'")
        print('\n' + '-'*6 + " The TOP '" + str(N) + "' listed in tags are " + '-'*6)
        print('There are only ' + str(N) + ' tags in the TOP ranking')
        headers = ['listed_in', 'count']
        printTabulatedData(filtered, headers)
        print('\n' + '-'*6 + " TOP " + str(N) + " listed in tags details " + '-'*6)
        print('There are only ' + str(N) + " tags in the TOP ranking")
        headers = ['rank', 'listed_in', 'count', 'type', 'streame_service']
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    elif int(inputs[0]) == 8:
        N = int(input('TOP: '))
        genre = input('Genre: ')
        startTime = controller.getTime()
        filtered, ditails, tags = controller.getTopNByActorInGenre(control, N, genre)
        print('\n\n' + '='*15 + 'Req No. 8 (BONUS) Inputs' + '='*15)
        print("Ranking the TOP '" + str(N) + "' actors for the genre '" + genre + "'")
        print('\n' + '='*15 + 'Req No. 8 (BONUS) Answer' + '='*15)
        print("There are '" + str(tags) + "' actors participating for the TOP '" + str(N) + "' actors for the genre '" + genre + "'")
        print('\n' + '-'*6 + " The TOP '" + str(N) + "' actor participations are " + '-'*6)
        print("There are only " + str(N) + ' in the TOP ranking.')
        headers = ['rank', 'actor', 'count']
        printTabulatedData(filtered, headers)
        print('\n' + '-'*6 + " TOP actors participation details " + '-'*6)
        print('There are only ' + str(N) + " in the TOP ranking")
        ditails = controller.firstAndLastThreeTitles(ditails)
        headers = [['actor', 'count_types', 'content_type'], ['actor', 'Movies', 'TV Shows']]
        printTabulatedData([filtered, ditails], headers, req= True)
        print('\n' + '-'*6 + " TOP actors colaboration details " + '-'*6)
        print('There are only ' + str(N) + " in the TOP ranking")
        filtered = controller.firstAndLastThreeTitles(filtered)
        headers = ['rank', 'actor', 'directors', 'actors']
        printTabulatedData(filtered, headers)
        finalTime = controller.getTime()
        deltaTime = str(round(controller.deltaTime(finalTime, startTime), 2)) + " ms"
        print("Tiempo de ejecución: ", deltaTime)

    else:
        sys.exit(0)

    input('\n\nPulse cualquier tecla para continuar...\n\n')
sys.exit(0)

