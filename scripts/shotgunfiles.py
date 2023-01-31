import os
import sys
from shutil import copy


def make_dir_and_cp(file):
    pwd = os.getcwd()
    for i in range(len(file)):
        if file[i] == '.':
            dirname = file[:i]
    try:
        os.mkdir(dirname)
        print(f'Made directory at ./{dirname}/')
    except FileExistsError:
        print(f"{pwd + '/' + dirname} already exists !")

    copy(pwd + '/' + file, pwd + '/' + dirname + '/' + file)
    print(f"Copied {pwd + '/' + file} to {pwd + '/' + dirname + '/' + file}")


files = sys.argv
files = files[1:]

for i in range(len(files)):
    make_dir_and_cp(files[i])

