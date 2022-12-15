# Day 15: Beacon Exclusion Zone 
# https://adventofcode.com/2022/day/15

from util.input_util import read_input_file


def parse_xy(xy):
    # x=1, y=2
    x, y = xy.split(', ')
    return int(x.split('=')[-1]), int(y.split('=')[-1])
    
    

def parse_lines():
    lines = read_input_file(15)
    sensors = {} # for each sensor, track closest beacon
    # Also find boundaries
    minX, maxX = float('inf'), float('-inf')
    minY, maxY = float('inf'), float('-inf')
    for l in lines:
        sensor, beacon = l.split(': ')
        xy = sensor.replace('Sensor at ', '')
        x, y = parse_xy(xy)
        
        ab = beacon.replace('closest beacon is at ', '')
        a, b = parse_xy(ab)
        
        d =  distance((x,y), (a,b))
        sensors[(x, y)] = (a, b, d)
        
        # Update boundaries
        minX = min(minX, x-d, a)
        maxX = max(maxX, x+7, a)
        
        minY = min(minY, y-d, b)
        maxY = max(maxY, y+d, b)
                
    return sensors, minX, maxX, minY, maxY
    


# Manhattan distance
def distance(loc1:tuple, loc2:tuple):
    return abs(loc1[0]-loc2[0]) + abs(loc1[1]-loc2[1])

def solution1():
    sensors, minX, maxX, minY, maxY = parse_lines()
    #print("Boundaries:", minX, maxX, minY, maxY)
    
    seen = set()
    for (a, b), (x, y, d) in sensors.items():
        seen.add((x, y))
        seen.add((a, b))
    
    # Start looking in row y = 2_000_000
    Y = 2_000_000
    count = 0
    for (a, b), (x, y, d) in sensors.items():
        #print(a, b, x, y, d)
        # calculate distance from sensor straight to Y
        dy = abs(b-Y)
        if dy > d:
            continue
        # Slack to move in x direction
        dx = d - dy
        for diff in range(dx+1):
            for x in (a-diff, a+diff):
                if (x, Y) not in seen:
                    count += 1
                    seen.add((x, Y))
                    
    return count


def tuning_freq(x, y):
    return x * 4_000_000 + y


def solution2():
    sensors, minX, maxX, minY, maxY = parse_lines()

    LOW = 0
    HIGH = 4_000_000
    
    seen = set()
    for (a, b), (x, y, d) in sensors.items():
        seen.add((x, y))
        seen.add((a, b))
    '''
    for (a, b), (x, y, d) in sensors.items():
        #print(a, b, x, y, d)
        # calculate distance from sensor straight to Y
        print(a,b)
        for X in range(a-d, a+d+1):
            for Y in range(b-d, b+d+1):
                if (X, Y) not in seen and distance((a, b), (X, Y)) <= d:
                    seen.add((X, Y))
    '''
    
    diagonals = set()
    # Search along diagonals for each sensor
    for (a, b), (x, y, D) in sensors.items():
        print(a,b)
        for d in range(D+2):
            dx = d
            dy = D+1-d
            if a+dx <= HIGH and b+dy <= HIGH:
                diagonals.add((a+dx, b+dy))
            if a+dx <= HIGH and b-dy >= LOW:
                diagonals.add((a+dx, b-dy))
            if a-dx >= LOW and b+dy <= HIGH:
                diagonals.add((a-dx, b+dy))
            if a-dx >= LOW and b-dy >= HIGH:
                diagonals.add((a-dx, b-dy))
    
    
    # Search each diagonal candidate to be the spot for beacon
    # This is super ugly....
    L = len(diagonals)
    i = 1
    for xd, yd in diagonals:
        print(f'{i} of {L} - [{i/L * 100}] with {xd}, {yd}')
        FOUND = True
        for (a, b), (x, y, D) in sensors.items():
            if distance((a,b), (xd,yd)) <= D:
                FOUND = False
                break
        
        if FOUND:
            print(xd, yd)
            return tuning_freq(xd, yd)
        
        i += 1

    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
