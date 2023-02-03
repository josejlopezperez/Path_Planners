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
    
def OnSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
  
def Orientation(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):return 1
    elif (val < 0):return 2
    else:return 0
  
def DoIntersect(p1,q1,p2,q2):
    o1 = Orientation(p1, q1, p2)
    o2 = Orientation(p1, q1, q2)
    o3 = Orientation(p2, q2, p1)
    o4 = Orientation(p2, q2, q1)
    if ((o1 != o2) and (o3 != o4)):
        return True
    if ((o1 == 0) and OnSegment(p1, p2, q1)):
        return True
    if ((o2 == 0) and OnSegment(p1, q2, q1)):
        return True
    if ((o3 == 0) and OnSegment(p2, p1, q2)):
        return True
    if ((o4 == 0) and OnSegment(p2, q1, q2)):
        return True
    return False