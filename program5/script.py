import view
import controller

controller.repeater(view.root)
view.root.mainloop()


#RuntimeError: Set changed during iteration 
#Blackhole has problems
#issue might be in update_all