"""
This class contains the matrix information, parkings, STD and SPC mechanics and Planes
"""

class Map():
    def __init__(self, n:int, m:int):
        self.size_matrix = (n, m)
        self.parkings = []
        self.std_mechanics = []
        self.spc_mechanics = []
        self.planes = []
