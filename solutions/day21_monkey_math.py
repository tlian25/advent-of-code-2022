# Day 21. Monkey Math
# https://adventofcode.com/2022/day/21

from copy import deepcopy
from util.input_util import read_input_file

# Operations
ADD = '+'
SUBTRACT = '-'
MULTIPLY = '*'
DIVIDE = '/'
EQUAL = '=='


class Monkey:
    def __init__(self, name):
        self.name = name
        self.num = None
        self.op = None
        self.m1 = None
        self.m2 = None
    
    # For part 1
    def get_num(self, monkeys:dict):
        if self.num is not None: # Don't need to operate if already done
            return self.num
        
        n1 = monkeys[self.m1].get_num(monkeys)
        n2 = monkeys[self.m2].get_num(monkeys)
        return self.operation(n1, n2)
    
    def operation(self, n1, n2):
        if self.op == EQUAL: return n1 == n2
        if self.op == ADD: return n1 + n2
        if self.op == SUBTRACT: return n1 - n2
        if self.op == MULTIPLY: return n1 * n2
        if self.op == DIVIDE: return n1 // n2
        raise ValueError(f"No operation set for monkey: {self.name}")
    
    def reverse_operation(self, n1, n2):
        if n1 is None:
            if self.op == ADD: return self.num - n2, n2
            if self.op == SUBTRACT: return self.num + n2, n2
            if self.op == MULTIPLY: return self.num // n2, n2
            if self.op == DIVIDE: return self.num * n2, n2
            if self.op == EQUAL: return n2, n2
        elif n2 is None:
            if self.op == ADD: return n1, self.num - n1
            if self.op == SUBTRACT: return n1, n1 - self.num
            if self.op == MULTIPLY: return n1, self.num // n1
            if self.op == DIVIDE: return n1, n1 // self.num
            if self.op == EQUAL: return n1, n1
     
            
        raise ValueError(f"No operation set for monkey: {self.name}")
    
    # For part 2
    def fill_down(self, monkeys):
        m1 = monkeys[self.m1]
        m2 = monkeys[self.m2]
        if m1 and m2:
            if m1.num is None and m1.num is None:
                raise ValueError('Both children are none')
        
            m1.num, m2.num = self.reverse_operation(m1.num, m2.num)
            
            m1.fill_down(monkeys)
            m2.fill_down(monkeys)
        
        
            
    def __str__(self):
        return f'{self.name} - {self.num} - {self.op}'
        
        

def parse_lines():
    lines = read_input_file(21)
    monkeys = {}
    for l in lines:
        s = l.split(' ')
        name = s[0].replace(':', '')
        m = Monkey(name)
        
        if len(s) == 2:
            num = int(s[1])
            m.num = num
            
        elif len(s) == 4:
            m.m1 = s[1]
            m.m2 = s[3]
            m.op = s[2]
        else:
            raise IndexError(f"Unknown line parsing: {l}")
        
        monkeys[name] = m
        
    return monkeys
            
            



def solution1():
    
    monkeys = parse_lines()
    return monkeys['root'].get_num(monkeys)
    
    
def solution2():
    
    monkeys = parse_lines()
    # Adjustments
    monkeys['root'].op = EQUAL
    monkeys['root'].num = True
    monkeys['humn'].num = None
    
    # Find which branch includes human
    curr = monkeys['root']
    while True:
        
        if curr.name == 'humn':
            return curr.num
        
        m1 = monkeys[curr.m1]
        m2 = monkeys[curr.m2]
        
        n1, n2 = None, None
        try: 
            n1 = m1.get_num(monkeys)
        except Exception as e:
            pass
        
        try:
            n2 = m2.get_num(monkeys)
        except Exception as e:
            pass
        
        if n1 is None and n2 is None:
            raise ValueError(f'Both children are None: {curr.name}')
        
        if n1 is None:
            n1, n2 = curr.reverse_operation(n1, n2)
            m1.num = n1
            curr = m1
            
        elif n2 is None:
            n1, n2 = curr.reverse_operation(n1, n2)
            m2.num = n2
            curr = m2
            
            
        
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
