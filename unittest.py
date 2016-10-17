import morphz

def run():
	#parseTest()
	gameStartTest()
	

def parseTest():
	parse = morphz.deckParse('default.xml')

	print "Listing %d cards in deck:" % len(parse.deck)
	for card in parse.deck:
		print card

def gameStartTest():
	chooseFunc = lambda x: 1
	game = morphz.Morphz('default', chooseFunc)
	print 'Game loaded...'

	print 'Cards in draw pile:'
	for card in game.getPile('draw'):
		print game.getCardByNum(card).getName()

	print

	displayHands(game)

	game.cardMove(0, game.handLoc(0), game.handLoc(1))

	displayHands(game)

def displayHands(game):
	for player in range(game.getNumPlayers()):
		print "Player %d's hand:" % (player + 1)
		for card in game.getHand(player):
			print game.getCardByNum(card).getName()
		print


if __name__ == '__main__':

	run()