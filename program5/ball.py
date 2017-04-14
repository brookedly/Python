# A Ball is Prey; it updates by moving in a straight
#   line and displays as blue circle with a radius
#   of 5 (width/height 10).


from prey import Prey


class Ball(Prey):
    def __init__(self, x, y):
        self.color = 'blue'
        self.radius = 5
        self.speed = 5 
        Prey.__init__(self, x, y, self.radius*2, self.radius*2,0, self.speed)
        self.randomize_angle()
        
    def update(self, m):
        self.move()
    
    def display(self, canvas):
        canvas.create_oval(self._x-self.radius, self._y-self.radius, self._x+self.radius, 
                           self._y+self.radius,
                           fill = self.color)