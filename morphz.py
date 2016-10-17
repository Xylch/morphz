import time
import random
import re
import string
import xml.etree.ElementTree as xml


class Morphz:
#===========================================================================
#	Global Variables
#===========================================================================

	# Location dictionary
	LOC = {'draw':   0,
	       'grave':  1,
	       'remove': 2,
	       'field':  3, # Global field
	       'field1': 4, # Player 1 field
	       'field2': 5,
	       'field3': 6,
	       'field4': 7,
	       'field5': 8,
	       'field6': 9,
	       'hand1': 10, # Player 1 hand
	       'hand2': 11,
	       'hand3': 12,
	       'hand4': 13,
	       'hand5': 14,
	       'hand6': 15,
	       }

	# Pile dictionary
	PILE = {'draw':   [],
	        'grave':  [],
	        'remove': [], # Out of game
	}

	# Limit dictionary (-1 means no limit)
	LIMIT = {'draw':    1, # Amount to draw
	         'play':    1, # Amount to play
	         'hand':   -1, # Maximum number of cards you can have in your hand (does not count during your turn)
	         'keeper': -1, # Maximum number of keepers you can have on the field (does not count during your turn)
	}

	CARD_TYPES = ['ACTION', 'RULE', 'GOAL', 'KEEPER', 'CREEPER']
	CARDS = []
	HAND = [[], [], [], [], [], []] # Player hands
	FIELD = [[], [], [], [], [], [], []] # Cards in field, players 0-5, global 6
	DECK_NAME = ''
	PLAYERS = 2 # Number of players in game, up to 6 are allowed
	TURN = 0 # Which players turn is it, 0-5
	PLAYER = {} # Player dictionary for override rules, cards drawn and played this turn, etc.

	CHOOSE_FUNCTION = None # Function defined by interface to determine a card to choose when multiple options are available
	CHOOSE = {}

	def __init__(self, deck_name, choose_func):
		self.deckLoad(deck_name)
		self.DECK_NAME = deck_name
		self.CHOOSE_FUNCTION = choose_func
		self.createDrawPile()
		self.handDeal()
		self.turnReset()

	def createDrawPile(self):
		self.PILE['draw'] = [card_num for card_num in range(len(self.getDeck()))]
		self.deckShuffle()

	def turnReset(self):
		self.PLAYER['play'] = 0
		self.PLAYER['draw'] = 0

	def turnNext(self):
		self.TURN += 1
		if self.PLAYERS == self.TURN:
			self.TURN = 0
		self.turnReset()

	#=======================================================================
	# 	Location Functions
	#=======================================================================

	def getLocation(self, location):
		""" Takes in LOC constant and returns the list of cards associated with it """
		if location == self.LOC['draw']:
			return self.PILE['draw']
		elif location == self.LOC['grave']:
			return self.PILE['grave']
		elif location == self.LOC['remove']:
			return self.PILE['remove']
		elif location == self.LOC['field']:
			return self.FIELD[6]
		elif location >= self.LOC['field1'] and location <= self.LOC['field6']:
			return self.FIELD[location - self.LOC['field1']]
		elif location >= self.LOC['hand1'] and location <= self.LOC['hand6']:
			return self.HAND[location - self.LOC['hand1']]

	def handLoc(self, player):
		return self.LOC['hand' + str(player + 1)]

	def fieldLoc(self, player):
		if player == 6 or player == 'global':
			return self.LOC['field']

		return self.LOC['field' + str(player + 1)]

	def pileLoc(self, pile):
		return self.LOC[pile]

	#=======================================================================
	# 	Deck Functions
	#=======================================================================

	def deckLoad(self, deck_name):
		""" Loads a deck. """
		try:
			file = open('%s.xml' % deck_name)
		except IOError:
			return 'Falsed to open deck file %s.xml' % deck_name

		parse = deckParse(file)
		self.CARDS = [card for card in parse.deck]

	def deckShuffle(self):
		""" Shuffles the deck. """
		random.shuffle(self.PILE['draw'])

	def deckDraw(self, player, amount=1):
		""" Draws cards from the draw pile for <player> in the amount of [amount] """
		cards = []
		for i in range(amount):
			cards.append(self.PILE['draw'].pop(0))

		self.HAND[player].extend(cards)

		return cards

	#===============================================================================
	#	Rule Functions
	#===============================================================================

	def ruleParse(self, card):
		""" Parses the rule and does what it says. """
		rule_dict = card.rules

		if card.type == 'action':
			self.ruleAction(rule_dict)
		elif card.type == 'rule':
			self.ruleRule(rule_dict)

		return True

	def ruleAction(self, rule_dict):
		""" Executes action rules """
		if 'draw' in rule_dict:
			num = self.getNumConversion(rule_dict['draw'])
			drawn = self.deckDraw(self.getTurn(), num)

			if 'give' in rule_dict['draw']:
				give = rule_dict['draw']['give']

				if give['method'] == 'choose':
					players = []

					if give['to'] == 'all':
						if give['amount'] == 'even':
							even = len(drawn) / self.getNumPlayers()
							for i in range(even):
								players.extend(range(self.getNumPlayers()))


					for card in drawn:
						player = self.choosePlayer(players)
						players.remove(player)

						self.cardMove(card, self.handLoc(self.getTurn()), self.handLoc(player))

	def ruleRule(self, rule_dict):
		if 'limit' in rule_dict:
			self.setLimit(rule_dict['limit']['type'], rule_dict['limit']['amount'])

	def ruleGoal(self, rule_dict):
		self.setGoal(rule_dict)

	def goalCheck(self):
		goal = self.getGoal()
		if 'cards' in goal:
			cards = goal['cards']

			if cards['amount'] == 'all':
				player = self.playerHasCards(cards['name'])
				if player:
					self.gameWon(player)

	def playerHasCards(self, cards, loc = 'field'):
		if type(cards) is int:
			pass
		else:
			pass

	def gameWon(self, player):
		pass

	def getHand(self, player):
		return self.HAND[player]

	def getPile(self, pile):
		return self.PILE[pile]

	def getDeck(self):
		return self.CARDS

	def getGoal(self):
		return self.GOAL

	def setGoal(self, rule_dict):
		self.GOAL = rule_dict

	def setLimit(self, limit, amount):
		self.LIMIT[limit] = amount

	def getTurn(self):
		return self.TURN

	def getNumConversion(self, num):
		if num == '#players':
			return self.getNumPlayers()
		else:
			return int(num)

	def getNumPlayers(self):
		return self.PLAYERS

	def choosePlayer(self, players):
		return self.CHOOSE['player'](players)

	#===============================================================================
	# 	Hand Functions
	#===============================================================================

	def handDeal(self):
		""" Deals the hand. """
		map(lambda x: self.deckDraw(x, 3), range(self.getNumPlayers()))

	#===============================================================================
	#	Card Functions
	#===============================================================================

	def getCardByNum(self, card_num):
		return self.CARDS[card_num]

	def cardMove(self, card_num, location_from, location_to):
		"""
			Moves card <card_num> from <location_from> and puts it in <location_to>
			<location_from>: Any valid location in the LOC dictionary
			<location_to>:	 ..
		"""
		card_from = self.getLocation(location_from)
		card_to = self.getLocation(location_to)

		for i, card in enumerate(card_from):
			if card == card_num:
				card_to.append(card_from.pop(i))


	def cardPlay(self, player, card_num):
		""" Plays card <card_num> from <player>'s hand """
		if card_num not in self.HAND[player]: # Make sure player has the card in their hand
			return False

		if player == self.TURN:
			if self.PLAYER['play'] >= self.LIMIT['play']:
				return False

		card = self.getCardByNum(card_num)

		if card.getType() == 'keeper' or card.getType() == 'creeper':
			self.cardMove(card_num, self.handLoc(player), self.fieldLoc(player))
		elif card.getType() == 'rule':
			self.cardMove(card_num, self.handLoc(player), self.fieldLoc('global'))
		else:
			self.cardMove(card_num, self.handLoc(player), self.pileLoc('grave'))

		if player == self.TURN:
			if card.getType() != 'creeper':
				self.PLAYER['play'] += 1

			if self.PLAYER['play'] == self.LIMIT['play']:
				self.turnNext()

	def cardChoose(self, cards):
		return self.CHOOSE_FUNCTION(cards)


	#===============================================================================
	#	Field Functions
	#===============================================================================

	def fieldFind(self, find):
		""" Finds cards located in the field """
		pass


class deckParse:
	def __init__(self, file):
		tree = xml.parse(file)
		deck = tree.getroot()
		cards = deck.findall('card')

		card_list = []
		for card in cards:
			for i in range(int(card.get('amount', 1))):
				card_list.append(self.parse(card))

		self.deck = card_list

	def parse(self, card):
#		card_dict = {
#			'name':         card.get('name'),
#		    'label':        string.upper(self.getText(card, 'label', card.get('name'))),
#		    'type':         self.getText(card, 'type'),
#		    'subtype':      self.getText(card, 'subtype'),
#		    'description':  self.getText(card, 'description'),
#		    'rules':        self.parseRules(card)
#			}

		card_object = Card(card.get('name'),
		                   string.upper(self.getText(card, 'label', card.get('name'))),
		                   self.getText(card, 'type'),
		                   self.getText(card, 'subtype'),
		                   self.getText(card, 'description'),
		                   self.parseRules(card))

		return card_object

	def parseRules(self, card):
		rules = card.find('rules')
		if rules is None:
			return {}
		return self.xmlToDict(rules)

			
	def getText(self, base, tag, default = ''):
		element = base.find(tag)

		if element is None or element.text is None:
			return default

		pattern = re.compile(r'^\s+|\t|\s+$')
		return re.sub(pattern, '', element.text)

	def xmlToDict(self, base):
		xml_dict = {}

		children = list(base)
		if not children:
			return base.text

		for element in children:
			count = base.findall(element.tag)
			debug('base: %s\telement: %s\tcount: %d' % (base.tag, element.tag, len(count)))
			if len(count) > 1:
				xml_dict[element.tag] = []
				for tag in count:
					xml_dict[element.tag].append(self.xmlToDict(tag))
			else:
				try:
					xml_dict[element.tag]
				except KeyError:
					xml_dict[element.tag] = self.xmlToDict(element)

		return xml_dict

class Card:
	def __init__(self, name, label, type, subtype, description, rules):
		self.name = name
		self.label = label
		self.type = type
		self.subtype = subtype
		self.description = description
		self.rules = rules

	def getName(self):
		return self.name

	def getLabel(self):
		return self.label

	def getType(self):
		return self.type

	def getSubtype(self):
		return self.subtype

	def getDescription(self):
		return self.description

	def getRules(self):
		return self.rules

					


#===============================================================================
#	Helper Functions
#===============================================================================

def striplist(strlist):
	""" Takes a list of strings and returns it with whitespace stripped. """
	return [str.strip() for str in strlist]

def flattenlist(ilist):
	return [item for sublist in ilist for item in sublist]

DEBUG = False
def debug(statement):
	if DEBUG:
		print statement

def elapsed(s):
	print 'Time elapsed in seconds: %0.8f' % (time.time() - s)