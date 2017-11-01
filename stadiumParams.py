pitchLineLeft=(30,300)
pitch_length=400
# pitchLineRight=(pitchLineLeft[0]+pitch_length,pitchLineLeft[1])

stumpLineBottom=pitchLineLeft
stumpLength=60
stumpLineTop=(stumpLineBottom[0], stumpLineBottom[1]-stumpLength)
ball_height=40

batHandPos=(stumpLineTop[0]+50,stumpLineTop[1]-10)
batLength=stumpLength+10


class HitEvent:
	HIT_PITCH=1
	HIT_STUMP=2
	HIT_BAT=4
	HIT_BOUNDARY=8
	NONE=0

class HitEventQueue:
	def __init__(self):
		self.hitEvent_past=HitEvent.NONE
		self.hitEvent_recent=HitEvent.NONE

	def push(self,hitEvent):
		self.hitEvent_past,self.hitEvent_recent=self.hitEvent_recent,hitEvent

	def getRecentHitEvent(self):
		return self.hitEvent_recent

	def getPastHitEvent(self):
		return self.hitEvent_past


class Score:
	def __init__(self):
		self.runs=0
		self.wickets=0
		self.overs=0
		self.balls=0

	def addRuns(self,runs):
		self.runs+=runs

	def addWicket(self):
		self.wickets+=1

	def addBall(self):
		if(self.balls==5):
			self.overs+=1
			self.balls=0
		else:
			self.balls+=1

	def toStr(self):
		return str(self.runs)+'/'+str(self.wickets)+' ('+str(self.overs)+'.'+str(self.balls)+' ovrs)'