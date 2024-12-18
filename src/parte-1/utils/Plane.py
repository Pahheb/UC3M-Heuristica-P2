"""
Class used for creating Plane instances for saving the data in a more precise and concise way.
"""

class Plane:
    VALID_MODELS = {"STD", "JMB"}  # Conjunto de modelos válidos

    def __init__(self, id: int, model: str, restriction: bool, t1_duties: int, t2_duties: int):
        """
        Initialize a Plane instance with the provided attributes.
        """
        self.id = id
        self.model = model
        self.restriction = restriction
        self.t1_duties = t1_duties
        self.t2_duties = t2_duties

    def __repr__(self):
        """
        String representation of the Plane object.
        """
        return (
            f"Plane(id={self.id}, model={self.model}, restr={self.restriction}, "
            f"t1_duties={self.t1_duties}, t2_duties={self.t2_duties})"
        )

    def __hash__(self):
        return hash(self.id)
    
        # Métodos de comparación
    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("The id of the plane must be a positive integer.")
        self._id = id

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if not isinstance(model, str) or model not in self.VALID_MODELS:
            raise ValueError(f"Model must be one of {self.VALID_MODELS}.")
        self._model = model

    @property
    def restriction(self):
        return self._restriction

    @restriction.setter
    def restriction(self, restriction):
        if not isinstance(restriction, bool):
            raise TypeError("Restriction must be a boolean value.")
        self._restriction = restriction

    @property
    def t1_duties(self):
        return self._t1_duties

    @t1_duties.setter
    def t1_duties(self, t1_duties):
        if not isinstance(t1_duties, int) or t1_duties < 0:
            raise ValueError("T1_duties must be a non-negative integer.")
        self._t1_duties = t1_duties

    @property
    def t2_duties(self):
        return self._t2_duties

    @t2_duties.setter
    def t2_duties(self, t2_duties):
        if not isinstance(t2_duties, int) or t2_duties < 0:
            raise ValueError("T2_duties must be a non-negative integer.")
        self._t2_duties = t2_duties
