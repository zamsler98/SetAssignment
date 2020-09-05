import Card
Card = Card.Card

class Deck:
    
    def __init__(self):
        self.cardList = []

        for color in range(1,2):
            for fill in range(1,4):
                for shape in range(1,4):
                    for number in range(1,4):
                        self.cardList.append(Card(color, fill, shape, number))
        self.shuffle()

    #Gets the number of cards that are left
    def getNumberOfCards(self):
        return len(self.cardList)

    #Removes the top card from the deck and returns it
    def draw(self):
        return self.cardList.pop()

    #shuffle method with three shuffles
    def shuffle(self):
        import random
        random.shuffle(self.cardList)
        random.shuffle(self.cardList)
        random.shuffle(self.cardList)
        return self.cardList
