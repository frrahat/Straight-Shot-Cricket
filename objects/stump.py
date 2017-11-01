import pygame
from .Object import Object
class stump(Object):
	def __init__(self,pos,width,length):
		super().__init__(pos)
		self.width=width
		self.length=length
		self.color=(0,0,200)
		self.rect=pygame.Rect(pos,(width,length))
		self.isDancing=False
		self.danceTimeout=0

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)

	def play(self,FPS):
		if not self.isDancing:
			return

		if self.danceTimeout<0:
			self.stopDance()
			return

		self.danceTimeout-=(10/FPS)
		if(int(self.danceTimeout)%2==0):
			self.color=(255,0,0)
		else:
			self.color=(0,0,200)




	def startDance(self):
		self.isDancing=True
		self.danceTimeout=20

	def stopDance(self):
		self.isDancing=False
		self.color=(0,0,200)

