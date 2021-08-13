#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingshpfile: has all the basic methods to read the shapefiles. More of them are for Natural Earth's Cities database

import shapefile
import readingcountryshpfile

#not really useful unless you're only testing methods in this file
def main():
    with shapefile.Reader('SVS_Data/ne_10m_populated_places/ne_10m_populated_places.shp') as sf:
        print(getRec(sf,14))
        
"""More important functions"""

#returns either a specific record or all of them
def getRec(sh,i=-1):
    if i==-1:
        return sh.records()
    else:
        return sh.record(i)

#returns name of city in requested language
def getCityName(sh,i,lang='en'):
    s='name_'+lang
    r=getRec(sh,i)
    return r[s]


"""Kind of important functions"""

#returns a string of all the cities with a given ScaleRank, in English
def getCitiesWithRank(sh,r):
    #only applies to min rank now but I can change it
    rec=getRec(sh)
    s=''
    j=0
    for i in rec:
        if i.RANK_MIN==r:
            s+=getCityName(sh,j,'en')+'\n'
            s+=str(getPop(sh,j))+'\n'
            s+=str(getCoords(sh,j))+'\n'
            s+=str(i.oid)+'\n'
            s+='\n'
        j+=1
    return s

#accessor method to get coordinates of Natural Earth cities
def getCoords(sh,i):
    r=getRec(sh,i)
    return (r.LONGITUDE,r.LATITUDE)

#returns city population (POP_MIN in database)
def getPop(sh,i):
    r=getRec(sh,i)
    return r.POP_MIN

#returns the continent of a given city
def getContinent(sh,j,lang='en'):#in order for this to work the adm0name has to be exactly the same as the country name
    s=createGetSF('SVS_Data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')#opens up database w actual continents for time being
    country=getRec(sh,j).ADM0NAME
    rec=getRec(s)
    i=0
    continent='N/A'#in case I don't want a specific continent I don't have to comment out
    for r in rec:
        if readingcountryshpfile.getNameWithLanguage(s,i,lang)==country:
            continent=rec[i].CONTINENT
            break
        i+=1
    closeThatSF(s)
    return continent

#opens shapefile from other file. can be done without this function.
def createGetSF(file):
    sh=shapefile.Reader(file)
    return sh

#closes shapefile from other file. can be done without this function
def closeThatSF(sh):
    sh.close()

"""Rarely used functions"""

#just returns array of all the available sections of the "shape" of a datapoint
def getShape(sh,i):
    s=sh.shapes()
    arr=[]
    for shape in dir(s[i]):
        if not shape.startswith('_'):
            arr.append(shape)
    return arr

#returns record of a shape for a data point
def getShapeRecs(sh,i,j):
    sr=sh.shapeRecords()
    return sr[i].record[j]

#returns string of all the cities in a country
def getCitiesFromCountry(sh,country):
    rec=getRec(sh)
    s=''
    j=0
    for i in rec:
        if i.ADM0NAME==country:
            s+=getCityName(sh,j,'en')+'\n'
            s+=str(getPop(sh,j))+'\n'
            s+=str(i.oid)+'\n'
        j+=1
    return s

#returns record of a city based on name. Sometimes not too accurate since some cities have the same name.
def getSpecificCity(sh,name):
    r=getRec(sh)
    for rec in r:
        if rec['name_en']==name:
            return rec

if __name__ == '__main__': main()