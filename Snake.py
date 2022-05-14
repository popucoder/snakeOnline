
import pygame
from pygame.math import Vector2



class Snake():

    FRAME_WIDTH = 40
    FRAME_HEIGHT = 40
    PADDING = 0


    def __init__(self, config_game, skinId):
        self.screen = config_game['display']
        self.CELL_SIZE = config_game['cell_size']
        self.CELL_NUMBER = config_game['cell_number']

        self.skinId = skinId
        self.new_block = False
        self.score = 0
        self.init_graphics()
        self.reset()

    
        
    def init_graphics(self):
        self.sprite_imgs = pygame.image.load('images/snake_{}.png'.format(self.skinId))
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

        self.head_up = self.set_sprite([0,0])
        self.head_down = self.set_sprite([1,0])
        self.head_right = self.set_sprite([2,0])
        self.head_left = self.set_sprite([3,0])

        self.body_vertical = self.set_sprite([4,0])
        self.body_horizontal = self.set_sprite([5,0])

        self.tail_up = self.set_sprite([0,1])
        self.tail_down = self.set_sprite([1,1])
        self.tail_right = self.set_sprite([2,1])
        self.tail_left = self.set_sprite([3,1])

        self.body_tr = self.set_sprite([0,2])
        self.body_tl = self.set_sprite([1,2])
        self.body_br = self.set_sprite([2,2])
        self.body_bl = self.set_sprite([3,2])

    def draw(self):
        self.update()   

        for index,block in enumerate(self.body):
            x_pos = int(block.x * self.CELL_SIZE)
            y_pos = int(block.y * self.CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, self.CELL_SIZE, self.CELL_SIZE)

            if index == 0:
                self.screen.blit(self.head, block_rect)

            elif index == len(self.body) - 1:
                self.screen.blit(self.tail, block_rect)

            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    self.screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        self.screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        self.screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        self.screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        self.screen.blit(self.body_br,block_rect)

    def update(self):
        self.update_head_graphics()
        self.update_tail_graphics()

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self, food):
        if self.direction == Vector2(0,0): 
            return
            
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

        self.check_collision(food)

    def add_block(self):
        self.score += 1
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.score = 0

    def handle(self, event):
        if event.key == pygame.K_UP:
            if self.direction.y != 1:
                self.direction = Vector2(0,-1)
        if event.key == pygame.K_RIGHT:
            if self.direction.x != -1:
                self.direction = Vector2(1,0)
        if event.key == pygame.K_DOWN:
            if self.direction.y != -1:
                self.direction = Vector2(0,1)
        if event.key == pygame.K_LEFT:
            if self.direction.x != 1:
                self.direction = Vector2(-1,0)

    def check_collision(self, food):
            if food.pos == self.body[0]:
                food.randomize()
                self.add_block()
                self.play_crunch_sound()

            for block in self.body[1:]:
                if block == food.pos:
                    food.randomize()

    def check_fail(self):
        isFail = False

        if not 0 <= self.body[0].x < self.CELL_NUMBER or not 0 <= self.body[0].y < self.CELL_NUMBER:
            isFail = True 

        for block in self.body[1:]:
            if block == self.body[0]:
                isFail = True 
        
        if(isFail):
            f = open('score_max.txt', 'r')
            score_max = int(f.read())
    
            if(self.score > score_max):
                f = open('score_max.txt', 'w')
                f.write(str(self.score))
            f.close()

            self.reset()

        return isFail    
    

    def set_sprite(self, index):
        x = (self.FRAME_WIDTH + self.PADDING) * index[0]
        y = (self.FRAME_HEIGHT + self.PADDING) * index[1]

        rect = pygame.Rect(x, y, self.FRAME_WIDTH, self.FRAME_HEIGHT)
        #pygame.SRCALPHA giup pygame chay nhanh hon tuong ung voi covert_aplpha()
        _surface = pygame.Surface((self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.SRCALPHA)
        _surface.blit(self.sprite_imgs, (0,0), rect)
        return _surface