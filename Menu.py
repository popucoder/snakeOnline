import sys, pygame, Button
class Menu():
	def __init__(self, screen):
		self.startImage = pygame.image.load('./images/start.png').convert_alpha()
		self.startBtn = Button.Button(100, 200, self.startImage,0.5)
		self.startBtn.draw(screen)