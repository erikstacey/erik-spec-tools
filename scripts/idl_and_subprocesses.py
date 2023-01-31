import subprocess
import os

def get_ls():
    listofstuff = os.listdir()
    for element in listofstuff:
        print(element)

def get_displayenv_loc():
    return subprocess.check_output(['tcsh','-c','echo $DISPLAY']).decode('utf-8').strip('\n')

def run_idl_cmd(command, file_s = None, append=False, suppress_xquartz = False):
    print(f"[IDL] Running {command}")
    if suppress_xquartz:
        localDISPLAYENV = 'Display connection suppressed in run_idl_cmd python script'
    else:
        localDISPLAYENV = DISPLAYENV
    idl_alias = '/Applications/harris/envi56/idl88/bin/idl/'
    if file_s == None:
        subprocess.run(['zsh', '-c', f'{idl_alias} -e "{command}"'],
                       env={'IDL_PATH': '/Applications/itt/idl/:/Applications/itt/idl/lib/:~/idlcodes',
                            'DISPLAY': localDISPLAYENV})
    elif append:
        subprocess.run(['zsh', '-c', f'{idl_alias} -e "{command}" >> {file_s}'],
                       env={'IDL_PATH': '/Applications/itt/idl/:/Applications/itt/idl/lib/:~/idlcodes',
                            'DISPLAY': localDISPLAYENV})
    else:
        subprocess.run(['zsh', '-c', f'{idl_alias} -e "{command}" 2>&1 | tee {file_s}'],
                       env={'IDL_PATH': '/Applications/itt/idl/:/Applications/itt/idl/lib/:~/idlcodes',
                            'DISPLAY': localDISPLAYENV})

global displayenv_loc
DISPLAYENV = get_displayenv_loc()