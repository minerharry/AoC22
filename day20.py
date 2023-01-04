from tqdm import tqdm
from text import getInput
import numpy as np

from wrap_list import WraparoundList

key = 811589153;
lines = [(n,int(i)*key) for n,i in enumerate(getInput())];

def shiftNum(nums,index,shift):
    shift %= len(nums)-1
    if shift < 0: shift -= 1;
    shift = len(nums) + shift if (index + shift) < 0 else (shift if (index + shift) < len(nums) else shift - len(nums) + 1);
    if shift == 0:
        # print("## no shift necessary")
        return nums
    else:


        s = shift >= 0;

        # print("## to shift:",nums)
        # print("## effectively shifting by",shift)
        # print("## negative shift:",s);

        num = [nums[index]]
        pre = nums[:index if s else index+shift];
        shiftRange = nums[index+1:index+shift+1:] if s else nums [index+shift:index];
        post = nums[index+shift+1 if s else index + 1:];

        # print("num",num);
        # print("pre",pre);
        # print("range",shiftRange);
        # print("post",post);

        c1 = [pre,num,shiftRange,post];
        c2 = [pre,shiftRange,num,post];

        # print("s:",s);
        # print("input nums:",nums);
        # print("original config",*(c1 if s else c2));
        # print("shifted config",*(c2 if s else c1));

        return sum((c2 if s else c1),start=[]);

if __name__ == "__main__":
        

    print("original",lines);
    ops = [lines];
    lCopy = lines.copy();
    zero = None
    for _ in tqdm(range(10)):
        for id,num in tqdm(lCopy):
            # print("#### shifting",num);
            ops.append(num);
            if num == 0:
                zero = (id,num);
            lines = shiftNum(lines,lines.index((id,num)),num);
            ops.append(lines);
            # print("#### shifted:",lines);
            # print();

    # print('\n'.join([str(op) for op in ops]))
    start = lines.index(zero);
    acc = 0;
    for off in [1000,2000,3000]:
        acc += lines[(start+off)%len(lines)][1]

    print(acc);