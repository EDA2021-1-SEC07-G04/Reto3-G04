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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Reproducciones basadas en el rango de una característica de contenido")
    print("3- Recomendaciones de canciones para fiestas (Danceability y Energy)")
    print("4- Recomendaciones de canciones para estudiar (Instrumentalness y Tempo)")
    print("5- Canciones y artistas únicos por cada género")
    print("6- Género de música más escuchado segun rango de tiempos")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=controller.startCatalog()
        answer=controller.startData(catalog)        
        print('Elementos en el arbol: ' + str(controller.treeSize(catalog)))
        print('Altura del arbol: ' + str(controller.treeHeight(catalog)))
        print('Artistas únicos cargados: ' + str(controller.artistsSize(catalog)))
        print('Pistas de audio únicas cargadas: ' + str(controller.tracksSize(catalog)))
        minmax5=controller.minmax5Tracks(catalog, 5)
        print("Menores 5 eventos de escucha cargados: \n"
              +str((lt.getElement(minmax5[0], 0))['value'])+"\n"
              +str((lt.getElement(minmax5[0], 1))['value'])+"\n"
              +str((lt.getElement(minmax5[0], 2))['value'])+"\n"
              +str((lt.getElement(minmax5[0], 3))['value'])+"\n"
              +str((lt.getElement(minmax5[0], 4))['value'])+"\n")
        print("Mayores 5 eventos de escucha cargados: \n"
              +str((lt.getElement(minmax5[1], 0))['value'])+"\n"
              +str((lt.getElement(minmax5[1], 1))['value'])+"\n"
              +str((lt.getElement(minmax5[1], 2))['value'])+"\n"
              +str((lt.getElement(minmax5[1], 3))['value'])+"\n"
              +str((lt.getElement(minmax5[1], 4))['value'])+"\n")
        print("Tiempo [ms]: ", answer[0], "  ||  ",
              "Memoria [kB]: ", answer[1])
        

        #Menor Llave: (datetime.datetime(2014, 1, 1, 5, 56, 11), '7cb1d732774911f119ffb443e5665e6c', '197136967')
        #Mayor Llave: (datetime.datetime(2014, 121 23, 7, 4, 43), '85bded2c26726c14f4668c4c25968f5c', '445590277')
    elif int(inputs[0]) == 2:
        charact = input("Seleccione una característica de contenido: ")
        valmax = float(input("Seleccione el limite superior del valor de la característica: "))
        valmin = float(input("Seleccione el limite inferior del valor de la característica: "))
        print("Resultados Requerimiento 1: ")
        answer = controller.instancesPerCharact(catalog, charact, valmax, valmin)
        print(answer[0])
        print("Tiempo [ms]: ", answer[1], "  ||  ",
              "Memoria [kB]: ", answer[2])

    elif int(inputs[0]) == 3:
        valmaxeng = float(input("Seleccione el limite superior del valor del Energy: "))
        valmineng = float(input("Seleccione el limite inferior del valor del Energy: "))
        valmaxdan = float(input("Seleccione el limite superior del valor del Danceability: "))
        valmindan = float(input("Seleccione el limite inferior del valor del Danceability: "))
        print("Resultados Requerimiento 2: ")
        answer = controller.partyRecommended(catalog, valmaxeng, valmineng, valmaxdan, valmindan)
        print(answer)

    elif int(inputs[0]) == 4:
        valmaxtemp = float(input("Seleccione el limite superior del valor del Tempo: "))
        valmintemp = float(input("Seleccione el limite inferior del valor del Tempo: "))
        valmaxinst = float(input("Seleccione el limite superior del valor del Instrumentalness: "))
        valmininst = float(input("Seleccione el limite inferior del valor del Instrumentalness: "))
        print("Resultados Requerimiento 3: ")
        answer = controller.studyRecomend(catalog, valmaxtemp, valmintemp, valmaxinst, valmininst)
        print(answer[0])
        print("Tiempo [ms]: ", answer[1], "  ||  ",
              "Memoria [kB]: ", answer[2])

    elif int(inputs[0]) == 5:
        generos_input = input("Escriba los géneros que desea buscar (separados por una coma): ")
        generos = generos_input.split(",")
        nuevo_genero = input("¿Desea agregar un nuevo género musical? (Si / No): ")
        if nuevo_genero == "Si":
            nombre_genero = input("Nombre su nuevo género: ")
            valmin = float(input("Valor mínimo del Tempo: "))
            valmax = float(input("Valor máximo del Tempo: "))
            generos.append(nombre_genero)
        else:
            nombre_genero = None
            valmin = None
            valmax = None
        print("Resultados Requerimiento 4: ")
        answer = controller.genresByTempo(catalog, generos, nombre_genero, valmin, valmax)
        print(answer[0])
        print("Tiempo [ms]: ", answer[1], "  ||  ",
              "Memoria [kB]: ", answer[2])
    elif int(inputs[0]) == 6:
        horamin = input("Seleccione el limite inferior de la hora: ")
        horamax = input("Seleccione el limite superior de la hora: ")
        answer = controller.genresByTime(catalog, horamax, horamin)
        print(answer[0])
        print("Tiempo [ms]: ", answer[1], "  ||  ",
              "Memoria [kB]: ", answer[2])
    else:
        sys.exit(0)
sys.exit(0)
