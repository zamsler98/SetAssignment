from tkinter import *
from Deck import *
from Sprites import *

#Returns whether or not the three cards are a set
def isSet(card1, card2, card3):
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
		self.images = [None] * 12
		self.cardsDisplayed = [None] * 12

	def displayNewCard(self, card, index):
		if (len(self.images) > index):
			self.canvas.delete(self.images[index])
		self.cardsDisplayed[index] = card
		x,y = self.getCoordsByIndex(index)
		self.images[index] = self.canvas.create_image(x,y,image = Sprites.getNormalSprite(card),anchor=NW)

	def getCoordsByIndex(self,index):
		return (10 + 200*(index % 4),10 + 150*(index // 4))

	def getClickedCard(self, x, y):
		for i in range(12):
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
		self.canvas.delete(self.images[index])

	def getIndexOfCard(self, card):
		return self.cardsDisplayed.index(card)

class GameBoard:
	
	def __init__(self, top):
		self.chosenCards = []
		self.deck = Deck()

		self.canvas = Canvas(top, width=900,height=500,bg='white')
		self.grid = Grid(self.canvas)
		self.canvas.focus_set()
		self.canvas.bind("t",self.test)
		self.canvas.bind("h",self.hint)
		self.canvas.bind("<Button-1>", self.clicked)
		self.canvas.pack()

		for i in range(12):
			self.newCard(i)

	def newCard(self, index):
		card = self.deck.draw()
		self.grid.displayNewCard(card,index)

	def test(self,event):
		print(len(getAllSets(self.grid.cardsDisplayed)))

	def hint(self,event):
		allsets = getAllSets(self.grid.cardsDisplayed)
		if len(allsets) > 0:
			print(self.grid.cardsDisplayed.index(allsets[0][0]),self.grid.cardsDisplayed.index(allsets[0][1]),self.grid.cardsDisplayed.index(allsets[0][2]))

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
	    		for i in range(3):
	    			curIndex = self.grid.getIndexOfCard(self.chosenCards[i])
	    			self.newCard(curIndex)
	    		print("This is a set,",self.deck.getNumberOfCards(),"cards remaining")
	    	else:
	    		for card in self.chosenCards:
	    			self.grid.unselectCard(card)
	    		print("Not a set")
	    	self.chosenCards = []

	

#Setting the taskbar icon
#https://stackoverflow.com/a/34547834/7255437
import ctypes
myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

top = Tk()
Sprites.loadSprites()
top.title("")
top.iconbitmap("res/gameIcon.ico")


gameBoard = GameBoard(top)

top.mainloop()