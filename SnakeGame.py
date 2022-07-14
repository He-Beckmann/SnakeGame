import pygame;
import time;
import copy
import random

class Snake:
    
    def __init__(self, rectangle):
        self.bodies = []
        self.bodies.append(rectangle)
        self.length = 1
        
    def grow(self):
        self.length += 1
        
    def draw(self):
        for body in self.bodies:
            body.draw() 
    
    def move(self, x, y):
        body = self.bodies[len(self.bodies)-1].__copy__()
        body.move(x, y)
        self.bodies.append(body)
        if(len(self.bodies) > self.length):
            self.bodies.pop(0)
            
    def collision(self, x, y):
        if(self.bodies[-1].collision(x, y)):
            self.grow()
            return True
        return False
            
    def selfCollision(self):
        headX = self.bodies[-1].x
        headY = self.bodies[-1].y
        
        for index, body in enumerate(self.bodies):
            if body.collision(headX, headY) == True and index != len(self.bodies) - 1:
                return True
        return False
        

class Figur:
    
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.x      = x
        self.y      = y
        self.color  = color
        
    def draw(self):
        pass
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    def move(self, x, y):
        self.x += x
        self.y += y
    
class Fruit(Figur):
    
    def __init__(self, screen, x, y, color, radius):
        super().__init__(screen, x, y, color)
        self.radius = radius
        
    def draw(self):
        pygame.draw.circle(self.screen,self.color,[self.x,self.y], self.radius)
        
class Rectangle(Figur):
    
    def __init__(self, screen, x, y, color, width, height):
        super().__init__(screen, x, y, color)
        self.width  = width
        self.height = height
        
    def __copy__(self):
        return type(self)(self.screen, self.x, self.y, self.color, self.width, self.height)
        
    def draw(self):
        pygame.draw.rect(self.screen,self.color,(self.x,self.y , self.width, self.height))
        
    def collision(self, x, y):
        return (self.x <= x and self.x + self.width >= x and self.y <= y and self.y + self.height >= y)
        

class SnakeGame:
    
    def __init__(self, width):
        self.score = 0
        height = width
        startX = width / 2
        startY = height / 2
        pygame.init()
        self.colors = self.defineColors()
        background = self.colors['white']
        self.screen = self.initalizeScreen(width, height, background)
        self.snakeLength = width / 20
        # Initalize Snake Object
        rect = Rectangle(self.screen, startX, startY, self.colors['blue'], self.snakeLength-1, self.snakeLength-1)
        self.snake  = Snake(rect)
        header = pygame.display.set_caption('Snake')
        self.fruit = Fruit(self.screen, 500, 500, self.colors['red'], self.snakeLength / 2)
        
        self.y1_change = 0
        self.x1_change = 0
        self.mainMenu()
        self.gameLoop()
        
        self.gameOver(self.colors)
        pygame.quit()
        quit()
        
    def gameLoop(self):
        game_over = False
        pause = False
        prevDirection = ''
        direction = ''
        clock = pygame.time.Clock()
        while not game_over:
            pygame.display.update()            
            self.screen.fill(self.colors['white'])
            print(prevDirection)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and prevDirection != 'right':
                        self.x1_change = -self.snakeLength
                        self.y1_change = 0
                        direction = 'left'
                    elif event.key == pygame.K_RIGHT and prevDirection != 'left':
                        self.x1_change = self.snakeLength
                        self.y1_change = 0
                        direction = 'right'
                    elif event.key == pygame.K_UP and prevDirection != 'down':
                        self.y1_change = -self.snakeLength
                        self.x1_change = 0
                        direction = 'up'
                    elif event.key == pygame.K_DOWN and prevDirection != 'up':
                        self.y1_change = self.snakeLength
                        self.x1_change = 0
                        direction = 'down'
                    # elif event.key == pygame.K_SPACE:
                    #     self.pause = True
            if self.snake.collision(self.fruit.x, self.fruit.y):
                pos = self.nextFruitPos()
                self.fruit.setPosition(pos[0], pos[1])
                self.score += 100
            self.snake.move(self.x1_change, self.y1_change)
            if self.score > 0:
                self.score -= 1
            prevDirection = direction
            if self.snake.selfCollision():
                game_over = True
            self.snake.draw()
            self.fruit.draw()
            self.updateScore()
            clock.tick(7)
        
    def initalizeScreen(self,width , height, background):
        size = width, height
        screen = pygame.display.set_mode(size)
        screen.fill(background)
        
        return screen
    
    def updateScore(self):
        my_font = pygame.font.Font('DAYPBL__.ttf', 30)
        text_surface = my_font.render(str(self.score), False, (0, 0, 0))
        self.screen.blit(text_surface, (700, 10))
    
    
    def mainMenu(self):
        self.screen.fill(self.colors['white'])
        my_font = pygame.font.Font('DAYPBL__.ttf', 40)
        start_text = my_font.render('START', False,self.colors['white'])
        quit_text = my_font.render('QUIT', False, (0, 0, 0))
        size = self.screen.get_size()
        startButton = Rectangle(self.screen, size[0] / 4, size[0] / 4, self.colors['black'], 200, 100)
        startButton.draw()
        self.screen.blit(start_text, (size[0] / 3, size[1]/3))
        self.screen.blit(quit_text, (size[0] / 3, size[1]/2))
        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    wait = False
    
    def gameOver(self, colors):
        self.screen.fill(colors['white'])
        my_font = pygame.font.Font('DAYPBL__.ttf', 60)
        text_surface = my_font.render('GAME OVER', False, (0, 0, 0))
        size = self.screen.get_size()
        self.screen.blit(text_surface, (size[0] / 4, size[1]/2.4))
        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    wait = False
                    
    
    def nextFruitPos(self):
        x = random.randint(0, 19) * self.snakeLength
        y = random.randint(0, 19) * self.snakeLength
        for body in self.snake.bodies:
            if body.x == x and body.y == y:
                self.nextFruitPos()
        return (x - self.snakeLength / 2 ,y - self.snakeLength / 2)
    
        
    
    def drawFruit(self, screen, color, radius):
        return pygame.draw.circle(screen,color,[500,500], 20)
    
    def defineColors(self):
        colors = {
            "red":    (255,0,0),
            "blue":   (0,0,255),
            "green":  (255,0,0),
            "white":  (255,255,255),
            "black":  (0,0,0)
        }
        return colors
    
SnakeGame(800)
