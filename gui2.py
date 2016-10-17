#/usr/bin/env python

import pygame
from pygame.locals import *
import morphz

class CardSprite(pygame.sprite.Sprite):
	def __init__(self, card, x = 0, y = 0, scale = 0.6, *groups):
		super(CardSprite, self).__init__(*groups)
		self.card = card
		type = card.getType()
		self.image = pygame.image.load('cards/Card-%s%s.png' % (type[0].upper(), type[1:]))
		self.image.convert()
		self.scale = scale

		self.rect = rect = self.image.get_rect()
		self.margin = rect.width / 5
		self.original = self.image

		black = (0, 0, 0)

		self.draw_border(black)

		font = pygame.font.Font('FreeSans.ttf', 20)
		font.set_bold(True)
		text = font.render(type.upper(), 1, black)
		self.image.blit(text, (self.margin, 10))

		text = font.render(card.getName(), 1, black)
		self.image.blit(text, (self.margin, self.rect.centery - 35))
		self.name = card.getName()

		if self.scale != 1.0:
			self.scaled = self.image = self.scale_surface(self.image)
			self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def scale_surface(self, surface):
		if self.scale == 1.0:
			return surface
		else:
			rect = surface.get_rect()
			return pygame.transform.scale(surface, (int(rect.width * self.scale), int(rect.height * self.scale)))

	def copy(self, scale = 1.0):
		return CardSprite(self.card, scale = scale)

	def draw_border(self, color):
		if color == 'black':
			color = (0, 0, 0)
		elif color == 'red':
			color = (255, 0, 0)

		rect = 0, 0, self.rect.width - 1, self.rect.height - 1
		pygame.draw.rect(self.image, color, rect, 1)

class CardGroup(pygame.sprite.LayeredUpdates):
	def __init__(self, *sprites, **kwargs):
		super(CardGroup, self).__init__(*sprites, **kwargs)

	def get_top_card(self):
		try:
			return self.get_sprites_at(pygame.mouse.get_pos())[-1]
		except IndexError:
			return


class Game:
	def main(self):
		pygame.init()

		screen = pygame.display.set_mode((1024, 700))
		pygame.display.set_caption('Morphz')

		game = morphz.Morphz('default', lambda: 1)

		hand = CardGroup()
		sprites = []

		rect = screen.get_rect()
		x = rect.centerx
		y = rect.bottom - 10
		for cn in game.getHand(0):
			card = game.getCardByNum(cn)
			sprite = CardSprite(card)
			sprites.append(sprite)

			sprite.rect.centerx = x
			sprite.rect.bottom = y
			print sprite.rect
			x += sprite.rect.width / 5

		hand.add(sprites)

		self.large_group = pygame.sprite.GroupSingle()
		self.large = None

		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				if event.type == MOUSEMOTION:
					if hand.get_sprites_at(pygame.mouse.get_pos()):
						right = hand.get_top_sprite().rect.right
						top = hand.get_top_sprite().rect.top
						top_card = hand.get_top_card()
						if top_card:
							self.large = top_card.copy()
							rect = screen.get_rect()
							self.large.rect.right = rect.right
							self.large.rect.bottom = rect.bottom

							self.large_group.add(self.large)

#							top_card.draw_border('red')
					else:
						if self.large:
							self.large_group.remove(self.large)
							self.large = None
#							top_card = hand.get_top_card()
#							if top_card:
#								top_card.draw_border('black')


				if event.type == MOUSEBUTTONDOWN:
					if hand.get_sprites_at(pygame.mouse.get_pos()):
						#print hand.get_sprites_at(pygame.mouse.get_pos())[-1].name
						print hand.get_top_card().name

			screen.fill((0, 255, 0))
			hand.draw(screen)
			self.large_group.draw(screen)

			pygame.display.flip()


def main():
	g = Game()
	g.main()

if __name__ == '__main__': main()