REGISTER = 'Register'

class Day17(object):
    def __init__(self, contents):
        registers, inputs = self.parse_contents(contents)

        self._inputs = inputs
        self._outputs = []

        self._register_a = registers['A']
        self._register_b = registers['B']
        self._register_c = registers['C']

        self._instruction_pointer = 0
        self._has_jumped = False

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return ','.join(self._outputs)

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

    def run(self):
        while self._instruction_pointer < len(self.inputs) - 1:
            self._has_jumped = False
            opcode = self.inputs[self._instruction_pointer]
            self._operand = self.inputs[self._instruction_pointer + 1]
            self.run_instruction(opcode)
            if not self._has_jumped:
                self._instruction_pointer += 2

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

    def run_instruction(self, opcode):
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
        return mapping[opcode]()

    def adv(self):
        new_a = self.register_a // (2 ** self.combo_operand)
        self._register_a = new_a

    def bdv(self):
        new_b = self.register_a // (2 ** self.combo_operand)
        self._register_b = new_b

    def cdv(self):
        new_c = self.register_a // (2 ** self.combo_operand)
        self._register_c = new_c

    def bxl(self):
        new_b = self.bitwise_xor(self.register_b, self.literal_operand)
        self._register_b = new_b

    def bst(self):
        new_b = self.combo_operand % 8
        self._register_b = new_b

    def jnz(self):
        if self.register_a == 0:
            return

        self._instruction_pointer = self.literal_operand
        self._has_jumped = True

    def bxc(self):
        new_b = self.bitwise_xor(self.register_b, self.register_c)
        self._register_b = new_b

    def out(self):
        val = self.combo_operand % 8
        self._outputs.append(str(val))

    def bitwise_xor(self, a, b):
        return a ^ b

if __name__ == '__main__':
    with open('17/day_17_input.txt', 'r') as f:
        contents = f.read()

    program = Day17(contents)
    print('registers: ', { 'A': program.register_a, 'B': program.register_b, 'C': program.register_c })
    print('inputs: ', program.inputs)

    program.run()
    print(program.outputs)
