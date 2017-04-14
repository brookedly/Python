#This Speical class works just like the Ball class, but the only things
#that are different is (1) the radius is randomize in the range 5-15, 
#(2) randomize ball colors
from ball import Ball
import random 

class Special(Ball):
    colors = ['red','orange', 'yellow', 'green', 'purple', 'pink', 'tan', 'hot pink' ]
    def __init__(self,x,y):
        self._r= random.randint(5,15)
        Ball.__init__(self, x, y)
        self.count = 0
        self.color = random.choice(Special.colors)
        
    def update(self, m):
        self.move()
        
    def display(self, canvas):
        canvas.create_oval(self._x - self._r, self._y - self._r, 
                           self._x + self._r, self._y + self._r, fill = self.color)