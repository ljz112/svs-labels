#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingreefshpfile: reads/draws shapefile for coral reefs

import readingshpfile
import writingonpic

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/ne_10m_reefs/ne_10m_reefs.shp') as sf:
        longmin=0
        longmax=5
        latmin=30
        latmax=35
        scale=120000
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','reefs.png',ranges)
        drawReefs(sf,ranges,pic)
        
#draws reefs onto a picture. in the form of lines, unfortunately no labels.
def drawReefs(sh,range,p):
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        p.drawLine(sh,num)
    p.save()

if __name__ == '__main__': main()