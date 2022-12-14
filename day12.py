from typing import DefaultDict
from text import getInput
import numpy as np

lines = getInput();


hmap = [];

start = None;
end = None;

for x,l in enumerate(lines):
    line = [];
    for y,c in enumerate(l):
        if c =='S':
            line.append(0);
            start = (x,y);
        elif c == 'E':
            line.append(25);
            end = (x,y);
        else:
            line.append(ord(c)-ord('a'));
    hmap.append(line);


hmap = np.array(hmap);
size = hmap.shape;

def getNeighbors(p:tuple[int,int]):
    offs = [(0,1),(1,0),(0,-1),(-1,0)];
    # print("finding neighbors of",p);
    for o in offs:
        of = p[0]+o[0],p[1]+o[1];
        # if (of == end):
        #     raise Exception();
        # print("checking potential neighbor",of);
        if (of[0]<size[0] and of[0] >= 0 and of[1] < size[1] and of[1] >= 0):
            if (hmap[of]+1 >= hmap[p]):
                yield of;
            else:
                # print("neighbor rejected, offset height",hmap[of],"too different from position height",hmap[p]);
                pass;
        else:
            # print("neighbor rejected, out of bounds");
            pass;
assert isinstance(start,tuple)

prev = {};
searched = [];
fscore = {end:0};

searchNext = [end];

while len(searchNext) > 0:
    pos = searchNext.pop(0);
    if pos in searched:
        continue
    count = fscore[pos];
    
    for n in getNeighbors(pos):
        if n not in fscore or fscore[n] > count+1:
            fscore[n] = count+1;
            prev[n] = pos;
        searchNext.append(n);
    searched.append(pos);

# def doSearch(pos:tuple[int,int],count=0):
#     if pos in searched:
#         return;
    
#     for n in getNeighbors(pos):
#         if n not in fscore or fscore[n] > count+1:
#             fscore[n] = count+1;
#         doSearch(n);

# doSearch(start);

# out = '';
# for x in range(size[0]):
#     l = ''
#     for y in range(size[1]):
#         p = (x,y);
#         if p == end:
#             l += 'E';
#             continue;
#         if p == start:
#             l += 'S';
#             continue;
#         if hmap[p] == (ord('h')-ord('a')):
#             l += 'H';
#             continue;
#         if p in prev:
#             l += '#';
#         else:
#             l += '.';
#         continue;
#         if p == end:
#             l += 'E';
#             continue;
#         if p == start:
#             l += 'S';
#             continue;
#         if p not in prev:
#             l = '.'+l;
#             continue;
#         pr = prev[p];
#         if (pr[1] > y):
#             l += '<';
#         if (pr[1] < y):
#             l += '>';
#         if (pr[0] > x):
#             l += '^';
#         if (pr[0] < x):
#             l += 'v';
#     l += '\n'
#     out += (l);
# print(out);


# path = [];
# length = 0;
# pos = end;
# while pos != start:
#     print("pathing before",pos);
#     path.insert(0,pos);
#     pos = prev[pos];
#     length += 1;




print(fscore);
print(start);
print(end);

best = float('inf');
bestDest = None;

for index in np.argwhere(hmap==0):
    # print(index);
    if tuple(index) not in fscore:
        continue;
    s = fscore[tuple(index)];
    if s < best:
        best = s;
        bestDest = tuple(index)
    # best = min(fscore[tuple(index)],best);
print(fscore[start]);

print(best);
print(bestDest);
print(hmap[bestDest])
# print(path);

# print(length);




