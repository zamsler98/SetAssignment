from tkinter import *
from Card import *

class Sprites:
	
	sprites = {}


	def loadSprites():
		colorList = ['red','blue','green']
		fillList = ['solid', 'shaded', 'clear']
		shapeList = ['circle', 'triangle','square']
		numList = ['1','2','3']
		filePath = "CardImages/"
		for i in range(3):
			for j in range(3):
				for k in range(3):
					for l in range(1,4):
						fileName = filePath+str(colorList[i])+" "+str(fillList[j])+" "+str(shapeList[k])+str(l)+".gif"
						Sprites.sprites[(i+1,j+1,k+1,l)] = PhotoImage(file=fileName)

	def getSprite(card: Card):
		return Sprites.sprites[card.getAll()]
