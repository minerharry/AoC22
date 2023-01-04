from functools import lru_cache
from operator import itemgetter
from typing import DefaultDict, Iterable, Literal
from text import getInput
from tqdm import tqdm
import numpy as np

lines = getInput('input3.txt');
length = 30;

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
estate = tuple[tuple[str,str],frozenset[str],tuple[int,int]] #elephant state

start:state = ('AA',goodValves,length);
tstart:tstate = ('AA',goodValves);
estart:estate = (('AA','AA'),goodValves,(length,length));


paths:dict[tuple[str,str],float] = DefaultDict(lambda:float('inf'));
# full_paths:dict[tuple[str,str],list[str]] = {};


# def getPath(end,start,prev):
#     if end == start:
#         return [start];
#     return getPath(prev[end],start,prev) + [end];

# def pathBetween(start:str,ends:list[str]):
#     all = list(valves.keys());
#     dist = DefaultDict(lambda: float('inf'));
#     dist[start] = 0;
#     prev = {};
#     all.sort(key=lambda x: dist[x]);
#     while len(all) > 0:
#         x = all.pop(0);
#         for n in neighbors[x]:
#             alt = dist[x] + 1;
#             if alt < dist[n]:
#                 dist[n] = alt;
#                 prev[n] = x;

#     path = getPath(end,start,prev);

#     return 0;

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

def egetNeighbors(pos:estate,turn:int)->Iterable[tuple[estate,int]]:
    for v in pos[1]:
        d = paths[pos[0][turn],v];
        if d+1 > pos[2][turn]:
            continue;
        # if d != int(d):
        #     raise Exception("invalid distance",d,"between",pos,"and",v,"")
        d = int(d);
        newt = pos[2][turn]-d-1;
        order = 1 if turn == 1 else -1;
        outv = tuple((v,pos[0][turn])[::-1])
        outt = tuple((newt,pos[2][turn])[::-1])

        yield ((outv,pos[1].difference((v,)),outt),valves[v]*newt);    


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

@lru_cache
def esearch(node:estate):
    if node[2][0] == 0 and node[2][1] == 0:
        return [0];
    turn:int = np.argmax(node[2]);
    # print(turn,node);
    neighs = list(egetNeighbors(node,turn));
    if len(neighs) == 0: #turn's stuff is dead
        newt = (0,node[2][1]) if turn == 0 else (node[2][0],0);
        return esearch((node[0],node[1],newt));
    result = []
    for n,p in neighs:
        best = max(esearch(n));
        result.append(best + p);
    return result;

    


    
# print(max(search(start)))
print(max(esearch(estart)));








