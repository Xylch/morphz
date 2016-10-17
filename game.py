import morphz

def run():
	game = morphz.Morphz('zombie', choose)
	print 'Loaded deck %s.' % game.DECK_NAME

	# valid = game.deck_check()
	# if not valid == True:
		# print 'Deck has invalid syntax: %s' % valid
		# return False
	# print 'Deck has valid syntax.'
	print 'Cards in deck:'
	for card in game.CARDS:
		print '%s = %s' % (card['NAME'], game.ruleParse(card, True))

	print 'Shuffling deck.'
	game.deckShuffle()
	print 'Dealing hands.'
	game.handDeal()
	for p in range(game.PLAYERS):
		print 'Player', p + 1, 'hand:',
		for card in game.HAND[p]:
			print card + ',',
		print ''

	while True:
		#print '!!!HAND!!!', game.HAND
		print 'Player', game.TURN + 1, 'turn. Here are your cards:'
		for i, card in enumerate(game.HAND[game.TURN]):
			#print '!!!Name!!!', card
			card_dict = game.getCardByName(card)
			print str(i) + ')', 'Name:', card_dict['NAME'], '\tType:', card_dict['TYPE'], '\tSubtype:', card_dict['SUBTYPE']
			print 'Desc:', card_dict['DESC']
			print ''

		which = raw_input('Which card would you like to play (Enter the number): ')
		#print '!!!CName!!!', game.HAND[game.TURN][int(which)]
		game.cardPlay(game.TURN, game.HAND[game.TURN][int(which)])

def choose(items):
	choices = []
	print 'Choose one of the following cards:'
	for player in items:
		player_nums = 0
		print 'Player', str(player + 1) + '...'
		for i, card in enumerate(items[player]):
			print str(i) + ')', card
			choices.append([player, player_nums])
			player_nums += 1
	card_choice = raw_input('Which card would you like (Enter the number): ')

	chosen = {'player': choices[card_choice][0], 'card': items[choices[card_choice][0]][choices[card_choice][1]]}
	return chosen

run()
