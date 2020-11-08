import unittest
import utility


class TestUtility(unittest.TestCase):
    def test_permutations(self):
        perm_gen = utility.permutations([1, 2, 3, 4, 5], 2)
        options = {0: {1, 2},
                   1: {1, 3},
                   2: {1, 4},
                   3: {1, 5},
                   4: {2, 3},
                   5: {2, 4},
                   6: {2, 5},
                   7: {3, 4},
                   8: {3, 5},
                   9: {4, 5}
                   }
        index = 0
        for x in perm_gen:
            self.assertEqual(set(x), options[index])
            index += 1


