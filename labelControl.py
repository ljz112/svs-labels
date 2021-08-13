#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#labelControl: User interface to access all the drawing methods and available pictures

import writingonpic
import readingshpfile
import readingcountryshpfile
import jointTest
import readingdisputes
import readingrivershpfile
import nepalCities
import readingreefshpfile
import readingroadshpfile
import readingstateshpfile
import readingglaciatedshpfile
import argparse
import os
            
#User interface: sets the general criteria for the picture(s)
def main():
    dp,fp=getDP()
    s='What do you want pictures for? Options are cities, rivers, countries, disputes, roads, glaciated areas, and reefs. Type in "end" when finished.'
    list=[]
    list.append(input(s+'\n'))
    while not (len(list)>0 and list[len(list)-1]=='end'):
        list.append(input())
    coord='What coordinate range do you want the picture(s)? You can either write "world", "CONUS" for Continental US, a name of a specific country, or longmin,latmin,longmax,latmax.'
    range=input(coord+'\n')
    box=getBounds(range,dp)
    longmin=box[0]
    longmax=box[2]
    latmin=box[1]
    latmax=box[3]
    mindiff=longmax-longmin if (longmax-longmin<latmax-latmin) else latmax-latmin
    w=int(input('How many pixels do you want the smallest side of the image to be?\n'))
    scale=(w*180)/mindiff
    ranges=[longmin,longmax,latmin,latmax]
    name=input('What do you want the name of your image(s) to be? .png will be added later, and the pictures will be distinguished.\n')
    for l in list:
        getFile(l,ranges,scale,name,dp,fp)
    print('Picture drawing complete.')
        
#does the specific procedure for each cultural/geographical feature
def getFile(l,ranges,scale,name,dp,fp):
    keylang='en-English, de-German, es-Spanish, fr-French, pt-Portugese, ru-Russian, zh-Chinese, ar-Arabic, bn-Bengali, el-Greek, hi-Hindi, hu-Hungarian, id-Indonesian, it-Italian, ja-Japanese, ko-Korean, nl-Dutch, pl-Polish, sv-Swedish, tr-Turkish, vi-Vietnamese'
    if l=='cities':
        cityq='What scale rank do you want for your cities? Write "key" to get the key for scale ranks, otherwise enter the rank you want.'
        rank=input(cityq+'\n')
        if rank=='key':
            print('The key: 14>10 mil, 13>5 mil, 12>1 mil, 11>500k, 10>200k, 9>100k, 8>50k, 7>20k, 6>10k, 5>5k, 4>2k, 3>1k, 2>200, 1>0')
            rank=input('Which do you want?\n')
        rank=int(rank)
        lang=input('What language do you want? If you want the key, write "key".\n')
        if lang=='key':
            print(keylang)
            lang=input('Which do you want?\n')
        font=float(input('What font size do you want?\n'))
        fname=name+'_cities.png'
        pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_populated_places/ne_10m_populated_places.shp')) as sf:
            ans=input('Do you want dots with your labels? Answer with y or n.\n')
            if ans=='y':
                a=input('Do you want the labels below the dots, or to the side? Answer "below" or "side".\n')
                print('Drawing picture...',flush=True)
                if a=='below':
                    jointTest.drawWorldCities(sf,rank,pic,lang,ranges,font,True)
                elif a=='side':
                    jointTest.drawWorldCities(sf,rank,pic,lang,ranges,font,False)
            elif ans=='n':
                ans=input('Do you want your city labels as individual pictures? Reply with y or n. Also, these labels won\'t be distorted.\n')
                if ans=='y':
                    fsize=int(input('What font size do you want your labels to be?\n'))
                    filename=name+'_cities'
                    print('Writing .txt file for the cities\' locations...',flush=True)
                    nepalCities.gregText(sf,ranges,filename,lang,rank)
                    print('Text file with the locations written.')
                    print(os.path.abspath(filename))
                    print('Drawing pictures...',flush=True)
                    nepalCities.getLabelPics(sf,ranges,name,fsize,lang,rank)
                    print('Cities pictures drawn, in your home directory as filename_City_Name.png')
                    return
                elif ans=='n':
                    deg=int(input('How much do you want the labels rotated in degrees? Say 0 if you want none.\n'))
                    print('Drawing picture...',flush=True)
                    nepalCities.drawNepalCities(sf,rank,pic,ranges,False,deg,lang,font)
        print('Cities picture drawn.')
        print(os.path.abspath(fname))
    elif l=='rivers':
        ans=input('Do you want outlines, labels, or both for your rivers?\n')
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_rivers_lake_centerlines/ne_10m_rivers_lake_centerlines.shp')) as sf:
            if ans=='labels' or ans=='both':
                lang=input('What language do you want for the labels? If you want the key, write "key".\n')
                if lang=='key':
                    print(keylang)
                    lang=input('Which do you want?\n')
                fc=int(input('What default font size do you want? The rivers that can\'t be written in this font size will be taken away.\n'))
                fname=name+'_riverLabels.png'
                pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
                print('Drawing picture...',flush=True)
                arr=readingrivershpfile.drawRiverLabels(sf,ranges,pic,fc,lang,ans)
                print('River labels picture drawn.')
                print(os.path.abspath(fname))
            if ans=='outlines' or ans=='both':
                fname=name+'_rivers.png'
                pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
                print('Drawing picture...',flush=True)
                if ans=='both':
                    readingrivershpfile.drawSpecificRivers(sf,arr,pic)
                else:
                    readingrivershpfile.drawRivers(sf,ranges,pic)
                print('Rivers picture drawn.')
                print(os.path.abspath(fname))
    elif l=='countries':
        ans=input('Do you want outlines, labels, or both for your countries?\n')
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')) as sf:
            if ans=='labels' or ans=='both':
                lang=input('What language do you want for the labels? If you want the key, write "key".\n')
                if lang=='key':
                    print(keylang)
                    lang=input('Which do you want?\n')
                fc=int(input('What default font size do you want? The countries that can\'t be written in this font size will be taken away.\n'))
                fname=name+'_countryLabels.png'
                pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
                print('Drawing picture...',flush=True)
                readingcountryshpfile.drawLabels(sf,pic,ranges,fc,lang)
                print('Country labels picture drawn.')
                print(os.path.abspath(fname))
            if ans=='outlines' or ans=='both':
                fname=name+'_countries.png'
                pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
                reg=input('Do you want subregions with your countries? Reply with y if you do.\n')
                if reg=='y':
                    with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_admin_1_states_provinces_lines/ne_10m_admin_1_states_provinces_lines.shp')) as sh:
                        list=[]
                        list.append(input('What specific subregions do you want? Write the names of the countries, then write "end".\n'))
                        while not (len(list)>0 and list[len(list)-1]=='end'):
                            list.append(input())
                        print('Drawing subregions...',flush=True)
                        readingstateshpfile.drawStates(sh,ranges,pic,list)
                print('Drawing picture...',flush=True)
                readingcountryshpfile.drawCountries(sf,ranges,pic)
                print('Countries picture drawn.')
                print(os.path.abspath(fname))
    elif l=='disputes':
        ans=input('Do you want outlines, labels, or both for your disputed territories?\n')#just for outline now, before I figure out labels
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_admin_0_disputed_areas/ne_10m_admin_0_disputed_areas.shp')) as sf:
            if ans=='labels' or ans=='both':
                fname=name+'_disputeLabels.png'
                pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
                lang=input('What language do you want for the labels? If you want the key, write "key".\n')
                if lang=='key':
                    print(keylang)
                    lang=input('Which do you want?\n')
                fsize=int(input('What font size do you want?\n'))
                print('Drawing picture...',flush=True)
                arr=readingrivershpfile.drawRiverLabels(sf,ranges,pic,fsize,lang,ans,True)
                print('Disputes labels picture drawn.')
                print(os.path.abspath(fname))
            if ans=='outlines' or ans=='both':
                fname=name+'_disputes.png'
                pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
                print('Drawing picture...',flush=True)
                if ans=='both':
                    readingdisputes.drawSpecificDisputes(sf,arr,pic)
                else:
                    readingdisputes.drawDisputes(sf,ranges,pic)
                print('Disputes picture drawn.')
                print(os.path.abspath(fname))
    elif l=='reefs':
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_reefs/ne_10m_reefs.shp')) as sf:
            fname=name+'_reefs.png'
            pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
            print('Drawing picture...',flush=True)
            readingreefshpfile.drawReefs(sf,ranges,pic)
            print('Reefs picture drawn.')
            print(os.path.abspath(fname))
    elif l=='roads':
        africasf=readingshpfile.shapefile.Reader(os.path.join(dp,'groads/groads-v1-africa-shp/gROADS-v1-africa.shp'))
        asiasf=readingshpfile.shapefile.Reader(os.path.join(dp,'groads/groads-v1-asia-shp/gROADS-v1-asia.shp'))
        europesf=readingshpfile.shapefile.Reader(os.path.join(dp,'groads/groads-v1-europe-shp/gROADS-v1-europe.shp'))
        americasf=readingshpfile.shapefile.Reader(os.path.join(dp,'groads/groads-v1-americas-shp/gROADS-v1-americas.shp'))
        eoceaniasf=readingshpfile.shapefile.Reader(os.path.join(dp,'groads/groads-v1-oceania-east-shp/gROADS-v1-oceania-east.shp'))
        woceaniasf=readingshpfile.shapefile.Reader(os.path.join(dp,'groads/groads-v1-oceania-west-shp/gROADS-v1-oceania-west.shp'))
        sfs=[africasf,asiasf,europesf,americasf,eoceaniasf,woceaniasf]
        rank=input('What rank of roads do you want? Write "key" to see more options.\n')
        if rank=='key':
            print('The key: 1=Highway, 2=Primary, 3=Secondary, 4=Tertiary, 5=Local/Urban, 6=Trail, 7=Private, 0=Unspecified')
            rank=input('Which do you want?\n')
        rank=int(rank)
        fname=name+'_roads.png'
        pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
        print('Drawing picture...',flush=True)
        readingroadshpfile.drawRoads(sfs,ranges,pic,rank)
        print('Roads picture drawn.')
        print(os.path.abspath(fname))
    elif l=='glaciated areas':
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_glaciated_areas/ne_10m_glaciated_areas.shp')) as sf:
            fname=name+'_glaciated_areas.png'
            pic=writingonpic.Picture('L',int(scale*((ranges[1]-ranges[0])/180)),int(scale*((ranges[3]-ranges[2])/180)),'black',fname,ranges,fp)
            print('Drawing picture...',flush=True)
            readingglaciatedshpfile.drawGlaciatedAreas(sf,ranges,pic)
            print('Glaciated areas picture drawn.')
            print(os.path.abspath(fname))
    else:
        return
    
#returns the coordinate bounds that the user wants. Options are single country, Continental US, world, or manual entry of coordinate range
def getBounds(range,dp):
    if range=='world':
        return [-180,-90,180,90]
    elif not (range[0].isdigit() or range[0]=='-'):
        with readingshpfile.shapefile.Reader(os.path.join(dp,'ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')) as sf:
            if range=='CONUS':
                countid=readingcountryshpfile.getSpecificCountry(sf,'United States of America').oid
                return readingcountryshpfile.getBiggestBbox(sf,countid)
            else:
                countid=readingcountryshpfile.getSpecificCountry(sf,range).oid
                return sf.shape(countid).bbox
    else:
        l=range.split(',')
        l=[int(a) for a in l]
        return l

#probably will have to change the default datapath to svs/data/SVS_Data, just gets data path and checks it exists
def getDP():
    description='User interface to output .png pictures of outlines and labels for multiple geographical features over a set coordinate range.'
    parser=argparse.ArgumentParser(description=description,formatter_class=argparse.RawTextHelpFormatter)
    defaultdp='/svs/data/earth/Shapefiles/labels_data'
    #defaultdp='SVS_Data'
    defaultfp='/svs/share/lib/python/PILfonts/ttf/'
    #defaultfp='/Library/Fonts/'
    parser.add_argument('--datapath',default=defaultdp,help='specifies path where data files should be found (default:%(defaultdp)s)')
    parser.add_argument('--fontpath',default=defaultfp,help='specifies path where font files should be found (default:%(defaultfp)s)')
    options=parser.parse_args()
    if not os.path.exists(options.datapath):
        parser.error('Data path does not exist: {}'.format(options.datapath))
    elif not os.path.exists(options.fontpath):
        parser.error('Font path does not exist: {}'.format(options.fontpath))
    else:
        return (options.datapath,options.fontpath)

if __name__ == '__main__': main()