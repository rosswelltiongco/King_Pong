class Base:
    def __init__(self, pos):
        self.pos = pos
        self.boundary_left = 400
        self.boundary_right = 0
    def move_right(self, delta):
        print("Moving right {}".format(delta))
        for step in range(delta):
            if self.pos <= self.boundary_right:
                break # pass or break
            else:
                self.pos -= 1
            print(self.pos)
    def move_left(self, delta):
        print("Moving left {}".format(delta))
        for step in range(delta):
            if self.pos >= self.boundary_left:
                break # pass or break
            else:
                self.pos += 1
            print(self.pos)
base = Base(0)
base.move_left(50)
base.move_right(100)
base.move_left(1000)
base.move_right(200)