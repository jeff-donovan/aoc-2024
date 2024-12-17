def make_registers_and_program_inputs(contents):
    return {'A': 0, 'B': 0, 'C': 0}, []

def get_combo_operand_value(combo_operand):
    match combo_operand:
        case 0 | 1 | 2 | 3:
            return combo_operand
        case 4:
            # return self.A?
            return get_A()
        case 5:
            return get_B()
        case 6:
            return get_C()
        case 7 | _:
            raise Exception()

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

# 8 instructions/opcodes
def get_instruction(opcode, literal_operand, combo_operand):
    match opcode:
        case 0:
            return adv(combo_operand)
        case 1:
            return bxl(literal_operand)
        case 2:
            return bst(combo_operand)
        case 3:
            return jnz(literal_operand)
        case 4:
            return bxc(combo_operand)
        case 5:
            return out(combo_operand)
        case 6:
            return bdv(combo_operand)
        case 7:
            return cdv(combo_operand)

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
    with open('16/day_16_input.txt', 'r') as f:
        contents = f.read()

    map_object = make_map_object(contents)
    print_map(map_object['map'])

    travel(map_object)

    end_i, end_j = map_object['end']
    scores = []
    for end_direction in ['up', 'down', 'right', 'left']:
        if (end_i, end_j, end_direction) in map_object['scores']:
            scores.append(map_object['scores'][(end_i, end_j, end_direction)])
    print(min(scores))
