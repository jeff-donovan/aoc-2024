import unittest
from day_21.part2 import group_by_A

class TestGroupByA(unittest.TestCase):

    def test_A(self):
        seq = '<A^A>^^AvvvA'
        expected = ['<A', '^A', '>^^A', 'vvvA']
        self.assertEqual(group_by_A(seq), expected)

if __name__ == '__main__':
    unittest.main()
