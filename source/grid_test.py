import unittest
import grid

class grid_creation(unittest.TestCase):
    def test_valid_sizes(self):
        """ the grid class should properly initialize at all sizes """

        # creation...
        for size in range(3, 26):
            test_grid = grid.Grid(size)

            # all elements should be None
            for x in range(size):
                for y in range(size):
                    self.assertEqual(None, test_grid.get(x, y))

    def test_invalid_sizes(self):
        """
        the grid class should throw an exception if you try to create it with a
        bad size
        """

        # sizes too low
        for size in range(-10, 3):
            self.assertRaises(ValueError, grid.Grid, size)

        # sizes too high
        for size in range(26, 35):
            self.assertRaises(ValueError, grid.Grid, size)

class move_testing(unittest.TestCase):
    def test_valid_moves(self):
        """
        All squares should be able to be moved in.
        Also tests undo and failure for invalid players.
        """
        
        for player in range(1, 3): # players 1 and 2
            # create grid of all valid sizes:
            for size in range(3, 26):
                test_grid = grid.Grid(size)

                # test all valid spaces
                for x in range(size):
                    for y in range(size):
                        # move on the grid
                        test_grid.move(x, y, player)
                        # confirm that it wrote
                        self.assertEqual(player, test_grid.get(x, y))
                        # make sure we can't write it again
                        self.assertRaises(ValueError, test_grid.move,
                                          x, y, player)
                        # undo the move
                        test_grid.undo()
                        # check to make sure it undid
                        self.assertEqual(None, test_grid.get(x, y))
                        # make a move with a bogus player
                        self.assertRaises(ValueError, test_grid.move,
                                          x, y, 345345)
                        
                
    def test_invalid_moves(self):
        """ Invalid squares should throw an IndexError. """
        for player in range(1, 3): # players 1 and 2
            # create grid of all valid sizes:
            for size in range(3, 26):
                test_grid = grid.Grid(size)
                # bogus indexes
                self.assertRaises(IndexError, test_grid.move,
                                  -1, -1, player)
                self.assertRaises(IndexError, test_grid.move,
                                  0, -1, player)
                self.assertRaises(IndexError, test_grid.move,
                                  -1, 0, player)
                self.assertRaises(IndexError, test_grid.move,
                                  size, size, player)
                self.assertRaises(IndexError, test_grid.move,
                                  size, size-1, player)
                self.assertRaises(IndexError, test_grid.move,
                                  size-1, size, player)

    def test_invalid_reads(self):
        """ Invalid get() should return an IndexError. """
        for player in range(1, 3): # players 1 and 2
            # create grid of all valid sizes:
            for size in range(3, 26):
                test_grid = grid.Grid(size)
                # bogus indexes
                self.assertRaises(IndexError, test_grid.get,
                                  -1, -1)
                self.assertRaises(IndexError, test_grid.get,
                                  0, -1)
                self.assertRaises(IndexError, test_grid.get,
                                  -1, 0)
                self.assertRaises(IndexError, test_grid.get,
                                  size, size)
                self.assertRaises(IndexError, test_grid.get,
                                  size, size-1)
                self.assertRaises(IndexError, test_grid.get,
                                  size-1, size)
        

if __name__ == "__main__":
    unittest.main()
