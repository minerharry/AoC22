from text import getInput

elves = [];
current = 0;
for l in getInput():
    if l == '' or l == '\n':
        elves.append(current);
        current = 0;
    else:
        current += int(l);
print(max(elves));
elves.sort(reverse=True);
print(sum(elves[:3]));