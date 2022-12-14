from text import getInput

acc = 0;
lines = getInput()

numCrates = 9;
crated = False;
stacks = {n+1:[] for n in range(numCrates)};
for l in lines:
    if not crated:
        if ('[' not in l):
            crated = True;
        else:
            for i in range(0,len(l),4):
                if (l[i+1] != ' '):
                    stacks[i//4+1].append(l[i+1]);
    else:
        if not l.startswith("move"):
            print("nonmoving line",l);
            continue;
        spots = l.split(' ');
        count = int(spots[1]);
        start = int(spots[3]);
        dest = int(spots[5]);
        # for i in range(count):
        #     stacks[dest].insert(0,stacks[start].pop(0));
        copy = stacks[start][:count];
        for i in range(count):
            stacks[start].pop(0);
            # print(i);
            stacks[dest].insert(0,copy[-i-1])


print(''.join([s[0] for s in stacks.values()]));
    
                
