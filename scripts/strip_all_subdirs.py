import os
import subprocess

def makenew_dir(topdir):
    print(f"Copying {topdir} to {topdir}_stripped")
    subprocess.run(['zsh', '-c', f'cp -R {topdir} {topdir}_stripped'])

def strip_all_subdirs(filetype, topdir):
    extensionlength = len(filetype)
    makenew_dir(topdir)
    for dir, _, files in os.walk(top=topdir+"_stripped"):
        for file in files:
            if file[-extensionlength:] == filetype:
                with open(dir+"/"+file,'w') as f:
                    f.write("Overwritten placeholder")




strip_all_subdirs('.s', '/Users/stacey/Documents/test_dirs/hd19400_copy')