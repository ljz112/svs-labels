#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingroadshpfile: reads/draws shapefile for roads

import readingshpfile
import writingonpic
import time

#not really that useful unless conducting tests from this function
def main():
    africasf=readingshpfile.shapefile.Reader('SVS_Data/groads/groads-v1-africa-shp/groads-v1-africa.shp')
    asiasf=readingshpfile.shapefile.Reader('SVS_Data/groads/groads-v1-asia-shp/groads-v1-asia.shp')
    europesf=readingshpfile.shapefile.Reader('SVS_Data/groads/groads-v1-europe-shp/groads-v1-europe.shp')
    americasf=readingshpfile.shapefile.Reader('SVS_Data/groads/groads-v1-americas-shp/gROADS-v1-americas.shp')
    eoceaniasf=readingshpfile.shapefile.Reader('SVS_Data/groads/groads-v1-oceania-east-shp/gROADS-v1-oceania-east.shp')
    woceaniasf=readingshpfile.shapefile.Reader('SVS_Data/groads/groads-v1-oceania-west-shp/gROADS-v1-oceania-west.shp')
    sfs=[africasf,asiasf,europesf,americasf,eoceaniasf,woceaniasf]
    longmin=-176.21930904899992
    longmax=-173.91425533799992
    latmin=-22.33879973799992
    latmax=-15.55950286299992
    scale=80000
    ranges=[longmin,longmax,latmin,latmax]
    pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','roads.png',ranges)
    drawRoads(sfs,ranges,pic,0)
    
#draws roads that are in given range. surprisingly, no label names. does take a while because of magnitude of database.
def drawRoads(sfs,range,p,rank):
    nums=[]
    r=[range[0],range[2],range[1],range[3]]
    for sf in sfs:
        if overlaps(sf.bbox,r,p) or overlaps(r,sf.bbox,p):
            recs=readingshpfile.getRec(sf)
            nums=[i for (i,rec) in enumerate(recs) for s in sf.shape(i).points if (rec.FCLASS==rank and range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
            nums=list(dict.fromkeys(nums))
            l=[p.drawLine(sf,num) for num in nums]
    p.save()
    
#checks if 2 bounding boxes overlap
def overlaps(s,o,p):
        return (((s[1]<=o[1]<=s[3]) or (s[1]<=o[1]+o[3]<=s[3]) or (s[1]<=o[1]<=o[3]<=s[3]) or (o[1]<=s[1]<=s[3]<=o[3])) and ((s[0]<=o[0]<=s[2]) or (s[0]<=o[2]<=s[2]) or (s[0]<=o[0]<=o[2]<=s[2]) or (o[0]<=s[0]<=s[2]<=o[2])))

if __name__ == '__main__': main()