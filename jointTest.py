#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#jointTest: contains city writing label methods for those with dots

import readingshpfile
import writingonpic
import nepalCities

#not really that useful unless conducting tests from this function
def main():
    longmin=-180   
    longmax=180
    latmin=-90
    latmax=90
    scale=1024
    ranges=[longmin,longmax,latmin,latmax]
    pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','worldCities.png',ranges)
    sf=readingshpfile.shapefile.Reader('SVS_Data/ne_10m_populated_places/ne_10m_populated_places.shp')
    drawWorldCities(sf,10,pic,'en',ranges,1.25,True)
    sf.close()
    
#method that stores all the information of cities that meet criteria, does overlap algorithm, and prints those that pass the overlap algorithm
def drawWorldCities(sh,level,p,lang,range,font,cent=False):
    rec=readingshpfile.getRec(sh)
    rec=[r for r in readingshpfile.getRec(sh) if (r.RANK_MIN>=level and range[0]<r.LONGITUDE<range[1] and range[2]<r.LATITUDE<range[3])]
    div=(10/font)*6
    labels=[]
    for r in rec:
        b=readingshpfile.getCityName(sh,r.oid,lang)
        if b:
            a=readingshpfile.getCoords(sh,r.oid)
            fc=font*(r.RANK_MIN/14)
            dc=div*(14/r.RANK_MIN)
            labels.append(writingonpic.Label(a[0],a[1],b,p,int((fc*p.getSize()[1])/512),r.POP_MIN,int(((r.RANK_MIN*p.getSize()[1])/512)/dc),range,r.RANK_MIN,cent,fc,lang,True,0))
    if cent:
        labels=sorted(labels,key=lambda l:l.lab[0]-l.lab[2]/2)
    else:
        labels=sorted(labels,key=lambda l:l.lab[0])
    i=0
    for l in labels:
        j=1
        while i+j<len(labels):
            if cent:
                a=(l.lab[0]-l.lab[2]/2<=labels[i+j].lab[0]-labels[i+j].lab[2]/2<=l.lab[0]+l.lab[2]/2)
            else:
                a=(l.lab[0]<=labels[i+j].lab[0]<=l.lab[0]+l.lab[2])
            if a:
                if cent:
                    x=l.overlapsCentDot(labels[i+j])
                    y=labels[i+j].overlapsCentDot(l)
                else:
                    x=l.overlaps(labels[i+j])
                    y=labels[i+j].overlaps(l)
                if (x or y) and l.getBoo() and labels[i+j].getBoo():
                    if l.popu>labels[i+j].popu:
                        labels[i+j].changeBoo()
                    else:
                        l.changeBoo()
            j+=1
        i+=1   
    for l in labels:
        if l.getBoo():
            a=(l.long,l.lat)
            b=l.name
            fc=font*(l.rank/14)
            dc=div*(14/l.rank)
            if cent:
                p.centWrite(b,a[0],a[1],'white',int((fc*p.getSize()[1])/512),int(((l.rank*p.getSize()[1])/512)/dc),fc,lang)
            else:
                p.mapWrite(b,a[0],a[1],'white',int((fc*p.getSize()[1])/512),int(((l.rank*p.getSize()[1])/512)/dc),fc,lang)
    p.save()
    
if __name__ == '__main__': main()