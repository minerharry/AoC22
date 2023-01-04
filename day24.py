from typing import DefaultDict
from text import getInput
import numpy as np
from numpy import typing as npt
from tqdm import tqdm
from functools import lru_cache

from utils import mDist


lines = getInput('input3.txt');
start = (0,-1);

dirCharMap = {".":0,">":1,"^":2,"<":4,"v":8};
dirOffMap = {1:(1,0),2:(0,-1),4:(-1,0),8:(0,1)};
dirs = [1,2,4,8];

arr = np.array([[dirCharMap[c] for c in l.strip("#")] for l in lines[1:-1]],dtype=int).transpose();

end = arr.shape; #one left from the diagonal past the bottom-right corner (cringe, I know)
end = (end[0]-1,end[1]);

shape = arr.shape;
# print(end);
# print(shape);

state = tuple[tuple[int,int],int];

offsets = [(0,1),(1,0),(0,-1),(-1,0),(0,0)];

def tick_map(map:np.ndarray)->np.ndarray:
    return sum([np.roll(map & d,dirOffMap[d],(0,1)) for d in dirs])#I love this

_states = {0:arr}
_m_index = 0;
cycle = -1;
def get_map_state(time:int):
    global cycle
    if True:
        if time not in _states:
            global _m_index
            for index in range(_m_index,time):
                m = tick_map(_states[index]);
                # if (_states[0] == m).all(): #we've looped!
                #     cycle = index+1;
                #     # print("loop found at time",cycle);
                #     return _states[0];
                _states[index+1] = m;
            _m_index = time;
        return _states[time];
    else:
        # print("using cycle!");
        return _states[time%cycle];


_char_out_map = {i:str(i.bit_count()) for i in range(16)};
_char_out_map.update({v: k for k, v in dirCharMap.items()});
def print_map_state(time:int):
    m = get_map_state(time);
    out = "\n";
    for y in range(shape[0]):
        row = "#";
        for x in range(shape[1]):
            row += _char_out_map[m[x,y]];
        out += row + "#\n";    
    top = "#." + "#"*shape[0];
    bottom = top[::-1];
    # print(top+out+bottom);
    


@lru_cache
def in_bounds(pos:tuple[int,int]):
    return pos[0] in range(shape[0]) and pos[1] in range(shape[1]);

edges = set([end,start]);
@lru_cache
def neighbors(p:state):
    if p[0] not in edges and get_map_state(p[1])[p[0]]:
        return [];
    for o in offsets:
        newPos =(p[0][0]+o[0],p[0][1]+o[1]);
        if newPos in edges or in_bounds(newPos):
            yield (newPos,p[1]+1);


@lru_cache
def heuristic(pos:state):
    return mDist(pos[0],end);

@lru_cache
def r_heuristic(pos:state):
    return mDist(pos[0],start);

def do_p1(forward=True,startTick=0):
    startPos = (start,startTick) if forward else (end,startTick);
    hFun = heuristic if forward else r_heuristic
    
    openset:list[state] = [startPos];

    f:dict[state,float] = DefaultDict(lambda:float('inf'));
    g:dict[state,float] = DefaultDict(lambda:float('inf'));
    came:dict[state,state] = {};

    f[startPos] = hFun(startPos);
    g[startPos] = startTick;

    final = None;

    min_dist = shape[0]*shape[1];
    max_depth = -1;
    total = None;
    with tqdm(desc="distance",total=None,smoothing=0.6) as nearness_bar,tqdm(desc="nodes") as node_bar,tqdm(desc="max depth") as depth_bar:
        while len(openset) > 0:
            curr = openset.pop();
            node_bar.update(1);
            if curr[1] > max_depth:
                depth_bar.n = curr[1];
                max_depth = curr[1];
                depth_bar.refresh();
            if curr[0] == (end if forward else start):
                final = curr;
                break;
            for n in neighbors(curr):
                t_g = g[curr] + 1;
                if t_g < g[n]:
                    g[n] = t_g;
                    came[n] = curr;
                    h = hFun(n);
                    if h < min_dist:
                        if total is None:
                            nearness_bar.total = total = h;
                        nearness_bar.n = total - h;
                        min_dist = h;
                        nearness_bar.refresh();
                    f[n] = t_g + h;
                    if n not in openset:
                        openset.append(n);
            openset.sort(key=lambda n:(f[n],hFun(n)),reverse=True);
    if final:
        print(f"steps1: {g[final]}")
        print(f"steps2: {f[final]}");
        return final[1];
    else:
        print("oh noes");
        raise Exception();

def do_p2():
    l1 = do_p1();
    l2 = do_p1(forward=False,startTick=l1);
    l3 = do_p1(forward=True,startTick=l2);
    print(l1,l2,l3);
    pass;


if __name__ == "__main__":
    do_p2();
    # for i in range(10):
    #     print(get_map_state(i));
    #     print_map_state(i);
    #     input();