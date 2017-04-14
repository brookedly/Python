import controller, sys
import model   #strange, but we need a reference to this module to pass this module to update

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special

# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
cycles = 0
clicked = None
rounds = set()
working = False 
stopp = False

#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global cycles, rounds, working, stopp
    working = False
    cycles = 0 
    rounds = set()
    stopp = False

#start running the simulation
def start ():
    global working
    working = True

#stop running the simulation (freezing it)
def stop ():
    global working
    working = False

#step just one update in the simulation
def step ():
    global working, stopp
    working = True
    stopp = True

#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global clicked 
    clicked = kind
    print(kind+' is selected')

#add the kind of remembered object to the simulation (or remove any objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    coord = (x,y)
    if clicked == 'Remove':
        print(clicked)
        for rs in rounds:
            if rs.contains(coord):
                remove(rs)                          
    else:
        #print(clicked)
        if clicked == 'None':
            pass
        elif clicked == None:
            pass
        else:
            rounds.add(eval(clicked+'(x,y)'))
#         elif clicked == 'Ball':
#             rounds.add(Ball(x, y))
#         elif clicked == 'Floater':
#             rounds.add(Floater(x,y))
#         elif clicked == 'Black_Hole':
#             rounds.add(Black_Hole(x,y))

#add simulton s to the simulation
def add(s):
    global rounds
    rounds.add(s)

# remove simulton s from the simulation    
def remove(s):
    global rounds
    rounds.remove(s)

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    s = set()
    for x in rounds:
        if p(x):
            s.add(x)
    return s

#call update for every simulton in the simulation
def update_all():
    global cycles, working, world
    if working:
        cycles += 1       
        for s in rounds.copy(): #using rounds itself would just create a problem in the set 
            s.update(model) 

#delete from the canvas every simulton in the simulation, and then call display for every
#  simulton in the simulation to add it back to the canvas possibly in a new location: to
#  animate it; also, update the progress label defined in the controller
def display_all():
    for x in controller.the_canvas.find_all():
        controller.the_canvas.delete(x)
    for y in rounds:
        y.display(controller.the_canvas)
    controller.the_progress.config(text = str(cycles) + ' cycles/' + str(len(rounds)) + ' simultons')
        
