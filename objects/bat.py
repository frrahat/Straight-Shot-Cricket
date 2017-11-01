import pygame
import math
from .Object import Object
class bat(Object):
	def __init__(self,pos,width,length):
		super().__init__(pos)
		self.width=width
		self.length=length
		self.color=(0,200,0)
		self.rect=pygame.Rect(pos,(width,length))
		self.endSwing()

	def draw(self, surface):
		pygame.draw.line(surface, self.color, self.pos, self.end_pos, self.width)


	def startSwing(self):
		self.isSwinging=True


	def endSwing(self):
		self.isSwinging=False
		self.angle=-1.0
		self.updateEndPos()

	def move(self,FPS):
		if not self.isSwinging:
			return

		self.angle+=4/FPS
		if(self.angle>1.5):
			self.endSwing()
			return

		self.updateEndPos()

		# print(self.end_pos)
	
	def updateEndPos(self):
		self.end_pos=(self.pos[0]+int(self.length*math.sin(self.angle)),\
			self.pos[1]+int(self.length*math.cos(self.angle)))

	def setAlignedTo(self,p):
		self.angle=math.atan2(p[0]-self.pos[0],p[1]-self.pos[1])
		self.updateEndPos()