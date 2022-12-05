# Day 5. Supply Stacks
# https://adventofcode.com/2022/day/5

from util.input_util import read_input_file


def find_break_index(lines:list) -> int:
    # Find line break
    idx = 0
    for l in lines:
        if l == '':
            break        
        idx += 1

    print("Break index:", idx)
    return idx


def parse_move(l:str) -> tuple:
    s = l.split(' ')
    return (int(s[1]), int(s[3]), int(s[5]))
    

def create_board(lines) -> list:
    
    board = [[] for _ in range(9)]
    
    idx = find_break_index(lines)
    
    row_indexes = []
    for i in range(len(lines[idx-1])):
        if lines[idx-1][i] != ' ':
            row_indexes.append(i)
            
    print(row_indexes)
    
    for c in range(idx-2, -1, -1):
        for i in range(len(row_indexes)):
            r = row_indexes[i]
            letter = lines[c][r]
            if letter != ' ':
                board[i].append(letter)
    
    return board



def solution1() -> str:
    
    lines = read_input_file(5)
    board = create_board(lines)
    
    idx = find_break_index(lines)
    for l in lines[idx+1:]:
        n, src, dst = parse_move(l)
                
        for _ in range(n):
            board[dst-1].append(board[src-1].pop())
            
    solution = ""
    for b in board:
        print(b)
        solution += b[-1]
        
    return solution
        
        
    
    
    
    
def solution2() -> str:
    lines = read_input_file(5)
    board = create_board(lines)
    
    idx = find_break_index(lines)
    for l in lines[idx+1:]:
        n, src, dst = parse_move(l)

        move = board[src-1][-n:]
        board[dst-1] += move
        board[src-1] = board[src-1][:-n]
        
    solution = ""
    for b in board:
        print(b)
        solution += b[-1]
        
    return solution
    
    
    
if __name__ == '__main__':
    print(solution1())
    
    print('-----------')

    print(solution2())