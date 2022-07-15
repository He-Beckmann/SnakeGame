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