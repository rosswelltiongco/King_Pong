from lib.Base import *

def main():
    
    positions = [20,150,260,360]
    
    base = Base(0)
    """
    base.step_left(5)
    base.step_left(15)
    
    base.step_right(20)
    
    base.step_left(100)
    
    base.step_right(25)
    
    base.step_left(10)
    
    base.step_right(100)
    """
    
    
    while 1:
        """
        # To find and calibrate
        position = int(input("Enter a position: "))
        base.go_to(position)
        """
        
        selected_cup = int(input("Enter cup")) - 1
        pos = positions[selected_cup]
        base.go_to(pos)
        
main()