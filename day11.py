from __future__ import annotations
from math import lcm
from typing import Callable
from text import getInput
from tqdm import tqdm

lines = getInput();

acc = 0;

monkeys:dict[int,Monkey] = {};


# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

class Item:
    def __init__(self,worry):
        self.worry:int = worry;

    def __repr__(self):
        return str(self.worry);

def getDivTest(num):
    def divisible(inp:int):
        return inp%num == 0;
    return divisible;

def getOp(op:str):
    def operate(inp:int):
        return eval(op.replace('old',str(inp)));
    return operate;

class Monkey:
    def __init__(self,name,items,operation,test,true,false):
        self.num = int(name.split(' ')[1].split(':')[0]);
        self.items = [Item(int(a)) for a in items.split(': ')[1].split(', ')];
    
        self.div = int(test.split(' ')[-1])
        self.test:Callable = getDivTest(self.div);
        self.operation:Callable = getOp(operation.split(' = ')[1]);

        self.true = int(true.split(' ')[-1])
        self.false = int(false.split(' ')[-1]);

        monkeys[self.num] = self;

        self.inspCount = 0;

    def turn(self,mod):
        while len(self.items) > 0:
            self.inspCount += 1;
            item = self.items.pop();
            w = item.worry;
            w = self.operation(w);
            w = w % mod;
            dest = self.true if self.test(w) else self.false;
            item.worry = w;
            monkeys[dest].items.append(item);
    
    def __repr__(self):
        return f"Monkey {self.num}: {self.items}"
            




for i in range(0,len(lines),7):
    Monkey(*lines[i:i+6]);

mod = lcm(*[m.div for m in monkeys.values()]);


# print("initial monkeys:\n",'\n'.join([str(m) for m in list(monkeys.values())]))

for i in tqdm(range(10000)):
    for m in range(len(monkeys)):
        monkeys[m].turn(mod);
    # print(f"After round {i+1}:\n",'\n'.join([str(m) for m in list(monkeys.values())]))

scores = [m.inspCount for m in monkeys.values()];

scores.sort(reverse=True)
print(scores);

print(scores[0]*scores[1]);