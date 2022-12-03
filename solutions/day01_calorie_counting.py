# Day 1: Calorie Counting
# https://adventofcode.com/2022/day/1

from util.input_util import read_input_file


def solution1():
    lines = read_input_file(1)

    max_total = 0
    curr_total = 0

    for l in lines:
        # new line case
        if l == '':
            # update totals
            max_total = max(max_total, curr_total)
            curr_total = 0
        else:
            curr_total += int(l)
            
    # Check last
    return max(max_total, curr_total)
            

def solution1b():
    lines = read_input_file(1)
    
    curr_total = 0
    totals = []
    for l in lines:
        if l == '':
            totals.append(curr_total)
            curr_total = 0
        else:
            curr_total += int(l)
    
    totals.append(curr_total)
    
    totals.sort()
    return totals[-1]
    

def solution2():
    lines = read_input_file(1)
    
    curr_total = 0
    totals = []
    for l in lines:
        if l == '':
            totals.append(curr_total)
            curr_total = 0
        else:
            curr_total += int(l)
    
    totals.append(curr_total)
    
    totals.sort()
    print(totals[-3:])
    return sum(totals[-3:])
    
            
            
if __name__ == '__main__':
    print(solution1())
    
    print("------")
    
    print(solution2())