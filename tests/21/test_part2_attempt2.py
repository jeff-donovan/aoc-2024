import unittest

import day_21.part2_attempt2 as part2_attempt2

class TestPart2Attempt2(unittest.TestCase):

    def test_group_by_A(self):
        seq = ['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']
        expected = [['<', 'A'], ['^', 'A'], ['>', '^', '^', 'A'], ['v', 'v', 'v', 'A']]
        self.assertEqual(part2_attempt2.group_by_A(seq), expected)

    def test_find_shortest_paths_returns_list_of_strings(self):
        for start in part2_attempt2.DIRECTIONAL_KEYPAD.keys():
            for end in part2_attempt2.DIRECTIONAL_KEYPAD.keys():
                result = part2_attempt2.find_shortest_paths(part2_attempt2.DIRECTIONAL_KEYPAD, start, end)
                for path in result:
                    self.assertEqual(str, type(path))

if __name__ == '__main__':
    unittest.main()
