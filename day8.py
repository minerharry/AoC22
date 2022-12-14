from text import getInput
import numpy as np

lines = getInput();

arr = []

for l in lines:
    le =  [];
    for c in l:
        le.append(int(c));
    arr.append(le);

shape = np.array(arr).shape;

visible = 0;

def isEdge(pos:tuple[int,int]):
    i,j = pos;
    return i == 0 or i == len(arr)-1 or j == 0 or j == shape[1]-1

def checkVisible(start:tuple[int,int],direction:tuple[int,int],height):
    if (isEdge(start)):
        return 0;
    else:
        start = (start[0] + direction[0], start[1] + direction[1])
        if (arr[start[0]][start[1]] >= height):
            return 1;
        return 1 + checkVisible(start,direction,height);
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if (isEdge((i,j))):
            continue;
        else:
            score = np.prod([checkVisible((i,j),dir,arr[i][j]) for dir in [(0,1),(1,0),(-1,0),(0,-1)]]);
            if score > visible:
                visible = score;

print(visible) 





