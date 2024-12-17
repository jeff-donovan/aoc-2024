REGISTER = 'Register'

def make_registers_and_inputs(contents):
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

def get_combo_operand_value(combo_operand):
    mapping = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: get_A(),
        5: get_B(),
        6: get_C(),
    }

    return mapping[combo_operand]

def get_A():
    pass

def set_A(val):
    pass

def get_B():
    pass

def set_B(val):
    pass

def get_C():
    pass

def set_C(val):
    pass

def set_instruction_pointer(val):
    pass

def set_should_pointer_increase_by_2(flag):
    pass

def run_instruction(opcode, literal_operand, combo_operand):
    mapping = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }
    return mapping[opcode]()  # TODO: once class method, this works

def adv(combo_operand):
    new_A = get_A() // (2 ^ (get_combo_operand_value(combo_operand)))
    set_A(new_A)

def bdv(combo_operand):
    new_B = get_B() // (2 ^ (get_combo_operand_value(combo_operand)))
    set_B(new_B)

def cdv(combo_operand):
    new_C = get_C() // (2 ^ (get_combo_operand_value(combo_operand)))
    set_C(new_C)

def bxl(literal_operand):
    new_B = None  # calculate the bitwise XOR of register B and literal_operand
    set_B(new_B)

def bst(combo_operand):
    new_B = get_combo_operand_value(combo_operand) % 8
    set_B(new_B)

def jnz(literal_operand):
    if get_A() == 0:
        return
    set_instruction_pointer(literal_operand)
    # should we check the response of set_instruction_pointer() to see if the instruction "jumps"?
    set_should_pointer_increase_by_2(False)

def bxc(operand):
    new_B = None  # calculate the bitwise XOR of register B and register C
    set_B(new_B)

def out(combo_operand):
    val = get_combo_operand_value(combo_operand) % 8
    print(val)  # unclear if we should print or return
    return val

if __name__ == '__main__':
    with open('17/day_17_test.txt', 'r') as f:
        contents = f.read()

    registers, inputs = make_registers_and_inputs(contents)
    print('registers: ', registers)
    print('inputs: ', inputs)
