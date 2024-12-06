class STD_Mechanic():
    def __init__(self, i: int, j: int):
        self.x = i
        self.y = j
        
    def __repr__(self):
        return f"STD_Mechanic(x={self.x}, y={self.y})"
        
    @property
    def i(self):
        return self._i
    
    @i.setter
    def i(self, i):
        if type(i) != int:
            raise TypeError("i position must be an integer")
        
    @property
    def j(self):
        return self._j
    
    @j.setter
    def j(self, j):
        if type(j) != int:
            raise TypeError("j position must be an integer")