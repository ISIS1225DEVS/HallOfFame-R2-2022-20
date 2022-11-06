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
from tabulate import tabulate
import os
from DISClib.ADT import list as lt
assert cf
from datetime import datetime

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# Funciones de Print

def printMovies(movies):
    size = lt.size(movies)
    if size:
        headers = [list(movies['first']['info'].keys())]
        table=[]
        for movie in lt.iterator(movies):
            table.append([movie['show_id'],movie['type'],movie['title'],movie['director'],movie['cast'],movie['country'],movie['date_added'],movie['release_year'],movie['rating'],movie['duration'],movie['listed_in'],movie['description'],movie['stream_service']])
        print(tabulate(table,headers[0],tablefmt="grid",maxcolwidths=14))    
        print('\n')    
    else:
        print('No se encontraron peliculas')

def printMoviesCant(movies,cant,head):
    size = lt.size(movies)
    if size:
        
        table=[]
        i=1
        for movie in lt.iterator(movies):
            headers = []
            for j in range(len(head)):
                headers.append(movie[head[j]])
            table.append(headers)
            if i==cant:
                break
            else:
                i+=1
        if size>=cant*2:
            i=0
            for movie in lt.iterator(movies):
                headers = []
                if size-i<=cant:
                    for j in range(len(head)):
                        headers.append(movie[head[j]])
                    table.append(headers)
                if size-i==0:
                    break
                else:
                    i+=1
                    
        print(tabulate(table,head,tablefmt="grid",maxcolwidths=7))    
        print('\n')

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Examinar las películas estrenadas en un año")
    print("2- Examinar los programas de televisión agregados en un año ")
    print("3- Encontrar el contenido donde participa un actor")
    print("4- Encontrar el contenido por un genero particular")
    print("5- Encontrar el contenido producido en un país")
    print("6- Encontrar el contenido con un director involucrado")
    print("7- Listar el TOP (N) de los géneros con más contenido")
    print("8- Listar el TOP (N) de los actores con más participaciones")
    print("9- Salir")

# Función crear controlador

def newController():
    control = controller.newController()
    return control

# Función Cargar Datos

def loadData(control,archiv,memory):
    movies= controller.loadData(control,archiv,memory)
    return movies

# Funciones Ejecutar opciones del menú

def playLoadData():
    print('\nCuántos datos desea cargar?')
    print('1: 0.5% de los datos')
    print('2: 5% de los datos')
    print('3: 10% de los datos')
    print('4: 20% de los datos')
    print('5: 30% de los datos')
    print('6: 50% de los datos')
    print('7: 80% de los datos')
    print('8: 100% de los datos')
    resp=int(input())
    if resp==1:
        archiv='small.csv'
    elif resp==2:
        archiv='5pct.csv'
    elif resp==3:
        archiv='10pct.csv'
    elif resp==4:
        archiv='20pct.csv'
    elif resp==5:
        archiv='30pct.csv'
    elif resp==6:
        archiv='50pct.csv'
    elif resp==7:
        archiv='80pct.csv'
    elif resp==8:
        archiv='large.csv'
    
    resp=input(('\nDesea Conocer la memoria utilizada? '))
    resp=castBoolean(resp)
    nf,am,hl,dy,features,time,memory= loadData(catalog,archiv,resp)
    os.system('cls')
    print('----------------------------------')
    print('Loaded straming service info: ')
    print('Total loaded titles: '+str(nf+am+hl+dy))
    print('Total features loaded: '+str(features))
    print('----------------------------------')
    table = [["Netflix",nf],["Amazon",am],["Disney",dy],['Hulu',hl]]
    headers = ["Stream Service", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))
    print('\n------ Content per stream service sorted by title ------')
    plats=['nf','am','dy','hl']
    plats_nombres=['Netflix','Amazon Prime','Disney Plus','Hulu']
    for i in range(4):
        print(f'\n{plats_nombres[i]}')
        print('First 3:')
        firstmovies = controller.getBestBooks(catalog, 3,plats[i])
        printMovies(firstmovies)
        print('Last 3:')
        lastmovies = controller.getLastMovies(catalog, 3,plats[i])
        printMovies(lastmovies)
    print(f'Tiempo de ejecución: {time:.3f}')
    print(f'Memoria Utilizada: {memory}')

def playReq1():
    anio= input("Ingrese el año de estreno que desea consultar, Ej. 2001: ")
    movies, time= controller.getReq1(catalog, anio)
    os.system('cls')
    print('============ Req No. 1 Inputs ============')
    print(f'Movies released in the year: "{anio}"')
    
    print('\n============ Req No. 1 Answer ============')
    print(f'There are only "{lt.size(movies)}" IPs (intelecual Properties) in Movie type released in the year  "{anio}"')
    head=['type','release_year','title','duration','stream_service','director','cast']
    printMoviesCant(movies,3,head) if lt.size(movies)>0 else print(f'\nThere are not "Movies" in {anio}\n')
    print('Tiempo de ejecución:',time,'ms')

def playReq2():
    date= input("Ingrese la fecha que desea consultar: ")
    series, time= controller.getReq2(catalog, date)
    os.system('cls')
    print('============ Req No. 2 Inputs ============')
    print(f'TV Shows released in the date: "{str(datetime.strptime(date, "%B %d, %Y"))[:10]}"')
    
    print('\n============ Req No. 2 Answer ============')
    if lt.size(series) < 6: 
        print(f'There are less than "6" "TV Show" in the date:  "{str(datetime.strptime(date, "%B %d, %Y"))[:10]}"')
    else:
        print(f'There are "{lt.size(series)}" "TV Show" in the date:  "{str(datetime.strptime(date, "%B %d, %Y"))[:10]}"')
    head=['type','date_added','title','duration','release_year','stream_service','director','cast']
    printMoviesCant(series,3,head) if lt.size(series)>0 else print(f'\nThere are not "TV show" in {str(datetime.strptime(date, "%B %d, %Y"))[:10]}\n')
    print('Tiempo de ejecución:',time,'ms')

def playReq3():
    actor=input('Ingrese el actor a consultar Ej. "Bing Crosby": ')
    movies,TV, Peli,time = controller.getReq3(catalog, actor)
    os.system('cls')

    print('============ Req No. 3 Inputs ============')
    print(f'Content with "{actor}" in the cast')
    
    print('\n============ Req No. 3 Answer ============')
    print(f'------ "{actor}" cast participation count ------')
    table = [["TV Show",TV],["Movies",Peli]]
    headers = ["Type", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))

    print('\n------ participation details ------')
    print(f'There are less than 6 participations of "{actor}" on record') if lt.size(movies)<6 else print(f'The first 3 and last 3 IPs with "{actor}" in the cast are:')

    head = ['release_year','title','duration','director','stream_service','type','cast','country','rating','listed_in','description']
    printMoviesCant(movies,3,head) if lt.size(movies)>0 else print(f'There are not "TV Shows" with {actor}')
    print('Tiempo de ejecución:',time,'ms')

def playReq4():
    genero= input("Ingrese el genero que desea consultar: ")
    lista_generos, movies, shows, time= controller.getReq4(catalog, genero)
    os.system('cls')

    print('============ Req No. 4 Inputs ============')
    print(f'The content is "listed in " {genero}')
    
    print('\n============ Req No. 4 Answer ============')
    print(f'------ {genero} content type count ------')
    head= ['type','count']
    table = [["Movies",movies],["TV Show",shows]] 
    print(tabulate(table, head, tablefmt="grid"))
    
    print('\n------ Content Details ------')
    print(f'There {lt.size(lista_generos)} are IPs (Intelectual Properties) with the "{genero}" label')
    if lt.size(lista_generos) < 6: 
        print(f'There are less than 6 "listed_in" {genero} on record')
    else:
        print(f'The first 3 and last 3 IPs in range are:')
    head2=['release_year','title','duration','stream_service','director','type','cast','country','rating','listed_in','description']
    printMoviesCant(lista_generos,3,head2) if lt.size(lista_generos)>0 else print(f'\nThere are not content for "{genero}"\n')
    print('Tiempo de ejecución:',time,'ms')

def playReq5():
    pais=input('Ingrese el país a consultar Ej. "United States": ')
    movies, TV,Peli,time = controller.getReq5(catalog, pais)
    os.system('cls')
    print('============ Req No. 5 Inputs ============')
    print(f'The content produced in the "{pais}"')
    
    print('\n============ Req No. 5 Answer ============')
    print(f'------ "{pais}" content type production count ------')
    table = [["Movies",Peli],["TV Show",TV]]
    headers = ["Type", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))

    print('\n------ Content details ------')
    print(f'There {lt.size(movies)} are IPs (Intelectual Properties) with the "{pais}" label')
    print(f'There are less than 6 produced in "{pais}" on record') if (lt.size(movies))<6 else print(f'The first 3 and last 3 IPs in produced in "{pais}" are:')

    head=['release_year','title','duration','stream_service','director','type','cast','country','rating','listed_in','description']
    printMoviesCant(movies,3,head) if lt.size(movies)>0 else print(f'There are not content in {pais}')
    print('Tiempo de ejecución:',time,'ms')

def playReq6():
    director = input("Digita el director: ")
    num_todo_director,num_movies_director, num_shows_director, numero_generos_autor, plataformas, filtro_director,timesito= controller.getReq6(catalog, director)
    os.system('cls')
    print('============ Req No. 6 Inputs ============')
    print(f'Find the content with "{director}" as ""director" ')
    
    print('\n============ Req No. 6 Answer ============')
    print(f'------ "{director}" Content type count ------')
    headers=["Type", "Count"]
    table1=[["Movies",num_movies_director],["Shows",num_shows_director]]
    print(tabulate(table1, headers, tablefmt="grid"))

    print(f'\n------ "{director}" Streaming content type count ------')
    headers2=["Service_name", "movie"]
    print(tabulate(plataformas,headers2,tablefmt="grid",maxcolwidths=18))

    print(f'\n------ "{director}" Listed in count ------')
    print("There are only", len(numero_generos_autor),"tags ib 'listed_in'")
    print('The first 3 and last 3 tags in range are:')
    headers3=['listed_in','count']
    print(tabulate(numero_generos_autor,headers3,tablefmt='grid'))
    
    print(f'\n------ "{director}" content details ------')
    print("There are only", num_todo_director, "IPs (Intelectual Properties) with", director, "as director")
    print('The first 3 and last 3 tags in range are:')
    printMoviesCant(filtro_director,3,['release_year','title','duration','director','stream_service','type','cast','country', 'rating','listed_in','description'])
    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

def playReq7():
    top_n=int(input("Digite el número (N) de géneros a identificar (ej.: TOP 3, 5, 10 o 20): ")) 
    cuenta_actores,info_actores,timesito=controller.getReq7(catalog, top_n)
    
    os.system('cls')
    print('============ Req No. 7 Inputs ============')
    print(f'the TOP "{top_n}" genres in "listed_in" ')
    
    print('\n============ Req No. 7 Answer ============')
    print(f'There are "{lt.size(cuenta_actores)}" tags participating for the TOP {top_n} genres for "listed_in"')

    print(f'\n------ The TOP "{top_n}" listed_in tags are: ------')
    print(f'The TOP "{top_n}" actors are:')
    table = []
    for i in range(top_n):
        table.append([cuenta_actores['elements'][i][0],cuenta_actores['elements'][i][1]])
    headers = ["Listed_in", "Count"]
    print(tabulate(table, headers, tablefmt="grid"))

    print(f'\n------ Top actors participations details: ------')
    print(f'The TOP "{top_n}" actors are:')
    headers2 = ["type", 'count']
    headerspro=['rank','listed_in','count','type','stream_service']
    headers3=['stream_service','count']
    
    tablepro=[]
    k=1
    for i in info_actores.keys():
        table2=[]
        table3=[]
        table2.append(['Movie',info_actores[i]['Movie']])
        table2.append(['TV Show',info_actores[i]['TV Show']])
        table3.append(['netflix',info_actores[i]['netflix']])
        table3.append(['amazon',info_actores[i]['amazon prime']])
        table3.append(['hulu',info_actores[i]['hulu']])
        table3.append(['disney',info_actores[i]['disney plus']])
        tablepro.append([k,i,cuenta_actores['elements'][k-1][1],tabulate(table2,headers2,tablefmt='plain'),tabulate(table3,headers3,tablefmt='plain')])
        k+=1
    print(tabulate(tablepro,headerspro,tablefmt='grid'))
    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

def playReq8():
    top_n=int(input('Que top desea consultar: '))
    resp=input('¿Desea filtrar la búsqueda por un género en específico? (1: Si 2:No) ')
    table = []
    if resp=='1':
        genero=input('Escriba el genero a consultar: ')
        cuenta_actores,info_actores,timesito=controller.getReq8(catalog,top_n,genero)
        j=0
        for i in info_actores.keys():
            table.append([cuenta_actores['elements'][j][0],cuenta_actores['elements'][j][1],genero])
            j+=1
    else:
        genero='"Genero no especifico"'
        cuenta_actores,info_actores,timesito=controller.getReq8_2(catalog,top_n)
        j=0
        for i in info_actores.keys():
            max_key = max(info_actores[i]['genero'], key = info_actores[i]['genero'].get)
            table.append([cuenta_actores['elements'][j][0],cuenta_actores['elements'][j][1],max_key])
            j+=1
    os.system('cls')
    print('============ Req No. 8 (BONUS) Inputs ============')
    print(f'Ranking the TOP "{top_n}" actors in "cast" with content listed in {genero} ')
    
    print('\n============ Req No. 8 (BONUS) Answer ============')
    print(f'There are "{lt.size(cuenta_actores)}" actors participating for the TOP {top_n} actors in "cast" with content listed in {genero}')

    print(f'\n------ The TOP "{top_n}" participations are: ------')
    print(f'The TOP "{top_n}" actors in {genero} are:')
    headers = ["Actor", "Count", 'Listed_in']
    print(tabulate(table, headers, tablefmt="grid"))

    print(f'\n------ Top actors participations details: ------')
    print(f'The TOP "{top_n}" actors are:')
    headers2 = ["stream_service", "type", 'count']
    headers3=['','actor','content_type','count_movies','count_tv_shows']
    plats=['netflix','amazon prime','hulu','disney plus']
    table3=[]
    table4=[['TV Show'],['Movie']]
    k=1
    for j in info_actores.keys():
        table2 = []
        for i in plats:
            table5=[[info_actores[j][i]['TV Show']],[info_actores[j][i]['Movie']]]
            table2.append([i,tabulate(table4,tablefmt='plain'),tabulate(table5, tablefmt='plain')])
        table3.append([k,j,tabulate(table2,headers2,tablefmt='plain'),info_actores[j]['Movie'],info_actores[j]['TV Show']])
        k+=1
    print(tabulate(table3, headers3, tablefmt="grid"))

    print(f'\n------ Top actors colaborations details: ------')
    print(f'The TOP "{top_n}" actors are:') 
    headers_colab=['','actor','colaborations_cast','colaboration_director']
    table_colab=[]
    i=1
    for j in info_actores:
        table_colab.append([i,j,info_actores[j]['colaborations'],info_actores[j]['direct_colab']])
        i+=1
    print(tabulate(table_colab,headers_colab,tablefmt='grid',maxcolwidths=60))

    print(f'\n--------- Top actors content details: ---------')
    head12=['type','release_year','title','duration','listed_in']
    for i in info_actores:
        print(f'------- Actor {i} Movies and TV Shows ------')
        printMoviesCant(info_actores[i]['movies'],3,head12) if lt.size(info_actores[i]['movies'])>0 else print(f'{i} no ha participado en películas\n')
        printMoviesCant(info_actores[i]['tvshow'],3,head12) if lt.size(info_actores[i]['tvshow'])>0 else print(f'{i} no ha participado en programas de TV\n')

    print(f'\nEl tiempo de ejecución es: {timesito} ms\n')

# Funciones Auxiliares

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
        print("Cargando información de los archivos ....")
        catalog = newController()
        playLoadData() 
    elif int(inputs[0])==1:
        playReq1()
    elif int(inputs[0])==2:
        playReq2()
    elif int(inputs[0])==3:
        playReq3()
    elif int(inputs[0])==4:
        playReq4()
    elif int(inputs[0])==5:
        playReq5()
    elif int(inputs[0])==6:
        playReq6()
    elif int(inputs[0])==7:
        playReq7()
    elif int(inputs[0])==8:
        playReq8() 
    else:
        sys.exit(0)



