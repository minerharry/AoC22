import itertools
from operator import itemgetter
from text import getInput
import math
from typing import Literal, Iterable, DefaultDict
import numpy as np
from tqdm import tqdm

from utils import most_frequent
from wrap_list import WraparoundList

lines = getInput('input2.txt');

jets = lines[0];


blocks = [
    np.array([
        [0,0,1,1,1,1,0],
    ]),
    np.array([
        [0,0,0,1,0,0,0],
        [0,0,1,1,1,0,0],
        [0,0,0,1,0,0,0],
    ]),
    np.array([
        [0,0,1,1,1,0,0],
        [0,0,0,0,1,0,0],
        [0,0,0,0,1,0,0],
    ]),
    np.array([
        [0,0,1,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,1,0,0,0,0],
    ]),
    np.array([
        [0,0,1,1,0,0,0],
        [0,0,1,1,0,0,0],
    ])
]

blocks = [b.astype(bool) for b in blocks];

segmentSize = 200000;
vOffset = 3;



blockIter = itertools.cycle(range(len(blocks)));
wrap_jets = WraparoundList(jets);
    
def runTetris(startblock=0,startjet=0,startboard=None,starttop=1,numBlocks=10000,blockPrints=[],shiftPrints={},boardPrints={}):
    length = 2022
    length = 1000000000000

    board = startboard if startboard is not None else np.zeros((segmentSize*2,7),dtype=bool);
    board[0] = 1;

    top = starttop + 1;

    patternTimes:dict[tuple[tuple[int,int]],list[tuple[int,int]]] = DefaultDict(lambda: []); #result is list of y position, block number

    counts:dict[tuple[tuple[int,int],],int] = DefaultDict(lambda: 0);

    patternState = tuple[tuple[int,int],int,int]; #offset from start, block index, jet index
    pattern:list[tuple[int,int]] = [];
    start:tuple[int,int] = None;
    broken = False;
    parody = 0;
    jIndex = startjet-1;
    bIdx = startblock-1;
    prim = None;
    cLength = 4;
    bstart = None;
    bFound = False;
    for i in tqdm(range(numBlocks)):
        bIdx = (bIdx + 1)%5;


        block = blocks[bIdx].copy();
        bHeight = block.shape[0]
        y = top + vOffset;
        x = 0;
        if bIdx == 0 and parody == 0:
            if not bFound:
                bstart = (board.copy(),top);
        if i in shiftPrints:
            l = shiftPrints[i];
            print("block number",i,"jet index:",jIndex,"next",l,"shifts from jets are:",wrap_jets[jIndex:jIndex+l]);
        while y > -10: #error case
            ##jet pushing
            jIndex = (jIndex + 1) % len(jets);
            direction = (-1,-1) if jets[jIndex] == "<" else (1,0); #direction in x, index of the y axis of the other side to check rollover
            sBlock = np.roll(block,direction[0],1);
            try:
                if not sBlock[:,direction[1]].any():
                    if not (board[y:y+bHeight] & sBlock).any(): #no rollover, no collision
                        # print(board[y:y+bHeight] & sBlock);
                        x += direction[0];
                        block = sBlock;      
                        # print("block moved","right" if direction[0] == 1 else "left");
            except:
                print(block[::-1].astype('uint8'));
                print(sBlock[::-1].astype('uint8'));
                print(bHeight)
                raise Exception();
            if y-1+bHeight > board.shape[0]:
                raise Exception("hit board length >:(");
            if (board[y-1:y-1+bHeight] & block).any(): #hit something
                board[y:y+bHeight] |= block;
                top = max(top,y+bHeight);
                break;
            y -= 1
        if (i in blockPrints):
            print("block number",i,"dropped at coordinates:",x,y);
        if (i in boardPrints):
            print("block number",i,"board state:");
            printBoard(board,top,top-boardPrints[i] if boardPrints[i] else None);
        if bIdx == 0 and parody == 0:
            start = (x,y);
        if start is not None: #don't count patterns until the beginning of a parody cycle is reached, in case of nonzero block start
            pattern.append(((x-start[0],y-start[1]),bIdx,jIndex));
            if bIdx == 4 and parody == cLength-1:
                p = tuple(pattern);
                patternTimes[p].append((y,i));
                counts[p] += 1;
                if ((prim and prim == p) or (not prim and counts[p] > 5)):
                    bFound = True;
                    if True and not prim:
                        prim = p;
                        # printBoard(board,top,lower=top-40);
                        # print();
                        # print(p);
                        # print(counts[p]);
                        # print()
                        # input();
                elif not bFound:
                    bstart = None;

                pattern = [];
        
        if bIdx == 4:
            parody = (parody + 1) % cLength;


    # print(patternTimes);
    cycle = max(counts.items(),key=itemgetter(1));
    print(cycle);
    times = patternTimes[cycle[0]];
    print(times)
    cycle_block = times[1][1] if len(times) > 1 else None;
    yOffs = [b[0]-a[0] for a,b in zip([(0,0)]+times,times+[(0,0)])];
    yDiff = most_frequent(yOffs);
    blockOffs = [b[1]-a[1] for a,b in zip([(0,0)]+times,times+[(0,0)])]
    blockDiff = most_frequent(blockOffs)
    print("Y offset:",yDiff,"XBlock offset:",blockDiff);
    print(top-1);
    return (board,bIdx,jIndex),top-1,cycle_block,yDiff,blockDiff;
        

def printBoard(board,top,lower=None):
    b = board[top+2:lower:-1]
    for row in b:
        print("".join(["#" if c else "." for c in row]))


if __name__ == "__main__":
    length = 1000000000000;
    _,_,blockStart,yD,bD = runTetris(); #find pattern and offsets

    numCycles,partialLength = divmod(length - blockStart,bD);

    print("num cycles:",numCycles,"partial length:",partialLength)
    ##test offset correctness
    b,t1,*_ = runTetris(numBlocks=blockStart)
    b,top,*_ = runTetris(numBlocks=blockStart+20*bD);
    assert top == t1+20*yD
    print("offset test passed successfully!");

    topOffset = numCycles*yD;

    numBlocks = blockStart+partialLength;

    _,top1,*_ = runTetris(numBlocks=numBlocks);
    totalTop = top1 + topOffset;
    print(top1,totalTop);

    # ##test continuability
    # n1 = 200
    # n2 = 200;
    # (board,bIdx,jIndex),t1,_,_,_ = runTetris(numBlocks=n1,
    #     blockPrints=[n1-2,n1-1,n1],
    #     shiftPrints={n1-2:5,n1-1:5,n1:5},
    #     );
    # _,t2,*_ = runTetris(startboard=board,startjet=jIndex,startblock=bIdx,starttop=t1,numBlocks=n2,
    #     blockPrints=[0,1,2],
    #     shiftPrints={0:5,1:5,2:5});
    # _,t3,*_ = runTetris(numBlocks=n1+n2,
    #     blockPrints=[n1-2,n1-1,n1,n1+1,n1+2],
    #     shiftPrints={n1-2:5,n1-1:5,n1:5,n1:5,n1+1:5,n1+2:5});
    # print(t1,t2,t1+t2);
    # print(t3);
    # assert t1+t2 == t3;

