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

class GameBoard:
	
	def __init__(self, top):
		self.chosenCards = []
		self.cardsDisplayed = [None] * 12
		self.images = [None] * 12
		self.deck = Deck()

		self.canvas = Canvas(top, width=900,height=500,bg='white')
		self.canvas.focus_set()
		self.canvas.bind("t",self.test)
		self.canvas.bind("h",self.hint)
		self.canvas.bind("<Button-1>", self.clicked)
		self.canvas.pack()

		for i in range(12):
			self.newCard(i)

	def newCard(self, index):
		card = self.deck.draw()
		self.cardsDisplayed[index] = card
		x,y = GameBoard.getCoordsByIndex(index)
		self.images[index] = self.canvas.create_image(x,y,image = Sprites.getSprite(card),anchor=NW)

	def getCoordsByIndex(index):
		return (10 + 200*(index % 4),10 + 150*(index // 4))

	def test(self,event):
		print(len(getAllSets(self.cardsDisplayed)))

	def hint(self,event):
		allsets = getAllSets(self.cardsDisplayed)
		if len(allsets) > 0:

			print(self.cardsDisplayed.index(allsets[0][0]),self.cardsDisplayed.index(allsets[0][1]),self.cardsDisplayed.index(allsets[0][2]))

	def clicked(self, event):
	    card = self.getClickedCard(event.x, event.y)
	    if card not in self.chosenCards:
	    	self.chosenCards.append(card)
	    print(len(self.chosenCards), "chosen")

	    if len(self.chosenCards) == 3:
	    	if isSet(self.chosenCards[0],self.chosenCards[1],self.chosenCards[2]):
	    		for i in range(3):
	    			curIndex = self.cardsDisplayed.index(self.chosenCards[i])
	    			self.canvas.delete(self.images[curIndex])
	    			self.newCard(curIndex)
	    		print("This is a set,",self.deck.getNumberOfCards(),"cards remaining")
	    	else:
	    		print("Not a set")
	    	self.chosenCards = []
	    #print("Card clicked",card.getAll())

	def getClickedCard(self, x, y):
		for i in range(12):
			imageX, imageY = GameBoard.getCoordsByIndex(i)
			if x >= imageX and x <= imageX + 200:
				if y >= imageY and y <= imageY + 150:
					return self.cardsDisplayed[i]

top = Tk()
Sprites.loadSprites()

gameBoard = GameBoard(top)

top.mainloop()