from math import log
from text import getInput

dtosMap = {2:'2',1:'1',0:'0',-1:'-',-2:'='};
def dtos(dec:int):
    top = int(log(dec,5))+1;
    # print("top power of 5:",top);
    res = ''
    for i in range(top,0,-1):
        # print(f"place #{i}, multiples of {5**i}")
        d =  (dec+(5**i-1)/2)//(5**i);
        # print("d:",d);
        dec -= d*(5**i);
        # print("remaining dec:",dec);
        res += dtosMap[d];
    return res.lstrip('0') + dtosMap[dec];
    pass;

stodMap = {'2':2,'1':1,'0':0,'-':-1,'=':-2}

def stod(snafu:str|int):
    if isinstance(snafu,int):
        snafu = str(snafu);
    acc = 0;
    for i,c in enumerate(snafu[::-1]):
        acc += (5**i)*(stodMap[c]);
    return acc

print(dtos(sum([stod(l) for l in getInput()])))