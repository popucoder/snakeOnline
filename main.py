
import sys, pygame
import Snake, Food, Button

class SnakeGame:
    # setup game
    CELL_SIZE = 40
    CELL_NUMBER = 16
    GAME_WITH = CELL_SIZE * CELL_NUMBER
    GAME_HEIGHT = CELL_SIZE * CELL_NUMBER 

    # setup navbar game
    NAV_WITH = GAME_WITH
    NAV_HEIGHT = 35

    # setup all display
    WITH = GAME_WITH
    HEIGHT = GAME_HEIGHT + NAV_HEIGHT
    FPS = 60

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = (self.WITH, self.HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont(None, 35)
        self.gameOver = False

        self.startImage = pygame.image.load('./images/start.png').convert_alpha()
        self.overImage = pygame.image.load('./images/gameOver.png').convert_alpha()
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
        self.snake1 = Snake.Snake(self.CONFIG_GAME, 1)
        self.food = Food.Food(self.CONFIG_GAME, 1)

        self.score_image = self.food.food_image
        self.isGameOver = False

        

    def menuGameOver(self):
        self.overImage = pygame.image.load('./images/gameOver.png').convert_alpha()
        xCenter = self.GAME_WITH/2
        yCenter = int(self.GAME_HEIGHT/2)
        score_max = self.font.render("SCORE MAX: " + str(self.score_max), True, (0,0,0))
        your_score = self.font.render("YOUR SCORE: " + str(self.your_score), True, (0,0,0))

        x_pos = int(self.GAME_WITH/2 - score_max.get_width()/2)
    
        overBtn = Button.Button( xCenter, yCenter, self.overImage, 0.5)
        isOut = False
        while not isOut:
            self.screen.fill((175,215,70))
            self.clock.tick(self.FPS)

            self.screen.blit(score_max, (x_pos, yCenter + 100))
            self.screen.blit(your_score, (x_pos, yCenter + 130))
            if overBtn.draw(self.screen):
                isOut = True
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

    def menu(self):

        self.startImage = pygame.image.load('./images/start.png').convert_alpha()
        xCenter = self.GAME_WITH/2
        yCenter = self.GAME_HEIGHT/2

        startBtn = Button.Button( xCenter, yCenter, self.startImage, 0.5)
        

        while True:
            self.screen.fill((175,215,70))
            self.clock.tick(self.FPS)

            if startBtn.draw(self.screen):
                self.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

    def run(self):

        f = open('score_max.txt', 'r')
        self.score_max = int(f.read())
        f.close()

        # main game loop
        self.isGameOver = False;
        while not self.isGameOver:
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
                self.isGameOver = True
                self.menuGameOver()
            else:
                self.draw()
            
    def draw(self):
        self.draw_navgame()
        self.draw_game()
        pygame.display.update()


    def draw_navgame(self):
        self.nav_surface.fill((175,0,70))

        self.draw_score()

        self.screen.blit(self.nav_surface, (0, 0))


    def draw_score(self):


        score_max = self.font.render("SCORE MAX: " + str(self.score_max), True, (0,0,0))
        score_surface = self.font.render(str(self.snake1.score), True, (0,0,0))

        x_pos = int(self.NAV_WITH/2 - score_max.get_width()/2)
        y_pos = int(self.NAV_HEIGHT/2 - score_surface.get_height()/2)

        score_rect = score_surface.get_rect(topleft = (50, y_pos))
        score_image_rect = self.score_image.get_rect(midright = (score_rect.left, score_rect.centery))


        self.nav_surface.blit(score_max, (x_pos, y_pos))
        self.nav_surface.blit(self.score_image, score_image_rect)
        self.nav_surface.blit(score_surface, score_rect)




    def draw_game(self):
        self.game_surface.fill((175,215,70))

        self.food.draw()
        self.snake1.draw()

        self.screen.blit(self.game_surface, (0, self.NAV_HEIGHT))

    def update(self):
        self.snake1.move_snake(self.food)

    def handle(self, event):
        self.snake1.handle(event)
        
    def game_over(self):
        self.your_score = self.snake1.score
        isFail = self.snake1.check_fail()
        if(isFail):
            f = open('score_max.txt', 'r')
            self.score_max = int(f.read())
    
            if(self.your_score > self.score_max):
                self.score_max = self.your_score
                f = open('score_max.txt', 'w')
                f.write(str(self.your_score))
            f.close()
        return isFail
        


g = SnakeGame()
g.menu()


