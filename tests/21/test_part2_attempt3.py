import unittest

import day_21.part2_attempt3 as part2_attempt3

class TestPart2Attempt3(unittest.TestCase):

    def test_group_by_A(self):
        seq = '<A^A>^^AvvvA'
        expected = ['<A', '^A', '>^^A', 'vvvA']
        self.assertEqual(part2_attempt3.group_by_A(seq), expected)

    def test_find_shortest_sequence_length(self):
        code = '029A'
        for depth, expected in [
            (0, 12),  # <A^A>^^AvvvA
            # (1, 28),  # v<<A>>^A<A>AvA<^AA>A<vAAA>^A
            # (2, 68),  # <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
        ]:
            self.assertEqual(expected, part2_attempt3.find_shortest_sequence_length({}, code, depth))

if __name__ == '__main__':
    unittest.main()
