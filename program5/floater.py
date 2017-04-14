# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage
#from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random, uniform
from tkinter import PhotoImage

class Floater(Prey):
    def __init__(self, x, y):
        self.gif = PhotoImage(file = 'ufo.gif')
        self.angle = 0
        self.speed = 5
        Prey.__init__(self, x, y, self.gif.width(), self.gif.height(),self.angle, self.speed)
        self.randomize_angle()
    
    def goodspeed(self):
        if 3 <= self.speed <= 7:
            return True
        else:
            return False 
    
    def update(self, m):
        if random() <= 0.3:
            self.speed = self.speed + uniform(-0.5, 0.5)
            self.angle = self.angle + uniform(-0.5, 0.5)
            if not Floater.goodspeed(self):
                self.angle = self.angle + uniform(-0.5, 0.5)
        self.move()
        
    def display(self, canvas):
        canvas.create_image(*self.get_location(), image = self.gif)