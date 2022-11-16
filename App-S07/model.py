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


from platform import platform
import re
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sa
from datetime import datetime
assert cf
from tabulate import tabulate

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog(structure):
    catalog = lt.newList(structure) 
    catalog['generalInformation'] = {'netflix': 0, 'amazon': 0, 'disney': 0, 'hulu': 0, 'features': 0}
    catalog['genres'] = mp.newMap(130, maptype='PROBING', loadfactor=0.5)
    catalog['actors'] = mp.newMap(63000, maptype='PROBING', loadfactor=0.5)
    catalog['years'] = mp.newMap(110, maptype='PROBING', loadfactor=0.5)
    catalog['addedYears'] = mp.newMap(20, maptype='PROBING', loadfactor=0.5)
    catalog['directors'] = mp.newMap(10200, maptype='PROBING', loadfactor=0.5)
    catalog['countries'] = mp.newMap(150, maptype='PROBING', loadfactor=0.5)
    return catalog

# Funciones para agregar informacion al catalogo
def addTitle(catalog, title, platform):
    lt.addLast(catalog, title)
    catalog['generalInformation'][platform] += 1
    if catalog['generalInformation']['features'] == 0:
        catalog['generalInformation']['features'] = len(title)
    actors = title['cast'].split(', ') 
    for actor in actors:
        addTitleActors(catalog, actor, title)
    #genres = title['listed_in'].split(', ')
    genres = re.split(', | & ', title['listed_in'])
    for genre in genres:
        addTitleGenre(catalog, genre, title)
    addTitleYear(catalog, title)
    addTitleAddedYear(catalog, title)
    addTittleDirector(catalog, title)
    countries = title['country'].split(', ')
    for country in countries:
        addTitleCountry(catalog, country, title)

def addTitleGenre(catalog, genreName, title):
    genres = catalog['genres']
    existGener = mp.contains(genres, genreName)
    if existGener:
        entry = mp.get(genres, genreName)
        genre = me.getValue(entry)
    else:
        genre = newGenre(genreName)
        mp.put(genres, genreName, genre)
    lt.addLast(genre['titles'], title)
    addDetails(genre, title, complex= True)
    actors = title['cast'].split(', ')
    for actor in actors:
        numberActor = genre['actors'].get(actor, 0)
        genre['actors'][actor] = numberActor + 1

def addTitleActors(catalog, actorName, title):
    actors= catalog['actors']
    existActor = mp.contains(actors, actorName)
    if existActor: 
        entry= mp.get(actors,actorName)
        actor= me.getValue(entry)
    else:
        actor = newActor(actorName)
        mp.put(actors, actorName, actor)
    lt.addLast(actor['titles'], title)
    addDetails(actor, title)
    addDetails(actor, title, req= True)

def addTitleCountry(catalog, countryName, title):
    countries = catalog['countries']
    existCountry = mp.contains(countries, countryName)
    if existCountry:
        entry = mp.get(countries, countryName)
        country = me.getValue(entry)
    else:
        country = newCountry(countryName)
        mp.put(countries, countryName, country)
    lt.addLast(country['titles'], title)
    addDetails(country, title)

def addTitleYear(catalog, title):
    years = catalog['years']
    pubyear = title['release_year']
    existYear = mp.contains(years, pubyear)
    if existYear:
        entry = mp.get(years, pubyear)
        year = me.getValue(entry)
    else:
        year = newYear(pubyear)
        mp.put(years, pubyear, year)
    addDetails(year, title, type= 'add')

def addTitleAddedYear(catalog, title):
    years = catalog['addedYears']
    if title['date_added'] != '':
        pubyear = datetime.strptime(title['date_added'], '%B %d, %Y').year
        existYear = mp.contains(years, pubyear)
        if existYear:
            entry = mp.get(years, pubyear)
            year = me.getValue(entry)
        else:
            year = newYear(pubyear)
            mp.put(years, pubyear, year)
        addDetails(year, title, type= 'add')

def addTittleDirector(catalog, title):
    directorName = title['director']
    directors = catalog['directors']
    existDirector = mp.contains(directors, directorName)
    if existDirector:
        entry = mp.get(directors, directorName)
        director = me.getValue(entry)
    else:
        director = newDirector(directorName)
        mp.put(directors, directorName, director)
    lt.addLast(director['titles'], title)
    addDetails(director, title, complex= True)
    genres = director['genres']
    generos = re.split(', | & ', title['listed_in'])
    for genero in generos:
        numberGenero = genres.get(genero, 0)
        genres[genero] = numberGenero + 1

# Funciones para creacion de datos
def addDetails(node, title, type= 'count', complex= False, req= False):
    if req:
        platform = title['streame_service']
        countType = node['streameServices'].get(platform, {'movies': 0, 'TVShows': 0, 'name': platform})
        if title['type'] == 'Movie':
            countType['movies'] += 1
        else:
            countType['TVShows'] += 1
        node['streameServices'][platform] = countType
        if (title['director'] != '') and (title['director'] not in node['colaborations']['directors']):
            if node['colaborations']['directors'] == '':
                node['colaborations']['directors'] = title['director']
            else:
                node['colaborations']['directors'] += ', ' + title['director']
        for actor in title['cast'].split(', '):
            if (actor not in node['colaborations']['actors']) and (actor != '') and (actor != node['actor']):
                if node['colaborations']['actors'] == '':
                    node['colaborations']['actors'] = actor
                else:
                    node['colaborations']['actors'] += ', ' + actor
    else:
        if type == 'count':
            if title['type'] == 'Movie':
                node['types']['movies'] += 1
            else:
                node['types']['TVShows'] += 1
        elif type == 'add':
            if title['type'] == 'Movie':
                lt.addLast(node['movies'], title)
            else:
                lt.addLast(node['TVShows'], title)
        if complex:
            platform = title['streame_service']
            streameServices = node['streameServices']
            numberPlatform = streameServices.get(platform, 0)
            streameServices[platform] = numberPlatform + 1

def newGenre(genreName):
    genre = {}
    genre['genre'] = genreName
    genre['titles'] = lt.newList()
    genre['types'] = {'movies': 0, 'TVShows': 0}
    genre['streameServices'] = {}
    genre['actors'] = {}
    return genre

def newActor(actorName): 
    actor = {}
    actor['actor'] = actorName
    actor['titles'] = lt.newList()
    actor['types'] = {'movies': 0, 'TVShows': 0}
    actor['streameServices'] = {}
    actor['colaborations'] = {'directors': '', 'actors': ''}
    return actor

def newCountry(countryName):
    country = {}
    country['country'] = countryName
    country['titles'] = lt.newList()
    country['types'] = {'movies': 0, 'TVShows': 0}
    return country

def newYear(pubyear):
    year = {}
    year['year'] = pubyear
    year['movies'] = lt.newList()
    year['TVShows'] = lt.newList()
    return year

def newDirector(directorName):
    director = {}
    director['diretor'] = directorName
    director['titles'] = lt.newList()
    director['types'] = {'movies': 0, 'TVShows': 0}
    director['streameServices'] = {}
    director['genres'] = {}
    return director

# Funciones de consulta
def getMoviesByYear(catalog, year):
    filtered = lt.newList()
    year = mp.get(catalog['years'], year)
    if year:
        filtered = me.getValue(year)['movies']
    sortTitles(filtered, compareReq1)
    return filtered

def getTVShowsByDate(catalog, year, date):
    filtered = lt.newList()
    year = mp.get(catalog['addedYears'], year)
    if year:
        titles = me.getValue(year)['TVShows']
        for title in lt.iterator(titles):
            if title['date_added'] != '':
                dateAdded = datetime.strptime(title['date_added'], '%B %d, %Y')
                if dateAdded == date:
                    lt.addLast(filtered, title)
    sortTitles(filtered, compareReq2)
    return filtered

def getTitlesByActor(catalog, actor): 
    filtered = lt.newList()
    details = {}
    actor = mp.get(catalog['actors'], actor)
    if actor:
        filtered = me.getValue(actor)['titles']
        details['Movie'] = me.getValue(actor)['types']['movies']
        details['TV Shows'] = me.getValue(actor)['types']['TVShows']
    sortTitles(filtered, compareReq3a6)
    return filtered, details

def getTitlesByGenre(catalog, genre):
    filtered = lt.newList()
    details = {}
    genre = mp.get(catalog['genres'], genre)
    if genre:
        filtered = me.getValue(genre)['titles']
        details['Movie'] = me.getValue(genre)['types']['movies']
        details['TV Shows'] = me.getValue(genre)['types']['TVShows']
    sortTitles(filtered, compareReq3a6)
    return filtered, details

def getTitlesByCountry(catalog, country):
    filtered = lt.newList()
    details = {}
    country = mp.get(catalog['countries'], country)
    if country:
        filtered = me.getValue(country)['titles']
        details['Movie'] = me.getValue(country)['types']['movies']
        details['TV Shows'] = me.getValue(country)['types']['TVShows']
    sortTitles(filtered, compareReq3a6)
    return filtered, details

def getTitlesByDirector(catalog, director):
    filtered = lt.newList()
    details = []
    types = {}
    platforms = {}
    genres = lt.newList()
    director = mp.get(catalog['directors'], director)
    if director:
        filtered = me.getValue(director)['titles']
        types['Movie'] = me.getValue(director)['types']['movies']
        types['TV Shows'] = me.getValue(director)['types']['TVShows']
        platforms = me.getValue(director)['streameServices']
        generos = me.getValue(director)['genres']
        for key, value in generos.items():
            info = {'listed_in': key, 'count': value}
            lt.addLast(genres, info)
    details.append(types)
    details.append(platforms)
    details.append(genres)
    sortTitles(filtered, compareReq3a6)
    return filtered, details

def getTopNByGenre(catalog, N):
    filtered = lt.newList()
    generos = mp.keySet(catalog['genres'])
    for genero in lt.iterator(generos):
        entry = mp.get(catalog['genres'], genero)
        genre = me.getValue(entry)
        info = {'listed_in': genero, 'count': lt.size(genre['titles']), 'type':{'Movie': genre['types']['movies'], 'TV Shows': genre['types']['TVShows']}, 'streame_service': genre['streameServices']}
        lt.addLast(filtered, info)
    sortTitles(filtered, compareDataCounts)
    topN = lt.newList()
    if N > lt.size(filtered):
        N = lt.size(filtered)
    for pos in range(1, N+1):
        title = lt.getElement(filtered, pos)
        title['rank'] = pos
        lt.addLast(topN, title)
    return topN, lt.size(filtered)

def getTopNByActorInGenre(catalog, N, genre):
    filtered = lt.newList()
    topActors = lt.newList()
    ditails = lt.newList()
    entry = mp.get(catalog['genres'], genre)
    if entry:
        genre = me.getValue(entry)
        actors = genre['actors']
        for key, value in actors.items():
            lt.addLast(topActors, {'actor': key, 'count': value})
        sortTitles(topActors, compareReq8)
        if N > lt.size(topActors):
            N = lt.size(topActors)
        for pos in range(1, N+1):
            count = lt.getElement(topActors, pos)
            entry = mp.get(catalog['actors'], count['actor'])
            actor = me.getValue(entry)
            info = {'rank': pos, 'actor': actor['actor'], 'count': count['count'], 'streame_service': actor['streameServices'], 'directors': actor['colaborations']['directors'], 'actors': actor['colaborations']['actors'], 'movies': actor['types']['movies'], 'TVShows': actor['types']['TVShows']}
            lt.addLast(filtered, info)
            ditail = lt.newList()
            for title in lt.iterator(actor['titles']):
                title['actor'] = actor['actor']
                lt.addLast(ditail, title)
            sortTitles(ditail, compareReq3a6)
            lt.addLast(ditails, {'rank': pos, 'actor': actor['actor'], 'titles': ditail})
    return filtered, ditails, lt.size(topActors)

# Funciones utilizadas para comparar elementos dentro de una lista
def compareLoadData(title1, title2):
    if title1['release_year'] == title2['release_year']:
        return compareTitle(title1, title2)
    else:
        return compareReleaseYear(title1, title2)

def compareReq1(title1, title2):
    if title1['title'] == title2['title']:
        return compareDurationMovies(title1, title2)
    else:
        return compareTitle(title1, title2)

def compareReq2(title1, title2):
    if title1['title'] == title2['title']:
        return compareDurationTVShows(title1, title2)
    else:
        return compareTitle(title1, title2)

def compareReq3a6(title1, title2):
    if title1['release_year'] == title2['release_year']:
        if title1['title'] == title2['title']:
            return compareDurations(title1, title2)
        else:
            return compareTitle(title1, title2)
    else:
        return not compareReleaseYear(title1, title2)

def compareReq8(title1, title2):
    if title1['count'] == title2['count']:
        return compareActor(title1, title2)
    else:
        return compareDataCounts(title1, title2)

def compareReleaseYear(title1, title2):
    return (int(title1['release_year']) < int(title2['release_year']))

def compareTitle(title1, title2):
    return (str(title1['title']) < str(title2['title']))

def compareActor(title1, title2):
    return (str(title1['actor']) < str(title2['actor']))

def compareDurationMovies(title1, title2):
    return (int(title1['duration'][:-4]) < int(title2['duration'][:-4]))

def compareDurationTVShows(title1, title2):
    return (int(title1['duration'][:-7]) < int(title2['duration'][:-7]))

def compareDurations(title1, title2):
    duration1 = title1['duration'].split(' ')
    duration2 = title2['duration'].split(' ')
    if (duration1[0] != '') and (duration2[0] != ''):
        return (int(duration1[0]) < int(duration2[0]))

def compareDataAmounts(amount1, amount2):
    return (int(amount1['amount']) > int(amount2['amount']))

def compareDataCounts(count1, count2):
    return (int(count1['count']) > int(count2['count']))

def compareDateAdded(title1, title2):
    return datetime.strptime(title1['date_added'], '%Y-%m-%d') > datetime.strptime(title2['date_added'], '%Y-%m-%d')

# Funciones de ordenamiento
def firstAndLastThreeTitles(lista):
    filteredTitles = lt.newList()
    size = lt.size(lista)
    if size >= 1:
        if size <= 5:
            filteredTitles = lista
        else:
            for pos in range(1, 4):
                title = lt.getElement(lista, pos)
                lt.addLast(filteredTitles, title)
            for pos in range(size-2, size+1):
                title = lt.getElement(lista, pos)
                lt.addLast(filteredTitles, title)
    return filteredTitles

def sortTitles(lista, compareReq):
    return sa.sort(lista, compareReq)

def sortDataAmounts(lista):
    return sa.sort(lista, compareDataAmounts)

