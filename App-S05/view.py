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
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from prettytable import PrettyTable
from datetime import datetime
import prettytable
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
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control

def printMenu():
    print("\nBienvenido.")
    print("1- Cargar información en el catálogo.")
    print("2- Requerimiento 1: Lista de las peliculas estrenadas en un año.")
    print("3- Requerimiento 2: Lista de los programas de televisión agregados en una fecha.")
    print("4- Requerimiento 3: Lista con contenido específico de un actor - Santiago Flórez - 201912420.")
    print("5- Requerimiento 4: Lista de contenido por género - Elkin Cuello - 202215037.")
    print("6- Requerimiento 5: Contenido producido en un país - Manuel Caro 202020303.")
    print("7- Requerimiento 6: Contenido con un director involucrado.")
    print("8- Requerimiento 7: Top N genero con mas contenido.")
    print("0- Salir.")

def createTableLoadData(first, last, Amazon_size, Disney_Size, Hulu_size, Netflix_size): 

    tabla_count = PrettyTable(hrules=prettytable.ALL)
    tabla_count.field_names = ['Stream service', 'Count']
    tabla_count.max_width = 30
    tabla_count.add_row(['Amazon Prime Video', Amazon_size])
    tabla_count.add_row(['Netflix', Netflix_size])
    tabla_count.add_row(['Hulu', Hulu_size])
    tabla_count.add_row(['Disney Plus', Disney_Size])
    
    tabla_data = PrettyTable(hrules=prettytable.ALL)
    tabla_data.field_names = ['Show_id', 'Title', 'Director', 'Cast', 'Country', 'Type', \
        'Date added', 'Release year', 'Rating', 'Duration', 'Listed in', 'Description', 'streaming service']
    tabla_data.max_width = 10
    for video in lt.iterator(first):
        tabla_data.add_row([video['show_id'], video['title'], video['director'], video['cast'], video['country'], \
            video['type'], video['date_added'], video['release_year'], video['rating'], video['duration'], \
                video['listed_in'], video['description'], video['service']])
    for video in lt.iterator(last):
        tabla_data.add_row([video['show_id'], video['title'], video['director'], video['cast'], video['country'], \
            video['type'], video['date_added'], video['release_year'], video['rating'], video['duration'], \
                video['listed_in'], video['description'], video['service']])
    return tabla_count, tabla_data

def createTableTops(data): # Requerimiento 7
    # data es la lista de generos
    table_count = PrettyTable(hrules=prettytable.ALL)
    table_count.field_names = ['Listed in', 'Count']
    table_count.max_width = 30
    for genero in lt.iterator(data):
        table_count.add_row([genero['name'], genero['count']])

    table_data = PrettyTable(hrules=prettytable.ALL)
    table_data.field_names = ['Rank', 'Listed in', 'Count', 'Type', 'Stream service']
    table_data.max_width = 30
    i=0
    for genero in lt.iterator(data):
        i+=1
        type = f'Count type:\nMovie: {genero["Movie"]}\nTV Show: {genero["TV Show"]}'
        str_service = f'Count stream service:\nAmazon Prime Video: {genero["Amazon Prime"]}\nNetflix: {genero["Netflix"]}\nHulu: {genero["Hulu"]}\nDisney+: {genero["Disney Plus"]}'
        table_data.add_row([i, genero['name'], genero['count'], type, str_service])

    return table_count, table_data


def createTableGeneros(data, data_count): # Requerimiento 4 
    # data es la lista de generos, data_count es la lista de conteos
    table_generos = PrettyTable(hrules=prettytable.ALL)
    table_generos.field_names = ['Release year', 'Title', 'Duration', 'Stream service', 'Director',\
        'Type', 'Cast', 'Country', 'Rating', 'Listed in', 'Description']
    table_generos.max_width = 10

    if lt.size(data)>=6:
        primeros = lt.subList(data, 1, 3)
        ultimos = lt.subList(data, lt.size(data)-2, 3)
        for genero in lt.iterator(primeros):
            genero['release_year'] = 'Unknown' if genero['release_year'] == 0 else genero['release_year']
            table_generos.add_row([genero['release_year'], genero['title'], genero['duration'], genero['service'], genero['director'],\
                genero['type'], genero['cast'], genero['country'], genero['rating'], genero['listed_in'], genero['description']])
        for genero in lt.iterator(ultimos):
            genero['release_year'] = 'Unknown' if genero['release_year'] == 0 else genero['release_year']
            table_generos.add_row([genero['release_year'], genero['title'], genero['duration'], genero['service'], genero['director'],\
                genero['type'], genero['cast'], genero['country'], genero['rating'], genero['listed_in'], genero['description']])

    else:
        for genero in lt.iterator(data):
            genero['release_year'] = 'Unknown' if genero['release_year'] == 0 else genero['release_year']
            table_generos.add_row([genero['release_year'], genero['title'], genero['duration'], genero['service'], genero['director'],\
                genero['type'], genero['cast'], genero['country'], genero['rating'], genero['listed_in'], genero['description']])

    table_count = PrettyTable(hrules=prettytable.ALL)
    table_count.field_names = ['Type', 'Count']
    table_count.max_width = 30

    table_count.add_row(['Movie', lt.firstElement(data_count)])
    table_count.add_row(['TV Show', lt.lastElement(data_count)])

    return table_generos, table_count

def createTableREQ2(data, data_count): # Requerimiento 4 
    # data es la lista de generos, data_count es la lista de conteos
    table_generos = PrettyTable(hrules=prettytable.ALL)
    table_generos.field_names = ['Release year', 'Title', 'Duration', 'Stream service', 'Director',\
        'Type', 'Cast', 'Country', 'Rating', 'Listed in', 'Date Added']
    table_generos.max_width = 10

    if lt.size(data)>=6:
        primeros = lt.subList(data, 1, 3)
        ultimos = lt.subList(data, lt.size(data)-2, 3)
        for genero in lt.iterator(primeros):
            genero['release_year'] = 'Unknown' if genero['release_year'] == 0 else genero['release_year']
            table_generos.add_row([genero['release_year'], genero['title'], genero['duration'], genero['service'], genero['director'],\
                genero['type'], genero['cast'], genero['country'], genero['rating'], genero['listed_in'], genero['date_added']])
        for genero in lt.iterator(ultimos):
            genero['release_year'] = 'Unknown' if genero['release_year'] == 0 else genero['release_year']
            table_generos.add_row([genero['release_year'], genero['title'], genero['duration'], genero['service'], genero['director'],\
                genero['type'], genero['cast'], genero['country'], genero['rating'], genero['listed_in'], genero['date_added']])

    else:
        for genero in lt.iterator(data):
            genero['release_year'] = 'Unknown' if genero['release_year'] == 0 else genero['release_year']
            table_generos.add_row([genero['release_year'], genero['title'], genero['duration'], genero['service'], genero['director'],\
                genero['type'], genero['cast'], genero['country'], genero['rating'], genero['listed_in'], genero['date_added']])

    table_count = PrettyTable(hrules=prettytable.ALL)
    table_count.field_names = ['Type', 'Count']
    table_count.max_width = 30

    table_count.add_row(['Movie', lt.firstElement(data_count)])
    table_count.add_row(['TV Show', lt.lastElement(data_count)])

    return table_generos, table_count    

def createTablePlat (data):
    t = PrettyTable(hrules=prettytable.ALL)
    t.field_names = ["Plataforma", "Numero"]
    t.max_width = 20
    t.add_row(["Netflix",lt.getElement(data,0)])
    t.add_row(["Amazon Prime",lt.getElement(data,1)])
    t.add_row(["Hulu",lt.getElement(data,2)])
    t.add_row(["Disney Plus",lt.getElement(data,3)])
    return t

def createTableGen(data):
    t = PrettyTable(hrules=prettytable.ALL)
    t.field_names = ["Genero", "Numero"]
    t.max_width = 20
    for i in lt.iterator(data):
        t.add_row(i)
    return t

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

#-------------------------------------carga de datos-------------------------------------

    if int(inputs[0]) == 1:

        catalog = None
        control = newController()

        print("Cargando información de los archivos ....")

        delta_time, delta_memory = controller.loadData(control)

        first, last, Amazon_size, Disney_Size, \
            Hulu_size, Netflix_size = controller.generalServiceFirstLast(control)

        general_size = lt.size(control['model']['general'])

        tabla_count, tabla_data = createTableLoadData(first, last, Amazon_size, Disney_Size, Hulu_size, Netflix_size)

        print(f'\nEl total de datos cargados es: {general_size}')

        print(tabla_count, '\n')

        print(f'Los primeros y últimos 3 elementos de los datos cargados son:\n{tabla_data}')

        print(f'Timepo = {delta_time:.2f} ms, \nMemoria = {delta_memory:.2f} kB')


#-------------------------------------Requerimiento 1-------------------------------------

    elif int(inputs[0]) == 2:
        valid_input = False
        while not valid_input:
            try:
                ano = int(input("Ingrese el Año: "))
                valid_input = True
            except:
                print('Ingrese un año valido.')

        print(f'Buscando peliculas producidas en el año {ano}...')

        delta_time, delta_memory, pelisano_data = controller.buscarAno(control, ano, "Movie")
        if pelisano_data != None:
            pelisano_data, pelisano_count = pelisano_data
        else:
            pelisano_data = None

        if pelisano_data != None:

            print(f'\nSe encontraron {lt.size(pelisano_data)} peliculas producidas en el año {ano}.')
            tabla_pelisano, tabla_count = createTableGeneros(pelisano_data, pelisano_count)

            print(f"\nTabla detallada de las peliculas producidas en el año {ano}")
            print(tabla_pelisano)

        else:
            print(f'\nNo se encontraron peliculas producidas en el año {ano}')

        print(f"\nTiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")
        pass

#-------------------------------------Requerimiento 2-------------------------------------

    elif int(inputs[0]) == 3:
        while True:
            fecha = input("Fecha en la que se agrego (con formato %B %d, %Y): ")
            try:
                fecha = datetime.strptime(fecha, '%B %d, %Y')
                break
            except ValueError:
                print("\nFecha no valida, Por favor ingrese una fecha con el formato especificado.\n")

        print(f'Buscando series agregadas en la fecha: {fecha}...')

        delta_time, delta_memory, seriesfecha_data = controller.buscarFecha(control, fecha, "TV Show")
        if seriesfecha_data != None:
            seriesfecha_data, seriesfecha_count = seriesfecha_data
        else:
            seriesfecha_data = None

        if seriesfecha_data != None:

            print(f'\nSe encontraron {lt.size(seriesfecha_data)} series agregadas en la fecha: {fecha}.')
            tabla_seriesfecha, tabla_count = createTableREQ2(seriesfecha_data, seriesfecha_count)

            print(f"\nTabla detallada de las series agregadas en {fecha}")
            print(tabla_seriesfecha)

        else:
            print(f'\nNo se encontró contenido producido en {ano}')

        print(f"\nTiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")
        pass

#-------------------------------------Requerimiento 3-------------------------------------
#-----------------------------Santiago Florez Castañeda - 201912420-----------------------

    elif int(inputs[0]) == 4:
        valid_input = False
        while not valid_input:
            try:
                actor = input('Ingrese el nombre del actor que desea buscar: ')
                valid_input = True
            except:
                print('Ingrese un actor valido.')

        print(f'Buscando el contenido que coincide con el actor {actor}...')

        delta_time, delta_memory, actor_data = controller.buscarActor(control, actor)
        if actor_data != None:
            actor_data, actor_count = actor_data
        else:
            actor_data = None

        if actor_data != None:

            print(f'\nSe encontraron {lt.size(actor_data)} resultados con el actor {actor}.')
            tabla_generos, tabla_count = createTableGeneros(actor_data, actor_count)

            print("\nConteo de actor por tipo de contenido:")
            print(tabla_count)
            print(f"\nTabla detallada de contenido por actor: {actor}")
            print(tabla_generos)

        else:
            print(f'\nNo se encontró contenido con el actor {actor}')

        print(f"\nTiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")
        print(mp.size(control["model"]["actores"]))

#-------------------------------------Requerimiento 4-------------------------------------
#-----------------------------Elkin Rafael Cuello Romero - 202215037----------------------

    elif int(inputs[0]) == 5:
        valid_input = False
        while not valid_input:
            try:
                genero = input('Ingrese el genero que desea buscar: ')
                valid_input = True
            except:
                print('Ingrese un genero valido.')

        print(f'Buscando el contenido que coincide con el genero {genero}...')

        delta_time, delta_memory, genero_data = controller.buscarGenero(control, genero)
        if genero_data != None:
            genero_data, genero_count = genero_data
        else:
            genero_data = None

        if genero_data != None:

            print(f'\nSe encontraron {lt.size(genero_data)} resultados con el genero {genero}.')
            tabla_generos, tabla_count = createTableGeneros(genero_data, genero_count)

            print("\nConteo de generos por tipo de contenido:")
            print(tabla_count)
            print(f"\nTabla detallada de contenido por genero: {genero}")
            print(tabla_generos)

        else:
            print(f'\nNo se encontró contenido con el genero {genero}')

        print(f"\nTiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")

#-------------------------------------Requerimiento 5-------------------------------------
#----------------------------------Manuel Caro - 202020303--------------------------------

    elif int(inputs[0]) == 6:
        valid_input = False
        while not valid_input:
            try:
                pais = input("Ingrese el País: ")
                valid_input = True
            except:
                print('Ingrese un pais valido.')

        print(f'Buscando peliculas y programas producidos en {pais}...')

        delta_time, delta_memory, pais_data = controller.buscarPais(control, pais)
        if pais_data != None:
            pais_data, pais_count = pais_data
        else:
            pais_data = None

        if pais_data != None:

            print(f'\nSe encontraron {lt.size(pais_data)} peliculas y series producidass en {pais}.')
            tabla_paises, tabla_count = createTableGeneros(pais_data, pais_count)

            print("\nConteo por tipo de contenido del pais:")
            print(tabla_count)
            print(f"\nTabla detallada de contenido producido en {pais}")
            print(tabla_paises)

        else:
            print(f'\nNo se encontró contenido del pais {pais}')

        print(f"\nTiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")
        
        

#-------------------------------------Requerimiento 6-------------------------------------

    elif int(inputs[0]) == 7:
        valid_input = False
        while not valid_input:
            try:
                director = input('Ingrese el nombre del director que desea buscar: ')
                valid_input = True
            except:
                print('Ingrese un director valido.')

        print(f'Buscando el contenido que coincide con el director {director}...')

        delta_time, delta_memory, director_data = controller.buscarDirector(control, director)
        if director_data != None:
            director_data, director_countType, director_countPlat, generos = director_data
        else:
            director_data = None

        if director_data != None:

            print(f'\nSe encontraron {lt.size(director_data)} resultados con el director {director}.')
            tabla_generos, tabla_count = createTableGeneros(director_data, director_countType)
            tabla_countPlat=createTablePlat(director_countPlat)
            tabla_gene=createTableGen(generos)

            print("\nConteo de director por tipo de contenido:")
            print(tabla_count)
            print("\nConteo de director por tipo de plataforma:")
            print(tabla_countPlat)
            print("\nConteo de generos por director espesificado:")
            print(tabla_gene)
            print(f"\nTabla detallada de contenido por director: {director}")
            print(tabla_generos)

        else:
            print(f'\nNo se encontró contenido con el actor {director}')

        print(f"\nTiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")
        print(mp.size(control["model"]["directores"]))

#-------------------------------------Requerimiento 7-------------------------------------
    elif int(inputs[0]) == 8:
        num_top = 0
        while num_top <= 0:
            try:
                num_top = int(input("Ingrese el numero de top de generos que desea ver: "))
            except:
                print("El valor ingresado no es valido, intente de nuevo.")

        print(f'Buscando el top {num_top} de géneros con más contenido...')

        delta_time, delta_memory, top_generos= controller.topGeneros(control, num_top)
        top_generos, top_size = top_generos

        print(f'\nSe encontraron {top_size} generos en total.\nEl Top {num_top} de géneros con más contenido es:\n')

        tabla_count, tabla_data = createTableTops(top_generos)

        print(tabla_count, '\n', tabla_data)

        print(f"Tiempo [ms]: {delta_time:.3f}\nMemoria [kB]: {delta_memory:.3f}")

    elif int(inputs[0]) == 0:
        sys.exit(0)

    else:
        sys.exit(0)
sys.exit(0)
