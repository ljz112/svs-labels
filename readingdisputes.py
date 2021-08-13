#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingdisputes: contains drawing method for disputed boundaries

import readingshpfile
import writingonpic
import readingrivershpfile

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/ne_10m_admin_0_disputed_areas/ne_10m_admin_0_disputed_areas.shp') as sf:
        longmin=-180
        longmax=180
        latmin=-90
        latmax=90
        scale=2048
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','disputes.png',ranges)
        arr=readingrivershpfile.drawRiverLabels(sf,ranges,pic,10,'en','label',True)
        drawSpecificDisputes(sf,arr,pic)
        
#draws the disputed boundaries in given range
def drawDisputes(sh,range,p):
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        p.drawCountry(sh,num)
    p.save()

#draws specified disputed boundaries
def drawSpecificDisputes(sh,arr,p):
    for a in arr:
        p.drawCountry(sh,a)
    p.save()

if __name__ == '__main__': main()