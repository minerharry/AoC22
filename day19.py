import contextlib
import inspect
import numpy as np
from text import getInput
from tqdm import tqdm
import re
from numpy.typing import NDArray

from utils import redirect_to_tqdm

nSteps = 24;

robot_regex = re.compile("Each ([a-zA-Z]+) robot costs (.*?)\\.")
cost_regex = re.compile("\\s*([0-9]+) ([a-zA-Z]*)")

names = ['ore','clay','obsidian','geode'];
gIndex = names.index("geode");
oIndex = names.index("ore");
blueprints:list[dict[str,dict[str,int]]] = [];
for line in getInput('blueprint2.txt'):
    robots = {};
    for r,cost in robot_regex.findall(line):
        robots[r] = {t:int(n) for n,t in cost_regex.findall(cost)}
    for r in names:
        for n in names:
            robots[r][n] = robots[r][n] if n in robots[r] else 0;
    blueprints.append(robots);

maxRs = [{ctype:max([cost[ctype] for r,cost in b.items() if r != ctype and ctype in cost]) for ctype in names} for b in blueprints];
print(maxRs)
print(line);
big = 5000
[ma.update({"geode":big}) for ma in maxRs];

def buildable_robots(blueprint_idx:int,amounts:dict[str,int],choices:list[str]):
    for rtype in choices:
        nAmounts = {n:amounts[n]-(blueprints[blueprint_idx][rtype][n] if n in blueprints[blueprint_idx][rtype] else 0) for n in names}
        if all([a >= 0 for a in nAmounts.values()]):
            yield rtype,nAmounts;

bar = None;
leaf_bar = None;
prune_bar = None;
best_bar = None;


def search_geode(blueprint_idx:int,robots:dict[str,int]={'ore':1,'clay':0,'obsidian':0,'geode':0},amounts:dict[str,int]={n:0 for n in names},steps:int=nSteps):
    bar.update(1);
    if steps == 0:
        leaf_bar.update(1);
        return [amounts['geode']]

    for rtype,count in robots.items():
        amounts[rtype] += count;

    l = []
    for b,newAmounts in buildable_robots(blueprint_idx,amounts,[n for n in names if robots[n] < maxRs[blueprint_idx][n]]):
        newRobots = robots.copy();
        newRobots[b] += 1;
        l.append(max(search_geode(blueprint_idx,robots=newRobots,amounts=newAmounts,steps=steps-1)));
    l.append(max(search_geode(blueprint_idx,robots,amounts,steps=steps-1)));

    return l;

# print([[[b[r] for c in names] for r in names]  for b in blueprints])

fast_prints = np.array([[[b[r][c] for c in names] for r in names]  for b in blueprints]);
fast_maxs = np.array([[m[n] for n in names] for m in maxRs]);

best_geodes = 0;

def ticks_til_satisfactory(resource:int,threshold:int,cutoff_ticks:int,idx:int,amounts:np.ndarray,robots:np.ndarray,pr=False):
    oT = threshold;
    threshold -= amounts[resource];
    ticks = 0;
    rs = robots[resource];
    costs = fast_prints[idx][resource];
    ticks_til_robot = 0 if threshold <= 0 else (min(cutoff_ticks,int((threshold/rs))) if resource == oIndex else max([ticks_til_satisfactory(rtype,c,ticks,idx,amounts,robots) for rtype,c in enumerate(costs) if c != 0]))
    if pr: print("able to construct",names[resource],"robot in",ticks_til_robot,"ticks");
    ticks += ticks_til_robot;
    threshold -= ticks_til_robot*rs;
    while threshold > 0 and ticks < cutoff_ticks:
        threshold -= rs;
        ticks += 1;
        rs += 1;
    if pr:
        if ticks < cutoff_ticks:
            print("able to meet resource requirement",oT,names[resource],"in",ticks,"ticks of the cutoff point of",cutoff_ticks,"ticks");
        else:
            print("unable to meet resource requirement",oT,names[resource],"in",cutoff_ticks,"ticks; got to",threshold,"remaining");
    return ticks;

def rec_pred_geodes(remaining_steps:int,idx:int,amounts:np.ndarray,robots:np.ndarray,pr=False):
    base = remaining_steps*robots[gIndex] + amounts[gIndex];
    mTicks = [ticks_til_satisfactory(rtype,c,remaining_steps,idx,amounts,robots,pr=pr) for rtype,c in enumerate(fast_prints[idx][gIndex]) if c != 0];
    build_steps = remaining_steps - max(mTicks);
    if build_steps < 0:
        print(mTicks);
        print(build_steps);
    assert build_steps >= 0


    extra = build_steps*((build_steps-1)/2);
    pred = base + extra
    if pr: print('for branch with amounts:',amounts,"robots:",robots,"and steps remaining:",remaining_steps,'- took',max(mTicks),'ticks ',mTicks,'to start accumulating geodes and predicted sum:',amounts[gIndex],"+",extra,"+",remaining_steps*robots[gIndex],"=",pred);
    
    #current geode count + (additional geodes if you spent every remaining cycle building geode robots) + (geodes from current robots)
    return pred
        



def pred_geodes(remaining_steps:int,idx:int,amounts:np.ndarray,robots:np.ndarray,pr=False):
    base = remaining_steps*robots[gIndex] + amounts[gIndex];
    build_steps = remaining_steps
    if (amounts < fast_prints[idx][gIndex]).all(): #can't build geode robot this tick
        if (amounts+robots < fast_prints[idx][gIndex]).all(): #can't build geode robot next tick
            build_steps -= 2;
        else:
            build_steps -= 1;


    extra = build_steps*((build_steps-1)/2);
    pred = base + extra
    if pr: print('for branch with amounts:',amounts,"robots:",robots,"and steps remaining:",remaining_steps,'predicting sum:',amounts[gIndex],"+",extra,"+",remaining_steps*robots[gIndex],"=",pred);
    
    #current geode count + (additional geodes if you spent every remaining cycle building geode robots) + (geodes from current robots)
    return pred

def fast_robots(idx:int,amounts:np.ndarray,choices:list[int]):
    for i in choices:
        nAmounts = amounts - fast_prints[idx][i];
        if (nAmounts < 0).any():
            continue;
        yield i,nAmounts;

def search_fast(idx:int,robots:np.ndarray=np.array((1,0,0,0)),amounts:np.ndarray=np.array((0,0,0,0)),steps:int=nSteps,exclude_search:set[int]=set()):
    bar.update(1);
    global best_geodes
    if steps == 0:
        if amounts[gIndex] > best_geodes:
            best_bar.update(amounts[gIndex]-best_geodes);
            best_geodes = amounts[gIndex];
            # print(amounts[gIndex]);
            # if amounts[gIndex] > 24:
            #     print("aaaaa");
        leaf_bar.update(1)
        return amounts[gIndex];
    else:
        pred = rec_pred_geodes(steps,idx,amounts,robots)
        # if pred == 0 and amounts[1] == 52 and robots[1] == 6:
        #     print("aaaa");
        if pred <= best_geodes:
            prune_bar.update(1);
            # print("pruning branch with",steps,"remaining,",robots[gIndex],"geode robots, and",amounts[gIndex],"geodes; projected geode count",pred,"worse than best-so-far",best_geodes);
            return 0;

    b_save = best_geodes;
    
    searched = set();
    # print(exclude_search)
    # print(np.isin(robots,exclude_search,invert=True))
    # print((fast_maxs[idx] > robots));
    # print((fast_maxs[idx] > robots) & np.isin(robots,exclude_search,invert=True));
    bList = [];
    if nSteps > 1: #don't build a robot on the last tick
        for b,namounts in fast_robots(idx,amounts,[gIndex] if (nSteps==2) else np.where((fast_maxs[idx] > robots) & np.isin(robots,exclude_search,invert=True))[0]):
            off = np.zeros(4,dtype=int);
            off[b] = 1;
            bList.append(search_fast(idx,robots=robots + off,amounts=namounts+robots,steps=steps-1));
            searched.add(b);
    if len(searched) < 4:
        bList.append(search_fast(idx,robots,amounts+robots,steps-1,exclude_search=searched.union(exclude_search)));
    b = max(bList);
    if pred < b:
        rec_pred_geodes(steps,idx,amounts,robots,pr=True)
        print("error: heuristic too pessimistic for branch with",steps,"remaining,",robots[gIndex],"geode robots, and",amounts[gIndex],"geodes; projected geode count was",pred,"and considered worse than the then best-so-far",b_save,"but actual best was",b);
    # elif b > 0:
    #     print(pred,b);
    return b;

def make_bars():
    global bar,leaf_bar,prune_bar,best_bar
    bar = tqdm(desc="Node");
    leaf_bar = tqdm(desc="Leaf");
    prune_bar = tqdm(desc="Prune");
    best_bar = tqdm(desc="Best geode count",unit=" geodes");

def clear_bars():
    bar.close();
    leaf_bar.close();
    prune_bar.close();
    best_bar.close();

def run_p1():
    global best_geodes
    acc = 0;
    with redirect_to_tqdm():
        for i,b in enumerate(tqdm(range(len(blueprints)),desc="Blueprints")):
            make_bars();
            best_geodes = 0;
            s = search_fast(b);
            # print(s,best_geodes);
            assert s == best_geodes
            g = best_geodes;
            clear_bars();
            print("blueprint",i+1,"returned with best geodes:",g,"and subscore:",g*(i+1));
            acc += g*(i+1);
        
    print();
    print(acc);

def run_p2():
    global best_geodes
    acc = [];
    with redirect_to_tqdm():
        for i,b in enumerate(tqdm(range(3),desc="Blueprints")):
            make_bars();
            best_geodes = 0;
            s = search_fast(b,steps=32);
            # print(s,best_geodes);
            assert s == best_geodes
            g = best_geodes;
            clear_bars();
            print("blueprint",i+1,"returned with best geodes:",g);
            acc.append(g);
        
    print();
    print(acc);

if __name__ == "__main__":
    run_p2();
