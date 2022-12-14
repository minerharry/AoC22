from text import getInput
result = 0;

for l in getInput():
    e1,e2 = [t.split('-') for t in l.split(",")];
    
    e1 = [x for x in range(int(e1[0]),int(e1[1])+1)];
    e2 = [x for x in range(int(e2[0]),int(e2[1])+1)];

    if len(set(e1).intersection(set(e2))) > 0:
        result += 1;

print(result);