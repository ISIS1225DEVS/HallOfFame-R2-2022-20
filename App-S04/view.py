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

from tkinter import N
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
#from tabulate import tabulate


def newController(estructura, can_netflix, can_amazon, can_disney, can_hulu):

    control = controller.newController(estructura, can_netflix, can_amazon, can_disney, can_hulu)
    return control

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Examinar las películas estrenadas en un año ")
    print("3- Examinar los programas de televisión agregados en un año")
    print("4- Encontrar el contenido donde participa un actor")
    print("5- Encontrar el contenido por un genero particular")
    print("6- Encontrar el contenido producido en un país")
    print("7- Encontrar el contenido con un director involucrado")
    print("8- Listar el TOP (N) de los géneros con más contenido ")
    print("9- Listar el TOP (N) de actores más populares para un género específico")


"""
Menu principal2
"""
while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))
    if inputs == 1:

        print("Escoja el tipo de dato a implementar")
        print("1- CHAINING")
        print("2- PROBING")         
        tipo = int(input(""))

        if tipo == 1:
            estructura = "CHAINING"
        elif tipo == 2:
            estructura = "PROBING"

        print("Escoja la cantidad de datos")
        print("1- small \n2- 5% \n3- 10% \n4- 20% \n5- 30% \n6- 50% \n7- 80% \n8- large")
        valor_dato = int(input(""))
        can_netflix = 88
        can_amazon = 96
        can_disney = 14
        can_hulu = 30

        if valor_dato == 1:
            tamanio = "small"
        elif valor_dato == 2:
            tamanio = "5pct"
            can_netflix = 440
            can_amazon = 483
            can_disney = 72
            can_hulu = 153
        elif valor_dato == 3:
            tamanio = "10pct"
            can_netflix = 880
            can_amazon = 967
            can_disney = 146
            can_hulu = 307
        elif valor_dato == 4:
            tamanio = "20pct"
            can_netflix = 1762
            can_amazon = 966
            can_disney = 298
            can_hulu = 624
        elif valor_dato == 5:
            tamanio = "30pct"
            can_netflix = 2646
            can_amazon = 2907
            can_disney = 435
            can_hulu = 931
        elif valor_dato == 6:
            tamanio = "50pct"
            can_netflix = 4404
            can_amazon = 4844
            can_disney = 726
            can_hulu = 1551
        elif valor_dato == 7:
            tamanio = "80pct"
            can_netflix = 7048
            can_amazon = 7748
            can_disney = 1161
            can_hulu = 2475
        elif valor_dato == 8:
            tamanio = "large"
            can_netflix = 8810
            can_amazon = 9688
            can_disney = 1451
            can_hulu = 3091
        
        print("Cargando información de los archivos ....")
        control = newController(estructura, can_netflix, can_amazon, can_disney, can_hulu)
        controller.loadData(control, tamanio)
        carga = controller.carga_datos(control)

        #print(carga[0])
        print("\nNetflix")
        print(carga[1])
        print("\nAmazon")
        print(carga[2])
        print("\nDisney")
        print(carga[1])
        print("\nHulu")
        print(carga[1])
        print("\nNetflix: ", controller.netflixSize(control))
        print("Amazon: ", controller.amazonSize(control))
        print("Disney: ", controller.disneySize(control))
        print("Hulu: ", controller.huluSize(control))

    elif inputs == 2:
        print("escriba el año")
        anio = str(input(""))
        carga = controller.req_1(control, anio)

        print("La cantidad de películas estrenadas en " + str(anio) + " es: ", carga[1])
        print("\n")
        print(carga[0]["elements"])
     
    elif inputs == 3: 
        print("escriba la fecha")
        date = str(input(""))
        anio = date.split(" ")[2]
        carga = controller.req_2(control, anio)

        print("La cantidad de programas añadidos en " + str(anio) + " es: ", carga[1])
        print("\n")
        print(carga[0]["elements"])
        

    elif inputs == 4: 
        print("Escriba el nombre del actor")
        Actor=str(input(""))
        carga=controller.req_3(control,Actor)
        print("\nMovie: ", carga[1])
        print("TV Show: ",carga[2])
        print("\n")
        print(carga[0]["elements"])
        print("\n")    

    elif inputs == 5:
        print("Escriba el genero")
        genero = str(input(""))
        carga = controller.req_4(control, genero)
        
        print("\nMovie: ", carga[1])
        print("TV Show: ", carga[2])
        print("\n")

        print(carga[0]["elements"])
        print("\n")
    
    elif inputs == 6:
        print("Escriba el país")
        pais = str(input(""))
        vals = controller.req_5(control, pais)

        print("\nMovie: ", vals[1])
        print("TV Show: ", vals[2])
        print("\n")

        print(vals[0]["elements"])
        print("\n")

    elif inputs == 7:
        print("Escriba el director")
        director = str(input(""))
        carga = controller.req_6(control, director)

        print("\nMovie: ", carga[1])
        print("TV Show: ", carga[2])
        print("\n")

        for genero in carga[3]:
            print(genero + ": ", carga[3][genero])
        print("\n")

        for genero in carga[4]:
            print(genero + ": ", carga[4][genero])
        print("\n")
        
        print(carga[0]["elements"])
        print("\n")
    
    elif inputs == 8:
        print("Escriba la cantidad del TOP")
        rank = int(input(""))
        result = controller.req_7(control, rank)

        for genero in result:
            print("\n")
            print(genero, ":", result[genero]["cantidad"])
            
        print("--------------------------------------------------------------------")
        for genero in result:
            print("\n")
            print(genero, ":", result[genero]["cantidad"])
            print("\n")
            for llave in result[genero]["list_cantidad"]:
                print(llave, ":", result[genero]["list_cantidad"][llave])
            print("\n")

            for llave in result[genero]["list_streams"]:
                print(llave, ":", result[genero]["list_streams"][llave])
            print("--------------------------------------------------------------------")

    elif inputs == 9:
        print("Escriba el genero")
        genero = str(input(""))
        print("Escriba la cantidad del TOP")
        rank = int(input(""))
        carga = controller.req_8(control, genero, rank)

        for actor in carga[1]:
            valor = carga[1][actor]
            print("\n")
            print(actor + ":", valor["cantidad"])
        
        print("------------------------------------------------------------------------------------") 
        for actor in carga[1]:
            valor = carga[1][actor]
            print("\n")
            print(actor + ":", valor["cantidad"])
            print("\n")
            for llave in valor["can_streams"]:
                print(llave + ":", valor["can_streams"][llave]) 
            print("\n")

            for llave in valor["program_stream"]:
                print(llave + ":", valor["program_stream"][llave]["elements"]) 
            print("\n")

            for llave in valor["plataform"]:
                print(llave + ":", valor["plataform"][llave])
            print("\n")

            print("Directores:", valor["directores"]["elements"])
            print("\n")

            print("Actores:", valor["actores"]["elements"])
            print("\n")
            print("------------------------------------------------------------------------------------")  

    else:
        sys.exit(0)
sys.exit(0)
