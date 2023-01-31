import make_mask_core
import sys
import subprocess
import os

def get_displayenv_loc():
    return subprocess.check_output(['tcsh', '-c', 'echo $DISPLAY']).decode('utf-8').strip('\n')





def make_mask_main(filename):
    make_mask_loc = '~/iLSD/make-masks-vald3-0.1/'
    make_mask_core.make_mask(filename,make_mask_loc)


global DISPLAYENV
DISPLAYENV = get_displayenv_loc()

if __name__ == "__main__":
    cmdlnargs = sys.argv
    vald_fname = cmdlnargs[1]
    make_mask_main(vald_fname)