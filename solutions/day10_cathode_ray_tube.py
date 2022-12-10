# Day 10. Cathode Ray Tube 
# https://adventofcode.com/2022/day/10

from util.input_util import read_input_file

# addx V - takes 2 cycles to complete - X increased by V
# noop - takes 1 cycle to complete - do nothing
# signal strength - cycle# * X value - every 20th cycle

NOOP = 'noop'
ADDX = 'addx'

def parse_lines():
    lines = read_input_file(10)
    
    commands = []
    for l in lines:
        if l == NOOP:
            commands.append(NOOP)
        else:
            _, v = l.split(' ')
            commands.append(int(v))
            
    return commands

def calculate_cycles(commands:list) -> list:
    X = 1
    # cycle[c] = value at end of cycle c
    cycles = []
    for c in commands:
        if c == NOOP:
            cycles.append(X)
        else:
            cycles.append(X)
            cycles.append(X)
            X += c
    
    cycles.append(X)
    return cycles


def solution1():
    cmds = parse_lines()
    cycles = calculate_cycles(cmds)
    
    VALUES_AT_THESE_CYCLES = [20, 60, 100, 140, 180, 220]
    signal = 0
    for V in VALUES_AT_THESE_CYCLES:
        #print(V, cycles[V-1])
        signal += (cycles[V-1] * V)

    return signal


# Spite is 3 pixels wide
# X is horizontal position of the middle of the sprite
# CRT 40w x 6h - draw left to right, top to down

def solution2():
    cmds = parse_lines()
    cycles = calculate_cycles(cmds)
    
    CRT = ""
    c = 0
    for row in range(6):
        for col in range(40):
            sprite_position = {cycles[c]-1, cycles[c], cycles[c]+1}
            if col in sprite_position:
                CRT += '#'
            else:
                CRT += '.'
            c += 1 
        CRT += '\n' # new Line
    
    return CRT
    
            
            
            
            
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
