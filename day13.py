from text import getInput
from functools import cmp_to_key

lines = getInput();


pairs:dict[int,tuple[list,list]] = {};


ind = 0;
for i in range(0,len(lines),3):
    ind += 1;
    p1 = eval(lines[i]);
    p2 = eval(lines[i+1]);
    pairs[ind]=(p1,p2);

#1 is good, -1 is bad, 0 is neutral

def compare(v1:list|int,v2:list|int):
    print("comparing",v1,"and",v2);
    int1 = isinstance(v1,int);
    int2 = isinstance(v2,int);
    if (int1 and int2):
        return 1 if v1<v2 else (0 if v1 == v2 else -1);
    
    if int1:
        v1 = [v1];
    if int2:
        v2 = [v2];
    
    l1 = len(v1);
    l2 = len(v2);
    for i in range(max(l1,l2)):
        if i >= l1:
            return 1;
        if i >= l2:
            return -1;
        c = compare(v1[i],v2[i]);
        if c: return c;
    return 0;

indices = [];

for index,pair in pairs.items():
    if compare(*pair) == 1:
        indices.append(index);


allp = [];
for p in pairs.values():
    allp.append(p[0]);
    allp.append(p[1]);

d1 = [[2]]
allp.append(d1);
d2 = [[6]];
allp.append(d2);

key = cmp_to_key(compare);

allp.sort(key=key,reverse=True);

i1 = allp.index(d1);
i2 = allp.index(d2);
# print('\n'.join([str(s) for s in allp]));
print(i1,i2);
print((i1+1)*(1+i2));

print('\n'.join([str(s) for s in indices]));
print(sum(indices));

        

