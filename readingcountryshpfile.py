#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingcountryshpfile: has all the country-writing/labelling methods in the utility

import readingshpfile
import writingonpic
import math
import time

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp') as sf:
        countname='South Korea'
        countid=getSpecificCountry(sf,countname).oid
        box=sf.shape(countid).bbox
        longmin=box[0]
        longmax=box[2]
        latmin=box[1]
        latmax=box[3]
        mindiff=longmax-longmin if (longmax-longmin<latmax-latmin) else latmax-latmin
        w=1500 
        scale=(w*180)/mindiff
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','countries.png',ranges)
        drawCountryLabel(sf,countid,pic)
        pic.drawCountry(sf,countid)
        getNamesAboveCharLimit(sf,20)
        
#prints the names that go above a given character limit, just for testing
def getNamesAboveCharLimit(sh,limit):
    count=[]
    for rec in readingshpfile.getRec(sh):
        name=rec.NAME_EN
        if len(name)>=limit:
            print(name)
            print(rec.as_dict())
            
     
#returns the country's name of the desired language
def getNameWithLanguage(sh,i,lang='en'):
    s='NAME_'+lang.upper()
    r=readingshpfile.getRec(sh,i)
    if len(r[s])>20 and lang=='en':
        s='NAME'
    return r[s]

#returns specific record of the country through searching by name. works if you know the official name of the country
def getSpecificCountry(sh,name):
    r=readingshpfile.getRec(sh)
    for rec in r:
        if rec['NAME_EN']==name:
            return rec
        
#returns the shape object of a specific country
def getShapes(sh,i):
    return sh.shapes()[i]

#draws each specific country label
def drawCountryLabel(sh,i,p,r,fsize,lang='en'):
    n=getNameWithLanguage(sh,i,lang)
    p.drawCountryLabel(sh,i,n,r,fsize,lang)
    
#draws all the countries in a given coordinate range
def drawCountries(sh,range,p):
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        p.drawCountry(sh,num)
    p.save()
    
#draws all the country labels in a given coordinate range
def drawLabels(sh,p,range,fc,lang='en'):
    fsize=int((fc*p.getSize()[1])/512)
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        r=getBiggestBbox(sh,num)
        drawCountryLabel(sh,num,p,r,fsize,lang)
    p.save()
    
#returns biggest 'part' of the country, important so that label is written in biggest landform
def getBiggestBbox(sh,i):
    shp=sh.shape(i)
    pts=shp.points
    part=shp.parts
    #find
    a=0
    longmin=180
    longmax=-180
    latmin=90
    latmax=-90
    for (j,pt) in enumerate(part):
        if len(part)==1:
            return shp.bbox
        elif j>=len(part)-1:
            break
        long=[p[0] for p in pts[part[j]:part[j+1]]]
        lat=[p[1] for p in pts[part[j]:part[j+1]]]
        b=(max(long)-min(long))*(max(lat)-min(lat))
        if b>a:
            a=b
            longmin=min(long)
            longmax=max(long)
            latmin=min(lat)
            latmax=max(lat)
    return [longmin,latmin,longmax,latmax]

if __name__=='__main__': main()