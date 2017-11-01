import pygame
from objects import pitch, ball, stump, bat
import stadiumParams
import random
import os
import math
pygame.init()

FPS = 30
display_width=800
display_height=600

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

displaySurf = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('cric')
clock = pygame.time.Clock()

paused = False

pitch=pitch.pitch(stadiumParams.pitchLineLeft,stadiumParams.pitch_length,5)
ball_pos=(pitch.pos[0]+ stadiumParams.pitch_length,pitch.pos[1]-stadiumParams.ball_height)

ball_boundary=pygame.Rect(0,100,int(stadiumParams.pitch_length*1.5),300)

ball=ball.ball(ball_pos,10,(-40.0,-3), ball_boundary)
stump=stump.stump(stadiumParams.stumpLineTop,3, stadiumParams.stumpLength)
bat=bat.bat(stadiumParams.batHandPos, 4, stadiumParams.batLength)
objects=[pitch,stump,ball,bat]


# main_dir = os.path.split(os.path.abspath(__file__))[0]
# data_dir = os.path.join(main_dir,'res')
# ballHitSound=pygame.mixer.Sound(os.path.join(data_dir,'sounds','baseball_hit_006.wav'))
score=stadiumParams.Score()
lastBallStatusStr="last ball :"
hitEventQueue=stadiumParams.HitEventQueue()


def showLastBallStatus():
	statusSurf=pygame.font.Font('freesansbold.ttf', 21).render(lastBallStatusStr,True,BLACK)
	statusRect=statusSurf.get_rect()
	statusRect.topleft=(30,450)
	displaySurf.blit(statusSurf,statusRect)

	scoreSurf=pygame.font.Font('freesansbold.ttf', 21).render(score.toStr(),True,BLACK)
	scoreRect=scoreSurf.get_rect()
	scoreRect.topleft=(500,40)
	displaySurf.blit(scoreSurf,scoreRect)

def updateLastBallStatus(distance):
	global lastBallStatusStr
	distance=abs(distance)
	cricEvent=''
	if(distance<100):
		if(hitEventQueue.getRecentHitEvent()&stadiumParams.HitEvent.HIT_STUMP>0):
			cricEvent='W'
		elif(hitEventQueue.getPastHitEvent()&stadiumParams.HitEvent.HIT_BAT>0):#recent hit event = hit_boundary
			cricEvent='W'
		else:
			cricEvent='0'
	elif(distance<200):
		cricEvent='1'
	elif(distance<300):
		cricEvent='2'
	elif(distance<400):
		cricEvent='3'
	elif(distance<500 or hitEventQueue.getPastHitEvent()&stadiumParams.HitEvent.HIT_PITCH>0):
		cricEvent='4'
	elif(distance>=500):
		cricEvent='6'

	lastBallStatusStr='last ball : '+cricEvent+' ('+str(round(distance,2))+'m)'
	# print(lastBallStatusStr)

	if(cricEvent=='W'):
		score.addWicket()
	else:
		score.addRuns(int(cricEvent))
	score.addBall()



running=True

while running:
	#captue events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				quit()
			if event.key == pygame.K_k:
				ball.kill()
			if event.key == pygame.K_SPACE:
				paused=not paused

		if event.type == pygame.MOUSEBUTTONDOWN:
			bat.startSwing()

		# if event.type == pygame.MOUSEMOTION:
		#   cursorPos=pygame.mouse.get_pos()
		#   bat.setAlignedTo(cursorPos)
	

	#update positions, color, text
	if not paused:
		bat.move(FPS)
		hitEvent=ball.move(FPS,bat)
		# print(hitEvent)
		stump.play(FPS)

		if(hitEvent!=stadiumParams.HitEvent.NONE):
			hitEventQueue.push(hitEvent)
			if(hitEvent&stadiumParams.HitEvent.HIT_BAT > 0):
				# paused=not paused
				# ballHitSound.play()
				bat.endSwing()
			elif(hitEvent&stadiumParams.HitEvent.HIT_STUMP > 0):
				ball.kill()
				stump.startDance()
				updateLastBallStatus(0)

			elif(hitEvent&stadiumParams.HitEvent.HIT_BOUNDARY > 0):
				ball.kill()
				height=(stadiumParams.pitchLineLeft[1]-ball.y)*(1/ball.meter2pixFactor)
				u=ball.vy
				d=math.sqrt(u*u+2*ball.gravity*height)
				t=(-u+d)/ball.gravity
				distance=ball.vx*t+(ball.x-bat.pos[0])*(1/ball.meter2pixFactor)

				updateLastBallStatus(distance)
			
		#draw
		displaySurf.fill(WHITE)
		
		for object in objects:
			object.draw(displaySurf)

		pygame.draw.rect(displaySurf, BLACK, ball_boundary, 2)

		showLastBallStatus()
		#update display
		pygame.display.update()

		if(ball.isDead):
			ball.reset((ball_pos[0],ball_pos[1]-random.randint(0,70)),(-random.randint(20,45),random.randint(0,5)-5))

	#wait
	clock.tick(FPS)     

pygame.quit()
quit()