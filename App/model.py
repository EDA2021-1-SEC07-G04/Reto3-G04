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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf
import copy
import random as rdm


# Construccion de modelos
def CatalNuevo():
 catalog={"instances":None, "byDates":None,"sentiments":None, 'artists':None, 'tracks':None}                         
         
 catalog["instances"]=lt.newList("ARRAY_LIST")
 catalog['byDates'] = om.newMap(omaptype='RST',comparefunction=compareDates)
 catalog["sentiments"]=mp.newMap(10,13,maptype="CHAINING",loadfactor=0.60,comparefunction=None)
 catalog['artists']=om.newMap(omaptype='BST',comparefunction=compareIds)
 catalog['tracks']=om.newMap(omaptype='BST',comparefunction=compareIds)

 return catalog


# Funciones para agregar informacion al catalogo

def addInstance(catalog, instance):
    lt.addLast(catalog["instances"], instance)
    orderByDates(catalog["byDates"], instance)
    orderByArtists(catalog['artists'], instance)
    orderByTracks(catalog['tracks'], instance)
    
def addSentiment(catalog, sentiment):
    mp.put(catalog['sentiments'], sentiment['hashtag'], sentiment)
        
def orderByDates(map, instance):
    occurreddate = instance['created_at']
    instancedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    instance_id = instance["track_id"]
    instance_user = instance["user_id"]
    key = (instancedate, instance_id, instance_user)
    #print(instancedate)
    entry = om.get(map, key)
    if entry is None:
        om.put(map, key, instance)
    return map
    
def orderByArtists(map, instance):
    artist = instance["artist_id"]
    entry = om.get(map, artist)
    if entry is None:
        om.put(map, artist, instance)
    return map

def orderByTracks(map, instance):
    track = instance["track_id"]
    entry = om.get(map, track)
    if entry is None:
        om.put(map, track, instance)
    return map

# Funciones para creacion de datos

# Funciones de consulta
def instancesPerCharact(catalog, charact, valmax, valmin):
    valores = om.valueSet(catalog['byDates'])
    artists = om.newMap(omaptype='BST',comparefunction=compareIds)
    trackcount = 0
    artistcount = 0
    for index in range(0, lt.size(valores)):
        data = lt.getElement(valores, int(index))
        if float(data[charact]) >= valmin and float(data[charact]) <= valmax:
            trackcount += 1
            if om.contains(artists, data['artist_id']) == False:
                 om.put(artists, data['artist_id'], data)
         

    print("Cuenta reproducciones: "+str(trackcount))
    print("Cuenta artistas: "+str(om.size(artists)))
    return None

def studyRecomend(catalog, valmaxtemp, valmintemp, valmaxinst, valmininst):
    valores = om.valueSet(catalog['byDates'])
    tracklist = lt.newList('ARRAY_LIST')
    trackcheck = lt.newList('ARRAY_LIST')
    generated = 1
    for index in range(0, lt.size(valores)):
        data = lt.getElement(valores, int(index))
        if float(data['instrumentalness']) >= valmininst and float(data['instrumentalness']) <= valmaxinst \
        and float(data['tempo']) <= valmaxtemp and float(data['tempo']) >= valmintemp and lt.isPresent(trackcheck, data['track_id']) == 0:
            lt.addLast(trackcheck, data['track_id'])
            lt.addLast(tracklist, data)

    mensaje = ('Total of unique tracks in events:'+str(lt.size(tracklist)))
    print(mensaje)
    repeated = []
    while generated < 6: 
        trackindex = int(rdm.randint(0, int(lt.size(tracklist))))
        if (trackindex in repeated) == False:
            trackdata = lt.getElement(tracklist, int(trackindex))
            mensaje += ('\nTrack {0}: {1} with instrumentalness of {2} and tempo of {3}.'.format(str(generated), str(trackdata['track_id']), str(trackdata['instrumentalness']), str(trackdata['tempo'])))
            generated += 1

    return mensaje

# Funciones utilizadas para comparar elementos dentro de una lista
def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def compareIds(id1, id2):
    """
    Compara dos instancias
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
# Funciones de ordenamiento
def instancesSize(catalog):
    return lt.size(catalog['instances'])


def treeHeight(catalog):
    """
    Altura del arbol
    """
    return om.height(catalog['byDates'])


def treeSize(catalog):
    """
    Numero de elementos en el indice
    """
    return om.size(catalog['byDates'])

def artistsSize(catalog):
    """
    Numero de artistas únicos
    """
    return om.size(catalog['artists'])

def tracksSize(catalog):
    """
    Numero de pistas únicos
    """
    return om.size(catalog['tracks'])


def minKey(catalog):
    return om.minKey(catalog['byDates'])


def maxKey(catalog):
    return om.maxKey(catalog['byDates'])

def minmax5Tracks(catalog, keyrange):
    min_5 = lt.newList("ARRAY_LIST")
    max_5 = lt.newList("ARRAY_LIST")
    catalogcopy = copy.deepcopy(catalog['byDates'])
    while keyrange > 0:
        keymin=om.minKey(catalogcopy)
        keymax=om.maxKey(catalogcopy)
        lt.addLast(min_5, om.get(catalogcopy, keymin))
        lt.addLast(max_5, om.get(catalogcopy, keymax))
        om.deleteMin(catalogcopy)
        om.deleteMax(catalogcopy)
        keyrange -=1
    return min_5, max_5

