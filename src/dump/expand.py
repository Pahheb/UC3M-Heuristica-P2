def expand_state(self)-> list[State]:
        childStates = []
        # 1. Get all possible valid and non-valid combinations
        possibleMoves= self.cartesian_product(self.possibleMoves*len(self.planeValues))
        possibleChilds = []
        for moveSet in possibleMoves:
            newPositions= []
            for i in range(len(self.planePositions)):
                x, y = self.planePositions[i]
                dx, dy = moveSet[i]
                newPositions.append((x + dx, y + dy))
            possibleChilds.append(newPositions)
        # 2. Apply restrictions for non-valid combinations 
        # No two planes in the same position
        nonRepeatedChilds = []
        for child in possibleChilds:
            for elem in child:
                if child.count(elem) == 1:
                    nonRepeatedChilds.append(child)
        # No two planes can cross
        for i in range(len(nonRepeatedChilds)):
            for j in range(len(nonRepeatedChilds[i]):
                for k in len(self.planePositions):
                    if not(nonRepeatedChilds[i][j] == self.planePositions[k] \
                           and nonRepeatedChilds[k] == self.planePositions[j]):
                
                childValues.append(nonRepeatedChilds[j]

        # 3. Create child states
            #3. for each move operation add 1 to the cost 
            #3.2 for each wait operation add to the cost

