from math import cos,sin,pi,sqrt,atan,asin,acos,floor
from random import random,uniform,seed,randint

import operator
import canvas
import time

def Distance(p1,p2):
  return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
  
sizeX = 800
sizeY = 1200
scale = 10
offsetX = 200
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

filename="⁨anim_%04d.png"
canvas.set_size(sizeX,sizeY)

# functions for constructing objects logo-style

penx = 0
peny = 0
angle = 0
penstack=[]

def Forward(d):
	global penx,peny
	penx += d*cos(angle*2.0*pi/360.0)
	peny += d*sin(angle*2.0*pi/360.0)
	
def Right(a):
	global angle
	angle -= a
	
def Left(a):
	global angle
	angle += a
	
def Atom(t):
	global nodePos,nodeVel,nodeExcite
	nodePos += [penx,peny]
	nodeVel+=[0.0,0.0]
	nodeExcite+=[0,t]

def Push():
	global penstack
	penstack += [(penx,peny,angle)]
	
def Pop():
	global penstack
	global penx,peny,angle
	(penx,peny,angle)=penstack[-1]
	penstack = penstack[:-1]
	
def Filament(n,t):
	for i in range(0,n):
		Atom(t)
		Forward(2)
		
def Filaturn(n):
	Forward(0.1)
	Atom(1)
	Forward(2)
	Filament(n,0)
	Right(0.1)
	Forward(0.1)
	Atom(3)

def Circle(n):
	for i in range(0,n):
		Atom(2)
		Left(360/n)
		Forward(2)

def Glider2():
	Atom(1)
	Forward(2.1)
	Atom(3)

def Thrustblock(n):
	Push()
	for i in range(0,n):
		Atom(0)
		Forward(2)
		Atom(3)
		Forward(-2)
		Left(90)
		Forward(2)
		Right(90)
	Pop()

def Test5():
	Atom(1)
	Forward(2)
	Atom(0)
	Forward(2)
	Thrustblock(5)
	
def Test7():
	Forward(10.1)
	Left(0.1)
	Push()
	Circle(80)
	Pop()
	Push()
	Left(90)
	Forward(4)
	Right(90)
	Circle(60)
	Pop()
	Left(90.2)
	Forward(8)
	Left(45)
	Glider2()
	Forward(14)
	Right(50)
	Glider2()
	Left(0)
	Forward(6)
	Filaturn(1)
		
def Test6():
	Push()
	Filaturn(8)
	Pop()
	Push()
	Left(90)
	Forward(2)
	Atom(2)
	Forward(2)
	Atom(2)
	Forward(2)
	Right(90)
	Filaturn(8)
	Pop()
	Left(90)
	Forward(3)
	Right(90)
	Forward(7)
	Atom(2)
	
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
	nodePos+=[x,y,x+2,y,x+4,y,x+1,y+1.73,x+3,y+1.73,x,y+3.46,x+2,y+3.46,x+4,y+3.46,x+2,y+5.46,x+2,y+7.46,x+2,y+9.46]
	nodeVel+=[0.0]*22
	nodeExcite+=[0,3,0,0,0,2,0,3,0,0,0,3,0,0,0,2,0,0,0,0,0,1]
			
def FindNode(x,y,d):
	for i in range(0,len(nodePos),2):
		xi=nodePos[i]
		yi=nodePos[i+1]
		if Distance((x,y),(xi,yi))<d:
			return i
	return -1

def RandomUniverse():
	global nodePos,nodeVel,nodeExcite
	seed(197)
	for i in range(0,500):
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
	Pusher(-5,21)
	nodePos+=[7,1.73]
	nodeVel+=[0.0]*2
	nodeExcite+=[0,2]
#	Square(13,4,6,1,2,2)

RandomUniverse()
#Test5()

t=0
while True:
	
	for i in range(0,len(nodePos),2):
		if nodeExcite[i]>0 and nodeExcite[i+1]==0:
			nodeExcite[i]-=1
		elif nodeExcite[i+1]==1:
			nodeExcite[i]=exciteMax-1
			
	if t%1==0:
		canvas.begin_updates()
		canvas.set_size(sizeX,sizeY)
		for i in range(0,len(nodePos),2):
			DrawNode(nodePos[i],nodePos[i+1],nodeExcite[i],nodeExcite[i+1])
		canvas.end_updates()
	#	canvas.save_png(filename % (t/4))
	#time.sleep(1)
	
	for i in range(0,len(nodePos)):
		nodePos[i]+=nodeVel[i]
		nodeVel[i]-=friction*nodeVel[i]

  # put node indices into boxes to speed up neighbour search later
	universeCell={}
			
	for i in range(0,len(nodePos),2):
		xc = floor(nodePos[i]/(4.0*rad))
		yc = floor(nodePos[i+1]/(4.0*rad))
		if (xc,yc) not in universeCell:
			universeCell[(xc,yc)]=set()
		universeCell[(xc,yc)].add(i)

	for i in range(0,len(nodePos),2):
#		possibleNeighbours=range(i+2,len(nodePos),2)
		possibleNeighbours=[]
		xc = floor(nodePos[i]/(4.0*rad))
		yc = floor(nodePos[i+1]/(4.0*rad))
		for xi in range(xc-1,xc+2):
			for yi in range(yc-1,yc+2):
				if (xi,yi) in universeCell:
					possibleNeighbours += list(universeCell[(xi,yi)])
		for j in possibleNeighbours:
			if j<=i:
				continue
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
	
