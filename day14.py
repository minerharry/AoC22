from text import getInput
import numpy as np

lines = getInput();


paths = [];



maxY = -1;

for l in lines:
    path = [];
    for p in l.split(" -> "):
        x,y = eval(p);
        print(x,y);
        maxY = max(y,maxY);
        path.append((x,y));
    paths.append(path);

print(paths);

rocks = set();
for path in paths:
    start = path[0];
    rocks.add(start);
    for p in path[1:]:
        offset = [];
        if start[0] - p[0] == 0:
            if start[1] - p[1] > 0:
                offset = [0,-1];
            else:
                offset = [0,1];
        else:
            if start[0] - p[0] > 0:
                offset = [-1,0];
            else:
                offset = [1,0];
        # print("offset between",start,"and",p,":",offset)
        while start != p:
            # print(start)
            start = (start[0] + offset[0], start[1] + offset[1]);
            rocks.add(start);

print(rocks);
print(maxY);
# raise Exception();
# rocks = set();
sStart = (500,0);
acc = 0;
while True:
    sand = sStart;
    while True:
        # print("blah")
        blocked = False;
        for nextSand in [(sand[0],sand[1]+1),(sand[0]-1,sand[1]+1),(sand[0]+1,sand[1]+1)]:
            if (nextSand not in rocks and nextSand[1] < maxY+2):
                sand = nextSand;
                # print(sand);
                blocked=True;
                break;
        if blocked:
            continue;
        rocks.add(sand);
        # print("sand",acc,"stopped at position",sand);
        break;
    if sand == sStart:
        break;
    else:
        acc += 1;

print(acc); 






    
