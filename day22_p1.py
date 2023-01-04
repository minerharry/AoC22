from typing import Literal
from text import getInput
import numpy as np
from tqdm import tqdm
from functools import lru_cache
import re

lines = getInput('input3.txt')

m = {' ':-1,'.':0,'#':1}
rows = [[m[c] for c in l] for l in lines[:-2]];
mLen = max([len(r) for r in rows]);
for r in rows:
    r += [-1] * (mLen - len(r));
maze = np.array(rows);
maze = maze.transpose(); #indexed x,y 

hbounds = [];
for row in maze.transpose():
    a = np.where(row != -1)[0]
    lBound = a.min();
    rBound = a.max();
    hbounds.append((lBound,rBound,rBound-lBound+1));

vbounds = []
for row in maze:
    a = np.where(row != -1)[0];
    lBound = a.min();
    rBound = a.max();
    vbounds.append((lBound,rBound,rBound-lBound+1));

print(maze.transpose());
print(hbounds)
print(vbounds);

start = (hbounds[0][0],0)
# print(start);
# maze[start] = 2;
# print(maze);

pos = np.array(start);

directionMap = {0:np.array([1,0]),1:np.array([0,-1]),2:np.array([-1,0]),3:np.array([0,1])};
directionAxis = {0:0,2:0,1:1,3:1};
inverse = {0:1,1:0};
rotationMap = {'R':-1,'L':1};
dire = 0;

instructions = lines[-1];

bounds = [hbounds,vbounds]

def moveForward(count:int):
    global pos
    print("moving",count,"steps",directionMap[dire]);
    for _ in range(count):
        # displayMaze();
        # input();
        # print("pos:",pos);
        nextpos = pos + directionMap[dire];
        # print("shifted pos:",nextpos);
        # print("dire axis",directionAxis[dire]);
        # print("relevant bounds",bounds[directionAxis[dire]][nextpos[inverse[directionAxis[dire]]]]);
        if nextpos[directionAxis[dire]] > bounds[directionAxis[dire]][nextpos[inverse[directionAxis[dire]]]][1]: #x-bound, row y, upper bound
            nextpos[directionAxis[dire]] -= bounds[directionAxis[dire]][nextpos[inverse[directionAxis[dire]]]][2]; #x-bound, row y, width
            # print("wrapping above, newpos:",nextpos);
        elif nextpos[directionAxis[dire]] < bounds[directionAxis[dire]][nextpos[inverse[directionAxis[dire]]]][0]: #x-bound, row y, lower bound
            nextpos[directionAxis[dire]] += bounds[directionAxis[dire]][nextpos[inverse[directionAxis[dire]]]][2];
            # print("wrapping below, newpos:",nextpos);

        # print("probing shifted pos, contents:",maze[tuple(nextpos)]);
        if maze[tuple(nextpos)] == 1: #wall
            # print("wall hit, ending early");
            break;
        pos = nextpos;
        
def rotate(direct:Literal["L","R"]):
    # displayMaze();
    # print("rotating","Right" if direct == "R" else "Left");
    # input();
    global dire
    dire += rotationMap[direct];
    dire %= 4;


directionCharMap = {0:'>',1:'^',2:'<',3:'v'};
dispMaze = maze.astype('str');
dispMaze[maze == -1] = ' '
def displayMaze():
    dispMaze[tuple(pos)] = directionCharMap[dire];
    print(dispMaze.transpose());


displayMaze();
print(start);
input();

numReg = r'\d+'
while True:
    # displayMaze();
    num = re.match(numReg,instructions);
    # print(instructions);
    # print(num);
    if not num:
        break;
    if num.end() < len(instructions):
        rotation = instructions[num.end()]
        instructions = instructions[num.end()+1:];
    else:
        rotation = None;
    num = int(num.group(0))
    moveForward(num);
    if rotation is None:
        break;
    rotate(rotation);


print("final pos",pos);
print("final direction",dire);
displayMaze()
dscore = {0:0,1:3,2:2,3:1}[dire];
score = (pos[1]+1)*1000 + 4 * (pos[0]+1) + dscore;
print(score);