import sys, pygame
import snake, food



class SnakeGame:
    # setup surface game
    CELL_SIZE = 40
    CELL_NUMBER = 20
    GAME_WITH = CELL_SIZE * CELL_NUMBER
    GAME_HEIGHT = CELL_SIZE * CELL_NUMBER

    # setup navbar game
    NAV_WITH = CELL_SIZE*CELL_NUMBER
    NAV_HEIGHT = 10

    # setup all display
    WITH = GAME_WITH
    HEIGHT = GAME_HEIGHT + NAV_HEIGHT
    FPS = 60
   
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = (self.WITH, self.HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
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
        self.snake2 = snake.Snake(self.CONFIG_GAME, 2)
        self.food = food.Food(self.CONFIG_GAME, 1)
        

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
            self.draw()
            
            
    def draw(self):
        self.draw_navgame()
        self.draw_game()

        pygame.display.update()
       
    def draw_navgame(self):
        self.nav_surface.fill((175,0,70))

        self.screen.blit(self.nav_surface, (0, 0))

    def draw_game(self):
        self.game_surface.fill((175,215,70))

        self.food.draw()
        self.snake1.draw()
        self.snake2.draw()

        self.screen.blit(self.game_surface, (0, self.NAV_HEIGHT))

    def update(self):
        self.snake1.move_snake(self.food)
        self.snake2.move_snake(self.food)

       

    def handle(self, event):
        #self.my_mario.handle(event)
        self.snake1.handle(event)



    


g = SnakeGame()
g.run()