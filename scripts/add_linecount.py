import subprocess
import os
import sys


def add_linecount_to_top(filename):
    print(f"Adding linecount to {filename}")
    lines = []
    lc = 0
    with open(filename, 'r') as f:
        while True:
            currentline = f.readline()
            if currentline == '':
                # search the next five lines to see if they're all empty too
                for i in range(5):
                    probeline = f.readline()
                    if probeline != '':
                        endoffile = False
                        break
                    else:
                        endoffile = True
                if endoffile:
                    break
            lc +=1
            lines.append(currentline)

    print(f"Found {lc} lines...")
    with open(filename,'w') as f:
        f.write(f'{lc}\n')
        for line in lines:
            f.write(line)
    print("Written successfully")

if __name__ == "__main__":
    filename = sys.argv[1]
    add_linecount_to_top(filename)
