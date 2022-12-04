# Day 4. Camp Cleanup
# https://adventofcode.com/2022/day/4

from util.input_util import read_input_file

def to_tuple(s:str):
    a, b = s.split('-')
    return (int(a), int(b))


def check_full_overlap(s1, s2):
    
    if s1[0] <= s2[0] and s1[1] >= s2[1]:
        return True
    if s2[0] <= s1[0] and s2[1] >= s1[1]:
        return True
    
    return False


def solution1():
    # Fully contain
    lines = read_input_file(4)
    
    total_overlap = 0
    for l in lines:
        #sections
        s1, s2 = l.split(',')
        s1 = to_tuple(s1)
        s2 = to_tuple(s2)
            
        # Check overlap
        if check_full_overlap(s1, s2):
            total_overlap += 1
    
    return total_overlap 



def check_partial_overlap(s1:tuple, s2:tuple):
    return s2[0] <= s1[0] <= s2[1] or s2[0] <= s1[1] <= s2[1]

    
def solution2():
    # Partial overlap
    lines = read_input_file(4)
    
    partial_overlap = 0
    for l in lines:
        #sections
        s1, s2 = l.split(',')
        s1 = to_tuple(s1)
        s2 = to_tuple(s2)
        
        # Check partial overlap
        if check_partial_overlap(s1, s2) or check_partial_overlap(s2, s1):
            partial_overlap += 1
    
    return partial_overlap



if __name__ == '__main__':
    print(solution1())
    
    print('----------')
    
    print(solution2())