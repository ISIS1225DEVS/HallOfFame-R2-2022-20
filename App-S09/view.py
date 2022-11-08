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

from turtle import title
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from prettytable import PrettyTable,ALL
from DISClib.ADT import map as mp



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
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar las peliculas estrenadas en un período de tiempo")
    print("3- Consultar los programas de televisión agregados en un período de tiempo")
    print("4- Consultar contenido donde participa un actor")
    print("5- Consultar contenido por un género especifico")
    print("6- Consultar contenido producido en un país")
    print("7- Consultar contenido con un director involucrado")
    print("8- Consultar el TOP (N) de los géneros con más contenido")
    print("9- Seleccionar represnetación de lista, tamnio de muestra y algoritmo de ordenamiento")
    print("0- Salir")

def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    Amazon, Disney, Hulu, Netflix ,time, mem = controller.loadData(control)
    return Amazon,  Disney, Hulu, Netflix, time, mem 

def sizetotalarch():
    size= controller.SizeTotal(control)
    return size

def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if len(answer) == 6:
        print("Tiempo [ms]: ", f"{answer[4]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[5]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[4]:.3f}")

def printRequerimmiento1Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 4:
        print("Tiempo [ms]: ", f"{answer[2]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[3]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[2]:.3f}")

def printRequerimmiento2Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 3:
        print("Tiempo [ms]: ", f"{answer[1]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[1]:.3f}")

def printRequerimmiento3Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 5:
        print("Tiempo [ms]: ", f"{answer[3]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[4]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[3]:.3f}")

def printRequerimmiento4Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 5:
        print("Tiempo [ms]: ", f"{answer[3]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[4]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[3]:.3f}")

def printRequerimmiento5Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 5:
        print("Tiempo [ms]: ", f"{answer[3]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[4]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[3]:.3f}") 

def printRequerimmiento6Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 6:
        print("Tiempo [ms]: ", f"{answer[4]:.2f}", "||",
              "Memoria [kB]: ", f"{answer[5]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[4]:.3f}")

def printRequerimmiento7Answer(answer):
    """
    Imprime los datos de tiempo y memoria de cada Req.
    """
    if len(answer) == 3:
        print("Tiempo [ms]: ", f"{answer[1]:.2f}", "||",
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


control= newController()

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.loadData(control, memflag=mem)
        printLoadDataAnswer(answer)
        
        if len(answer) == 6:
            Amaz, Dis, Hul, Net, time, memsize = answer
        else:
             Amaz, Dis, Hul, Net, time = answer

        tabla_stream= PrettyTable()
        tabla_stream.field_names = ["stream_service", "count"]
        tabla_stream.add_row(["amazon", Amaz])
        tabla_stream.add_row(["netflix", Net])
        tabla_stream.add_row(["hulu", Hul])
        tabla_stream.add_row(["disney", Dis])

        print(tabla_stream)
        
        print("Los primeros 3 y los últimos 3 shows de Amazon son...")
        print("                                                       ")
        tabla_amaz = PrettyTable()
        tabla_amaz.field_names = ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]
        tabla_amaz._max_witdh = {"cast":13}
        for i in range(1, 4):
            tabla_amaz.add_row([lt.getElement(control["model"]["Amazon"], i)["show_id"],
                 lt.getElement(control["model"]["Amazon"], i)["type"],
                 lt.getElement(control["model"]["Amazon"], i)["title"],
                 lt.getElement(control["model"]["Amazon"], i)["director"],
                 lt.getElement(control["model"]["Amazon"], i)["cast"],
                 lt.getElement(control["model"]["Amazon"], i)["country"],
                 lt.getElement(control["model"]["Amazon"], i)["date_added"],
                 lt.getElement(control["model"]["Amazon"], i)["release_year"],
                 lt.getElement(control["model"]["Amazon"],i)["rating"],
                 lt.getElement(control["model"]["Amazon"], i)["duracionstr"],
                 lt.getElement(control["model"]["Amazon"], i)["listed_in"],
                 lt.getElement(control["model"]["Amazon"], i)["description"][0:50]+"..."])
        print("                                                         ")
        for i in range(-2, 1):
            tabla_amaz.add_row([lt.getElement(control["model"]["Amazon"], i)["show_id"],
                 lt.getElement(control["model"]["Amazon"], i)["type"],
                 lt.getElement(control["model"]["Amazon"], i)["title"],
                 lt.getElement(control["model"]["Amazon"], i)["director"],
                 lt.getElement(control["model"]["Amazon"], i)["cast"],
                 lt.getElement(control["model"]["Amazon"], i)["country"],
                 lt.getElement(control["model"]["Amazon"], i)["date_added"],
                 lt.getElement(control["model"]["Amazon"], i)["release_year"],
                 lt.getElement(control["model"]["Amazon"],i)["rating"],
                 lt.getElement(control["model"]["Amazon"], i)["duracionstr"],
                 lt.getElement(control["model"]["Amazon"], i)["listed_in"],
                 lt.getElement(control["model"]["Amazon"], i)["description"][0:50]+"..."])
        print(tabla_amaz)
        print("                                                          ")
        
        tabla_dis = PrettyTable()
        tabla_dis.field_names = ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]
        tabla_dis._max_witdh = {"cast":13}
        print("Los primeros 3 y los últimos 3 shows de Disney son...")
        print("                                                       ")
        for i in range(1, 4):
           tabla_dis.add_row([lt.getElement(control["model"]["Disney"], i)["show_id"],
                 lt.getElement(control["model"]["Disney"], i)["type"],
                 lt.getElement(control["model"]["Disney"], i)["title"],
                 lt.getElement(control["model"]["Disney"], i)["director"],
                 lt.getElement(control["model"]["Disney"], i)["cast"],
                 lt.getElement(control["model"]["Disney"], i)["country"],
                 lt.getElement(control["model"]["Disney"], i)["date_added"],
                 lt.getElement(control["model"]["Disney"], i)["release_year"],
                 lt.getElement(control["model"]["Disney"],i)["rating"],
                 lt.getElement(control["model"]["Disney"], i)["duracionstr"],
                 lt.getElement(control["model"]["Disney"], i)["listed_in"],
                 lt.getElement(control["model"]["Disney"], i)["description"][0:50]+"..."])
        print("                                                         ")
        for i in range(-2, 1):
            tabla_dis.add_row([lt.getElement(control["model"]["Disney"], i)["show_id"],
                 lt.getElement(control["model"]["Disney"], i)["type"],
                 lt.getElement(control["model"]["Disney"], i)["title"],
                 lt.getElement(control["model"]["Disney"], i)["director"],
                 lt.getElement(control["model"]["Disney"], i)["cast"],
                 lt.getElement(control["model"]["Disney"], i)["country"],
                 lt.getElement(control["model"]["Disney"], i)["date_added"],
                 lt.getElement(control["model"]["Disney"], i)["release_year"],
                 lt.getElement(control["model"]["Disney"],i)["rating"],
                 lt.getElement(control["model"]["Disney"], i)["duracionstr"],
                 lt.getElement(control["model"]["Disney"], i)["listed_in"],
                 lt.getElement(control["model"]["Disney"], i)["description"][0:50]+"..."])
        print(tabla_dis)
        print("                                                          ")
        
        print("Los primeros 3 y los últimos 3 shows de Hulu son...")
        print("                                                       ")
        tabla_hul = PrettyTable()
        tabla_hul.field_names = ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]
        tabla_hul._max_witdh = {"cast":13}
        print("                                                       ")
        for i in range(1, 4):
            tabla_hul.add_row([lt.getElement(control["model"]["Hulu"], i)["show_id"],
                 lt.getElement(control["model"]["Hulu"], i)["type"],
                 lt.getElement(control["model"]["Hulu"], i)["title"],
                 lt.getElement(control["model"]["Hulu"], i)["director"],
                 lt.getElement(control["model"]["Hulu"], i)["cast"],
                 lt.getElement(control["model"]["Hulu"], i)["country"],
                 lt.getElement(control["model"]["Hulu"], i)["date_added"],
                 lt.getElement(control["model"]["Hulu"], i)["release_year"],
                 lt.getElement(control["model"]["Hulu"],i)["rating"],
                 lt.getElement(control["model"]["Hulu"], i)["duracionstr"],
                 lt.getElement(control["model"]["Hulu"], i)["listed_in"],
                 lt.getElement(control["model"]["Hulu"], i)["description"][0:50]+"..."])
        print("                                                         ")
        for i in range(-2, 1):
            tabla_hul.add_row([lt.getElement(control["model"]["Hulu"], i)["show_id"],
                 lt.getElement(control["model"]["Hulu"], i)["type"],
                 lt.getElement(control["model"]["Hulu"], i)["title"],
                 lt.getElement(control["model"]["Hulu"], i)["director"],
                 lt.getElement(control["model"]["Hulu"], i)["cast"],
                 lt.getElement(control["model"]["Hulu"], i)["country"],
                 lt.getElement(control["model"]["Hulu"], i)["date_added"],
                 lt.getElement(control["model"]["Hulu"], i)["release_year"],
                 lt.getElement(control["model"]["Hulu"],i)["rating"],
                 lt.getElement(control["model"]["Hulu"], i)["duracionstr"],
                 lt.getElement(control["model"]["Hulu"], i)["listed_in"],
                 lt.getElement(control["model"]["Hulu"], i)["description"][0:50]+"..."])
        print(tabla_hul)
        print("                                                          ")
        
        print("Los primeros 3 y los últimos 3 shows de Netflix son...")
        print("                                                       ")
        tabla_net = PrettyTable()
        tabla_net.field_names = ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration", "listed_in", "description"]
        tabla_net._max_witdh = {"cast":13}
        print("                                                       ")
        for i in range(1, 4):
            tabla_net.add_row([lt.getElement(control["model"]["Netflix"], i)["show_id"],
                 lt.getElement(control["model"]["Netflix"], i)["type"],
                 lt.getElement(control["model"]["Netflix"], i)["title"],
                 lt.getElement(control["model"]["Netflix"], i)["director"],
                 lt.getElement(control["model"]["Netflix"], i)["cast"],
                 lt.getElement(control["model"]["Netflix"], i)["country"],
                 lt.getElement(control["model"]["Netflix"], i)["date_added"],
                 lt.getElement(control["model"]["Netflix"], i)["release_year"],
                 lt.getElement(control["model"]["Netflix"],i)["rating"],
                 lt.getElement(control["model"]["Netflix"], i)["duracionstr"],
                 lt.getElement(control["model"]["Netflix"], i)["listed_in"],
                 lt.getElement(control["model"]["Netflix"], i)["description"][0:50]+"..."])
        print("                                                         ")
        for i in range(-2, 1):
            tabla_net.add_row([lt.getElement(control["model"]["Netflix"], i)["show_id"],
                 lt.getElement(control["model"]["Netflix"], i)["type"],
                 lt.getElement(control["model"]["Netflix"], i)["title"],
                 lt.getElement(control["model"]["Netflix"], i)["director"],
                 lt.getElement(control["model"]["Netflix"], i)["cast"],
                 lt.getElement(control["model"]["Netflix"], i)["country"],
                 lt.getElement(control["model"]["Netflix"], i)["date_added"],
                 lt.getElement(control["model"]["Netflix"], i)["release_year"],
                 lt.getElement(control["model"]["Netflix"],i)["rating"],
                 lt.getElement(control["model"]["Netflix"], i)["duracionstr"],
                 lt.getElement(control["model"]["Netflix"], i)["listed_in"],
                 lt.getElement(control["model"]["Netflix"], i)["description"][0:50]+"..."])
        print(tabla_net)
        print("                                                          ")
    
    #Listas de peliculas en un anio
    
    elif int(inputs[0]) == 2: 
        """
        Se crea una lista que registra las peliculas estrenadas en un anio específico. La lista esta 
        ordenada  por el criterio compuesto del título (title) y la duración(duration)
        """
        anio=int(input("Ingrese el anio a consultar(con formato AAAA): "))
        print("Consultando películas estrenadas en el anio "+str(anio)+ "....") 
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.peliculasbyanio(control,anio, memflag=mem)
        printRequerimmiento1Answer(answer)
        if len(answer) == 4: 
            Nopeliculas, listapeliculas, time, memsize = answer
        else:
            Nopeliculas, listapeliculas, time = answer
       
        tam_list= lt.size(listapeliculas)


        tabla_req1 = PrettyTable()
        tabla_req1.field_names = ["type", "release_year", "title", "duration", "stream_service", "director", "cast"]

        if tam_list==0:
            print("No se encontraron registros de peliculas estrenadas en el anio consultado")
        elif tam_list <=6:
            print("Se encontraron "+str(Nopeliculas)+ " Movies estrenadas en el anio "+str(anio))
            for i in range(1,tam_list+1):
                tabla_req1.add_row([lt.getElement(listapeliculas, i)["type"],
                    lt.getElement(listapeliculas, i)["release_year"],
                    lt.getElement(listapeliculas, i)["title"],
                    lt.getElement(listapeliculas, i)["duracionstr"],
                    lt.getElement(listapeliculas, i)["stream_service"],
                    lt.getElement(listapeliculas, i)["director"],
                    lt.getElement(listapeliculas, i)["cast"]])
            
        else:
            print("Se encontraron "+str(Nopeliculas)+ " Movies estrenadas en el anio "+str(anio))
            for i in range(1, 4):
                tabla_req1.add_row([lt.getElement(listapeliculas, i)["type"],
                    lt.getElement(listapeliculas, i)["release_year"],
                    lt.getElement(listapeliculas, i)["title"],
                    lt.getElement(listapeliculas, i)["duracionstr"],
                    lt.getElement(listapeliculas, i)["stream_service"],
                    lt.getElement(listapeliculas, i)["director"],
                    lt.getElement(listapeliculas, i)["cast"]])
            
            for i in range(-2, 1):
                tabla_req1.add_row([lt.getElement(listapeliculas, i)["type"],
                    lt.getElement(listapeliculas, i)["release_year"],
                    lt.getElement(listapeliculas, i)["title"],
                    lt.getElement(listapeliculas, i)["duracionstr"],
                    lt.getElement(listapeliculas, i)["stream_service"],
                    lt.getElement(listapeliculas, i)["director"],
                    lt.getElement(listapeliculas, i)["cast"]])
        
        print(tabla_req1)

        

    elif int(inputs[0]) == 3:  
        date1 = input("Ingrese la fecha a consultar: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.Show_by_time(control, date1, memflag=mem)
        printRequerimmiento2Answer(answer)
        if len(answer) == 3: 
            list1, time, memsize = answer
        else:
            list1, time = answer
        
        tam_list= lt.size(list1)
        print("\n")
        print("----------------Requerimiento No2 Inputs---------------")
        print("\n")
        print("TV Shows released in the date: " + date1)
        print("\n")
        print("----------------Requerimiento No2 Answers---------------")
        print("\n")
        print("There are " + str(lt.size(list1)) + " 'TV Show' in the date: " + date1 )
        print("\n")
        print("\n")                                                         
        tabla = PrettyTable()
        tabla.field_names = ["type","date_added","title","duration","release_year","stream_service","director","cast"]
        tabla._max_witdh = {"cast":13}
        if lt.size(list1) > 6:
            print("The first 3 an the last 3 in range are: ")
            first = lt.subList(list1,1,3)
            last = lt.subList(list1,lt.size(list1)-2,3)
            for i in lt.iterator(first):
                if i["director"] == "":
                    i["director"] = "Unknown"
                list_cast = str(i["cast"])
                x = list_cast.replace("[", "")
                y = x.replace("'", "")
                z = y.replace("]", "")
                if z == "":
                    z = "Unknown"
                tabla.add_row([i["type"],i["date_added"],i["title"],i["duration"],i["release_year"],i["stream_service"],i["director"],z])
            for i in lt.iterator(last):
                if i["director"] == "":
                    i["director"] = "Unknown"
                list_cast = str(i["cast"])
                x = list_cast.replace("[", "")
                y = x.replace("'", "")
                z = y.replace("]", "")
                if z == "":
                    z = "Unknown"
                tabla.add_row([i["type"],i["date_added"],i["title"],i["duration"],i["release_year"],i["stream_service"],i["director"],z])
        else:
            for i in lt.iterator(list1):
                if i["director"] == "":
                    i["director"] = "Unknown"
                list_cast = str(i["cast"])
                x = list_cast.replace("[", "")
                y = x.replace("'", "")
                z = y.replace("]", "")
                if z == "":
                    z = "Unknown"
                tabla.add_row([i["type"],i["date_added"],i["title"],i["duration"],i["release_year"],i["stream_service"],i["director"],z])
        print(tabla)
    
    
    #Peliculas y shows filtrado por actores.

    elif int(inputs[0]) == 4:
        """
        Se busca contenido en donde participe un actor en especifico, indicado por parametro por el usuario. Se crea
        una lista ordenada alfabeticamente por el titulo.
        """
        print("Consultando contenido por actor ....")
        actorname = input("Nombre del autor a buscar: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.Shows_by_Actor(control, actorname, memflag=mem)
        printRequerimmiento3Answer(answer)
        if len(answer) == 5: 
            lista, num_peliculas, num_programas, time, memsize = answer
        else:
             lista, num_peliculas, num_programas, time = answer
        tam_list= lt.size(lista)
        if tam_list==0:
            print("El actor no se encuentra registrado ninguna plataforma de Streaming")
        elif tam_list <=6:     
            tipo_req3 = PrettyTable()
            tipo_req3.field_names = ["Movies", "TV Shows"]
            tipo_req3.add_row([num_peliculas, num_programas])
            print(tipo_req3)
            tabla_req3 = PrettyTable()
            tabla_req3.field_names = ["type", "title", "release_year", "director", "stream_service", "duration", "cast","country", "listed_in", "description"]
            for i in range (1,tam_list+1):
                 tabla_req3.add_row([lt.getElement(lista, i)["type"],
                    lt.getElement(lista, i)["title"],
                    lt.getElement(lista, i)["release_year"],
                    lt.getElement(lista, i)["director"],
                    lt.getElement(lista, i)["stream_service"],
                    lt.getElement(lista,i)["duration"],
                    lt.getElement(lista, i)["cast"],
                    lt.getElement(lista, i)["country"],
                    lt.getElement(lista, i)["listed_in"],
                    lt.getElement(lista, i)["description"][0:50]+"..."])
            print(tabla_req3)
            print("                                                         ")
        else:
            tipo_req3 = PrettyTable()
            tipo_req3.field_names = ["Movies", "TV Shows"]
            tipo_req3.add_row([num_peliculas, num_programas])
            print(tipo_req3)
            tabla_req3 = PrettyTable()
            tabla_req3.field_names = ["type", "title", "release_year", "director", "stream_service", "duration", "cast","country", "listed_in", "description"]
            for i in range(1, 4):
                tabla_req3.add_row([lt.getElement(lista, i)["type"],
                    lt.getElement(lista, i)["title"],
                    lt.getElement(lista, i)["release_year"],
                    lt.getElement(lista, i)["director"],
                    lt.getElement(lista, i)["stream_service"],
                    lt.getElement(lista,i)["duration"],
                    lt.getElement(lista, i)["cast"],
                    lt.getElement(lista, i)["country"],
                    lt.getElement(lista, i)["listed_in"],
                    lt.getElement(lista, i)["description"][0:50]+"..."])
            print("                                                         ")
            for i in range(-2, 1):
                tabla_req3.add_row([lt.getElement(lista, i)["type"],
                    lt.getElement(lista, i)["title"],
                    lt.getElement(lista, i)["release_year"],
                    lt.getElement(lista, i)["director"],
                    lt.getElement(lista, i)["stream_service"],
                    lt.getElement(lista,i)["duration"],
                    lt.getElement(lista, i)["cast"],
                    lt.getElement(lista, i)["country"],
                    lt.getElement(lista, i)["listed_in"],
                    lt.getElement(lista, i)["description"][0:50]+"..."])
            print(tabla_req3)
            print("                                                         ")
        

    #Contenido por un genero especifico

    elif int(inputs[0]) == 5:
        """
        Se crea una lista de peliculas y shows de television que se clasifican por un genero especifico, dado por parametro
        por el usuario. La lista esta ordenada alfabeticamente por titulos.
        """
        print("Consultando contenido por género ....")
        genero = input("Tipo de genero a buscar: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.contentbyGenero(control,genero,memflag=mem)
        printRequerimmiento4Answer(answer)
        if len(answer) == 5: 
            genContent, Peliculas, Shows, time, memsize = answer
        else:
            genContent, Peliculas, Shows, time = answer

        tamanio= lt.size(genContent)
        if tamanio==0:
            print("No hay contenido relacionado con este tipo de genero.")
        elif tamanio <=6:     
            tipo_req4 = PrettyTable()
            tipo_req4.field_names = ["Movies", "TV Shows"]
            tipo_req4.add_row([Peliculas, Shows])
            print(tipo_req4)
            tabla_req4 = PrettyTable()
            tabla_req4.field_names = ["release_year", "title", "duration", "stream_service", "director", "type", "cast","country","rating", "listed_in", "description"]
            for i in range (tamanio):
                tabla_req4.add_row([lt.getElement(genContent, i)["release_year"],
                    lt.getElement(genContent, i)["title"],
                    lt.getElement(genContent, i)["duration"],
                    lt.getElement(genContent, i)["stream_service"],
                    lt.getElement(genContent, i)["director"],
                    lt.getElement(genContent,i)["type"],
                    lt.getElement(genContent, i)["cast"],
                    lt.getElement(genContent, i)["country"],
                    lt.getElement(genContent, i)["rating"],
                    lt.getElement(genContent, i)["listed_in"],
                    lt.getElement(genContent, i)["description"][0:50]+"..."])
            
        else:
            tipo_req4 = PrettyTable()
            tipo_req4.field_names = ["Movies", "TV Shows"]
            tipo_req4.add_row([Peliculas, Shows])
            print(tipo_req4)
            tabla_req4 = PrettyTable()
            tabla_req4.field_names = ["release_year", "title", "duration", "stream_service", "director", "type", "cast","country","rating", "listed_in", "description"]
            for i in range(1, 4):
                tabla_req4.add_row([lt.getElement(genContent, i)["release_year"],
                    lt.getElement(genContent, i)["title"],
                    lt.getElement(genContent, i)["duration"],
                    lt.getElement(genContent, i)["stream_service"],
                    lt.getElement(genContent, i)["director"],
                    lt.getElement(genContent,i)["type"],
                    lt.getElement(genContent, i)["cast"],
                    lt.getElement(genContent, i)["country"],
                    lt.getElement(genContent, i)["rating"],
                    lt.getElement(genContent, i)["listed_in"],
                    lt.getElement(genContent, i)["description"][0:50]+"..."])
            print("                                                         ")
            for i in range(-2, 1):
                tabla_req4.add_row([lt.getElement(genContent, i)["release_year"],
                    lt.getElement(genContent, i)["title"],
                    lt.getElement(genContent, i)["duration"],
                    lt.getElement(genContent, i)["stream_service"],
                    lt.getElement(genContent, i)["director"],
                    lt.getElement(genContent,i)["type"],
                    lt.getElement(genContent, i)["cast"],
                    lt.getElement(genContent, i)["country"],
                    lt.getElement(genContent, i)["rating"],
                    lt.getElement(genContent, i)["listed_in"],
                    lt.getElement(genContent, i)["description"][0:50]+"..."])
            
        print(tabla_req4)
        print("                                                         ")

    #Contenido por pais especifico.

    elif int(inputs[0]) == 6:
        """
        Se crea una lista donde el pais de produccion sea el mismo que el indicado por parametro. 
        La lista esta ordenada alfabeticamente por titulo.
        """
        country = input("Ingrese el pais: ")
        print("Consultando contenido por pais ....")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.MoviesByCountry(control,country, memflag=mem)
        printRequerimmiento5Answer(answer)
        if len(answer) == 5: 
            country_list, Movie, tv, time, memsize = answer
        else:
            country_list, Movie, tv, time = answer
        
        print("-----------------------------------------------------------------------------")
        print("Paises Agregados: "+ str(controller.CountrySize(control)))
        print("-----------------------------------------------------------------------------")
        print("No. de Shows por pais: "+ str(lt.size(country_list)))
        print("="*15, "req No. 5 Answer", "="*15)
        print("-"*6,country, "content type production count", "-"*6)
        print("\n")
        tipo_req5 = PrettyTable()
        tipo_req5.field_names = ["Movies", "TV Shows"]
        tipo_req5.add_row([Movie, tv])
        print(tipo_req5)
        print("\n")
        print("-"*6,"Content details","-"*6)
        print("There are "+ str(Movie+tv)+ " IPs (Intelectual Properties) produced in "+country)
        print("\n")
        
        tabla_req5 = PrettyTable()
        tabla_req5.field_names = ["release_year", "title", "duration", "stream_service", "director", "type","cast", "country","rating","listed_in", "description"]
        if lt.size(country_list) >= 6:
            for i in range(1,4):
                tabla_req5.add_row([lt.getElement(country_list, i)["release_year"],
                    lt.getElement(country_list, i)["title"],
                    lt.getElement(country_list, i)["duration"],
                    lt.getElement(country_list, i)["stream_service"],
                    lt.getElement(country_list,i)["director"],
                    lt.getElement(country_list, i)["type"],
                    lt.getElement(country_list, i)["cast"],
                    lt.getElement(country_list, i)["country"],
                    lt.getElement(country_list, i)["rating"],
                    lt.getElement(country_list, i)["listed_in"],
                    lt.getElement(country_list, i)["description"][0:50]+"..."])
                print("\n")
            for i in range(lt.size(country_list)-2,lt.size(country_list)+1): 
                tabla_req5.add_row([lt.getElement(country_list, i)["release_year"],
                    lt.getElement(country_list, i)["title"],
                    lt.getElement(country_list, i)["duration"],
                    lt.getElement(country_list, i)["stream_service"],
                    lt.getElement(country_list,i)["director"],
                    lt.getElement(country_list, i)["type"],
                    lt.getElement(country_list, i)["cast"],
                    lt.getElement(country_list, i)["country"],
                    lt.getElement(country_list, i)["rating"],
                    lt.getElement(country_list, i)["listed_in"],
                    lt.getElement(country_list, i)["description"][0:50]+"..."])
                
        else:
            for i in range(1,lt.size(country_list)+1):
                tabla_req5.add_row([lt.getElement(country_list, i)["release_year"],
                    lt.getElement(country_list, i)["title"],
                    lt.getElement(country_list, i)["duration"],
                    lt.getElement(country_list, i)["stream_service"],
                    lt.getElement(country_list,i)["director"],
                    lt.getElement(country_list, i)["type"],
                    lt.getElement(country_list, i)["cast"],
                    lt.getElement(country_list, i)["country"],
                    lt.getElement(country_list, i)["rating"],
                    lt.getElement(country_list, i)["listed_in"],
                    lt.getElement(country_list, i)["description"][0:50]+"..."])
                
        print(tabla_req5)
        print("\n")
        

    elif int(inputs[0]) == 7:
        """
        Se crea una lista de peliculas y shows de television respecto a un director especifico, dado por 
        parametro por el usuario. La lista esta ordenada por periodos de estreno del mas antiguo al mas reciente.
        """
        director_name=input("Ingrese el nombre del director a buscar: ")
        print("Consultando contenido del director ....")
        print("Consultando shows dirigidos por "+director_name+ " ....")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.Shows_by_director(control, director_name, memflag=mem)
        printRequerimmiento6Answer(answer)
        if len(answer) == 6: 
           titles_list,type_dict,service_dict,listed_in_dict, time, memsize = answer
        else:
            titles_list,type_dict,service_dict,listed_in_dict, time = answer
        
        table1 = PrettyTable(field_names=["type","count"])
        table2 = PrettyTable(field_names=["service_name","type"])
        table3 = PrettyTable(field_names=["listed_in","count"])
        table4 = PrettyTable(field_names=["release_year","title","duration","director","stream_service",
            "type","cast","country","rating","description"])

        for i in type_dict:
            table1.add_row([i,type_dict[i]])
        for i in service_dict:
            table2.add_row([i,service_dict[i]])
        for i in listed_in_dict:
            table3.add_row([i,listed_in_dict[i]])
        if lt.size(titles_list) > 6:
            first = lt.subList(titles_list,1,3)
            last = lt.subList(titles_list,lt.size(titles_list)-2,3)
            for i in lt.iterator(first):
                table4.add_row([i["release_year"],i["title"],i["duration"],i["director"],
                i["stream_service"],i["type"],i["cast"],i["country"],i["rating"],
                i["description"][0:100]])
            for i in lt.iterator(last):
                table4.add_row([i["release_year"],i["title"],i["duration"],i["director"],
                i["stream_service"],i["type"],i["cast"],i["country"],i["rating"],
                i["description"][0:100]])
        else:
            for i in lt.iterator(titles_list):
                table4.add_row([i["release_year"],i["title"],i["duration"],i["director"],
                i["stream_service"],i["type"],i["cast"],i["country"],i["rating"],
                i["description"][0:100]])
        print(table1)
        print(table2)
        print(table3)
        print("El total de las peliculas donde participó el director "+director_name+" es: "+str(lt.size(titles_list)))
        print(table4)
    #TOP de generos con mas contenido.

    elif int(inputs[0]) == 8:

        """
        Se crea una lista para consultar los generos con mayor numero de peliculas y shows de television,
        el genero es dado por parametro por el usuario. La lista esta ordenada de mayor a menor numero de 
        conenido en cada tipo de genero.
        """
        top= int(input("Ingrese el número de géneros a identificar: "))
        print("Consultando el TOP "+"("+str(top)+")"+" de los géneros con más contenido....")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        answer = controller.TOP_genero(control,top, memflag=mem)
        printRequerimmiento7Answer(answer)
        if len(answer) == 3: 
           sublist, time, memsize = answer
        else:
           sublist, time = answer

        tabla_1 = PrettyTable(field_names= ["listed_in","count"])
        tabla_2 = PrettyTable(field_names= ["rank","listed_in","count","type","stream_service"])
        rank = 1
        if top <= 6:
            for i in lt.iterator(sublist):
                Movie,shows,amazon,netflix,hulu,disney = i["count"]
                movie_str = "Movie:"+str(Movie),"TV Shows:"+str(shows)
                stream_str = "amazon:"+str(amazon),"netflix:"+str(netflix),"hulu:"+str(hulu),"disney:"+str(disney)
                tabla_1.add_row([i["genre"],lt.size(i["titles"])])
                tabla_2.add_row([rank,i["genre"],lt.size(i["titles"]),movie_str,stream_str])
                rank += 1
        else:
            first = lt.subList(sublist,1,3)
            last = lt.subList(sublist,lt.size(sublist)-2,3)
            for i in lt.iterator(first):
                Movie,shows,amazon,netflix,hulu,disney = i["count"]
                movie_str = "Movie:"+str(Movie),"TV Shows:"+str(shows)
                stream_str = "amazon:"+str(amazon),"netflix:"+str(netflix),"hulu:"+str(hulu),"disney:"+str(disney)
                tabla_1.add_row([i["genre"],lt.size(i["titles"])])
                tabla_2.add_row([rank,i["genre"],lt.size(i["titles"]),movie_str,stream_str])
                rank += 1
            rank =top-2
            for i in lt.iterator(last):
                Movie,shows,amazon,netflix,hulu,disney = i["count"]
                movie_str = "Movie:"+str(Movie),"TV Shows:"+str(shows)
                stream_str = "amazon:"+str(amazon),"netflix:"+str(netflix),"hulu:"+str(hulu),"disney:"+str(disney)
                tabla_1.add_row([i["genre"],lt.size(i["titles"])])
                tabla_2.add_row([rank,i["genre"],lt.size(i["titles"]),movie_str,stream_str])
                rank += 1
            
        print(tabla_1)
        print(tabla_2)
        
    
    elif int(inputs[0])==9:
        lista_generos= mp.keySet(control["model"]["Generos"])
        print(mp.size(control["model"]["Generos"]))
        for genero in lt.iterator(lista_generos):
            print(genero)
       
    else:
        sys.exit(0)
sys.exit(0)
