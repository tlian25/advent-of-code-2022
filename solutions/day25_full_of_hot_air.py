# Day 25 
# https://adventofcode.com/2022/day/25

import itertools
import math
from util.input_util import read_input_file

MINUS = '-'
DMINUS = '='

ADJ = {MINUS:-1, DMINUS:-2}

def parse_lines():
    lines = read_input_file(25)
    return lines
    



# Output and flow rate = sum of the fuel reqs of all the hot air ballons
# SNAFU powers of 5 instead of 10


def convert_snafu_to_decimal(snafu:str):
    total = 0
    adjust = None
    currplace = 0
    # Scan backwards
    for i in range(len(snafu)-1, -1, -1):
        if snafu[i] in (MINUS, DMINUS):
            s = ADJ[snafu[i]]
        else:
            s = int(snafu[i])
            
        n = 5 ** currplace * s
        currplace += 1
        total += n
    
    return total
            


def convert_decimal_to_snafu(decimal:int):
    DIGITS = ('0', '1', '2', '-', '=')

    N = math.floor(math.log(decimal, 5))
    S = ['0' for _ in range(N+1)]
    for i in range(N+1):
        
        closestD = '0'
        mindist = float('inf')
        for d in DIGITS:
            S[i] = d
            s = convert_snafu_to_decimal(''.join(S))
            dist = abs(s - decimal)
            if dist < mindist:
                mindist = dist
                closestD = d
            S[i] = closestD
             
    return ''.join(S)
    


def solution1():
    snafus = parse_lines()
    total = 0
    for s in snafus:
        d = convert_snafu_to_decimal(s)
        #print(s, '\t\t', d)
        total += d
        
    s = convert_decimal_to_snafu(total)
    return s
    
    
def solution2():
    pass
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
