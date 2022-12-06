# Day 6. Tuning Trouble
# https://adventofcode.com/2022/day/6

from util.input_util import read_input_file




def solution1():
    lines = read_input_file(6)
    line = lines[0]
    
    for i in range(4, len(line)+1):
        if len(set(line[i-4:i])) == 4:
            return i
        
    
def solution2():
    lines = read_input_file(6)
    line = lines[0]
    
    for i in range(14, len(line)+1):
        if len(set(line[i-14:i])) == 14:
            return i
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
