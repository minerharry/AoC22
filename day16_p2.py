from functools import lru_cache
from operator import itemgetter
from typing import DefaultDict, Iterable
from text import getInput
from tqdm import tqdm
import numpy as np

lines = getInput('input2.txt');
length = 10;

valves = {};
neighbors = {};
goodValves = []

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
for l in lines:
    v = l.split(" ")[1];
    rate = int(l.split("=")[1].split(";")[0]);
    ns = l.split("valves ")[1].split(", ") if "valves" in l else [l.split("valve ")[1]];
    neighbors[v] = ns;
    valves[v] = rate;
    if rate != 0:
        goodValves.append(v);

goodValves = frozenset(goodValves)

print(valves);
print(neighbors);

state = tuple[str,frozenset[str],int] #position, remaining valves, remaining steps
tstate = tuple[str,frozenset[str]]

start:state = ('AA',goodValves,length);
tstart:tstate = ('AA',goodValves);


paths:dict[tuple[str,str],float] = DefaultDict(lambda:float('inf'));


vs = valves.keys();

for v in vs:
    paths[v,v] = 0;
    for k in neighbors[v]:
        paths[k,v] = 1;
    
for k in vs:
    for i in vs:
        for j in vs:
            if paths[i,j] > paths[i,k] + paths[k,j]:
                paths[i,j] = paths[i,k] + paths[k,j];


# print(paths);
# print(paths['AA','BB'])
# print(paths['AA','CC'])
# print(paths['AA','DD']);
# print(paths['AA','JJ']);


def getNeighbors(pos:state)->Iterable[tuple[state,int]]:
    for v in pos[1]:
        d = paths[pos[0],v];
        if d+1 > pos[2]:
            continue;
        if d != int(d):
            raise Exception("invalid distance",d,"between",pos,"and",v,"")
        d = int(d);
        newt = pos[2]-d-1;
        yield ((v,pos[1].difference((v,)),newt),valves[v]*newt);
    


    # if pos[2] == 0:# or not any(pos[1]):
    #     # print("end reached:",pos);
    #     return
    # if pos[0] in pos[1]:
    #     # print("activating valve")
    #     yield ((pos[0],pos[1].difference((pos)),pos[2]-1),valves[pos[0]]*(pos[2]-1));
    # for v in neighbors[pos[0]]:
    #     yield ((v,pos[1],pos[2]-1),0);

def tgetNeighbors(pos:tstate)->Iterable[tuple[tstate,int]]:
    # if not any(pos[1]):
    #     return
    if pos[0] in pos[1]:
        yield ((pos[0],pos[1].difference((pos))),valves[pos[0]]);
    for v in neighbors[pos[0]]:
        yield ((v,pos[1]),0);
        

@lru_cache
def path_search(node:state,pr=False):
    neighs = list(getNeighbors(node));
    if len(neighs) == 0:
        return [([node],0)];
    result = [];
    for n,p in neighs:
        best = max(path_search(n),key=itemgetter(1));
        result.append(([node] + best[0],p+best[1]));
    return result

@lru_cache
def path_tsearch(node:tstate,remaining=length):
    neighs = list(tgetNeighbors(node));
    if remaining == 0 or not any(neighs):
        return [([node],0)];
    result = [];
    for n,p in neighs:
        best = max(path_tsearch(n,remaining-1),key=itemgetter(1));
        result.append(([node] + best[0],p*(remaining-1)+best[1]));
    return result;

@lru_cache
def search(node:state,pr=False):
    neighs = list(getNeighbors(node));
    if len(neighs) == 0:
        return [0];
    result = [];
    for n,p in neighs:
        best = max(search(n));
        # print("best successor of",node,"is",best);
        result.append(p+best);
    return result

@lru_cache
def tsearch(node:tstate,remaining=length):
    neighs = list(tgetNeighbors(node));
    if remaining == 0 or not any(neighs):
        return [0];
    result = [];
    for n,p in neighs:
        best = max(tsearch(n,remaining-1));
        result.append(p*(remaining-1)+best);
    return result;

# while any(openSet):
#     curr = open.pop();
#     openSet.remove(curr);
#     for n,p in getNeighbors(curr):
#         print(curr,fscore[curr],n,p);


#         f = fscore[curr] + p;
#         if n not in openSet:
#             print("new n found adding to open")
#             openSet.add(n);
#             open.append(n);
#         elif f > fscore[n]:
#             print("new n found adding to open")
#             openSet.add(n);
#             open.append(n);
#         if f > fscore[n]:
#             print("score",f,"better than existing score",fscore[n]);
#             fscore[n] = f
#             prev[n] = curr,p;
#     open.sort(key=sortKey);
#     closedSet.add(curr);
#     if curr[2] == 0:
#         endSet.add(curr);
#     elif not(any(curr[1])):
#         end = (curr[0],curr[1],-1);
#         endSet.add(end);
#         prev[end] = curr,0;


# def getPath(end:state)->tuple[list[tuple[str,int]],int]:
#     if end == start:
#         return [(start[0],0)],0;
    
#     n,c = prev[end];
#     p,a = getPath(n);
#     return p + [(end[0],c)],c+a;


def elephantSearch(elephantValves:frozenset):
    myValves = goodValves.difference(elephantValves);

    myScore = max(search(('AA',myValves,length-4)));
    eScore = max(search(('AA',elephantValves,length-4)));
    # print(eScore);
    return myScore + eScore;

    
def chooseElephant(choices:list[str],acc:list[str]=[],bar:tqdm|None=None):
    if len(choices) == 0:
        return elephantSearch(frozenset(acc));
    else:
        if bar is not None:
            bar.update(1);
        n = choices[1:];
        return max(chooseElephant(n,acc+[choices[0]],bar),chooseElephant(n,acc,bar));





# print(max(search(start)))
with tqdm(total=2**len(goodValves)) as bar:
    print(chooseElephant(list(goodValves),bar=bar));








