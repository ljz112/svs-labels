#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#readingstateshpfile: reads/draws shapefile for subregions of countries. not really that useful to be honest because these boundaries change constantly

import readingshpfile
import writingonpic

#not really that useful unless conducting tests from this function
def main():
    with readingshpfile.shapefile.Reader('SVS_Data/ne_10m_admin_1_states_provinces_lines/ne_10m_admin_1_states_provinces_lines.shp') as sf:
        longmin=-120
        longmax=-60
        latmin=0
        latmax=90
        scale=2000
        ranges=[longmin,longmax,latmin,latmax]
        pic=writingonpic.Picture('L',int(scale*((longmax-longmin)/180)),int(scale*((latmax-latmin)/180)),'black','states.png',ranges)
        drawStates(sf,ranges,pic)
        
#draws the subregions
def drawStates(sh,range,p,cts=['United States of America']):
    recs=readingshpfile.getRec(sh)
    nums=[i for (i,shape) in enumerate(recs) for s in sh.shape(i).points if (range[0]<s[0]<range[1] and range[2]<s[1]<range[3])]
    nums=list(dict.fromkeys(nums))
    for num in nums:
        if cts.count(readingshpfile.getRec(sh,num).adm0_name)>0:
            p.drawLine(sh,num)
    p.save()

if __name__ == '__main__': main()