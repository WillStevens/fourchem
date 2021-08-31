from math import cos,sin,pi,sqrt,atan,asin,acos
from random import random,uniform,seed,randint

import operator
import canvas
import time

def Distance(p1,p2):
  return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
  
sizeX = 1000
sizeY = 1200
scale = 10
offsetX = 300
offsetY = 300

rad=1.0
friction=0.1
repel=1.0
attract=0.04
repel2=0.04
thrust=0.03

noise=0.00

# This is equal to the number of states
exciteMax=3

canvas.set_size(sizeX,sizeY)

# 0 = wire: red, dark red, black
# 1 = exciter: magenta
# 2 = insulator : green
# 3 = thruster : cyan

def DrawNode(x,y,e,t):
#	canvas.draw_ellipse(offsetX+x*scale-rad*scale,offsetY+y*scale-rad*scale, rad*scale*2,rad*scale*2)
	canvas.set_fill_color(1.0 if e==2 else 0.5 if e==1 else 0.0,0.0 if t in [0,1] else 0.7,0.7 if t in [1,3] else 0.0)
	canvas.fill_ellipse(offsetX+x*scale-rad*scale,offsetY+y*scale-rad*scale, rad*scale*2,rad*scale*2)

nodePos=[]
nodeVel=[]
nodeExcite=[]

def Square(x,y,w,h,s,t):
	global nodePos,nodeVel,nodeExcite
	for i in range(0,w):
		for j in range(0,h):
			nodePos+=[x+i*s*rad,y+j*s*rad]
			nodeVel+=[0.0,0.0]
			nodeExcite+=[0,t]

def Pusher(x,y):
	global nodePos,nodeVel,nodeExcite
	nodePos+=[x,y,x+2,y,x+4,y,x+1,y+1.73,x+3,y+1.73,x,y+3.46,x+2,y+3.46,x+4,y+3.46]
	nodeVel+=[0.0]*16
	nodeExcite+=[0,3,0,1,0,2,0,3,0,1,0,3,0,1,0,2,0,2]
			
def FindNode(x,y,d):
	for i in range(0,len(nodePos),2):
		xi=nodePos[i]
		yi=nodePos[i+1]
		if Distance((x,y),(xi,yi))<d:
			return i
	return -1

def RandomUniverse():
	global nodePos,nodeVel,nodeExcite
	seed(196)
	for i in range(0,400):
		x=uniform(0,40)
		y=uniform(0,40)
		if FindNode(x,y,2.0*rad)==-1:
			nodePos+=[x,y]
			nodeVel+=[uniform(-0.1,0.1),uniform(-0.1,0.1)]
			nodeExcite+=[0,randint(0,3)]
		
def Test1():
	global nodePos,nodeVel,nodeExcite
	nodePos=[0,0,2,0,1,1.73,-1,1.73]
	nodeVel=[0,0,0,0,0,0,0,0]
	nodeExcite=[0,0,0,0,0,0,0,0]

def Test2():
	global nodePos,nodeVel,nodeExcite
	nodePos=[0.1,0.0,2.0,0.0,10.0,0.1,12.1,0.1]
	nodeVel=[0.0]*8
	nodeExcite=[0,3,0,1,0,1,0,3]
	
def Test3():
	global nodePos,nodeVel,nodeExcite
	nodePos=[0.1,0.0,2.0,0.0]
	nodeVel=[0.0]*4
	nodeExcite=[0,3,0,1]
	Square(10.0,-5.2,15,15,2,2)
	
def Test4():
	global nodePos,nodeVel,nodeExcite
	Pusher(0,0)
	nodePos+=[7,1.73]
	nodeVel+=[0.0]*2
	nodeExcite+=[0,2]
	Square(13,-5.2,10,10,2,2)

RandomUniverse()
#Test4()

t=0
while True:
	
	for i in range(0,len(nodePos),2):
		if nodeExcite[i]>0 and nodeExcite[i+1]==0:
			nodeExcite[i]-=1
		elif nodeExcite[i+1]==1:
			nodeExcite[i]=exciteMax-1
			
	if t%4==0:
		canvas.begin_updates()
		canvas.set_size(sizeX,sizeY)
		for i in range(0,len(nodePos),2):
			DrawNode(nodePos[i],nodePos[i+1],nodeExcite[i],nodeExcite[i+1])
		canvas.end_updates()
#	time.sleep(1)
	
	for i in range(0,len(nodePos)):
		nodePos[i]+=nodeVel[i]
		nodeVel[i]-=friction*nodeVel[i]


	for i in range(0,len(nodePos),2):
		for j in range(i+2,len(nodePos),2):
			d=Distance((nodePos[i],nodePos[i+1]),(nodePos[j],nodePos[j+1]))
			df=0
			dfi=0
			dfj=0
			
			if d<3.0*rad:
				if nodeExcite[j]==exciteMax-1 and nodeExcite[i]==0 and nodeExcite[i+1]==0:
					nodeExcite[i]=exciteMax
				if nodeExcite[i]==exciteMax-1 and nodeExcite[j]==0 and nodeExcite[j+1]==0:
					nodeExcite[j]=exciteMax
				if nodeExcite[j]==exciteMax-1 and nodeExcite[i+1]==3:
					dfi -= thrust
				if nodeExcite[i]==exciteMax-1 and nodeExcite[j+1]==3:
					dfj -= thrust
			
			if d<2.0*rad:
				f=(2.0*rad-d)
				df+=f*f*repel
			elif d<3.0*rad:
				f=1-(1+cos(2.0*pi*(d-2.0*rad)/(rad)))/2.0
				df-=f*attract
			elif d<3.46*rad:
				f=1-(1+cos(2.0*pi*(d-3.0*rad)/(0.46*rad)))/2.0
				df+=f*repel2
				
			if df!=0:
				xfi=(df+dfi)*(nodePos[j]-nodePos[i])/d
				yfi=(df+dfi)*(nodePos[j+1]-nodePos[i+1])/d
	
				xfj=(df+dfj)*(nodePos[j]-nodePos[i])/d
				yfj=(df+dfj)*(nodePos[j+1]-nodePos[i+1])/d
				
				nodeVel[i]-=xfi
				nodeVel[j]+=xfj
				nodeVel[i+1]-=yfi
				nodeVel[j+1]+=yfj
		nodeVel[i]+=uniform(-noise,noise)
		nodeVel[i+1]+=uniform(-noise,noise)
		
	t+=1
	
