# Day 13. Distress Signal
# https://adventofcode.com/2022/day/13

from util.input_util import read_input_file

def compare_packets(first:list, second:list) -> int:
    assert isinstance(first, list)
    assert isinstance(second, list)
    l1 = len(first)
    l2 = len(second)
    
    for i in range(min(l1, l2)):
        a = first[i]
        b = second[i]
        if isinstance(a, int) and isinstance(b, int):
            if a < b: return 1
            elif a > b: return -1
            continue
        elif isinstance(a, int) and isinstance(b, list):
            c = compare_packets([a], b)
        elif isinstance(a, list) and isinstance(b, int):
            c = compare_packets(a, [b])
        elif isinstance(a, list) and isinstance(b, list): # both lists
            c = compare_packets(a, b)
        else:
            raise TypeError(f'Unknown types: {type(a)}, {type(b)}')
        
        if c == 1: return 1
        elif c == -1: return -1
    
    if l1 == l2: return 0
    elif l1 < l2: return 1
    else: return -1
    

class Packet:
    def __init__(self, value:list):
        self.v = value
        
    def __lt__(self, other):
        c = compare(self.v, other.v)
        return c == 1
    
    def __eq__(self, other):
        c = compare(self.v, other.v)
        return c ==0
        
    def __str__(self) -> str:
        return str(self.v)

def parse_lines():
    lines = read_input_file(13)
    # pakcers are list and integers
    # if both values integers, the lower should come first
    # if both values are lists, compare the first value of each list
    # first list len <= second list len
    # if one value is a list, convert to list and compare
    first = None
    second = None
    packets = []
    for l in lines:
        if l == '':
            packets.append((first, second))
            first = None
            second = None
        elif first is None:
            first = eval(l)
        elif second is None:
            second = eval(l)
    
    if first and second:
        packets.append((first, second))
    return packets
            

# Recursive comparison function
# If first == second -> return 0
# If first < second -> return 1
# If first > second -> return -1
def compare(first:list, second:list) -> int:
    assert isinstance(first, list)
    assert isinstance(second, list)
    l1 = len(first)
    l2 = len(second)
    
    for i in range(min(l1, l2)):
        a = first[i]
        b = second[i]
        if isinstance(a, int) and isinstance(b, int):
            if a < b: return 1
            elif a > b: return -1
            continue
        elif isinstance(a, int) and isinstance(b, list):
            c = compare([a], b)
        elif isinstance(a, list) and isinstance(b, int):
            c = compare(a, [b])
        elif isinstance(a, list) and isinstance(b, list): # both lists
            c = compare(a, b)
        else:
            raise TypeError(f'Unknown types: {type(a)}, {type(b)}')
        
        if c == 1: return 1
        elif c == -1: return -1
    
    if l1 == l2: return 0
    elif l1 < l2: return 1
    else: return -1
        
        
    
    
def solution1():
    packets = parse_lines()
    
    sum_indexes = 0
    for i in range(len(packets)):
        first, second = packets[i]
        #print(f"======= Pair: {i+1} ========")
        
        c = compare(first, second)
        if c >= 0: 
            #print()
            sum_indexes += i+1 # 1-indexed
            #print('TRUE\n')
    
    return sum_indexes




def solution2():
    pair_packets = parse_lines()
    # Flatten from tuples to list. Include divider packets.
    div1 = Packet([[2]])
    div2 = Packet([[6]])
    packets = [div1, div2]
    for a, b in pair_packets:
        packets.append(Packet(a))
        packets.append(Packet(b))
        
    sorted_packets = sorted(packets)
    
    for i in range(len(sorted_packets)):
        p = sorted_packets[i]
        if p == div1:
            #print('Div1 index:', i+1)
            idx1 = i+1
        if p == div2:
            #print('Div2 index:', i+i)
            idx2 = i+1
            
    return idx1 * idx2
    
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
