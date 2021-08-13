#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#nepalCities: labels cities without a dot, used this for Greg's Glacial Lakes

import readingshpfile
import writingonpic
import readingcountryshpfile

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/nepal-latest-free.shp/gis_osm_places_free_1.shp') as sf:
        s=readingshpfile.createGetSF('SVS_Data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
        countid=readingcountryshpfile.getSpecificCountry(s,'Nepal').oid
        box=s.shape(countid).bbox
        s.close()
        longmin=box[0]
        longmax=box[2]
        latmin=box[1]
        latmax=box[3]
        mindiff=longmax-longmin if (longmax-longmin<latmax-latmin) else latmax-latmin
        w=1500
        scale=(w*180)/mindiff
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','nepCities.png',ranges)
        drawNepalCities(sf,6,pic,ranges,False,45)
        
#returns coordinates of point(for city)
def getCoords(sh,i):
    return sh.shapes()[i].points[0]

#queries by name to find specific rec. not really that used, I think
def getSpecificPoint(sh,name):
    r=readingshpfile.getRec(sh)
    recs=[]
    for rec in r:
        if rec['name'].find(name)!=-1:
            recs.append(rec)
    return recs

#returns scale rank of city from OpenEarth database. only used if using Nepal specific database.
def getRank(sh,j):
    if __name__ == '__main__':
        n=readingshpfile.getRec(sh,j)['fclass']
        r=0
        if n=='national_capital':
            r=8
        elif n=='city':
            r=7
        elif n=='town':
            r=6
        elif n=='suburb':
            r=5
        elif n=='locality':
            r=4
        elif n=='county':
            r=3
        elif n=='village':
            r=2
        elif n=='hamlet':
            r=1
        else:
            r=0
        return r
    else:
        return readingshpfile.getRec(sh,j).RANK_MIN
    
#just like drawWorldCities in jointTest but for anything without a dot and with constant rotation
def drawNepalCities(sh,rank,p,range,dot,deg=0,lang='en',font=10):
    s=sh.shapes()
    rec=[r for r in readingshpfile.getRec(sh) if (getRank(sh,r.oid)>=rank and range[0]<s[r.oid].points[0][0]<range[1] and range[2]<s[r.oid].points[0][1]<range[3])]
    labels=[]
    for i in rec:
        j=i.oid
        c=s[j].points[0]
        r=getRank(sh,j)
        b=deleteNonAsc(i,sh,lang).strip()
        if __name__ == '__main__':
            pop=i['population']
            fc=font
        else:
            pop=i.POP_MIN
            fc=(font*getRank(sh,j))//14
        if b:
            labels.append(writingonpic.Label(c[0],c[1],b,p,int((fc*p.getSize()[1])/512),pop,int((((r/2)+1)*p.getSize()[1])/833),range,r,False,fc,lang,dot,deg))
    labels=sorted(labels,key=lambda l:l.lab[0])
    j=0
    i=0
    for l in labels:
        j=1
        while i+j<len(labels) and l.lab[0]<=labels[i+j].lab[0] and l.lab[0]+l.lab[2]>=labels[i+j].lab[0]:
            if dot:
                x=l.overlaps(labels[i+j])
                y=labels[i+j].overlaps(l)
            else:
                x=l.overlapsCent(labels[i+j])
                y=labels[i+j].overlapsCent(l)
            if (x or y) and l.getBoo() and labels[i+j].getBoo():
                if l.popu>=labels[i+j].popu:
                    labels[i+j].changeBoo()
                else:
                    l.changeBoo()
            j+=1
        i+=1
    for l in labels:
        if l.getBoo():
            a=(l.long,l.lat)
            b=l.name
            if __name__ == '__main__':
                fc=font
            else:
                fc=(font*getRank(sh,j))//14
            if dot:
                p.mapWrite(b,a[0],a[1],'white',int((fc*p.getSize()[1])/512),int((((l.rank/2)+1)*p.getSize()[1])/833))
            else:
                p.nepWrite(b,a[0],a[1],'white',int((fc*p.getSize()[1])/512),deg,lang)
    p.save()
    
#returns all the types of classes. just because I wanted to see one day
def getClassTypes(sh):
    types=[]
    for r in readingshpfile.getRec(sh):
        if types.count(r['fclass'])==0:
            types.append(r['fclass'])
    return types

#takes away the chinese/nepali characters in the labels in the nepal-specific database
def deleteNonAsc(i,sh,lang='en'):
    if __name__ == '__main__':
        worldwide=i['name']
        b=worldwide
        for mr in worldwide:
            if not (ord(mr)<=127):
                b=b.replace(mr,'')
        return b
    else:
        worldwide=readingshpfile.getCityName(sh,i.oid,lang)
        return worldwide
    
#returns .txt file of coordinates and names of cities in a Maya-compatible format.
def gregText(sh,range,fname='otherLabels',lang='en',rank=0):
    s=sh.shapes()
    rec=[r for r in readingshpfile.getRec(sh) if (getRank(sh,r.oid)>=rank and range[0]<s[r.oid].points[0][0]<range[1] and range[2]<s[r.oid].points[0][1]<range[3])]
    text=open(fname+'.txt','w')
    text.write('//      name        lon     lat     alt(maya)       scale\n')
    text.write('string $labels_list[]={')
    for (i,r) in enumerate(rec):
        j=r.oid
        c=s[j].points[0]
        b=deleteNonAsc(r,sh,lang).strip()
        if b:
            text.write(f'"{b}",')
            text.write(f'"{c[0]}",')
            text.write(f'"{c[1]}",')
            text.write('"0.0",')
            if i==len(rec)-1:
                text.write('"0.2"\n};')
            else:
                text.write('"0.2"\n,')
    text.close()
    
#return a series of pictures, one label for each picture. so that the labels can hover above the ground.
def getLabelPics(sh,range,fname='label',fsize=100,lang='en',rank=0):
    s=sh.shapes()
    rec=[r for r in readingshpfile.getRec(sh) if (getRank(sh,r.oid)>=rank and range[0]<s[r.oid].points[0][0]<range[1] and range[2]<s[r.oid].points[0][1]<range[3])]
    for (i,r) in enumerate(rec):
        b=deleteNonAsc(r,sh,lang).strip()
        if b:
            vers=b.replace(' ','_')
            name=f'{fname}_{vers}.png'
            temp=writingonpic.Picture('L',1,1,'white','')
            wh=temp.getTextWH(b,fsize,lang)
            p=writingonpic.Picture('L',wh[0],wh[1],'black',name)
            p.addText(b,0,0,'white',fsize,lang)
            p.save()
            
#just returns .txt file of the bounds of the region.
def getRangeTxt(b):
    text=open('nepalBound.txt','w')
    text.write(f'longmin: {b[0]}\n')
    text.write(f'longmax: {b[2]}\n')
    text.write(f'latmin: {b[1]}\n')
    text.write(f'latmax: {b[3]}')
    text.close()
    
if __name__ == '__main__': main()