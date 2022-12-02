# Day 1: Calorie Counting
# https://adventofcode.com/2022/day/1

def readfile():
    with open("input/day01_input.txt") as f:
        lines = f.readlines()
    return lines


def solution_part1():
    lines = readfile()

    max_total = 0
    curr_total = 0

    for l in lines:
        # new line case
        if l == '\n':
            # update totals
            max_total = max(max_total, curr_total)
            curr_total = 0
        else:
            curr_total += int(l)
            
    # Check last
    return max(max_total, curr_total)
            

def solution_part1_b():
    lines = readfile()
    
    curr_total = 0
    totals = []
    for l in lines:
        if l == '\n':
            totals.append(curr_total)
            curr_total = 0
        else:
            curr_total += int(l)
    
    totals.append(curr_total)
    
    totals.sort()
    return totals[-1]
    

def solution_part2():
    lines = readfile()
    
    curr_total = 0
    totals = []
    for l in lines:
        if l == '\n':
            totals.append(curr_total)
            curr_total = 0
        else:
            curr_total += int(l)
    
    totals.append(curr_total)
    
    totals.sort()
    print(totals[-3:])
    return sum(totals[-3:])
    
            
            
if __name__ == '__main__':
    print(solution_part1())
    
    print("------")
    
    print(solution_part2())