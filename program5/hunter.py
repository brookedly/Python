# A Hunter is both a Mobile_Simulton and a Pulsator: it updates
#   like a Pulsator, but it also moves (either in a straight line
#   or in pursuit of Prey), and displays as a Pulsator.
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from prey import Prey
from math import atan2

class Hunter(Pulsator,Mobile_Simulton):
    def __init__(self, x, y):
        self.goodbye = 200
        Pulsator.__init__(self, x, y)
        width, height = self.get_dimension()
        self.angle = 0 
        self.speed = 5
        Mobile_Simulton.__init__(self, x, y, width, height, self.angle, self.speed)
        self.randomize_angle()
 
    def peace(self, x):
        return self.distance(x) <= self.goodbye
     
    def location(self):
        return self.get_location()
     
    def angl(self,x, y):
        return atan2(y - self._y, x - self._x)
 
    def update(self, m):
        goner = Pulsator.update(self,m)
        major = lambda x: self.distance(x)
        peaceout  = m.find(lambda x : isinstance(x,Prey) and self.peace(x.get_location())) 
        if peaceout:
            x,y = min([y.get_location() for y in peaceout], key = major)
            #x,y = p
            self.set_angle(self.angl(x,y))
        #Hunter is instructed to move 
        self.move()   
        return goner
