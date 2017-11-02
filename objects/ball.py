import pygame
from .Object import Object
import stadiumParams
import math
import random

def getDist(p1,p2):
	return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

class ball(Object):
	meter2pixFactor=10
	def __init__(self, pos, radius, velocity, ball_boundary):
		super().__init__(pos)
		self.radius=radius
		self.color=(255,0,0)
		self.boundary=ball_boundary
		self.reset(pos,velocity)
		

	def draw(self, surface):
		pygame.draw.circle(surface, self.color, self.pos, self.radius)

	def move(self, FPS, bat):
		hitEvent=stadiumParams.HitEvent.NONE

		if self.isDead:
			return hitEvent

		if self.ifHitBoundary():
			hitEvent|=stadiumParams.HitEvent.HIT_BOUNDARY
			return hitEvent

		t=1/FPS
		self.x=self.x+self.vx*t*self.meter2pixFactor
		self.y=self.y+(self.vy+0.5*self.gravity*t)*t*self.meter2pixFactor


		self.pos=(int(self.x),int(self.y))
		# print(self.x,self.y,int(self.x),int(self.y))
		self.vy=self.vy+self.gravity*t


		if self.ifHitPitch():
			#velocity will change
			# before=self.vy
			if(self.vx<0):
				self.vx=self.vx*random.randint(8,20)/10
				self.vy=-(self.vy*random.randint(3,15)/10)
			else:
				self.vx=self.vx*0.9
				self.vy=-(self.vy*0.7)
			# print('pitched : ',self.vx,'|', before,'-->',self.vy)
			if(abs(self.vx)<5 and abs(self.vy)<0.5):
				hitEvent|=stadiumParams.HitEvent.HIT_LAZY
				return hitEvent

			hitEvent|=stadiumParams.HitEvent.HIT_PITCH

		if self.ifHitStump():
			hitEvent|=stadiumParams.HitEvent.HIT_STUMP
			return hitEvent

		
		#hit bat checking and update
		if(abs(self.pos[0]-bat.pos[0])<bat.length and self.vx<0):
			a=bat.pos[1]-bat.end_pos[1]
			b=-(bat.pos[0]-bat.end_pos[0])
			c=-(b*bat.pos[1]+a*bat.pos[0])
			d2=(a**2+b**2)
			d=math.sqrt(d2)
			p=abs(a*self.pos[0]+b*self.pos[1]+c)/d
			# print(p)
			if(p<(self.radius)):
				# print('\n','#'*10,'\ndist:',p)
				k=b*self.pos[0]-a*self.pos[1]
				x1=(b*k-a*c)/d2
				y1=(-a*k-b*c)/d2
				t1=getDist((x1,y1),bat.pos)
				t2=getDist((x1,y1),bat.end_pos)
				q=bat.length+self.radius
				# print('--',t1,t2,'|',bat.length+self.radius*2-t1-t2)
				if(t1<q and t2<q):#bat hit
					#normal is(b/d,-a/d), normal to the bat
					dotProduct=self.vx*a+self.vy*b #avoided division by d
					normalValue=1
					if bat.isSwinging:
						normalValue+=(t1/bat.length)*0.8

					k=2*dotProduct*normalValue
					# print('prev vx, vy :',self.vx,self.vy)
					self.vy=self.vy-(k*b)/d2
					self.vx=self.vx-(k*a)/d2
					# print(bat.angle, '|', normalValue, '|',self.vx,'|',self.vy)
					
					hitEvent |= stadiumParams.HitEvent.HIT_BAT
					return hitEvent
				# else: bat didn't hit
			# else: near outside of bat hit area
		# else: far from bat
		return hitEvent

	def getVlocity(self):
		return self.velocity

	def getHeight(self):
		return self.height


	def ifHitBoundary(self):
		if(self.x<self.boundary.x or self.y<self.boundary.y or\
		 self.x>(self.boundary.x+self.boundary.w) or self.y>(self.boundary.y+self.boundary.h)):
			return True
		return False 

	def ifHitPitch(self):
		if(self.vy>0 and self.y+self.radius+0.5>stadiumParams.pitchLineLeft[1]):
			return True
		return False

	def ifHitStump(self):
		if(abs(self.pos[0]-stadiumParams.stumpLineTop[0])<(self.radius+5) and \
			(self.pos[1]+self.radius)>=stadiumParams.stumpLineTop[1]):
			return True
		return False

	# def powerIfHitBat(self,bat,t):
	# 	if(abs(self.pos[0]-bat.pos[0])<bat.length):
	# 		a=bat.pos[1]-bat.end_pos[1]
	# 		b=-(bat.pos[0]-bat.end_pos[0])
	# 		c=-(b*bat.pos[1]+a*bat.pos[0])

	# 		k=b*self.pos[1]+c
	# 		p0=a*self.pos[0]+k
	# 		x1=self.x+self.vx*t*self.meter2pixFactor
	# 		p1=a*int(x1)+k

	# 		if(p0*p1<0):
	# 			t1=getDist(self.pos,bat.pos)
	# 			t2=getDist(self.pos,bat.end_pos)
	# 			q=bat.length+self.radius
	# 			# print('--',t1,t2,'|',bat.length+self.radius*2-t1-t2)
	# 			if(t1<q and t2<q):
	# 				if not bat.isSwinging:
	# 					return 1
	# 				return t1
	# 	return -1


	def reset(self,pos,velocity):
		self.pos=pos
		self.vx=velocity[0]
		self.vy=velocity[1]
		self.x=pos[0]
		self.y=pos[1]
		self.isDead=False

	def kill(self):
		self.isDead=True