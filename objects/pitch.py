import pygame
from .Object import Object
class pitch(Object):
	def __init__(self,pos,length,depth):
		super().__init__(pos)
		self.length=length
		self.depth=depth
		self.color=(0,0,0)
		self.rect=pygame.Rect(pos,(length,depth))

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)

if __name__ == '__main__':
	p=pitch(30,2)
	print(p.name)