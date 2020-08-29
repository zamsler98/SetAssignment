

from tkinter import *
from Deck import *
from Sprites import *

top = Tk()

Sprites.loadSprites()

canvas = Canvas(top, width=900,height=500,bg='white')
canvas.pack()

deck = Deck()
deck.shuffle()

for i in range(12):
	card = deck.draw()

	canvas.create_image(10 + 200*(i % 4),10 + 150*(i // 4),image = Sprites.getSprite(card),anchor=NW)

top.mainloop()