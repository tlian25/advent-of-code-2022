# Day 16. Proboscidea Volcanium
# https://adventofcode.com/2022/day/16

from collections import deque
from util.input_util import read_input_file

START = 'AA'
TIME = 30 # 30 minutes

class Valve:
    def __init__(self, name:str, rate:int):
        self.name = name
        self.rate = rate
        self.next = set()
        
    def __str__(self):
        return f'{self.name} - {self.rate} - {self.next}'

def parse_lines():
    lines = read_input_file(16)
    valves = {}
    for l in lines:
        s = l.split(' ')
        name = s[1]
        rate = int(s[4].replace('rate=', '').replace(';', ''))
        v = Valve(name, rate)
        for i in range(9, len(s)):
            v.next.add(s[i].replace(',', ''))
        valves[name] = v
    return valves
        

# 1 minute to open a single valve
# 1 minute to follow any tunnel
# Need to find the next best move in terms of pressure * time left
# Build distance matrix

def build_distance_matrix(valves):
    dist = {}
    # BFS from each valve
    def bfs(start):
        q = deque([(start, 0)])
        while q:
            curr, d = q.popleft()
            if (start, curr) not in dist or d < dist[(start, curr)]:
                dist[(start, curr)] = d
                for next in valves[curr].next:
                    q.append((next, d+1))
    
    for v in valves:
        bfs(v)

    return dist
                


def solution1():
    valves = parse_lines()
    dist = build_distance_matrix(valves)
    q = deque([(START, 30, 0, set())])
    
    highest = 0
    while q:
        curr, m, p, seen = q.popleft()
        highest = max(highest, p)
        for v in valves:
            if v not in seen:
                t = dist[(curr, v)] + 1
                if t <= m and valves[v].rate > 0:
                    r = valves[v].rate * (m-t)
                    s = seen.copy()
                    s.add(v)
                    q.append((v, m-t, p+r, s))

    return highest

        
    
    
def solution2():
    valves = parse_lines()
    dist = build_distance_matrix(valves)
    
    highest = 0
    opened = None
    
    # You
    q = deque([(START, 26, 0, set())])
    while q:
        curr, m, p, seen = q.popleft()
        if p > highest:
            opened = seen
            highest = p

        for v in valves:
            if v not in seen:
                t = dist[(curr, v)] + 1
                if t <= m and valves[v].rate > 0:
                    r = valves[v].rate * (m-t)
                    s = seen.copy()
                    s.add(v)
                    q.append((v, m-t, p+r, s))

    # Elephant helper
    q = deque([(START, 26, highest, opened)])
    while q:
        curr, m, p, seen = q.popleft()
        if p > highest:
            opened = seen
            highest = p
        
        for v in valves:
            if v not in seen:
                t = dist[(curr, v)] + 1
                if t <= m and valves[v].rate > 0:
                    r = valves[v].rate * (m-t)
                    s = seen.copy()
                    s.add(v)
                    q.append((v, m-t, p+r, s))

    return highest
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
