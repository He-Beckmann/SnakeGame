import pygame;
import time;
import copy
from threading import Thread

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
        height = width
        x = 0
        y = 0
        pygame.init()
        eventHandler = Thread(target=self.handleEvents)
        eventHandler.setDaemon(True)
        eventHandler.start()
        colors = self.defineColors()
        background = colors['white']
        screen = self.initalizeScreen(width, height, background)
        self.snakeLength = width / 20
        # Initalize Snake Object
        rect = Rectangle(screen, x, y, colors['blue'], self.snakeLength-1, self.snakeLength-1)
        self.snake  = Snake(rect)
        header = pygame.display.set_caption('Snake')
        fruit = Fruit(screen, 500, 500, colors['red'], self.snakeLength / 2)
        
        self.y1_change = 0
        self.x1_change = 0
        game_over = False
        clock = pygame.time.Clock()
        pause = False
        while not game_over:
            pygame.display.update()            
            screen.fill(colors['white'])
            
            self.snake.collision(fruit.x, fruit.y)
            self.snake.move(self.x1_change, self.y1_change)
            self.snake.draw()
            fruit.draw()
            clock.tick(7)

        pygame.quit()
        quit()
        
    def initalizeScreen(self,width , height, background):
        size = width, height
        screen = pygame.display.set_mode(size)
        screen.fill(background)
        
        return screen
    
    def handleEvents(self):
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.x1_change = -self.snakeLength
                            self.y1_change = 0
                        elif event.key == pygame.K_RIGHT:
                            self.x1_change = self.snakeLength
                            self.y1_change = 0
                        elif event.key == pygame.K_UP:
                            self.y1_change = -self.snakeLength
                            self.x1_change = 0
                        elif event.key == pygame.K_DOWN:
                            self.y1_change = self.snakeLength
                            self.x1_change = 0
                        # elif event.key == pygame.K_SPACE:
                        #     self.pause = True
        
    
    def getFruitPos(self):
        x = random.randint(0, 9) * self.snakeLength
        y = random.randint(0, 9) * self.snakeLength
        for body in self.snake.bodies:
            if body.x == x and body.y == y:
                self.getFruitPos()
        return (x,y)
    
        
    
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
