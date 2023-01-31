import os
import subprocess
import sys

def makenew_dir(topdir):
    print(f"Copying {topdir} to {topdir}_stripped")
    subprocess.run(['zsh', '-c', f'cp -R {topdir} {topdir}_stripped'])

def list_files(startpath, fileext):
    count = 0
    lenfileext = len(fileext)
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if fileext == '' or f[-lenfileext:] == fileext:
                print('{}{}'.format(subindent, f))
                count+=1
    if fileext != '':
        print(f"Found {count} files ending in {fileext}")
    else:
        print(f"Found {count} files")




if __name__ == '__main__':
    argv = sys.argv
    try:
        fileext = argv[1]
    except IndexError:
        fileext = ''
        print("No filename specified... listing everything")
    currentdir = os.getcwd()
    list_files(currentdir,fileext)