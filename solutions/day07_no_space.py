# Day 7. No Space Left on Device 
# https://adventofcode.com/2022/day/7

from util.input_util import read_input_file

class Dir:
    def __init__(self, name:str):
        self.name = name
        self.parent = None
        self.size = 0
        self.files = dict() # Name: size (int)
        self.subdirs = dict() # Name: Dir
        
    def __repr__(self):
        return self.name

# Build filesystem
# Traverse DFS for sizes    

def build_file_system() -> Dir:
    
    lines = read_input_file(7)
    root = Dir(name='/')
    curr = root
    
    for l in lines:
        s = l.split(' ')
        if s[0] == '$':
            # Change directory to root
            if s[1] == 'cd' and s[2] == '/':
                curr = root
            
            # Change directory to parent
            elif s[1] == 'cd' and s[2] == '..':
                curr = curr.parent
                
            # Change directory to subdir
            elif s[1] == 'cd':
                #If subdir doesn't exist, first create
                if s[2] not in curr.subdirs:
                    curr.subdirs[s[2]] = Dir(s[2])
                    curr.subdirs[s[2]].parent = curr
                curr = curr.subdirs[s[2]]
                
            # List directory - No op
            elif s[1] == 'ls':
                continue
            else:
                raise(f"Unknown command: {s}")
        
        # ls directory contents - filename, size
        else:
            if s[0] == 'dir':
                curr.subdirs[s[1]] = Dir(s[1])
                curr.subdirs[s[1]].parent = curr
            else:
                curr.files[s[1]] = int(s[0])
                       
    return root


def dfs_print(root:Dir) -> None:
    
    SPACER = '  '
    stack = [(root, 0)]
    
    while stack:
        curr, level = stack.pop()
        
        print(SPACER * level, curr.name, '(dir)')
        
        for file, size in curr.files.items():
            print(SPACER * (level+1), '-', file, size)
        
        # Add subdirs to stack
        for name, dir in curr.subdirs.items():
            stack.append((dir, level+1))


def dfs_sizes(root:Dir) -> list:
    dir_sizes = []
    stack = [root]
    while stack:
        curr = stack[-1]
        
        # Put all subdirs on stack. Clear out subdirs dict.
        if curr.subdirs:
            while curr.subdirs:
                name, subdir = curr.subdirs.popitem()
                stack.append(subdir)

        # This is the lowest level. 
        else:
            # Sum file sizes
            for file, size in curr.files.items():
                curr.size += size
                
            dir_sizes.append((curr.size, curr.name))
                
            # Add to parent
            if curr.parent:
                curr.parent.size += curr.size
            # Remove from stack
            stack.pop()
    
    #print(small_dirs)
    return dir_sizes
            
    
    

def solution1() -> int:
    
    root = build_file_system()
    #dfs_print(root)
    dir_sizes = dfs_sizes(root)
    
    SIZE_THRESHOLD = 100000
    
    total_size = 0
    for size, dir in dir_sizes:
        if size <= SIZE_THRESHOLD:
            total_size += size
            
    return total_size



    
    
def solution2():
    
    root = build_file_system()
    dir_sizes = dfs_sizes(root)
    dir_sizes.sort()
    
    TOTAL_SPACE = 70000000
    UNUSED_SPACE = 30000000
    SPACED_NEEDED = dir_sizes[-1][0] - (TOTAL_SPACE - UNUSED_SPACE)
    #print(TOTAL_SPACE, UNUSED_SPACE, SPACED_NEEDED)

    # binary search
    l, r = 0, len(dir_sizes)
    while l < r:
        m = (l + r) // 2
        if dir_sizes[m][0] < SPACED_NEEDED:
            l = m + 1
        else:
            r = m
    
    #print(dir_sizes[l-1:l+2])
    return dir_sizes[l][0]
            

    
    
if __name__ == '__main__':
    print(solution1())
    
    print('--------------')
    
    print(solution2())
