import itertools
from text import getInput
import math
from typing import Literal, Iterable, DefaultDict
import numpy as np
from tqdm import tqdm

lines = getInput('input.txt');

jets = itertools.cycle(lines[0]);

# out = "";
# for j in range(len(lines[0])*4):
#     out += next(jets);

# print(out);
# exit();


blocks = [ #
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






board = np.zeros((segmentSize*2,7),dtype=bool);
board[0] = 1;

top = 1;

blockIter = itertools.cycle(blocks);

boards = [board[:segmentSize],board[segmentSize:]];
boardIdx = 0;

    

length = 2022
length = 1000000000000

for _ in tqdm(range(length)):
# while top < 3068:
    block = next(blockIter).copy();
    bHeight = block.shape[0]
    # print(block)
    y = top + vOffset;
    # print(block);
    # bCopy = board.copy();
    # bCopy[y:y+bHeight] |= block;
    # print(bCopy[top+4::-1].astype('uint8'))
    # print("")
    # print("")
    while y > -10: #error case
        ##jet pushing
        direction = (-1,-1) if next(jets) == "<" else (1,0); #direction in x, index of the y axis of the other side to check rollover
        sBlock = np.roll(block,direction[0],1);
        try:
            if not sBlock[:,direction[1]].any():
                if not (board[y:y+bHeight] & sBlock).any(): #no rollover, no collision
                    # print(board[y:y+bHeight] & sBlock);
                    block = sBlock;      
                    # print("block moved","right" if direction[0] == 1 else "left");
        except:
            print(block[::-1].astype('uint8'));
            print(sBlock[::-1].astype('uint8'));
            print(bHeight)
            raise Exception();
        #     else:
        #         print("no x movement, collision with block")
        # else:
        #     print("no x movement, rollover detected")
        # print(block.astype('uint8'));
        # bCopy = board.copy();
        # bCopy[y:y+bHeight] |= block;
        # print(bCopy[y+4::-1].astype('uint8'))
        ##vertical movement
        if (board[y-1:y-1+bHeight] & block).any(): #hit something
            board[y:y+bHeight] |= block;
            top = max(top,y+bHeight);
            break;
        y -= 1
        # print(y);
        # print("block moved down");
        # bCopy = board.copy();
        # bCopy[y:y+bHeight] |= block;
        # print(bCopy[y+4::-1].astype('uint8'))


def printBoard(lower=None):
    b = board[top+2:lower:-1]
    for row in b:
        print("".join(["#" if c else "." for c in row]))





# print(board[top+2:top-10:-1].astype('uint8'));
# printBoard();
print(top-1);


