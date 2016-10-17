import cocos
import cocos.layer
import cocos.sprite
import cocos.text
import pyglet
import morphz
from cocos.director import director


class Background(cocos.layer.ColorLayer):
	def __init__(self):
		super(Background, self).__init__(0, 255, 0, 255)

		#director.window.maximize()


class CardDisplay(cocos.layer.Layer):
	def __init__(self):
		super(CardDisplay, self).__init__()

		self.scale = 0.6
		self.anchor = (0, 0)

		sprites = []

		hand = game.getHand(game.getTurn())
		for card_num in hand:
			card = game.getCardByNum(card_num)
			sprites.append(CardSprite(card))

		x = director.window.width / 2 - (len(sprites) * 30 / 2)
		y = sprites[0].height / 2
		x, y = self.point_to_local((x, y))

		for sprite in sprites:
			sprite.position = x, y
			self.add(sprite)
			x += 30

		sprite.on_top = True


class CardLabel(cocos.text.RichLabel):
	def __init__(self, text, position, bold = False, font_size = 12, color = (0, 0, 0, 255), ucase = False, **kwargs):
		if ucase: text = text.upper()
		super(CardLabel, self).__init__(text, position, bold = bold, font_size = font_size, color = color, **kwargs)

class CardSprite(cocos.sprite.Sprite):
	is_event_handler = True

	def __init__(self, card, **kwargs):
		type = card.getType()
		type = type[0].upper() + type[1:]

		self.card = card

		super(CardSprite, self).__init__('cards/Card-%s.png' % type, **kwargs)
		director.window.push_handlers(self.on_mouse_press)
		director.window.push_handlers(self.on_mouse_motion)

		self._border_red_ = cocos.sprite.Sprite('cards/Card-Border-Red.png')
		self.highlight = False
		self.on_top = False

		border = cocos.sprite.Sprite('cards/Card-Border-Black.png')
		self.add(border)

		base_x = -52
		type_pos = (base_x, 114)
		label_pos = (base_x - 13, -125)
		name_pos = (base_x, 30)

		color_white = (255, 255, 255, 225)

		type = card.getType()
		if type == 'rule':
			type = 'new rule'

		text = CardLabel(type, type_pos, True, 16, ucase = True)
		self.add(text)

		name = card.getLabel()

		if type == 'creeper':
			text = CardLabel(name, label_pos, True, color = color_white)
		else:
			text = CardLabel(name, label_pos, True)

		text.rotation = -90

		self.add(text)

		name = card.getName()
		text = CardLabel(name, name_pos, True, width = 135, height = 38, multiline = True)

		print text.element.content_height
		text.element.content_valign = 'bottom'
		
		self.add(text)

	def is_highlighted_card(self, x, y):
		rect = self.get_rect()
		#x, y = self.point_to_local((x, y))
		rect.x, rect.y = self.point_to_local((rect.position))
		rect.width, rect.height = (rect.width * 0.6, rect.height * 0.6)
		if rect.contains(x, y):
			print 'rect:\t\tx: %d\ty: %d' % (rect.x, rect.y)
			print 'norm:\t\tx: %d\ty: %d' % (x, y)
			if self.on_top:
				return True
			else:
				width = self.width - 30
				if rect.contains(x + width, y):
					return True

		return False

	def on_mouse_press(self, x, y, button, modifiers):
		if self.is_highlighted_card(x, y):
			pass

	def ToFront(self):
		parent = self.parent
		parent.remove(self)
		parent.add(self, 1)

	def ToBack(self):
		parent = self.parent
		parent.remove(self)
		parent.add(self, 0)

	def on_mouse_motion(self, x, y, dx, dy):
		if self.is_highlighted_card(x, y):
			self.ToFront()
			self.add(self._border_red_)
			self.highlight = True
		else:
			if self.highlight:
				self.ToBack()
				self.remove(self._border_red_)
				self.highlight = False

if __name__ == '__main__':
	#screen = pyglet.window.get_platform().get_default_display().get_default_screen()
	#director.init(screen.width, screen.height)
	game = morphz.Morphz('default', lambda x: x)
	director.init(1024, 700)
	director.run(cocos.scene.Scene(Background(), CardDisplay()))


#class HelloWorld(cocos.layer.ColorLayer):
#	def __init__(self):
#		super(HelloWorld, self).__init__(64, 64, 224, 255)
#
#		label = cocos.text.Label('Hello, World',
#								font_name='Times New Roman',
#								font_size=32,
#								anchor_x='center', anchor_y='center')
#
#		label.position = 320, 240
#		self.add(label)
#
#		sprite = cocos.sprite.Sprite('Ace.png')
#		sprite.position = 320, 240
#		sprite.scale = 3
#
#		self.add(sprite, 1)
#
#		scale = ScaleBy(3, duration=2)
#		label.do(Repeat(scale + Reverse(scale)))
#		sprite.do(Repeat(Reverse(scale) + scale))
#
#class KeyDisplay(cocos.layer.Layer):
#	# Required for layer to receive director.window events
#	is_event_handler = True
#
#	def __init__(self):
#		super(KeyDisplay, self).__init__()
#
#		self.text = cocos.text.Label(x=100, y=280)
#
#		self.keys_pressed = set()
#		self.update_text()
#		self.add(self.text)
#
#	def update_text(self):
#		key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
#		text = 'Keys:' + ','.join(key_names)
#
#		self.text.element.text = text
#
#	def on_key_press(self, key, modifiers):
#		self.keys_pressed.add(key)
#		self.update_text()
#
#	def on_key_release(self, key, modifiers):
#		self.keys_pressed.remove(key)
#		self.update_text()
#
#class MouseDisplay(cocos.layer.Layer):
#	is_event_handler = True
#
#	def __init__(self):
#		super(MouseDisplay, self).__init__()
#
#		self.drag = False
#		self.posx = 200
#		self.posy = 240
#		self.text = cocos.text.Label('No Mouse Events Yet',
#									x = self.posx,
#									y = self.posy,
#		                            anchor_x = 'center',
#		                            anchor_y = 'center',
#									font_size = 18)
#
#		self.add(self.text)
#
#	def update_text(self, x, y):
#		vx, vy = director.get_virtual_coordinates(x, y)
#		text = 'Mouse @ %d:%d' % (vx, vy)
#		self.text.element.text = text
#
#		w, h = director.get_window_size()
#		if vx > w:
#			self.posx = vx - w
#		elif vx < 0:
#			self.posx = w + vx
#
#		if vy > h:
#			self.posy = vy - h
#		elif vy < 0:
#			self.posy = h + vy
#
#		self.text.element.x = self.posx
#		self.text.element.y = self.posy
#
#	def on_mouse_motion(self, x, y, dx, dy):
#		self.update_text(x, y)
#
#	def on_mouse_press(self, x, y, buttons, modifiers):
#		self.posx, self.posy = director.get_virtual_coordinates(x, y)
#		self.update_text(x, y)
#
#		cursor = director.window.get_system_mouse_cursor(director.window.CURSOR_SIZE)
#		director.window.set_mouse_cursor(cursor)
#
#	def on_mouse_release(self, x, y, button, modifiers):
#		cursor = director.window.get_system_mouse_cursor(director.window.CURSOR_DEFAULT)
#		director.window.set_mouse_cursor(cursor)
#
#	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
#		self.posx, self.posy = director.get_virtual_coordinates(x, y)
#		self.update_text(x, y)
#
#
#if __name__ == '__main__':
#	director.init(resizable=True)
#	director.run(cocos.scene.Scene(KeyDisplay(), MouseDisplay()))