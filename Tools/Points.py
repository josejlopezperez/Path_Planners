class Point3D():
    def __init__(self, *args):
        self.x = 0
        self.y = 0
        self.z = 0
        if len(args) == 1:
            self.x, self.y, self.z = args[0]
        elif len(args) == 2:
            self.x, self.y = args[0], args[1]
            
    def Distance(self, point):
        distance = ((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2) ** (1/2)
        return distance