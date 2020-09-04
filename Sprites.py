from tkinter import *
from Card import *

class Sprites:
	
	normal = {}
	selected = {}
	gameIcon = None
	colorList = ['orange','blue','green']
	fillList = ['solid', 'open', 'geo']
	shapeList = ['circle', 'triangle','square']
	numList = ['1','2','3']

	def getAllCards(filePath):
		res = {}
		for i in range(3):
			for j in range(3):
				for k in range(3):
					for l in range(1,4):
						fileName = filePath+str(Sprites.colorList[i])+" "+str(Sprites.fillList[j])+" "+str(Sprites.shapeList[k])+str(l)+".gif"
						res[(i+1,j+1,k+1,l)] = PhotoImage(file=fileName)
		return res

	def loadSprites():
		Sprites.normal = Sprites.getAllCards("res/Normal/")
		Sprites.selected = Sprites.getAllCards("res/Selected/")
		Sprites.gameIcon = PhotoImage("res/gameIcon.ico")
		

	

	def getNormalSprite(card: Card):
		return Sprites.normal[card.getAll()]

	def getSelectedSprite(card: Card):
		return Sprites.selected[card.getAll()]
