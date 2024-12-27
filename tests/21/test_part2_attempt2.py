import unittest

import day_21.part2_attempt2 as part2_attempt2

class TestPart2Attempt2(unittest.TestCase):

    def test_group_by_A(self):
        seq = ['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']
        expected = [['<', 'A'], ['^', 'A'], ['>', '^', '^', 'A'], ['v', 'v', 'v', 'A']]
        self.assertEqual(part2_attempt2.group_by_A(seq), expected)

    def test_find_shortest_paths(self):
        result = part2_attempt2.find_shortest_paths(part2_attempt2.DIRECTIONAL_KEYPAD, 'A', '<')
        print(result)

if __name__ == '__main__':
    unittest.main()
