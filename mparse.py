import re

def mparse(rule):
	if re.search('None', rule): return None
	rules = {}
	rules['who'] = regex(r'PLAYER|ANY|ALL', rule)
	rules['what'] = regex(r'DECK|GRAVE|HAND|FIELD', rule)
	rules['action'] = regex(r'KILL|MOVE|SWAP|DISCARD|MORPH|OWN', rule)
	rules['direction'] = regex(r'LEFT|RIGHT|EITHER', rule)
	rules['receive'] = regex(r'KILLED', rule)
	rules['cards'] = r_cards(r'[\'"](.+?)[\'"]', rule)
	rules['cards_none'] = r_cards(r'![\'"](.+?)[\'"]', rule)
	return rules

def r_cards(str, rule):
	cards_dict = {}
	cards = regex(str, rule)
	if regex(r'&', cards): cards_dict['and'] = cards.split('&')
	elif regex(r'\|', cards): cards_dict['or'] = cards.split('|')
	else: return cards

	if 'and' in cards_dict:
		for i, clist in enumerate(cards_dict['and']):
			if regex(r'\|', clist): cards_dict['and'][i] = {'or': clist.split('|')}

	return cards_dict

def regex(str, rule):
	try:
		return re.search(str, rule).group(1)
	except:
		try:
			return re.search(str, rule).group()
		except:
			return None