#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingrivershpfile: contains drawing and labelling methods for rivers

import readingshpfile
import writingonpic
import readingcountryshpfile
import math

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/ne_10m_rivers_lake_centerlines/ne_10m_rivers_lake_centerlines.shp') as sf:
        i=1034
        num=i
        box=sf.shape(num).bbox
        longmin=box[0]-10
        longmax=box[2]+10
        latmin=box[1]-10
        latmax=box[3]+10
        mindiff=longmax-longmin if (longmax-longmin<latmax-latmin) else latmax-latmin
        w=1500
        scale=(w*180)/mindiff
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','rivers.png',ranges)
        lab=drawRiverLabels(sf,ranges,pic,10,'en','both')
            
#only draws rivers
def drawRivers(sh,range,p):
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        p.drawLine(sh,num)
    p.save()
    
#finds the location of each possible river label
def drawRiverLabel(sh,ind,p,fsize,dis,lang):
    PI=math.pi
    label=[]
    shp=sh.shape(ind)
    pts=shp.points
    part=shp.parts
    ptsc=[p.convert(pt[0],pt[1]) for pt in pts]
    rnum=0
    if dis:
        n=readingcountryshpfile.getNameWithLanguage(sh,ind,lang)
    else:
        n=readingshpfile.getCityName(sh,ind,lang)
        rnum=readingshpfile.getRec(sh,ind).rivernum
    wh=p.getTextWH(n,fsize,lang)
    i=0
    for pt in ptsc:
        if i>=len(ptsc):
            break
        tlat=pts[i][1]
        sf=math.cos((tlat*PI)/180)
        ws=wh[0]/sf
        j=getStartingIndex(ptsc,i,ws)
        while i+j<len(pts)-1 and getDistance(pt,ptsc[i+j])<2*ws:
            dist=getDistance(pt,ptsc[i+j])
            if dist==0:
                j+=1
                break
            deg=(math.asin(abs(ptsc[i+j][1]-pt[1])/dist)/PI)*180
            if not ((pt[0]<ptsc[i+j][0] and pt[1]>ptsc[i+j][1]) or (pt[0]>ptsc[i+j][0] and pt[1]<ptsc[i+j][1])):
                deg*=-1
            w,h=[ws*math.cos((deg*PI)/180)+wh[1]*abs(math.sin((deg*PI)/180)),ws*abs(math.sin((deg*PI)/180))+wh[1]*math.cos((deg*PI)/180)]
            if pt[1]>ptsc[i+j][1]:
                low=pt
                high=ptsc[i+j]
            else:
                low=ptsc[i+j]
                high=pt
            if deg>0:
                posx=low[0]-((wh[1]*math.sin((deg*PI)/180))/2)
                posy=low[1]-(h-((wh[1]*math.cos((deg*PI)/180))/2))
            else:
                posx=high[0]+((wh[1]*math.sin((deg*PI)/180))/2)
                posy=high[1]-((wh[1]*math.cos((deg*PI)/180))/2)
            r=[posx,posy,posx+w,posy+h]
            boo=True
            inside=ptsc[i:i+j]
            for ins in inside:
                if j==1:
                    break
                if not (r[0]<ins[0]<r[2] and r[1]<ins[1]<r[3]):
                    boo=False
                    break
            if boo:
                place=[r[0],r[1]]
                label.append(RiverLabel(n,sf,deg,fsize,lang,place,ind,r,rnum))
                i+=j
                break
            j+=1
        i+=1
    return label

#just distance formula to get distance between two points
def getDistance(o,t):
    return ((o[0]-t[0])**2+(o[1]-t[1])**2)**0.5

#gets index to start on for the while loop in the river label method
def getStartingIndex(ptsc,i,length):
    j=0
    while i+j<len(ptsc)-1 and getDistance(ptsc[i],ptsc[i+j])<length:
        j+=1
    return j

#draws all the river labels
def drawRiverLabels(sh,range,p,fc,lang,s='label',dis=False):
    fsize=int((fc*p.getSize()[1])/512)
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    riverlabels=[]
    for num in nums:
        label=drawRiverLabel(sh,num,p,fsize,dis,lang)
        for l in label:
            if l.listed[0]:
                riverlabels.append(l)
    riverlabels=sorted(riverlabels,key=lambda l:l.lab[0])
    i=0
    for l in riverlabels:
        j=1
        while i+j<len(riverlabels):
            a=(l.lab[0]<=riverlabels[i+j].lab[0]<=l.lab[2])
            if a:
                x=l.rOverlaps(riverlabels[i+j])
                y=riverlabels[i+j].rOverlaps(l)
                if (x or y) and l.getBoo() and riverlabels[i+j].getBoo():
                    if isFirstDistBigger(sh,i,i+j):
                        riverlabels[i+j].changeBoo()
                    else:
                        l.changeBoo()
            j+=1
        i+=1
    arr=[]
    for rl in riverlabels:
        if rl.boo:
            n,sf,deg,fsize,lang,place,ind=rl.listed
            p.drawRiverLabel(n,sf,deg,fsize,lang,place)
            if s=='both':
                if dis:
                    rivnum=[ind]
                else:
                    rivnum=[r.oid for r in readingshpfile.getRec(sh) if (r.rivernum==rl.rnum)]
                if __name__ == '__main__':
                    for riv in rivnum:
                        p.drawLine(sh,riv)
                else:
                    for riv in rivnum:
                        arr.append(riv)
    p.save()
    arr=list(dict.fromkeys(arr))
    return arr

#draws only the rivers specified from the river labelling, so that layered design is easier to carry out
def drawSpecificRivers(sh,arr,p):
    for a in arr:
        p.drawLine(sh,a)
    p.save()
    
#returns if the first mentioned river has a greater distance from start to end than the other. a little iffy, but no stats for river length in here.
def isFirstDistBigger(sh,i,j):
    shp=sh.shape(i)
    ptsone=shp.points
    shp=sh.shape(j)
    ptstwo=shp.points
    onedist=getDistance(ptsone[0],ptsone[-1])
    twodist=getDistance(ptstwo[0],ptstwo[-1])
    return onedist>twodist

#holds information of all the labels for cities (and maybe rivers) before they are actually printed onto the picture. the writingonpic label class didn't work for what I wanted.
class RiverLabel:
    
    #constructor class
    def __init__(self,name,scale,deg,fsize,lang,place,index,range,rnum):
        self.listed=(name,scale,deg,fsize,lang,place,index)
        self.lab=range
        self.rnum=rnum
        self.boo=True

    #quick copied alg to see if labels overlap
    def rOverlaps(self,other):
        s=self.lab
        o=other.lab
        return (((s[1]<=o[1]<=s[3]) or (s[1]<=o[3]<=s[3]) or (s[1]<=o[1]<=o[3]<=s[3]) or (o[1]<=s[1]<=s[3]<=o[3])) and ((s[0]<=o[0]<=s[2]) or (s[0]<=o[2]<=s[2]) or (s[0]<=o[0]<=o[2]<=s[2]) or (o[0]<=s[0]<=s[2]<=o[2])))
    
    #copied, returns overlap boolean
    def getBoo(self):
        return self.boo
    
    #copied, changes overlap boolean so label/river isn't written down
    def changeBoo(self):
        self.boo=False

if __name__=='__main__': main()