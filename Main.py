
import sys, pygame
import snake, food, Button





class SnakeGame:
    # setup surface game
    CELL_SIZE = 32
    CELL_NUMBER = 20
    GAME_WITH = CELL_SIZE * CELL_NUMBER
    GAME_HEIGHT = CELL_SIZE * CELL_NUMBER

    # setup navbar game
    NAV_WITH = CELL_SIZE*CELL_NUMBER
    NAV_HEIGHT = 30

    # setup all display
    WITH = GAME_WITH
    HEIGHT = GAME_HEIGHT + NAV_HEIGHT
    FPS = 60

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = (self.WITH, self.HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.startImage = pygame.image.load('./images/start.png').convert_alpha()
        xCenter = self.GAME_WITH/2
        yCenter = self.GAME_HEIGHT/2
        
        self.startBtn = Button.Button( xCenter, yCenter, self.startImage,0.5)
        self.nav_surface = pygame.Surface((self.NAV_WITH, self.NAV_HEIGHT))
        self.game_surface = pygame.Surface((self.GAME_WITH, self.GAME_HEIGHT))

        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

        self.CONFIG_GAME = {
            'display': self.game_surface,
            'cell_size': self.CELL_SIZE,
            'cell_number': self.CELL_NUMBER
        }
        self.snake1 = snake.Snake(self.CONFIG_GAME, 1)
        self.food = food.Food(self.CONFIG_GAME, 1)


    def Menu(self):
        self.screen = pygame.display.set_mode(self.size)
        self.startImage = pygame.image.load('./images/start.png').convert_alpha()
        xCenter = self.GAME_WITH/2
        yCenter = self.GAME_HEIGHT/2
        startBtn = Button.Button( xCenter, yCenter, self.startImage,0.5)
        while True:
            self.screen.fill((175,215,70))
            self.clock.tick(self.FPS)

            if startBtn.draw(self.screen):
                self.run()
                #break
                # # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()

    def run(self):

        # main game loop
    
        while True:
            # so lan lap trong 1 giay
            self.clock.tick(self.FPS)
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.SCREEN_UPDATE:
                    self.update()



                if event.type == pygame.KEYDOWN:
                    self.handle(event)

            # re-draw elements
            if(self.game_over()):
                break
            self.draw()
            
    def draw(self):
        self.draw_navgame()
        self.draw_game()

        pygame.display.update()
    def draw_navgame(self):
        self.nav_surface.fill((175,0,70))
        _score = self.snake1.score
        scoreImage = pygame.image.load('images/food_1.png'.format(1)).convert_alpha()
        width = scoreImage.get_width()
        height = scoreImage.get_height()
        scoreImage = pygame.transform.scale(scoreImage,(int(width * 0.8), int(height * 0.8)))
        font = pygame.font.SysFont(None, 24)
        scoreSurface = font.render(str(_score), True, (0,0,0))
        score_rect = scoreSurface.get_rect(center = (30,15))
        scoreImage_rect = scoreImage.get_rect(midright = (score_rect.left, score_rect.centery))
        self.nav_surface.blit(scoreImage,scoreImage_rect)
        self.nav_surface.blit(scoreSurface,score_rect)
        self.screen.blit(self.nav_surface, (0, 0))

    def draw_game(self):
        self.game_surface.fill((175,215,70))

        self.food.draw()
        self.snake1.draw()

        self.screen.blit(self.game_surface, (0, self.NAV_HEIGHT))

    def update(self):
        self.snake1.move_snake(self.food)
    def handle(self, event):
        #self.my_mario.handle(event)
        self.snake1.handle(event)
        
    def game_over(self):
        return self.snake1.check_fail()
        



g = SnakeGame()
g.Menu()

