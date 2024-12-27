import unittest
import day_21.part2 as part2

class TestPart2(unittest.TestCase):

    def test_group_by_A(self):
        seq = '<A^A>^^AvvvA'
        expected = ['<A', '^A', '>^^A', 'vvvA']
        self.assertEqual(part2.group_by_A(seq), expected)

if __name__ == '__main__':
    unittest.main()
