from text import getInput
import re
from functools import lru_cache

m_regex = re.compile("([a-zA-Z]+): (?:(\\d+)|(([a-zA-Z]+) [\\*\\+/-] ([a-zA-Z]+)))");

monkeys:dict[str,tuple[list[str],str]] = {}; #value is [dependencies], operation



for l in getInput():
    m = m_regex.match(l);
    if m:
        print(m.groups());
        monkey,*ops = m.groups();
        dep:list[str] = []
        op:str = ops[0];
        if ops[0] is None: #complex
            op = ops[1];
            dep = ops[2:];
        if monkey == 'root':
            op = op.replace("+",",");
        monkeys[monkey] = (dep,op);
    else:
        raise Exception(f"unable to match line {l}")

del(monkeys['humn']);

# print(monkeys);
       


monkey_results = {'humn':'humn'};

def eval_monkey(name:str):
    if name in monkey_results:
        return monkey_results[name];
    deps,op = monkeys[name];
    for d in deps:
        op = op.replace(d,str(eval_monkey(d)));
    try:
        return eval(op);
    except NameError:
        return f"({op})" #if op[0] != '(' and op[-1] != ')' else op;


@lru_cache
def cache_eval_monkey(name:str):
    deps,op = monkeys[name];
    for d in deps:
        op.replace(d,str(eval_monkey(d)));
    return eval(op);

r = eval_monkey("root");
print(r);
print(r.replace(",","=").replace("humn","x"));
