from idl_and_subprocesses import run_idl_cmd
import os

cdir = os.getcwd()
for root, dirs, files in os.walk(top=cdir):
    os.chdir(root)
    run_idl_cmd('process')