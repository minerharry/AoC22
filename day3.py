from text import getInput

def getP(t:str):
    if t.isupper():
        # print('upper');
        return ord(t) - ord('A') + 27;
    else:
        return ord(t) - ord('a') + 1;

s = 0;
# for l in getInput(): day 1
#     left = l[:int(len(l)/2)];
#     right = l[int(len(l)/2):len(l)];
#     for i in range(len(left)):
#         c = left[i]
#         if c in right and c not in l[:i]:
#             # print(c);
#             # print(getP(c));
#             s += getP(c);
l = getInput() # day 2
for i in range(0,len(l),3):
    lines = l[i:i+3];
    unique = set(lines[0]).intersection(set(lines[1])).intersection(set(lines[2]));
    s += getP(list(unique)[0]);


print(s);

