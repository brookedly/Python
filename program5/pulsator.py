# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions
from blackhole import Black_Hole

class Pulsator(Black_Hole):
    
    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self.radius = 10
        self.color = 'black' 
        self.cycles = 0 
        self.counter = 30
        
#     def dim(self):
#         return self.get_dimension()[0]/2
#  
#     def contains(self, i):
#         return self.distance(i) <= self.dim()

    def dim(self):
        return self.get_dimension()[0]
    
    def update(self, m): 
        self.cycles = self.cycles +1
        goner = Black_Hole.update(self, m)
        if goner:
            self.cycles = 0
            x = len(goner)
            self.change_dimension(x, x)
        elif self.cycles == self.counter:
            #if the cycle counter reaches 30 then decrease the dimension
            #of the pulsator by -1
            y = -1
            self.change_dimension(y, y)
            #if the dimensions of the pulsator becomes 0, you must remove it
            if self.dim() == 0: 
                m.remove(self)
            #reset the cycle counter once the object is removed 
            self.cycles = 0
        return goner
    #writing the display and contains functions aren't necessary because the 
    #Black_Hole class is being inherited
    
#     def display(self, canvas):
#         width, height = self.get_dimension()
#         canvas.create_oval(self._x-width/2,self._y-height/2,self._x+width/2,self._y+height/2, fill = self.color)
        