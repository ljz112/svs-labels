#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingglaciatedshpfile: reads/draws shapefile for glaciated areas. disclaimer: this database is kind of old (around 10 yrs), so some of these areas may be gone due to climate change. Doesn't have any names like reefs either. There are also weird boundaries in Greenland and Antarctica.

import readingshpfile
import writingonpic

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/ne_10m_glaciated_areas/ne_10m_glaciated_areas.shp') as sf:
        longmin=-180
        longmax=180
        latmin=-90
        latmax=90
        scale=1024
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','glaciated.png',ranges)
        drawGlaciatedAreas(sf,ranges,pic)

#draws glaciated areas onto picture
def drawGlaciatedAreas(sh,range,p):
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        p.drawCountry(sh,num)
    p.save()

if __name__ == '__main__': main()