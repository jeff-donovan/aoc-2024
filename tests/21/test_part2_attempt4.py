import unittest

import day_21.part2_attempt4 as part2_attempt4

class TestPart2Attempt4(unittest.TestCase):

    def test_split_by_A(self):
        seq = '<A^A>^^AvvvA'
        expected = ['<A^A', '>^^AvvvA']
        self.assertEqual(part2_attempt4.split_by_A(seq), expected)

    def test_calculate_shortest_path_length(self):
        for seq, depth, expected in [
            ('<A^A>^^AvvvA', 0, len('<A^A>^^AvvvA')),
            ('<A^A>^^AvvvA', 1, len('v<<A>>^A<A>AvA<^AA>A<vAAA>^A')),
            ('<A^A>^^AvvvA', 2, len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A')),
        ]:
            self.assertEqual(expected, part2_attempt4._calculate_shortest_path_length({}, seq, depth))

    def test_directional_to_directional_with_winner(self):
        print('hi jeff')
        print(part2_attempt4._directional_to_directional_with_winner({}, 'vvvA'))

if __name__ == '__main__':
    unittest.main()
