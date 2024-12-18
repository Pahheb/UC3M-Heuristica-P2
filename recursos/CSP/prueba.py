#!/usr/bin/env python

from constraint import Problem

# Clase de ejemplo
class Plane:
    def __init__(self, id, model):
        self.id = id
        self.model = model

    def __repr__(self):
        return f"Plane(id={self.id}, model={self.model})"
    
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

# Crear instancias de Plane
planes = [Plane(1, "STD"), Plane(2, "JMB"), Plane(3, "STD")]

# Crear el problema
problem = Problem()

# Añadir variables: cada avión será una variable
for plane in planes:
    # Dominio: posibles posiciones (x, y)
    problem.addVariable(plane, [(0, 0), (1, 1), (2, 2)])

# Restricción personalizada: los aviones no pueden compartir la misma posición
def unique_positions(*args):
    return len(args) == len(set(args))

problem.addConstraint(unique_positions, planes)

# Resolver el problema
solutions = problem.getSolutions()
for solution in solutions:
    print(solution)
