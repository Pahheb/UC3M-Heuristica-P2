"""
Class used for creating Plane instances for saving the data in a more precise and concise way
"""

class Plane():
    def __init__(self, id: int, type: str, restriction: bool, t1_duties: int, t2_duties: int, i: int, j: int):
        self.id = id
        self.type = type
        self.restriction = restriction
        self.t1_duties = t1_duties
        self.t2_duties = t2_duties
        self.position = {"x": i, "y": j}
        
    def __str__(self) -> str:
        output = f"{self.id}-{self.type}-{self.restriction} --- Current T1 Duties: {self.t1_duties}. Current T2 Duties: {self.t2_duties}\n"
        return output
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if id <= 0:
            raise ValueError("The id of the plane must be 1 or bigger")
        if type(id) != int:
            raise TypeError("The id must be an integer")
        
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type):
        if type != "STD" or type != "JMP":
            raise ValueError("Type must be either STD or JMP")
        if type(type) != "str":
            raise TypeError("The type must be a string")
      
    @property  
    def restriction(self):
        return self._restriction
    
    @restriction.setter
    def restriction(self, restriction):
        if type(restriction) != bool:
            raise TypeError("Restriction must be a boolean value")
        
    @property
    def t1_duties(self):
        return self._t1_duties
    
    @t1_duties.setter
    def t1_duties(self, t1_duties):
        if 0 > t1_duties:
            raise ValueError("T1_duties must be at least 0 or a positive integer")
        if type(t1_duties) != int:
            raise TypeError("T1_duties must be an integer")

    @property
    def t2_duties(self):
        return self._t2_duties
    
    @t2_duties.setter
    def t2_duties(self, t2_duties):
        if 0 > t2_duties:
            raise ValueError("T2_duties must be at least 0 or a positive integer")
        if type(t2_duties) != int:
            raise TypeError("T2_duties must be an integer")
        
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