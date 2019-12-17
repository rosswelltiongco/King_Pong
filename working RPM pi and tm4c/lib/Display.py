class Display:
    def __init__(self):
        self.cup_0 = "[0]"
        self.cup_1 = "[1]"
        self.cup_2 = "[2]"
        self.cup_3 = "[3]"
        self.cup_4 = "[4]"
        self.cup_5 = "[5]"
        self.cup_6 = "[6]"
        self.cup_7 = "[7]"
        self.cup_8 = "[8]"
        self.cup_9 = "[9]"
        
        self.display_cups()
        

    def remove_cup(self,remove_cup):
            # todo: implement check to make sure cup isnt already gone
            if remove_cup == 0:
                self.cup_0 = "   "
            elif remove_cup == 1:
                self.cup_1 = "   "
            elif remove_cup == 2:
                self.cup_2 = "   "
            elif remove_cup == 3:
                self.cup_3 = "   "
            elif remove_cup == 4:
                self.cup_4 = "   "
            elif remove_cup == 5:
                self.cup_5 = "   "
            elif remove_cup == 6:
                self.cup_6 = "   "    
            elif remove_cup == 7:
                self.cup_7 = "   "                 
            elif remove_cup == 8:
                self.cup_8 = "   "
            elif remove_cup == 9:
                self.cup_9 = "   " 
            else:
                pass
                
                
    def display_cups(self):
        cups =  """

    ------ KING PONG ------
    _______________________
    |                     |
    |   {3} {2} {1} {0}   |
    |     {6} {5} {4}     |
    |       {8} {7}       |
    |         {9}         |
    |_____________________|
        """.format(self.cup_0,self.cup_1,self.cup_2,self.cup_3,self.cup_4,self.cup_5,self.cup_6,self.cup_7,self.cup_8,self.cup_9)
        
        print(cups)
