import math

def length(point1_xcoor, point1_ycoor, point2_xcoor, point2_ycoor):
    return math.sqrt((point1_xcoor - point2_xcoor)**2 + (point1_ycoor - point2_ycoor)**2)