import datetime


REGISTER = 'Register'

class Day17(object):
    def __init__(self, register_a, inputs):
        self._inputs = inputs
        self._outputs = []

        self._register_a = register_a  # ignore register_a value from contents
        self._register_b = 0
        self._register_c = 0

        self._instruction_pointer = 0
        self._has_jumped = False

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    def raise_if_outputs_invalid(self):
        for i, output in enumerate(self._outputs):
            if output != self._inputs[i]:
                raise Exception()

    def print_outputs(self):
        print(','.join([str(x) for x in self.outputs]))

    def is_copy(self):
        if len(self._inputs) != len(self._outputs):
            return False

        for i in range(len(self._inputs)):
            if self._inputs[i] != self._outputs[i]:
                return False
        return True

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
        self._outputs.append(val)
        self.raise_if_outputs_invalid()

    def bitwise_xor(self, a, b):
        return a ^ b

def parse_contents(contents):
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

def is_valid(initial_A):
    return (
        (2 == (((((initial_A // 8) % 8) ^ 5) ^ ((initial_A // 8) // (2 ** (((initial_A // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (4 == ((((((initial_A // 8) // 8) % 8) ^ 5) ^ (((initial_A // 8) // 8) // (2 ** ((((initial_A // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (1 == (((((((initial_A // 8) // 8) // 8) % 8) ^ 5) ^ ((((initial_A // 8) // 8) // 8) // (2 ** (((((initial_A // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (5 == ((((((((initial_A // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((initial_A // 8) // 8) // 8) // 8) // (2 ** ((((((initial_A // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (7 == (((((((((initial_A // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((initial_A // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((initial_A // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (5 == ((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (4 == (((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (5 == ((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (0 == (((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (3 == ((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (1 == (((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (6 == ((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (5 == (((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (5 == ((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (3 == (((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8) and
        (0 == ((((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8)
        # True
    )

if __name__ == '__main__':
    with open('17/day_17_input.txt', 'r') as f:
        contents = f.read()

    registers, inputs = parse_contents(contents)

    # register_a = 168046722  # what i left off at last time

    # start = datetime.datetime.now()
    # register_a = 0
    # while True:
    #     print('register a: ', register_a)
    #     program = Day17(register_a, inputs)
    #     program.run()
    #     if program.is_copy():
    #         print('SOLUTION IS: ', register_a)
    #         break
    #     register_a += 1
    # print('SOLUTION APPROACH 1 TOOK: ', datetime.datetime.now() - start)
    # print()

    start = datetime.datetime.now()
    # # initial_A = 29641936
    # initial_A = 281474976710655
    # initial_A = 2251799813685247  # I think initial_A MUST BE BELOW THIS NUMBER
    # initial_A = 2251799813685250
    # low = 8 ** 16
    # high = 8 ** 17
    # initial_A = -1
    # initial_A = 8 ** 16
    # initial_A = 281475043819520

    # while low <= high:
    #     mid = (low + high) // 2
    #     if is_valid(mid):
    #     # if 1 == ((((((((((((((((mid // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8:
    #         initial_A = mid
    #         high = mid - 1
    #     else:
    #         low = mid + 1
    # while not is_valid(initial_A):
    #     initial_A += 1

    constraints = [
        lambda initial_A : (2 == (((((initial_A // 8) % 8) ^ 5) ^ ((initial_A // 8) // (2 ** (((initial_A // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (4 == ((((((initial_A // 8) // 8) % 8) ^ 5) ^ (((initial_A // 8) // 8) // (2 ** ((((initial_A // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (1 == (((((((initial_A // 8) // 8) // 8) % 8) ^ 5) ^ ((((initial_A // 8) // 8) // 8) // (2 ** (((((initial_A // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (5 == ((((((((initial_A // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((initial_A // 8) // 8) // 8) // 8) // (2 ** ((((((initial_A // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (7 == (((((((((initial_A // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((initial_A // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((initial_A // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (5 == ((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (4 == (((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (5 == ((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (0 == (((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (3 == ((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (1 == (((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (6 == ((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (5 == (((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (5 == ((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (3 == (((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ ((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** (((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
        lambda initial_A : (0 == ((((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5) ^ (((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // (2 ** ((((((((((((((((((initial_A // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) // 8) % 8) ^ 5)))) ^ 6) % 8),
    ]

    # initial_A = 8 ** 16
    initial_A = 1047014855769602392064

    while len(constraints) > 0:
        check = constraints.pop(0)
        while not check(initial_A):
            initial_A += 1
        print(initial_A)

    print(initial_A)
    print('SOLUTION APPROACH 2 TOOK: ', datetime.datetime.now() - start)

    # start = datetime.datetime.now()
    # # register_a = 2563700000  # what i left off at last time
    # register_a = 0
    # num_outputs = 0
    # while register_a < 1001:
    #     # if register_a % 100 == 0:
    #     #     print('register a: ', register_a)
    #     program = Day17(register_a, inputs)
    #     try:
    #         program.run()
    #         if program.is_copy():
    #             print('SOLUTION IS: ', register_a)
    #             break
    #         register_a += 1
    #     except:
    #         register_a += 1

    #     # if len(program.outputs) >= num_outputs:
    #     #     num_outputs = len(program.outputs)
    #     #     print(f'{num_outputs} OUTPUTS | {register_a}')
    #     num_outputs = len(program.outputs)
    #     print(f'{num_outputs} OUTPUTS | {register_a - 1}')  # remember - we've already incremented register_a
    # print('SOLUTION APPROACH 3 TOOK: ', datetime.datetime.now() - start)
    # print()
