pitchLineLeft=(30,300)
pitch_length=600
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
	HIT_LAZY=16
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

class RecentBallsQueue():
	def __init__(self):
		self.balls=['-','-','-','-','-','-']

	def push(self,cricEvent):
		del self.balls[0]
		self.balls.append(cricEvent)

	def toStr(self):
		s=''
		for i in range(5):
			s+=self.balls[i]+', '
		s+=self.balls[5]
		return s

class Score:
	def __init__(self):
		self.runs=0
		self.wickets=0
		self.overs=0
		self.balls=0
		self.currentPartnership=0
		self.partnerShipBalls=0
		self.recentOverRuns=0
		self.recentOverWickets=0
		self.lastOverRuns=0
		self.lastOverWickets=0
		self.battingScoreCard=BattingScoreCard()

	def addRuns(self,runs):
		self.battingScoreCard.addRuns(runs)#should precede addBall
		self.runs+=runs
		self.recentOverRuns+=runs
		self.currentPartnership+=runs
		self.__addBall()

	def addWicket(self):
		self.battingScoreCard.dropWicket()#should precede addBall
		self.wickets+=1
		self.currentPartnership=0
		self.recentOverWickets+=1
		self.__addBall()
		self.partnerShipBalls=0


	def __addBall(self):
		self.partnerShipBalls+=1
		if(self.balls==5):
			self.overs+=1
			self.balls=0
			self.lastOverRuns=self.recentOverRuns
			self.lastOverWickets=self.recentOverWickets
			self.recentOverWickets=self.recentOverRuns=0
			self.battingScoreCard.startNewOver()
		else:
			self.balls+=1

	def toStr(self):
		return str(self.runs)+'/'+str(self.wickets)+' ('+str(self.overs)+'.'+str(self.balls)+' ovrs)'

	def getRunRate(self):
		totalBalls=(self.overs*6+self.balls)
		if(totalBalls==0):
			return 0.00
		runRate=round((self.runs*6)/totalBalls,2)
		return runRate

	def getCurrentPartnerShipStr(self):
		return str(self.currentPartnership)+' ('+str(self.partnerShipBalls)+')*'

	def getLastOverScoreStr(self):
		return str(self.lastOverRuns)+' runs, '+str(self.lastOverWickets)+' wickets'



class BattingScoreCard:
	def __init__(self):
		self.batsMen=[[0,0,False] for i in range (11)]
		self.currentBatsManIndices=[0,1]
		self.hittingBatsmanIndex=0

	def addRuns(self,runs):
		batsmanIndex=self.currentBatsManIndices[self.hittingBatsmanIndex]
		self.batsMen[batsmanIndex][0]+=runs	
		self.batsMen[batsmanIndex][1]+=1
		if(runs%2==1):
			self.__swapBatsmanPositions()


	def dropWicket(self):
		#dropHittingBatsman
		batsmanIndex=self.currentBatsManIndices[self.hittingBatsmanIndex]
		self.batsMen[batsmanIndex][1]+=1
		self.batsMen[batsmanIndex][2]=True
		newBatsmanIndex=max(self.currentBatsManIndices)+1
		del self.currentBatsManIndices[self.hittingBatsmanIndex]

		#new batsman coming in the crease
		self.currentBatsManIndices.append(newBatsmanIndex)
		self.hittingBatsmanIndex=1 #last of the two item list


	def startNewOver(self):
		self.__swapBatsmanPositions()

	def __swapBatsmanPositions(self):
		self.hittingBatsmanIndex = 1 - self.hittingBatsmanIndex

	def getBatsmanScoreStrAt(self, index):
		scr=self.batsMen[index]
		s=str(index+1)+'. '+chr(65+index)
		if(index==self.currentBatsManIndices[self.hittingBatsmanIndex]):
			s+=' ** '
		else:
			s+=' -- '
		if(scr[1]>0 or index in self.currentBatsManIndices):
			s+=str(scr[0])+' ('+str(scr[1])+')'
			if(scr[2]==False):
				s+='*'
		return s