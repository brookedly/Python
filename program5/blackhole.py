# A Black_Hole is a Simulton; it updates by removing
#   any Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter
from simulton import Simulton
from prey import Prey         

class Black_Hole(Simulton):
    def __init__(self, x,y):
        self.radius = 10
        self.color = 'black'
        Simulton.__init__(self, x, y, self.radius*2, self.radius*2)
        
    def update(self, m):
        def spot(x):
            return self.contains(x.get_location())
        goner = m.find(lambda y: isinstance(y, Prey) and spot(y))
        for sucker in goner:
            m.remove(sucker)
        return goner
 
    def dim(self):
        return self.get_dimension()[0]/2
 
    def contains(self, i):
        return self.distance(i) <= self.dim()

    def display(self, canvas):
        width, height = self.get_dimension()
        canvas.create_oval(self._x-width/2,self._y-height/2,self._x+width/2,self._y+height/2, fill = self.color)
