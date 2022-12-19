# Day 19. Not Enough Minerals
# https://adventofcode.com/2022/day/19

from collections import deque
from copy import deepcopy
from util.input_util import read_input_file

ORE = 'ore'
CLAY = 'clay'
OBS = 'obsidian'
GEO = 'geode'
NOOP = 'noop'

class Blueprint:
    def __init__(self, num:int):
        self.num = num
        self.ore = None
        self.clay = None
        self.obs = None
        self.geo = None
        self.maxspend = {v:0 for v in [ORE, CLAY, OBS]}
        
    def build(self, rtype, robots, rocks):
        if rtype == ORE:
            return self.build_ore(robots, rocks)
        elif rtype == CLAY:
            return self.build_clay(robots, rocks)
        elif rtype == OBS:
            return self.build_obs(robots, rocks)
        elif rtype == GEO:
            return self.build_geo(robots, rocks)
        
    def build_ore(self, robots, rocks):
        if rocks[3] < self.ore[ORE]:
            return NOOP
        newrocks = (rocks[0], rocks[1], rocks[2], rocks[3]-self.ore[ORE])
        newrobots = (0, 0, 0, 1) 
        return newrobots, newrocks
    
    def build_clay(self, robots, rocks):
        if rocks[3] < self.clay[ORE]:
            return ORE # Need ore
        newrocks = (rocks[0], rocks[1], rocks[2], rocks[3]-self.clay[ORE])
        newrobots = (0, 0, 1, 0)
        return newrobots, newrocks
    
    def build_obs(self, robots, rocks):
        if rocks[2] < self.obs[CLAY]:
            return CLAY # Need clay
        if rocks[3] < self.obs[ORE]:
            return ORE # Need ore
        newrocks = (rocks[0], rocks[1], rocks[2]-self.obs[CLAY], rocks[3]-self.obs[ORE])
        newrobots = (0, 1, 0, 0)
        return newrobots, newrocks
    
    def build_geo(self, robots, rocks):
        if rocks[1] < self.geo[OBS]:
            return OBS # Need obs
        if rocks[3] < self.geo[ORE]:
            return ORE # Need ore
        newrocks = (rocks[0], rocks[1]-self.geo[OBS], rocks[2], rocks[3]-self.geo[ORE])
        newrobots = (1, 0, 0, 0)
        return newrobots, newrocks

    def __str__(self):
        s = f'Blueprint [{self.num}]\n'
        s += f'Ore: {self.ore}\n'
        s += f'Clay: {self.clay}\n'
        s += f'Obs: {self.obs}\n'
        s += f'Geo: {self.geo}\n'
        return s
        

def parse_lines():
    blueprints = []
    lines = read_input_file(19)
    for l in lines:    
        # blueprint num
        s = l.split(' ')
        num = int(s[1].replace(':', ''))
        bp = Blueprint(num)
        # robots
        bp.ore = {ORE: int(s[6]), CLAY: 0, OBS: 0} 
        bp.clay = {ORE: int(s[12]), CLAY: 0, OBS: 0}
        bp.obs = {ORE: int(s[18]), CLAY: int(s[21]), OBS: 0}
        bp.geo = {ORE: int(s[27]), CLAY: 0, OBS: int(s[30])}
        bp.maxspend[GEO] = 10000000
        for rtype in [ORE, CLAY, OBS]:
            bp.maxspend[rtype] = max(bp.ore[rtype], bp.clay[rtype], bp.obs[rtype], bp.geo[rtype])
        blueprints.append(bp)
    return blueprints
    

# One ore robot
# 1 resource type per minute

def bfs(blueprint, T):
    # State = time + robot counts + ore counts
    q = deque( [(T, (0, 0, 0, 1), (0, 0, 0, 0))] )
    maxspend = tuple(blueprint.maxspend[v] for v in [GEO, OBS, CLAY, ORE])
    maxtimerobots = {x:0 for x in range(T+1)}
    maxgeos = 0
    seen = set()
    while q:
        print(f'{len(q)}\r', end = '')
        s = q.popleft()
        if s in seen:
            continue
        seen.add(s)
        
        t, robots, rocks = s
        if maxtimerobots[t] > robots[0]:
            maxgeos = max(maxgeos, robots[0] + rocks[0])
            continue
    
        maxtimerobots[t] = robots[0]
        if t == 1:
            maxgeos = max(maxgeos, robots[0] + rocks[0])
            continue
        
        # Try to build any robot type
        ROBOT_TYPES = [GEO, OBS, CLAY, ORE]
        for i in range(4):
            rtype = ROBOT_TYPES[i]
            # More than enough current robots producing that rock
            if maxspend[i] <= robots[i]:
                continue
            # Build robot first
            result = blueprint.build(rtype, robots, rocks)
            if result in (ORE, OBS, CLAY, NOOP):
                newrocks = deepcopy(rocks)
                newrobots = (0, 0, 0, 0)
            else:
                newrobots, newrocks = result
                
            # Harvest any rocks with existing robots adjust for maxspend to reduce on seens
            newrocks = tuple(min(maxspend[i] * (t-1), newrocks[i] + robots[i]) for i in range(4))
            # Then add new robots to count
            newrobots = tuple(newrobots[i] + robots[i] for i in range(4))
            nextstate = (t-1, newrobots, newrocks)
            if nextstate not in seen:
                q.append(nextstate)
                
    return maxgeos



def solution1():
    blueprints = parse_lines()
    
    quality = 0
    for i in range(len(blueprints)):
    #for i in [22]:
        bp = blueprints[i]
        print(bp)
        print()
        mxgeo = bfs(bp, 24)
        print()
        print(i+1, mxgeo)
        print()
        quality += (i+1) * mxgeo
        
    return quality



def solution2():
    blueprints = parse_lines()
    
    quality = 1
    for i in range(3):
        bp = blueprints[i]
        print(bp)
        mxgeo = bfs(bp, 32)
        print()
        print(i, mxgeo)
        print()
        quality *= mxgeo
        
    return quality
    
    
    
if __name__ == '__main__':
    #print(solution1())
    
    print('--------------')
    
    print(solution2())
