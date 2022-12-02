# Day 2: Rock Paper Scissors
# https://adventofcode.com/2022/day/2


def readfile():
    with open("input/day02_input.txt") as f:
        lines = f.readlines()
    return lines



# CONSTANTS
LOST = 0
DRAW = 3
WON = 6

ROCK = 'X'
PAPER = 'Y'
SCISSOR = 'Z'

score_mapping = {ROCK: 1, PAPER: 2, SCISSOR: 3}

def convert(op):
    mapping = {'A': ROCK, 'B': PAPER, 'C': SCISSOR}
    return mapping[op]

def score(op, you):
    score = score_mapping[you]
    
    if op == you:
        score += DRAW
    
    elif op == ROCK and you == PAPER:
        score += WON
    
    elif op == SCISSOR and you == ROCK:
        score += WON
    
    elif op == PAPER and you == SCISSOR:
        score += WON
    
    return score
     


def solution1():
    
    lines = readfile()
    
    total = 0
    for l in lines:
        op, you = l.replace('\n','').split(' ')
        op = convert(op)
        s = score(op, you)
        total += s
        print(op, you, s)
        
    return total


#################################


def should_play_to_win(op):
    if op == ROCK: return PAPER
    if op == PAPER: return SCISSOR
    return ROCK
    

def should_play_to_lose(op):
    if op == ROCK: return SCISSOR
    if op == PAPER: return ROCK
    return PAPER

def should_play_to_draw(op):
    return op


strategy_mapping = {'X': should_play_to_lose, 'Y': should_play_to_draw, 'Z': should_play_to_win}

def solution2():
    
    total = 0
    
    lines = readfile()
    for l in lines:
        op, strat = l.replace('\n', '').split(' ')
        op = convert(op)
        strategy = strategy_mapping[strat]
        
        play = strategy(op)
        s = score(op, play)
        
        total += s
        
    return total
        
    
    
    




if __name__ == '__main__':
    print(solution1())
    print(solution2())