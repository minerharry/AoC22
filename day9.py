from text import getInput

names = getInput();

length = 10;
rope = [[0 for _ in range(2)] for _ in range(length)]

positions = set((0,0));

def moveHead(offset:tuple[int,int],count:int):
    for i in range(count):
        moveKnot(0,offset);

def moveKnot(index,offset):
    rope[index][0] += offset[0];
    rope[index][1] += offset[1];
    # print("moved knot",index,"to pos",rope[index]);
    # print(rope[1])
    if index < length-1:
        validKnot(index+1);
    else:
        positions.add(tuple(rope[index]));

def validKnot(index):
    diff = [rope[index-1][0]-rope[index][0],rope[index-1][1]-rope[index][1]];
    tail = [0,0];

    if abs(diff[0]) <= 1 and abs(diff[1]) <= 1:
        # print("no adjustment needed for knot",index,"diff:",diff)
        return;

    if (diff[1] != 0):
        tail[1] += abs(diff[1])/diff[1];
    
    if (diff[0] != 0):
        tail[0] += abs(diff[0])/diff[0];
    moveKnot(index,tail);

for l in names:
    com,count = l.split(' ');
    count = int(count);
    offset = {"R":[0,1],"L":[0,-1],"U":[1,0],"D":[-1,0]}[com];
    moveHead(offset,count);

print(len(positions));