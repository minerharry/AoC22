from typing import DefaultDict
from text import getInput
from functools import lru_cache

lines = getInput('input.txt');

blocks = set([eval(l) for l in lines]);

connections = 0;
# airCounts = DefaultDict(lambda: 0)

@lru_cache
def getNeighbors(b:tuple[int,int,int]):
    for o in [-1,1]:
        yield (b[0],b[1],b[2]+o);
        yield (b[0],b[1]+o,b[2]);
        yield (b[0]+o,b[1],b[2]);


min_bounds = list(next(iter(blocks)));
max_bounds = min_bounds.copy();


# p1
for b in blocks:
    exec("max_bounds = [max(max_bounds[i],b[i]) for i in range(3)]")
    exec("max_bounds = [max(max_bounds[i],b[i]) for i in range(3)]".replace("max","min"))

    for n in getNeighbors(b):
        if n in blocks:
            connections += 1
print(len(blocks)*6-connections); #p1

min_bounds = tuple([b - 2 for b in min_bounds]);
max_bounds = tuple([b + 2 for b in max_bounds]);

def in_bounds(p:tuple[int,int,int]):
    for i in range(3):
        if p[i] < min_bounds[i] or p[i] > max_bounds[i]:
            return False;
    return True;

#p2
surfaces = 0;
filled = set();
open = set([min_bounds]);
while len(open) > 0:
    pos = open.pop();
    filled.add(pos);
    for n in getNeighbors(pos):
        if in_bounds(n):
            if n not in blocks:
                if n not in filled:
                    open.add(n);
            else:
                surfaces += 1;


print(surfaces);




# airgaps = [(b,c) for (b,c) in airCounts.items() if c == 6]
# print(airgaps);
# print(len(blocks)*6-connections-6*len(airgaps)) #p2


