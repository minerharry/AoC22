from typing import DefaultDict
from text import getInput
import numpy as np
from tqdm import tqdm
from functools import lru_cache

lines = getInput();

elves:set[tuple[int,int]] = set();

#north is -y, south is +y, east is +x, west is -x
neighbors = [[0,-1],[-1,-1],[1,-1],[0,1],[-1,1],[1,1],[1,0],[-1,0]];
n_neigh = [0,1,2];
s_neigh = [3,4,5];
w_neigh = [7,1,4];
e_neigh = [6,2,5];
dirMap = {0:"North",3:"South",7:"West",6:"East"};
checks = [n_neigh,s_neigh,w_neigh,e_neigh];
# checkMap = DefaultDict(lambda: checks.copy());


def tickElves(elves:set[tuple[int,int]]):
    global checks
    propositions = {};
    # newChecks = {};
    for e in sorted(elves):
        ns = [(e[0]+n[0],e[1]+n[1]) for n in neighbors];
        nRes = [n not in elves for n in ns]
        if all(nRes):
            # print("skipping elf",e);
            propositions[e] = e;
            # newChecks[e] = checkMap[e];
            continue;
        # print("check order for elf",e,"is",[dirMap[check[0]] for check in checks]);
        for check in checks:
            if all(nRes[c] for c in check):
                direction = ns[check[0]];
                # print("moving",dirMap[check[0]],"from",e,"to",direction);
                propositions[e] = direction;
                # newChecks[e] = checkMap[e][1:] + [checkMap[e][0]];
                break;
        if e not in propositions:
            # print("no available moves for elf",e)
            propositions[e] = e;
            # newChecks[e] = checkMap[e];
    
    newElves = set();
    vList = list(propositions.values());
    for e,p in propositions.items():
        if vList.count(p) > 1:
            newPos = e
            # print("duplicate detected:",p);
        else:
            newPos = p;
        newElves.add(newPos);
        # checkMap[newPos] = newChecks[e];
    checks = checks[1:] + [checks[0]];
    return newElves;

for y,row in enumerate(lines):
    for x,c in enumerate(row):
        if c == "#":
            elves.add((x,y));

print(elves);

shape = (len(lines),len(lines[0]))


def displayElves(bounds:list[int]|None=None):
    out = "";
    if bounds:
        xrange = range(bounds[1],bounds[0]+1);
        yrange = range(bounds[3],bounds[2]+1);
    else:
        yrange = range(shape[0]);
        xrange = range(shape[1]);
    for y in yrange:
        for x in xrange:
            out += "#" if (x,y) in elves else ".";
        out += '\n';
    print(out);
    # print(sorted(elves));
    if not bounds:
        writeSample(out);

outFile = "small_sample_out.txt";
with open(outFile,'w') as f: pass; #create, clear contents

def writeSample(t):
    with open(outFile,"a") as f:
        f.write(f"{t}\n");

def do_p1():
    global elves
    displayElves();
    for i in range(10):
        input();
        newElves = tickElves(elves);
        if newElves == elves:
            break;
        elves = newElves
        displayElves();

    elfBounds = [max(e[0] for e in elves),min(e[0] for e in elves),max(e[1] for e in elves),min(e[1] for e in elves)];
    area = (elfBounds[0]-elfBounds[1]+1)*(elfBounds[2]-elfBounds[3]+1);
    print("side lengths:",elfBounds[0]-elfBounds[1]+1,"by",elfBounds[2]-elfBounds[3]+1)
    print("full area:",area);
    area -= len(elves);
    print("empty area:",area);
    print("elf bounds:",elfBounds);
    displayElves(bounds=elfBounds);

def do_p2():
    global elves
    displayElves();
    i = 0;
    with tqdm() as bar:
        while True:
            bar.update(1);
            # input();
            newElves = tickElves(elves);
            if newElves == elves:
                break;
            elves = newElves
            # displayElves();
            i += 1;

    elfBounds = [max(e[0] for e in elves),min(e[0] for e in elves),max(e[1] for e in elves),min(e[1] for e in elves)];
    area = (elfBounds[0]-elfBounds[1]+1)*(elfBounds[2]-elfBounds[3]+1);
    print("side lengths:",elfBounds[0]-elfBounds[1]+1,"by",elfBounds[2]-elfBounds[3]+1)
    print("full area:",area);
    area -= len(elves);
    print("empty area:",area);
    print("elf bounds:",elfBounds);
    displayElves(bounds=elfBounds);
    print(i);

if __name__ == "__main__":
    do_p2();