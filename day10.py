from text import getInput

lines = getInput();

acc = 0;

xreg = 1

cycle = 0;

triggers = [20,60,100,140,180,220];

out = []

def incCycle(num=1):
    global cycle,acc;
    cycle += 1;
    print("cycle",cycle)
    print("xreg",xreg)
    # if cycle in triggers:
    #     acc += cycle*xreg;
    if (abs((cycle-1)%40-xreg+1) <= 1): #draw
        print("drawing #");
        out.append(cycle)
    else:
        print("drawing .");
    if (num > 1):
        incCycle(num-1);

for l in lines:
    args = l.split(' ');
    comm = args[0];
    if (comm == 'noop'):
        incCycle();
        continue;
    if (comm == 'addx'):
        incCycle();
        xreg += int(args[1]);
        incCycle();
print(xreg);
print(cycle);
print(acc);

draw = [];
line = [];
for i in range(cycle+1):
    if i % 40 == 0:
        draw.append(line)
        line = [];
    if i in out:
        line.append("#");
    else:
        line.append(".");

print(len(draw[1]))

print('\n'.join([''.join(l) for l in draw]));
    

