from typing import Literal
from text import getInput
import numpy as np
from tqdm import tqdm
from functools import lru_cache
import re

from utils import rotatePos, splitlist

lines = getInput('input2.txt');
t = splitlist(lines,'');
mazeRows,instructions,mSize,mMap,connections,start,face = t
print([[len(s) for s in l] for l in t])

m = {' ':-1,'.':0,'#':1}
rows = [[m[c] for c in l] for l in mazeRows];
mLen = max([len(r) for r in rows]);
for r in rows:
    r += [-1] * (mLen - len(r));
maze = np.array(rows);
maze = maze.transpose();

faceSize = int(mSize[0])

# print(mMap);
# print(instructions);
faceMap = np.array([[int(c) for c in l] for l in mMap]).transpose();
faces = {};
faceOffsets = {};
for i in range(6):
    coord = np.where(faceMap == i+1);
    print(coord);
    coord = (coord[0][0]*faceSize,coord[1][0]*faceSize)
    faceOffsets[i+1] = np.array(coord);
    faces[i+1] = maze[coord[0]:coord[0] + faceSize,coord[1]:coord[1] + faceSize];




edgeRotMap = {'d':3,'u':1,'l':2,'r':0};
edgeMap = {}

for connection in connections:
    c1,c2 = [(int(c[0]),edgeRotMap[c[1]]) for c in connection.split('<->')];
    edgeMap[c1] = c2;
    edgeMap[c2] = c1;

# print(edgeMap);
# input();


directionMap = {0:np.array([1,0]),1:np.array([0,-1]),2:np.array([-1,0]),3:np.array([0,1])};
directionAxis = {0:0,2:0,1:1,3:1};
inverse = {0:1,1:0};
rotationMap = {'R':-1,'L':1};
dire = 0;

start = eval(start[0]);
face = int(face[0])
pos = np.array(start) % faceSize;

def moveForward(count:int):
    global pos
    global dire
    global face
    print("moving",count,"steps",directionMap[dire]);
    for _ in range(count):
        # displayMaze();
        # input();
        nextpos = pos + directionMap[dire];
        if any(nextpos >= faceSize) or any(nextpos < 0):
            # print("changing faces!");
            nextpos = nextpos % faceSize;
            nextFace,edge = edgeMap[(face,dire)];
            # print("next face:",nextFace,"next edge:",edge);
            newDire:int = (edge + 2) % 4;
            nextpos = rotatePos(nextpos,newDire-dire,faceSize);
            if faces[nextFace][tuple(nextpos)] == 1:
                #hit a wall
                break;
            dire = newDire;
            pos = nextpos;
            face = nextFace
        else:
            if faces[face][tuple(nextpos)] == 1:
                #hit a wall
                break;
            pos = nextpos

            
        
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
# print(face);
# print(faceOffsets);
def displayMaze():
    absPos = pos + faceOffsets[face];
    dispMaze[tuple(absPos)] = directionCharMap[dire];
    print(dispMaze.transpose());


displayMaze();
print(start);
input();

instructions = instructions[0];

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


absPos = pos + faceOffsets[face];
print("final abolute pos",absPos);
print("final relative pos",pos);
print("final face",face)
print("final direction",dire);
displayMaze()
dscore = {0:0,1:3,2:2,3:1}[dire];
score = (absPos[1]+1)*1000 + 4 * (absPos[0]+1) + dscore;
print(score);