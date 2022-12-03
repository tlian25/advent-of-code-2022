# Day 3. Rucksack Reorganization
# https://adventofcode.com/2022/day/3

from util.input_util import read_input_file

# Each line a rucksack
# Each rucksack has 2 compartments
# First half in first compartment
# Second half in second compartment

# Lowercase priority 1-26
# Uppercase priority 27-52

def priority(letter:str) -> int:
    if ord('a') <= ord(letter) <= ord('z'):
        return ord(letter) - ord('a') + 1
    return ord(letter) - ord('A') + 27

def solution1():
    lines = read_input_file(3)
    total = 0
    
    for l in lines:
        split_idx = len(l) // 2
        
        first = set(l[:split_idx])
        second = set(l[split_idx:])
        
        common = first.intersection(second).pop()
        #print(common, priority(common))
        total += priority(common)
        
    return total
        

# Every set of three lines is a single group

def solution2():
    lines = read_input_file(3)
    total = 0
    
    i = 0
    while i < len(lines):
        first = set(lines[i])
        second = set(lines[i+1])
        third = set(lines[i+2])
        
        common = first.intersection(second).intersection(third).pop()
        #print(i, common, priority(common))
        total += priority(common)
        i += 3
    
    return total
        
    
    

if __name__ == '__main__':
    print(solution1())
    
    print("------------")
    
    print(solution2())
        
        