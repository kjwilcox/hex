
class Grid:
    """ A hex grid object. """

    def __init__(self, size=11):
        """ Initializes an empty grid. """

        if size < 3 or size > 25:
            raise ValueError, "size is not in [3, 25]"

        if int(size) is not size:
            raise ValueError, "size is not an integer"

        self.size = size            
        self.data = [[None for i in range(size)] for i in range(size)]
        self.moves = []

    def get(self, x, y):
        """ Returns the contents of a given cell. """

        if x not in range(self.size) or y not in range(self.size):
            raise IndexError, "x and y is not in range"

        return self.data[y][x]
        

    def move(self, x, y, player):
        """ Applies a move to the grid. """

        if x not in range(self.size) or y not in range(self.size):
            raise IndexError, "x and y is not in range"

        if player is not 1 and player is not 2:
            raise ValueError, "player is not 1 or 2"

        if self.get(x, y) is not None:
            raise ValueError, "cell is already filled"

        self.data[y][x] = player
        self.moves.append((x, y))

    def is_chain(self, orientation, player):
        """ Determines whether or not a player has completed a chain. """

        if player is not 1 and player is not 2:
            raise ValueError, "player is not 1 or 2"

        if orientation is not 'h' and orientation is not 'v':
            raise ValueError, "orientation is not 'h' or 'v'"

        starting_coords = []
        ending_coords = []

        for num in range(self.size):
            if orientation is 'h':
                starting_coords.append((0, num))
                ending_coords.append((self.size - 1, num))
            else: # orientation is 'v'
                starting_coords.append((num, 0))
                ending_coords.append((num, self.size - 1))

        for start in starting_coords:
            data = self._get_traversable_grid()
            result = self._traverse(data, start[0], start[1], player, ending_coords)

            if result:
                return True

        return False

    def undo(self):
        """ Removes the last move made from the grid. """

        move = self.moves.pop()
        self.data[move[1]][move[0]] = None

    def _get_neighbors(self, x, y):
        """ Return a list of the coordinates of neighbors. """

        if x not in range(self.size) or y not in range(self.size):
            raise IndexError, "x and y is not in range"

        neighbors = []

        # upper neighbors
        if y > 0:
            neighbors.append((x, y - 1))
            if x > 0:
                neighbors.append((x - 1, y - 1))

        # side neighbors
        if x > 0:
            neighbors.append((x - 1, y))
        if x < 10:
            neighbors.append((x + 1, y))

        # lower neighbors
        if y < 10:
            neighbors.append((x, y + 1))
            if x < 10:
                neighbors.append((x + 1, y + 1))

        return neighbors

    def _get_traversable_grid(self):
        """
        Returns a copy of the grid to walk.
        The tuple contains the cell data,
        and whether the cell has been visited.
        """
        
        data = [[None for i in range(self.size)] for i in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                data[row][col] = (self.data[row][col], False)

        return data

    def _traverse(self, data, x, y, player, endings):
        """ Mark node visited and look around more """

        if x not in range(self.size) or y not in range(self.size):
            raise IndexError, "x and y is not in range"
        
        if player is not 1 and player is not 2:
            raise ValueError, "player is not 1 or 2"

        # already been here
        if data[y][x][1]:
            return False

        # set current cell to visited
        data[y][x] = (data[y][x][0], True)

        # we can't recurse if it's not our square
        if data[y][x][0] is not player:
            return False

        # base case: sucess
        if (x, y) in endings:
            return True

        # recurse into the neighbors
        for neighbor in self._get_neighbors(x, y):
            if self._traverse(data, neighbor[0], neighbor[1], player, endings):
                return True

        return False
