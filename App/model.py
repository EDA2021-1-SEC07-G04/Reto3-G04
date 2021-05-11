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
 catalog['hashtags']=om.newMap(omaptype='BST',comparefunction=compareIds)
 catalog['byInst']=om.newMap(omaptype='BST',comparefunction=compareIds)
 catalog['byTemp']=om.newMap(omaptype='BST',comparefunction=compareIds)

 return catalog


# Funciones para agregar informacion al catalogo

def addInstance(catalog, instance):
    lt.addLast(catalog["instances"], instance)
    orderByDates(catalog["byDates"], instance)
    orderByArtists(catalog['artists'], instance)
    orderByTracks(catalog['tracks'], instance)
    orderByInst(catalog['byInst'], instance)
    orderByTemp(catalog['byTemp'], instance)
    
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

def orderByInst(map, instance):
    inst = instance['instrumentalness']
    entry = om.get(map, inst)
    if entry is None:
        om.put(map, inst, instance)
    return map

def orderByTemp(map, instance):
    temp = instance['tempo']
    entry = om.get(map, temp)
    if entry is None:
        om.put(map, temp, instance)
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
         

    mensaje = "Cuenta reproducciones: "+str(trackcount)
    mensaje += "\nCuenta artistas: "+str(om.size(artists))
    return mensaje

def partyRecommend(catalog, valmaxEng, valminEng, valmaxDan, valminDan):
    valores = om.valueSet(catalog['byDates'])
    tracklist = lt.newList('ARRAY_LIST')
    trackcheck = lt.newList('ARRAY_LIST')
    generated = 1
    for index in range(0, lt.size(valores)):
        data = lt.getElement(valores, int(index))
        if float(data['danceability']) >= valminDan and float(data['danceability']) <= valmaxDan \
        and float(data['energy']) <= valmaxEng and float(data['energy']) >= valminEng and lt.isPresent(trackcheck, data['track_id']) == 0:
            lt.addLast(trackcheck, data['track_id'])
            lt.addLast(tracklist, data)

    mensaje = ('Total of unique tracks in events:'+str(lt.size(tracklist)))
    print(mensaje)
    repeated = []
    while generated < 6: 
        trackindex = int(rdm.randint(0, int(lt.size(tracklist))))
        if (trackindex in repeated) == False:
            trackdata = lt.getElement(tracklist, int(trackindex))
            mensaje += ('\nTrack {0}: {1} with energy of {2} and danceability of {3}.'.format(str(generated), str(trackdata['track_id']), str(trackdata['energy']), str(trackdata['danceability'])))
            generated += 1

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
            repeated.append(trackindex)

    return mensaje

def genresByTempo(catalog, generos, nombre_genero, valmin, valmax):
    valores = om.valueSet(catalog['byDates'])
    mensaje = ""
    tempo_generos = mp.newMap(numelements=13,
           prime=17,
           maptype='CHAINING',
           loadfactor=0.5,
           comparefunction=None)
    canciones_generos = mp.newMap(numelements=13,
           prime=17,
           maptype='CHAINING',
           loadfactor=0.5,
           comparefunction=None)
    mp.put(tempo_generos, "Reggae", (60.0, 90.0))
    mp.put(tempo_generos, "Down-tempo", (70.0, 100.0))
    mp.put(tempo_generos, "Chill-out", (90.0, 120.0))
    mp.put(tempo_generos, "Hip-hop", (85.0, 115.0))
    mp.put(tempo_generos, "Jazz and Funk", (120.0, 125.0))
    mp.put(tempo_generos, "Pop", (100.0, 130.0))
    mp.put(tempo_generos, "R&B", (60.0, 80.0))
    mp.put(tempo_generos, "Rock", (110.0, 140.0))
    mp.put(tempo_generos, "Metal", (100.0, 160.0))
    if nombre_genero != None:
        mp.put(tempo_generos, nombre_genero, (valmin, valmin))
    
    for gen in generos:
        artists = lt.newList('ARRAY_LIST')
        for index in range(0, lt.size(valores)):
            data = lt.getElement(valores, int(index))
            #print(mp.get(tempo_generos, gen)['value'][0])
            if float(data['tempo']) >= float((mp.get(tempo_generos, gen))['value'][0]) and float(data['tempo']) <= float((mp.get(tempo_generos, gen))['value'][1]):
                if mp.contains(canciones_generos, gen):
                    mp.get(canciones_generos, gen)['value'] += 1
                else:
                    mp.put(canciones_generos, gen, 1)
                if lt.isPresent(artists, data['artist_id'])==0:
                    lt.addLast(artists, data['artist_id'])
        mensaje += "\n\n====="+str(gen).upper()+"====="
        mensaje += "\nFor "+str(gen)+" the tempo is bewteen "+str(mp.get(tempo_generos, gen)['value'][0])+" BPM.\n"
        mensaje += str(gen)+" reproductions: "+str(mp.get(canciones_generos, gen)['value'])+" with "+str(lt.size(artists))+" different artists."
        mensaje += "\n-----First 10 artists-----"
        for i in range(1, 11):
            mensaje += "n\Artist {0}: {1}".format(i, (lt.getElement(artists, i)))

    return mensaje

def genresByTime(catalog, horamax, horamin):

    return None

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

