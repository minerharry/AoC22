from text import getInput

buffer = getInput()[0];

for i in range(len(buffer)-14):
    if (len(set(buffer[i:i+14]))) == 14:
        print(i+14);
        exit();