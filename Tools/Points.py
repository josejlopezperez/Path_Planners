class Point3D():
    def __init__(self, *args):
        self.x = 0
        self.y = 0
        self.z = 0
        if len(args) == 1:
            if type(args[0]) == Point3D:
                self.x, self.y, self.z = args[0].x, args[0].y, args[0].z
            else:
                self.x, self.y, self.z = args[0]
        elif len(args) == 3:
            self.x, self.y, self.z = args[0], args[1], args[2]
    
    @property
    def ToVector(self):
        return [self.x, self.y, self.z]
            
    def Distance(self, point):
        distance = ((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2) ** (1/2)
        return distance