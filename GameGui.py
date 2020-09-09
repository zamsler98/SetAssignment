from tkinter import *
from Deck import *
from Sprites import *
import random
import time

#Returns whether or not the three cards are a set
def isSet(card1, card2, card3):
	if card1 is None or card2 is None or card3 is None:
		return False
	colors = card1.getColor() + card2.getColor() + card3.getColor()
	fills = card1.getFill() + card2.getFill() + card3.getFill()
	shapes = card1.getShape() + card2.getShape() + card3.getShape()
	numbers = card1.getNumber() + card2.getNumber() + card3.getNumber()
	#1+1+1 = 3, 2+2+2=6, 3+3+3=9, 1+2+3=6
	valid = [3, 6, 9]
	return colors in valid and fills in valid and shapes in valid and numbers in valid

def getAllSets(cards):
	res = []
	for i in range(len(cards)):
		for j in range(i+1,len(cards)):
			for k in range(j+1,len(cards)):
				if (isSet(cards[i],cards[j],cards[k])):
					res.append((cards[i],cards[j],cards[k]))
	return res

class Grid:
	def __init__(self, canvas):
		self.canvas = canvas
		self.images = [None] * 15
		self.cardsDisplayed = [None] * 15

	def displayNewCard(self, card, index):
		if (len(self.images) > index):
			self.canvas.delete(self.images[index])
		self.cardsDisplayed[index] = card
		x,y = self.getCoordsByIndex(index)
		self.images[index] = self.canvas.create_image(x,y,image = Sprites.getNormalSprite(card),anchor=NW)

	def getCoordsByIndex(self,index):
		if index < 12:
			return (10 + 200*(index % 4),10 + 150*(index // 4))
		else:
			return (100 + 200 * (index - 12),460)

	def getClickedCard(self, x, y):
		for i in range(15):
			imageX, imageY = self.getCoordsByIndex(i)
			if x >= imageX and x <= imageX + 200:
				if y >= imageY and y <= imageY + 150:
					return self.cardsDisplayed[i]

	def selectCard(self, card):
		index = self.cardsDisplayed.index(card)
		self.canvas.delete(self.images[index])
		x,y = self.getCoordsByIndex(index)
		self.images[index] = self.canvas.create_image(x,y,image =Sprites.getSelectedSprite(card),anchor=NW)

	def unselectCard(self, card):
		index = self.cardsDisplayed.index(card)
		self.canvas.delete(self.images[index])
		x,y = self.getCoordsByIndex(index)
		self.images[index] = self.canvas.create_image(x,y,image=Sprites.getNormalSprite(card),anchor=NW)

	def removeCard(self,card):
		index = self.cardsDisplayed.index(card)
		self.removeCardAtIndex(index)

	def removeCardAtIndex(self, index):
		self.canvas.delete(self.images[index])
		self.cardsDisplayed[index] = None
		self.images[index] = None

	def getIndexOfCard(self, card):
		return self.cardsDisplayed.index(card)

	def addExtraCards(self, deck):
		for i in range(3):
			self.cardsDisplayed[12+i] = deck.draw()
			x,y = self.getCoordsByIndex(i + 12)
			self.images[12+i] = self.canvas.create_image(x,y,image =Sprites.getNormalSprite(self.cardsDisplayed[12+i]),anchor=NW)

	def hasSets(self):
		return len(getAllSets(self.cardsDisplayed)) > 0

	def hasExtraCards(self):
		return self.cardsDisplayed[14] is not None

	def clearExtras(self, chosenCards):
		for card in chosenCards:
			index = self.getIndexOfCard(card)
			if index < 12:
				self.removeCardAtIndex(index)
				for i in range(12,15):
					if self.cardsDisplayed[i] is not None:
						self.displayNewCard(self.cardsDisplayed[i],index)
						self.removeCardAtIndex(i)
						break
			else:
				self.removeCardAtIndex(index)
			
class Timer:
	def __init__(self):
		self.start = time.time()

	def start(self):
		self.start = time.time()

	def restart(self):
		elapsed = time.time() - self.start
		self.start = time.time()
		return elapsed

	def elapsed(self):
		elapsed = time.time() - self.start
		return elapsed

class GameBoard:
	
	def __init__(self, canvas, cardsRemainingLabel):
		self.chosenCards = []
		self.deck = Deck()

		self.cardsRemainingLabel = cardsRemainingLabel
		self.canvas = canvas
		#self.canvas.bind("t",self.test)
		self.canvas.bind("h",self.hint)
		#self.canvas.bind("x",self.extra)
		self.canvas.bind("<Button-1>", self.clicked)
		self.canvas.config(width=845,height=610)

		self.initGrid()

		self.timesPerSet = []
		self.mistakes = 0
		self.hintNumber = 0
		self.timer = Timer()

	def initGrid(self):
		self.grid = Grid(self.canvas)

		for i in range(12):
			self.newCard(i)

		if not self.grid.hasSets():
			self.grid.addExtraCards(self.deck)

		self.setCardsRemaining()

	def setCardsRemaining(self):
		self.cardsRemainingLabel["text"] = str(self.deck.getNumberOfCards())

	def newCard(self, index):
		if self.deck.getNumberOfCards() > 0:
			card = self.deck.draw()
			self.grid.displayNewCard(card,index)
		else:
			self.grid.removeCardAtIndex(index)

	def test(self,event):
		print(len(getAllSets(self.grid.cardsDisplayed)))

	def extra(self, event):
		if not self.grid.hasExtraCards() and self.deck.getNumberOfCards() > 0:
			self.grid.addExtraCards(self.deck)
			self.setCardsRemaining()

	def hint(self,event):
		self.hintNumber += 1
		allsets = getAllSets(self.grid.cardsDisplayed)
		if len(allsets) > 0:
			randSet = random.choice(allsets)
			for chosenCard in self.chosenCards:
				self.grid.unselectCard(chosenCard)
			self.chosenCards = [randSet[1]]
			self.grid.selectCard(self.chosenCards[0])
			#print(self.grid.cardsDisplayed.index(randSet[0]),self.grid.cardsDisplayed.index(randSet[1]),self.grid.cardsDisplayed.index(randSet[2]))

	def clicked(self, event):
	    card = self.grid.getClickedCard(event.x, event.y)
	    if card is None:
	    	return
	    if card not in self.chosenCards:
	    	self.chosenCards.append(card)
	    	self.grid.selectCard(card)
	    else:
	    	self.chosenCards.remove(card)
	    	self.grid.unselectCard(card)
	    	return

	    if len(self.chosenCards) == 3:
	    	if isSet(self.chosenCards[0],self.chosenCards[1],self.chosenCards[2]):
	    		self.setFound()
	    	else:
	    		for card in self.chosenCards:
	    			self.grid.unselectCard(card)
	    		self.mistakes += 1
	    	self.chosenCards = []

	def setFound(self):
		self.timesPerSet.append(self.timer.restart())
		if not self.grid.hasExtraCards():
			for i in range(3):
				curIndex = self.grid.getIndexOfCard(self.chosenCards[i])
				self.newCard(curIndex)
		else:
			self.grid.clearExtras(self.chosenCards)
		if not self.grid.hasSets():
			if self.deck.getNumberOfCards() > 0:
				self.grid.addExtraCards(self.deck)
			else:
				self.deckComplete()
		self.setCardsRemaining()

	def deckComplete(self):
		self.endGame()

	def endGame(self):
		self.canvas.delete("all")
		print(self.timesPerSet)
		label = Message(self.canvas, text="Sets found: "+str(len(self.timesPerSet)),font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 50, anchor=NW, window=label)
		if len(self.timesPerSet) == 0:
			self.timesPerSet.append(0)
		label = Message(self.canvas, text="Total time taken: "+str(round(sum(self.timesPerSet))) +" seconds",font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 100, anchor=NW, window=label)
		label = Message(self.canvas, text="Average time per set: "+str(round(sum(self.timesPerSet)/len(self.timesPerSet),2)) +" seconds",font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 150, anchor=NW, window=label)
		label = Message(self.canvas, text="Fastest time to find a set: "+str(round(min(self.timesPerSet),2)) +" seconds",font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 200, anchor=NW, window=label)
		label = Message(self.canvas, text="Longest time to find a set: "+str(round(max(self.timesPerSet),2)) +" seconds",font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 250, anchor=NW, window=label)
		label = Message(self.canvas, text="Number of mistakes made: "+str(self.mistakes),font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 300, anchor=NW, window=label)
		label = Message(self.canvas, text="Number of times hint was used: "+str(self.hintNumber),font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 350, anchor=NW, window=label)
		self.grid = Grid(self.canvas)

class TimedGame(GameBoard):
	def __init__(self, canvas, cardsRemainingLabel):
		GameBoard.__init__(self,canvas,cardsRemainingLabel)
		self.canvas.config(width=845,height=610)
		self.canvas.create_rectangle(820,10,840,445)
		self.bar = self.canvas.create_rectangle(820,10,840,445,fill='#ffa372')
		self.lengthOfBar = 435
		self.timeLimit = 30
		self.decksCompleted = 0
		self.timedGameTimer = Timer()
		self.updateBar()

	def updateBar(self):
		if (self.bar != None):
			elapsed = self.timedGameTimer.elapsed()
			if (elapsed < self.timeLimit):
				percent = elapsed / self.timeLimit
				self.canvas.delete(self.bar)
				y = 10 + int(self.lengthOfBar * percent)
				self.bar = self.canvas.create_rectangle(820,y,840,445,fill='#ffa372')
				self.canvas.after(10,self.updateBar)
			else:
				self.endGame()

	def setFound(self):
		self.timedGameTimer.restart()
		self.timeLimit = self.timeLimit * .9
		super().setFound()

	def remove(self):
		self.bar = None

	def deckComplete(self):
		self.decksCompleted += 1
		self.deck = Deck()
		self.initGrid()

	def endGame(self):
		super().endGame()
		label = Message(self.canvas, text="Decks fully completed: "+str(self.decksCompleted),font=("Constantia Bold Italic","16"),bg='light gray',width=500)
		self.canvas.create_window(50, 0, anchor=NW, window=label)

class GUI:
	def __init__(self):
		#Setting the taskbar icon
		#https://stackoverflow.com/a/34547834/7255437
		import ctypes
		myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

		top = Tk()
		top.configure(background='light gray')
		Sprites.loadSprites()
		top.title("SET")
		top.iconbitmap("res/gameIcon.ico")
		top.resizable(False,False)

		self.canvas = Canvas(top, width=810,height=610,bg='light gray',highlightthickness=0)
		self.canvas.focus_set()

		self.menu = Canvas(top,width=110,height=610,bg='light gray',highlightthickness=0)

		self.buttons = Canvas(top,width=810,height=50,bg='light gray',highlightthickness=0)

		self.canvas.grid(column=0,row=0)
		self.menu.grid(column=1,row=0)
		self.buttons.grid(row=1)

		self.cardsRemainingLabel = Label(self.menu, text='',bg='light gray',font=("Constantia Bold Italic", "24", "bold"))
		self.menu.create_window(10, 10, anchor=NW, window=self.cardsRemainingLabel)

		label = Message(self.menu, text="Cards remaining in the deck",font=("Constantia Bold Italic","12"),bg='light gray')
		self.menu.create_window(5, 50, anchor=NW, window=label)

		
		self.gameBoard = GameBoard(self.canvas, self.cardsRemainingLabel)

		self.hintButton = Button(self.buttons,text="Hint",command = self.hint, relief=FLAT, borderwidth=0)
		imgH = PhotoImage(file="res/buttons/Hint.gif")
		self.hintButton.config(image=imgH)
		self.buttons.create_window(690,20, window=self.hintButton)
		
		self.newGameButton = Button(self.buttons,text="New Game",command=self.newGame, relief=FLAT, borderwidth=0)
		imgN = PhotoImage(file="res/buttons/NewGame.gif")
		self.newGameButton.config(image=imgN)
		self.buttons.create_window(110,20, window=self.newGameButton)

		self.timedGameButton = Button(self.buttons,text="Timed Game",command=self.timedGame, relief=FLAT, borderwidth=0)
		imgT = PhotoImage(file="res/buttons/TimedGame.gif")
		self.timedGameButton.config(image=imgT)
		self.buttons.create_window(400,20, window=self.timedGameButton)

		top.mainloop()

	def newGame(self):
		if (isinstance(self.gameBoard,TimedGame)):
			self.gameBoard.remove()
		self.canvas.delete("all")
		self.gameBoard = GameBoard(self.canvas, self.cardsRemainingLabel)

	def timedGame(self):
		if (isinstance(self.gameBoard,TimedGame)):
			self.gameBoard.remove()
		self.canvas.delete("all")
		self.gameBoard = TimedGame(self.canvas, self.cardsRemainingLabel)

	def hint(self):
		self.gameBoard.hint(None)

