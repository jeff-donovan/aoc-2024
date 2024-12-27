import json
import unittest

import day_21.part2 as part2

class TestPart2(unittest.TestCase):

    def test_group_by_A(self):
        seq = ['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']
        expected = [['<', 'A'], ['^', 'A'], ['>', '^', '^', 'A'], ['v', 'v', 'v', 'A']]
        self.assertEqual(part2.group_by_A(seq), expected)

    def test_directional_to_directional(self):
        seq = ['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']
        expected = ['v', '<', '<', 'A', '>', '>', '^', 'A', '<', 'A', '>', 'A', 'v', 'A', '<', '^', 'A', 'A', '>', 'A', '<', 'v', 'A', 'A', 'A', '>', '^', 'A']
        self.assertIn(expected, part2.directional_to_directional(seq))

    def test_directional_to_directional_by_depth(self):
        initial_seq = ['v', 'v', 'v', 'A']
        second_level_sequences = part2.directional_to_directional(initial_seq)
        print('num second_level_sequences: ', len(second_level_sequences))
        print(second_level_sequences[0])
        for i in range(len(second_level_sequences)):
            third_level_sequences = part2.directional_to_directional(second_level_sequences[i])
            print(f'{i} - {part2.calculate_min_path_length(third_level_sequences)}')
            for seq in third_level_sequences:
                fourth_level_sequences = part2.directional_to_directional(seq)
                print(f'{i} - {part2.calculate_min_path_length(fourth_level_sequences)}')
                for four_seq in fourth_level_sequences:
                    fifth_level_sequences = part2.directional_to_directional(four_seq)
                    print(f'{i} - {part2.calculate_min_path_length(fifth_level_sequences)}')

    def test_directional_to_directional_using_group_by_A(self):
        seq = ['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']
        expected = ['v', '<', '<', 'A', '>', '>', '^', 'A', '<', 'A', '>', 'A', 'v', 'A', '<', '^', 'A', 'A', '>', 'A', '<', 'v', 'A', 'A', 'A', '>', '^', 'A']
        self.assertIn(expected, part2.directional_to_directional_using_group_by_A(seq))

    def test_shortest_d_to_d(self):
        seq = ['>', '^', '^', 'A']
        expected = ['v', 'A', '<', '^', 'A', 'A', '>', 'A']
        self.assertEqual(expected, part2.shortest_d_to_d({}, seq))

if __name__ == '__main__':
    unittest.main()
