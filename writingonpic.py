#!/usr/bin/env python3

"""NASA SVS Label Utility Code
Written by Lucas Zurbuchen"""
#writingonpic: contains all the methods for drawing on a picture

from PIL import Image, ImageDraw, ImageFont
import math
import time
import os

#not really that useful unless conducting tests from this function
def main():
    longmin=45
    longmax=90
    latmin=45
    latmax=90
    ranges=[longmin,longmax,latmin,latmax]
    pic=Picture('L',2000,3000,'black','pic.png',ranges)

#holds all the information of each picture, contains all the picture-writing methods
class Picture:
    
    """constructor methods"""
    
    #constructor class for Picture objects
    def __init__(self, mode,x,y,color,name,ranges=[-180,180,-90,90],fp='/Library/Fonts/'):
        self.p=self.decompressCheck(x,y,mode,color)
        self.n=name
        self.draw=ImageDraw.Draw(self.p)
        self.r=ranges
        self.fontDP=fp
        
    #checks for decompression bomb error passed if someone makes a large picture. I think this works, but I'm not sure.
    def decompressCheck(self,x,y,mode,color):
        try:
            p=Image.new(mode,(x,y),color)
        except DecompressionBombError or DecompressionBombWarning:
            pass
            return Image.new(mode,(x,y),color)
        return p
        
    """picture drawing methods"""
    
    #adds normal text onto a picture
    def addText(self,text,x,y,color,fsize,lang='en'):
        f=self.langFont(lang)
        font=ImageFont.truetype(f,fsize)
        self.draw.text((x,y),text,font=font,fill=color)
        
    #draws dots and labels onto a picture with labels to side of the dot. Mostly for labelling cities.
    def mapWrite(self,text,long,lat,color,fsize,width,fontc=10,lang='en'):
        PI=math.pi
        latc=fontc*0.2
        sepc=fontc/10
        b=self.convert(long,lat)
        i=b[0]
        j=b[1]
        self.drawMapPoint(long,lat,color,width)
        a=self.convert(long+(0*(self.r[1]-self.r[0]))/360,lat+((latc*(self.r[3]-self.r[2]))/180))
        x=a[0]+self.convertOrig(-180+sepc,0)[0]
        y=a[1]
        self.addText(text,x+width,y,color,fsize,lang)
        img=Image.new('L',(1,1),'black')
        wh=list(self.getTextWH(text,fsize,lang))
        wh[0]+=2*width+self.convertOrig(-180+sepc,0)[0]
        img=self.p.transform((int(wh[0]//(math.cos((lat*PI)/180))),wh[1]),Image.EXTENT,data=[i-width,j-wh[1]//2,i+wh[0],j+wh[1]//2])
        self.p.paste(img,(i-width,j-wh[1]//2))
        
    #method to draw the dot label
    def drawMapPoint(self,long,lat,color,width):
        a=self.convert(long,lat)
        x=a[0]
        y=a[1]
        self.draw.ellipse(((x-width,y-width),(x+width,y+width)),fill=color)
        
    #method to draw countries and any other polygon shapefile data point
    def drawCountry(self,sh,i):
        shp=sh.shape(i)
        pts=shp.points
        part=shp.parts
        pts=[self.convert(p[0],p[1]) for p in pts]
        for (j,pt) in enumerate(part):
            if j>=len(part)-1:
                self.draw.polygon(pts[part[j]:len(pts)],fill=None,outline='white')
                break
            self.draw.polygon(pts[part[j]:part[j+1]],fill=None,outline='white')
            
    #method to draw any line object
    def drawLine(self,sh,i):
        shp=sh.shape(i)
        pts=shp.points
        part=shp.parts
        pts=[self.convert(p[0],p[1]) for p in pts]
        for (j,pt) in enumerate(part):
            if j>=len(part)-1:
                self.draw.line(pts[part[j]:len(pts)],fill='white')
                break
            self.draw.line(pts[part[j]:part[j+1]],fill='white')
            
    #draws country label onto picture. single default font, stretches spacing between characters to accomodate for space
    def drawCountryLabel(self,sh,i,n,range,fsize,lang='en'):
        PI=math.pi
        b=range
        hrange,vrange=self.convert(b[2],b[3])
        other=self.convert(b[0],b[1])
        hrange,vrange=[abs(hrange-other[0]),abs(vrange-other[1])]
        hfont,vfont=[0,0]
        s=self.convert((b[0]+b[2])/2,(b[1]+b[3])/2)
        lat=self.reverseConvert(0,s[1])[1]
        sf=math.cos((lat*PI)/180)
        div=2
        size=self.getTextWHSpaced(n,fsize,lang,0)
        if size[0]/sf>=hrange/div or size[1]>=vrange/div:
            return
        spacing=int((((hrange*sf)/div)-self.getTextWHSpaced(n,fsize,lang,0)[0])/(len(n)-1))
        wh=self.getTextWHSpaced(n,fsize,lang,spacing)
        x,y=[s[0]-(wh[0]//2),s[1]-(wh[1]//2)]
        self.addTextSpaced(n,x,y,'white',fsize,lang,spacing)
        img=self.p.transform((int(wh[0]/sf),wh[1]),Image.EXTENT,[x,y,x+wh[0],y+wh[1]])
        z=int(((wh[0]/sf)-wh[0])/2)
        self.p.paste(img,(x-z,y))
        
    #writes names centered upon the location of the point coordinate. no dot involved. also has an option to rotate the labels, but doesn't distort.
    def nepWrite(self,text,long,lat,color,fsize,deg=0,lang='en'):
        i,j=self.convert(long,lat)
        wh=list(self.getTextWH(text,fsize,lang))
        img=Picture('L',wh[0],wh[1],'black','buffer.png')
        img.addText(text,0,0,'white',fsize,lang)
        img=img.p.rotate(deg,expand=1)
        l=img.size
        self.p.paste(img,(i-(l[0]//2),j-(l[1]//2)))
        
    #writes names centered below the dot for point coordinate labels.
    def centWrite(self,text,long,lat,color,fsize,width,fontc=10,lang='en'):
        PI=math.pi
        self.drawMapPoint(long,lat,color,width)
        i,j=self.convert(long,lat)
        wh=list(self.getTextWH(text,fsize,lang))
        self.addText(text,i-(wh[0]//2),j,'white',fsize,lang)
        sf=math.cos((lat*PI)/180)
        img=self.p.transform((int(wh[0]/sf),wh[1]+width),Image.EXTENT,[i-(wh[0]//2),j-width,i+(wh[0]//2),j+wh[1]])
        z=int(((wh[0]/sf)-wh[0])/2)
        self.p.paste(img,(i-(wh[0]//2)-z,j-width))
    
    #adds text but with spacing option. no kerning. used for country labels.
    def addTextSpaced(self,txt,x,y,color,fsize,lang='en',spacing=0):
        f=self.langFont(lang)
        font=ImageFont.truetype(f,fsize)
        for (i,t) in enumerate(txt):
            self.draw.text((x,y),t,font=font,fill=color)
            if i<len(txt)-1:
                x+=self.getTextWH(t,fsize,lang='en')[0]+spacing
                
    #draws river label -- rotates and distorts
    def drawRiverLabel(self,name,scale,deg,fsize,lang,place):
        wh=self.getTextWH(name,fsize,lang)
        img=Picture('L',wh[0],wh[1],'black','buffer.png')
        img.addText(name,0,0,'white',fsize,lang)
        img=img.p.transform((int(wh[0]/scale),wh[1]),Image.EXTENT,[0,0,wh[0],wh[1]])
        img=img.rotate(deg,expand=1)
        self.p.paste(img,(int(place[0]),int(place[1])))
        
    """methods to get stats text, pictures, etc"""
    
    #converts global coordinates to picture pixels
    def convert(self,long, lat):
        x=int(((long-self.r[0])/(self.r[1]-self.r[0]))*self.p.size[0])
        y=self.p.size[1]-int(((lat-self.r[2])/(self.r[3]-self.r[2]))*self.p.size[1])
        return (x,y)
    
    #variation of convert() method but it converts as if the specific picture had the coordinate range of the entire world
    def convertOrig(self,long,lat):
        x=math.ceil(self.p.size[0]*((long+180)/360))
        y=int(self.p.size[1]*((90-lat)/180))
        return (x,y)
    
    #converts from pixels into global coordinates
    def reverseConvert(self,x,y):
        long=((x*(self.r[1]-self.r[0]))/self.p.size[0])+self.r[0]
        lat=(((self.p.size[1]-y)*(self.r[3]-self.r[2]))/self.p.size[1])+self.r[2]
        return (long,lat)
    
    #returns width and height of text at given font size
    def getTextWH(self,text,fsize,lang='en'):
        f=self.langFont(lang)
        font=ImageFont.truetype(f,fsize)
        w,h=self.draw.textsize(text,font=font)
        return (w,h)
    
    #returns size of picture
    def getSize(self):
        return (self.p.size[0],self.p.size[1])
    
    #returns Unicode font if the language needs it
    def langFont(self,lang):
        f='arial'
        if lang=='zh' or lang=='ja' or lang=='ko' or lang=='bn' or lang=='hi':
            f+='-unicode-ms'
        return os.path.join(self.fontDP,f+'.ttf')
    
    #returns width and height of text with set amount of spacing
    def getTextWHSpaced(self,text,fsize,lang='en',spacing=0):
        f=self.langFont(lang)
        font=ImageFont.truetype(f,fsize)
        h=self.draw.textsize(text,font=font)[1]
        l=[self.draw.textsize(t,font=font)[0] for t in text]
        w=sum(l)+(spacing*(len(text)-1))
        return (w,h)
    
    """other methods, like picture manipulation and some others that aren't really too used"""
    
    #crops an image and saves cropped image
    def cropper(self,tx,ty,bx,by):
        self.p=self.p.crop((tx,ty,bx,by))
        self.p.save(self.n)
    
    #scales an image by scale factor n for x, o for y. saves scaled picture.
    def scale(self,n,o):
        sf=(int(self.p.size[0]*n),int(self.p.size[1]*o))
        self.p=self.p.resize(sf)
        self.p.save(self.n)
    
    #pulls up picture right after code is run
    def show(self):
        self.p.show()
    
    #rotates picture by given angle in degrees
    def rotate(self,n=0):
        return self.p.rotate(n,expand=1)      
    
    #saves picture
    def save(self):
        self.p.save(self.n)

    #crops and resizes picture at the same time
    def transform(self,size,d):
        return self.p.transform(size,Image.EXTENT,data=d)
    
    #pastes picture on another
    def paste(self,pic,coord):
        self.p.paste(pic,coord)

"""holds information of all the labels for cities (and maybe rivers) before they are actually printed onto the picture"""
class Label:
    
    """constructor methods"""
    
    #constructor method for all Label class objects. used for cities
    def __init__(self,long,lat,name,p,fsize,popu,width,ranges,rank,cent=False,font=10,lang='en',b=True,deg=0):
        PI=math.pi
        self.name=name
        self.long=long
        self.lat=lat
        self.r=ranges
        self.width=width
        self.rank=rank
        self.p=p
        c=p.convert(self.long,self.lat)
        wh=list(p.getTextWH(name,fsize,lang))
        sepc=font/10
        if cent:
            wh[1]+=width
        elif b:
            wh[0]+=p.convertOrig(-180+sepc,0)[0]
            wh[0]+=2*width
        wh[0],wh[1]=[int(wh[0]*math.cos((deg*PI)/180)+wh[1]*math.sin((deg*PI)/180)),int(wh[0]*math.sin((deg*PI)/180)+wh[1]*math.cos((deg*PI)/180))]
        self.lab=(c[0],c[1],wh[0]/(math.cos((lat*PI)/180)),wh[1])
        self.popu=popu
        self.boo=True
        
    """overlap methods"""
    
    #simple overlap method -- for city labels with label on side of dot
    def overlaps(self,other):
        s=self.lab
        o=other.lab
        return (((s[1]<=o[1]<=s[1]+s[3]) or (s[1]<=o[1]+o[3]<=s[1]+s[3]) or (s[1]<=o[1]<=o[1]+o[3]<=s[1]+s[3]) or (o[1]<=s[1]<=s[1]+s[3]<=o[1]+o[3])) and ((s[0]<=o[0]<=s[0]+s[2]) or (s[0]<=o[0]+o[2]<=s[0]+s[2]) or (s[0]<=o[0]<=o[0]+o[2]<=s[0]+s[2]) or (o[0]<=s[0]<=s[0]+s[2]<=o[0]+o[2])))
    
    #overlap method for point labels without dot
    def overlapsCent(self,other):
        s=self.lab
        o=other.lab
        s0,s1=[s[0]-(s[2]/2),s[1]-(s[3]/2)]
        o0,o1=[o[0]-(o[2]/2),o[1]-(o[3]/2)]
        return (((s1<=o1<=s1+s[3]) or (s1<=o1+o[3]<=s1+s[3]) or (s1<=o1<=o1+o[3]<=s1+s[3]) or (o1<=s1<=s1+s[3]<=o1+o[3])) and ((s0<=o0<=s0+s[2]) or (s0<=o0+o[2]<=s0+s[2]) or (s0<=o0<=o0+o[2]<=s0+s[2]) or (o0<=s0<=s0+s[2]<=o0+o[2])))
    
    #overlap method for labels below dot
    def overlapsCentDot(self,other):
        s=self.lab
        o=other.lab
        s0,s1=[s[0]-(s[2]/2),s[1]-self.width]
        o0,o1=[o[0]-(o[2]/2),o[1]-other.width]
        return (((s1<=o1<=s1+s[3]) or (s1<=o1+o[3]<=s1+s[3]) or (s1<=o1<=o1+o[3]<=s1+s[3]) or (o1<=s1<=s1+s[3]<=o1+o[3])) and ((s0<=o0<=s0+s[2]) or (s0<=o0+o[2]<=s0+s[2]) or (s0<=o0<=o0+o[2]<=s0+s[2]) or (o0<=s0<=s0+s[2]<=o0+o[2])))
    
    """ other methods"""
    
    #default printing of labels is the name of the label/city/etc
    def __str__(self):
        return self.name
    
    #marks the overlap boolean set as false, means that it will not be printed on the picture
    def changeBoo(self):
        self.boo=False
        
    #returns the overlap boolean
    def getBoo(self):
        return self.boo
    
if __name__ == '__main__': main()