from text import getInput

lines = getInput();

tree = {'/':{}};

pwd = [];

def indexTree(path):
    if path == []:
        return tree;
    
    return indexTree(path[:-1])[path[-1]]

for i in range(len(lines)):
    l = lines[i];
    if l.startswith("$"): #command
        # print("commanding")
        line = l.split(' ');
        if line[1] == 'cd':
            # print("changing");
            off = line[2];
            if (off == '..'):
                pwd.pop();
            elif off == '/':
                pwd = ['/'];
            else:
                pwd.append(off);
        if line[1] == 'ls':
            # print("losing")
            current = indexTree(pwd);
            while i+1 < len(lines) and not lines[i+1].startswith("$"):
                i += 1;
                out = lines[i].split(' ');
                if out[0] == 'dir': #directory:
                    if out[1] not in current:
                        current[out[1]] = {};
                else: #file
                    size = int(out[0])
                    current[out[1]] = size;

print(tree);

def get_dir_sizes(path:list[str]):
    subfolder = indexTree(path);
    topsize = 0;
    for name,val in subfolder.items():
        if isinstance(val,int):
            topsize += val;
        else:
            # print("testing subdir",path+[name]);
            sizes = get_dir_sizes(path + [name]);
            for s in sizes:
                if len(s[0]) == len(path) + 1: 
                    topsize += s[1];
                yield s;
    
    yield [path,topsize];

limit = 100000;

res = 0;
sizes = list(get_dir_sizes(['/']))
for s in sizes:
    if s[1] < limit:
        res += s[1];

print(res);

print(sizes)
                    
total = 70000000;
need = 30000000;

diff = need - (total - sizes[-1][1])
print(sizes[-1])
print(total-sizes[-1][1])

candidates = []
for s in sizes:
    if s[1] > diff:
        candidates.append(s);

candidates.sort(key=lambda x: x[1]);
print(candidates[0])
print(candidates[:10])
print(diff);

