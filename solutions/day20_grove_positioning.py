# Day 20. Grove Positioning System 
# https://adventofcode.com/2022/day/20

from copy import deepcopy
from collections import deque
from util.input_util import read_input_file

def parse_lines():
    lines = read_input_file(20)
    seq = []
    for i in range(len(lines)):
        seq.append((i, int(lines[i]))) #(order, num)
    return seq


def swap(seq, i, j):
    seq[i], seq[j] = seq[j], seq[i]


def mix(seq, idx, num, MOD):
    i = seq.index((idx, num))
    
    if num > 0:
        for _ in range(num % (MOD-1)):
            j = (i+1) % MOD
            swap(seq, i, j)
            i = j

    elif num < 0:
        for _ in range(abs(num) % (MOD-1)):
            j = (i-1) % MOD
            swap(seq, i, j)
            i = j

        

COORD_IDXS = (1000, 2000, 3000)

def solution1():
    seq = parse_lines()
    MOD = len(seq)
    original_order = deepcopy(seq)
    
    for idx in range(MOD):
        idx, num = original_order[idx]
        print(f'{str(idx+1).zfill(4)} \t {str(num).zfill(5)}\r', end='')
        mix(seq, idx, num, MOD)

    print()
    zi = None
    for i in range(len(seq)):
        idx, n = seq[i]
        if n == 0:
            zi = i
            break
    
    coords = tuple(seq[(zi+x) % MOD][1] for x in COORD_IDXS)
    print(coords)
    return sum(coords)
    
 
    
def solution2():
    DECRYPT_KEY = 811589153

    seq = parse_lines()    
    seq = [(i, n * DECRYPT_KEY) for i, n in seq]
    MOD = len(seq)
    original_order = deepcopy(seq)
    
    for m in range(10):
        print(f'Mix: {m+1}')
        for idx in range(MOD):
            idx, num = original_order[idx]
            print(f'{str(idx+1).zfill(4)} \t {str(num).zfill(5)}\r', end='')
            mix(seq, idx, num, MOD)
        print()

    zi = None
    for i in range(len(seq)):
        idx, n = seq[i]
        if n == 0:
            zi = i
            break
    
    coords = tuple(seq[(zi+x) % MOD][1] for x in COORD_IDXS)
    print(coords)
    return sum(coords)
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
