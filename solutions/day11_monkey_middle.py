# Day 11. Monkey in the Middle
# https://adventofcode.com/2022/day/11

from util.input_util import read_input_file

class Monkey:
    def __init__(self, num:int, worry_level:int, lcm:int):
        self.n = num
        self.worry_level = worry_level
        self.lcm = lcm
        self.items = None
        self.operation = None
        self.test = None
        self.inspects = 0
        
    def add(self, item:int):
        self.items.append(item)
    
    def inspect_items(self) -> list:
        self.inspects += len(self.items)
        items = [self.operation(itm) // self.worry_level for itm in self.items]
        self.items = []
        return [(self.test(itm), itm % self.lcm) for itm in items]
    
    def build_operation(self, op):
        def func(old):
            return eval(op)
        self.operation = func
        
    def build_test(self, divisor, t, f):
        def func(x):
            if x % divisor == 0: return t
            return f
        self.test = func
    
    def __str__(self):
        return f'Monkey {self.n} - {self.inspects} - {self.items}'
        


def build_monkeys(worry_level):
    lines = read_input_file(11)
    
    # Need Least Common Multiple to keep the worry level manageable
    lcm = 1
    for l in lines:
        if 'divisible' in l:
            lcm *= int(l.split(' ')[-1])

    monkeys = []
    curr_monkey = None
    divisor = None
    t = None
    f = None
    for l in lines:
        if 'Monkey' in l: 
            # Monkey 0: -> 0
            n = l.split(' ')[1].replace(':', '')
            curr_monkey = Monkey(n, worry_level, lcm)
        elif 'Starting items:' in l:
            # Starting items: 79, 98 -> [79, 98]
            items = l.split(': ')[1].split(', ')
            curr_monkey.items = [int(x) for x in items]
        elif 'Operation:' in l:
            op = l.split('= ')[1]
            curr_monkey.build_operation(op)
        elif 'Test: ' in l:
            divisor = int(l.split('by ')[1])
        elif 'If true:' in l:
            t = int(l.split(' ')[-1])
        elif 'If false:' in l:
            f = int(l.split(' ')[-1])
        else: # newline
            curr_monkey.build_test(divisor, t, f)
            monkeys.append(curr_monkey)
        
    curr_monkey.build_test(divisor, t, f)
    monkeys.append(curr_monkey)
    return monkeys



# Mutate monkeys state
def run_round(monkeys:list) -> None:
    for m in monkeys:
        items = m.inspect_items()

        for target, itm in items:
            monkeys[target].add(itm)



def calulculate_monkey_business(monkeys:list) -> int:
    inspects = sorted([m.inspects for m in monkeys])
    return inspects[-1] * inspects[-2]
    


def solution1():
    monkeys = build_monkeys(worry_level = 3)
    
    # After inspect, but before test, worry level // 3
    # Single monkey's turn, inspect and and throws all of items it is holding
    # Count total number of times each monkey inspects items over 20 rounds
    
    for _ in range(20):
        run_round(monkeys)

    for m in monkeys:
        print(m)
    
    return calulculate_monkey_business(monkeys)



def solution2():
    monkeys = build_monkeys(worry_level = 1)
    
    for i in range(10000):
        run_round(monkeys)
        #if (i+1) % 250 == 0:
            #print(f'==== ROUND {i+1} ====')
            #for m in monkeys:
            #    print(m)

    for m in monkeys:
        print(m)
    
    return calulculate_monkey_business(monkeys)

    

    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
