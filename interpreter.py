# Brainfuck interpreter

import sys
from typing import List, Tuple

def find_matching_bracket(instructions: List[str], instruction_pointer: int) -> int:
    """
    Finds a matching bracket on the same level as the given bracket
    """
    #print("finding bracket")
    bracket_counter = 1
    inst = instructions
    ptr = instruction_pointer+1
    while bracket_counter != 0:
        if ptr >= len(inst):
            raise IndexError(f"missing ] for [ at {instruction_pointer}")
        #print(inst[ptr], ptr)
        if inst[ptr] == "]":
            bracket_counter -= 1
        elif inst[ptr] == "[":
            bracket_counter += 1
        ptr += 1
    #print(f"found bracket at {ptr}")
    return ptr-1

def interpret(instructions: List[str],
              instruction_pointer: int,
              registers: List[int],
              register_pointer: int) \
              -> Tuple[List[int], int]:
    """
    Interprets a script written in brainfuck
    
    Instructions:
    + : increase value of current register by 1
    - : decrease value of current register by 1
    > : increase the value of the pointer by 1
    < : decrease the value of the pointer by 1
    [ : begin loop, 'while current register != 0' 
    ] : end loop
    , : set the value of current register to ascii value of input
    """
    while instruction_pointer < len(instructions):
        current_instruction = instructions[instruction_pointer]
        #print(f"inst: {current_instruction}, registers: {registers}, reg_ptr: {register_pointer}")
        if current_instruction   == "+":
            registers[register_pointer] += 1
            if registers[register_pointer] > 255:
                raise ValueError(f"register {register_pointer} > 255")

        elif current_instruction == "-":
            registers[register_pointer] -= 1
            if registers[register_pointer] < 0:
                raise ValueError(f"register {register_pointer} < 0")

        elif current_instruction == ">":
            register_pointer += 1
            if register_pointer >= len(registers):
                registers.append(0)

        elif current_instruction == "<":
            register_pointer -= 1

        elif current_instruction == ".":
            print(chr(registers[register_pointer]), end="")

        elif current_instruction == "[":
            matching_bracket = find_matching_bracket(instructions, instruction_pointer)
            while registers[register_pointer] != 0:
                #print("looping")
                registers, register_pointer\
                = interpret(instructions[instruction_pointer+1:matching_bracket], 0,  registers, register_pointer)
            instruction_pointer = matching_bracket
        elif current_instruction == "]":
            pass
        elif current_instruction == ",":
            pass
        else:
            raise KeyError(f"invalid instruction: {current_instruction}")
        #print(registers)
        instruction_pointer += 1
    return (registers, register_pointer)

def main():
    if len(sys.argv) == 1:
        quit()
    
    with open(sys.argv[1], "r") as file:
        instructions = list(file.read().strip().replace(" ",""))
        print(' '.join(instructions))
    registers = [0]
    register_pointer = 0
    instruction_pointer = 0
    print("\nResult:")
    interpret(instructions, instruction_pointer, registers, register_pointer)
    print("\n")
    
if __name__ == "__main__":
    main()
