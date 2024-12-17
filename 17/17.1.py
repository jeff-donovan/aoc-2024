REGISTER = 'Register'

class Day17(object):
    def __init__(self, contents):
        registers, inputs = self.parse_contents(contents)

        self._inputs = inputs

        self._register_a = registers['A']
        self._register_b = registers['B']
        self._register_c = registers['C']

    @property
    def inputs(self):
        return self._inputs

    @property
    def register_a(self):
        return self._register_a

    @property
    def register_b(self):
        return self._register_b

    @property
    def register_c(self):
        return self._register_c

    @property
    def literal_operand(self):
        return self._operand

    @property
    def combo_operand(self):
        mapping = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.register_a,
            5: self.register_b,
            6: self.register_c,
        }
        return mapping[self._operand]

    def parse_contents(self, contents):
        register_contents, input_contents = contents.split('\n\n')
        registers = {}
        for line in register_contents.split('\n'):
            if line:
                register_data = line.split(': ')
                register_code = register_data[0][len(REGISTER) + 1:]
                register_value = int(register_data[1])
                registers[register_code] = register_value

        inputs = []
        for line in input_contents.split('\n'):
            if line:
                inputs_data = line.split(': ')
                for input in inputs_data[1].split(','):
                    if input:
                        inputs.append(int(input))

        return registers, inputs

    def set_instruction_pointer(val):
        pass

    def set_should_pointer_increase_by_2(flag):
        pass

    def run_instruction(self):
        mapping = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        return mapping[self._opcode]()

    def adv(self):
        new_a = self.register_a // (2 ** self.combo_operand)
        self._register_a = new_a

    def bdv(self):
        new_b = self.register_b // (2 ** self.combo_operand)
        self._register_b = new_b

    def cdv(self):
        new_c = self.register_c // (2 ** self.combo_operand)
        self._register_c = new_c

    def bxl(self):
        new_b = None  # calculate the bitwise XOR of register B and literal_operand
        self._register_b = new_b

    def bst(self):
        new_b = self.combo_operand % 8
        self._register_b = new_b

    def jnz(self):
        if self.register_a == 0:
            return
        self.set_instruction_pointer(self.literal_operand)
        # should we check the response of set_instruction_pointer() to see if the instruction "jumps"?
        self.set_should_pointer_increase_by_2(False)

    def bxc(self):
        new_b = None  # calculate the bitwise XOR of register B and register C
        self._register_b = new_b

    def out(self):
        val = self.combo_operand % 8
        print(val)  # unclear if we should print or return
        return val

if __name__ == '__main__':
    with open('17/day_17_test.txt', 'r') as f:
        contents = f.read()

    program = Day17(contents)
    print('registers: ', { 'A': program.register_a, 'B': program.register_b, 'C': program.register_c })
    print('inputs: ', program.inputs)
