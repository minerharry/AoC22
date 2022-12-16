from typing import Literal
from text import getInput
import numpy as np
from tqdm import tqdm

lines = getInput();

acc = 0;

sensedBeacons = {}

def mDist(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1]);

for l in lines:
    s,b = l.split("at")[1:];
    out = [];
    for t in [s,b]:
        x = int(t.split("x=")[1].split(",")[0]);
        y = int(t.split("y=")[1].split(":")[0]);
        out.append((x,y));
    sensedBeacons[out[0]] = out[1];

# print(sensedBeacons);

# rT = 10;
# rT = 2000000
# tLimit = 20;
tLimit = 4000000;
for rT in tqdm(range(tLimit)):
    edges:list[tuple[int,Literal['R']|Literal["L"]]] = [];
    dEdges = list[tuple[int,int]]
    for s,b in sensedBeacons.items():
        ran = mDist(s,b);
        off = abs(s[1]-rT);
        if off <= ran: #sensor's limit in range
            off = ran-off
            # if s[0]-off == -8:
            #     print(s,b);
            #     print(off)
            edges.append((s[0]-off,"L"));
            edges.append((s[0]+off,"R"));




    total = 0;
    edges.sort(key=lambda x: x[0] + (0.5 if x[1] == "R" else 0))
    # print(edges);
    open = -1;
    stack = 0;
    for pos,side in edges:
        if side == "L":
            if stack == 0:
                if open < 0 and pos > 0  and rT >= 0 and rT < tLimit:
                    print("left boundary surpassed (x is 0),previous open:",open)
                    print(pos,rT);
                    print(edges)
                elif open < tLimit and pos > tLimit  and rT >= 0 and rT < tLimit:
                    print("right boundary surpassed (x is tLimit)");
                    print(pos,rT);
                elif pos - open > 1 and rT >= 0 and rT < tLimit:
                    print(pos);
                    print(pos-1,rT);
                    print(edges);
                open = pos;
            stack += 1;
        if side == "R":
            stack -= 1;
            if stack == 0:
                total += pos - open;
                open = pos;

    # print(total);


        






