from text import getInput




lines = getInput();
score = 0;

for l in lines:
    o,m = l.split(' ');
    o = {'A':0,'B':1,'C':2}[o];

    if (m == 'X'): #lose
        m = (o - 1)%3;
    elif (m == 'Y'):
        m = o;
    elif (m == 'Z'):
        m = (o + 1)%3;

    score += m + 1;
    if (m == (o+1)%3):
        score += 6;
    elif (m == o):
        score += 3;
    # print(score);

print(score);
