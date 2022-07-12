import pygame;
import time;
import copy

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
        
        pygame.init()
        
        colors = self.defineColors()
        background = colors['white']
        screen = self.initalizeScreen(width, height, background)
        snakeLength = width / 20
        header = pygame.display.set_caption('Snake')
        fruit = Fruit(screen, 500, 500, colors['red'], snakeLength / 2)
        x = 0
        y = 0
        rect = Rectangle(screen, x, y, colors['blue'], snakeLength-1, snakeLength-1)
        snake  = Snake(rect)
        y1_change = 0
        x1_change = 0
        game_over = False
        clock = pygame.time.Clock()
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -snakeLength
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = snakeLength
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -snakeLength
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = snakeLength
                        x1_change = 0
            pygame.display.update()
            screen.fill(colors['white'])
            snake.collision(fruit.x, fruit.y)
            snake.move(x1_change, y1_change)
            snake.draw()
            fruit.draw()
            clock.tick(7)
            test = 0
        
        pygame.quit()
        quit()
        
    def initalizeScreen(self,width , height, background):
        size = width, height
        screen = pygame.display.set_mode(size)
        screen.fill(background)
        
        return screen
    
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
