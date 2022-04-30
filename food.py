import pygame, random
from pygame.math import Vector2

class Food:
    def __init__(self, config_game, skinId):
           # surface
        self.screen = config_game['display']
        self.CELL_SIZE = config_game['cell_size']
        self.CELL_NUMBER = config_game['cell_number']

        self.food = pygame.image.load('images/food_{}.png'.format(skinId)).convert_alpha()
        self.randomize()

    def draw(self):
        x_pos = int(self.pos.x * self.CELL_SIZE)
        y_pos = int(self.pos.y * self.CELL_SIZE)
        fruit_rect = pygame.Rect( x_pos, y_pos, self.CELL_SIZE, self.CELL_SIZE)
        self.screen.blit(self.food, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, self.CELL_NUMBER - 1)
        self.y = random.randint(0, self.CELL_NUMBER - 1)
        self.pos = Vector2( self.x, self.y)