"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

import config as cf
import tracemalloc
import time
import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

#memory and time counters
def getTime():
 """
 devuelve el instante tiempo de procesamiento en milisegundos
 """
 return float(time.perf_counter()*1000)

def getMemory():
 """
 toma una muestra de la memoria alocada en instante de tiempo
 """
 return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
 """
 calcula la diferencia en memoria alocada del programa entre dos 
 instantes de tiempo y devuelve el resultado en kBytes (ej.: 2100.0 kB)
 """
 memory_diff = stop_memory.compare_to(start_memory, "filename")
 delta_memory = 0.0
# suma de las diferencias en uso de memoria
 for stat in memory_diff:
  delta_memory = delta_memory + stat.size_diff
# de Byte -> kByte
 delta_memory = delta_memory/1024.0
 return delta_memory




# Inicialización del Catálogo de videos
def startCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.CatalNuevo()
    return catalog

# Funciones para la carga de datos
def startData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    tracemalloc.start()
    delta_time = -1.0
    delta_memory = -1.0
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    #EJECUCIÓN DE CARGA
    loadInstances(catalog)
    loadSentiments(catalog)
    #EJECUCIÓN DE CARGA
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time, delta_memory
    


def loadInstances(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    instancefile = cf.data_dir + 'context_content_features-small.csv'
    input_file = csv.DictReader(open(instancefile, encoding='utf-8'))
    for instance in input_file:
        model.addInstance(catalog, instance)


def loadSentiments(catalog):
    sentfile = cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(sentfile, encoding='utf-8'))
    for sentiment in input_file:
        #print(categ)
        model.addSentiment(catalog, sentiment)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def instancesPerCharact(catalog, charact, valmax, valmin):
    tracemalloc.start()
    delta_time = -1.0
    delta_memory = -1.0
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    #EJECUCIÓN DE CARGA
    instances = model.instancesPerCharact(catalog, charact, valmax, valmin)
    #EJECUCIÓN DE CARGA
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return instances, delta_time, delta_memory

def partyRecommended(catalog,valmaxeng,valmineng,valmaxdan,valmindan):
    return model.partyRecommend(catalog,valmaxeng,valmineng,valmaxdan,valmindan)

def studyRecomend(catalog, valmaxtemp, valmintemp, valmaxinst, valmininst):
    tracemalloc.start()
    delta_time = -1.0
    delta_memory = -1.0
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    #EJECUCIÓN DE CARGA
    recommend = model.studyRecomend(catalog, valmaxtemp, valmintemp, valmaxinst, valmininst)
    #EJECUCIÓN DE CARGA
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return recommend, delta_time, delta_memory

def genresByTempo(catalog, generos, nombre_genero, valmin, valmax):
    tracemalloc.start()
    delta_time = -1.0
    delta_memory = -1.0
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    #EJECUCIÓN DE CARGA
    genres = model.genresByTempo(catalog, generos, nombre_genero, valmin, valmax)
    #EJECUCIÓN DE CARGA
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return genres, delta_time, delta_memory

def genresByTime(catalog, horamax, horamin):
    tracemalloc.start()
    delta_time = -1.0
    delta_memory = -1.0
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    #EJECUCIÓN DE CARGA
    genres = model.genresByTime(catalog, horamax, horamin)
    #EJECUCIÓN DE CARGA
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return genres, delta_time, delta_memory

def instancesSize(catalog):
    """
    Numero de instancias de reproducción leidas
    """
    return model.instancesSize(catalog)


def treeHeight(catalog):
    """
    Altura del indice (arbol)
    """
    return model.treeHeight(catalog)


def treeSize(catalog):
    """
    Numero de nodos en el arbol
    """
    return model.treeSize(catalog)

def artistsSize(catalog):
    """
    Numero de artistas cargados en el arbol
    """
    return model.artistsSize(catalog)

def tracksSize(catalog):
    """
    Numero de artistas cargados en el arbol
    """
    return model.tracksSize(catalog)

def minKey(catalog):
    """
    La menor llave del arbol
    """
    return model.minKey(catalog)


def maxKey(catalog):
    """
    La mayor llave del arbol
    """
    return model.maxKey(catalog)

def minmax5Tracks(catalog, keyrange):
    return model.minmax5Tracks(catalog, keyrange)


