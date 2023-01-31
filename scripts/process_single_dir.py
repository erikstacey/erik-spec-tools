'''
NAME: process_single_dir.py
;
; PURPOSE: Automatically generate LSD profiles for and extract longitudinal field measurements, FAPs, and radial velocity/vmac components
        from espadons, narval, or harpspol spectra.

; INPUTS:
files_to_use: The filenames of the spectra to use (with extensions)

maskname: The filename of the mask to use

int_width: The bounds to use when generating LSD profiles. The bounds of integration for Bl calcs are set by the user
during runtime
nstars: Number of stars in system

; CALLING SEQUENCE:
process_single_dir.py, files_to_use, maskname, int_width, nstars
; OUTPUTS:
For single spectra:
    [filename].lsd: LSD profile corresponding to that spectrum.
for multiple spectra:
    mean.lsd: LSD profile corresponding to the co-addition of the unnormalized spectra OR LSD profiles
Always:
    [filename]_comp_bl_output.txt: Logged terminal output from comp_bl
    [filename]_det_many_output.txt: Logged terminal output from run_det_many
    [filename]_fits_output.txt: Logged terminal output from running 3 iterations of fit_lsd_single
    [filename]_fullmeasurements.csv:

    Figures of each LSD profile in the /figures/ directory

; EXAMPLE:

Using shell window in directory with the spectra and mask, with an alias set to the location of this program:
process_single_dir_py "hd19400_v_01.s,hd19400_v_02.s" "14000.mask3" "-300,300" 1

; METHOD:
PUT THE LINE "export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES" IN .zshrc IN YOUR HOME DIRECTORY
IF YOU'RE USING A VIRTUALENV YOU NEED TO SET THIS ENVIRONMENT VARIABLE

For single spectrum:
    -if unnormalized, runs norm_gui and saves normalized spectrum with [filename].sN extension
    -runs ilsd to generate a temp lsd profile and displays, then prompts user to enter bounds for bl integration
    -generates LSD profile for the spectrum with 20 pixels across the bl integration range and saves to '[filename].lsd'

For multiple unnormalized spectra:
    -Sums all the spectra and saves sum spectrum to "mean.s". Then runs norm_gui to normalize and generate "mean.sN"
    -runs ilsd to generate a temp lsd profile and displays, then prompts user to enter bounds for bl integration
    -generates LSD profile for the mean spectrum with 20 pixels across the bl integration range, saving to 'mean.lsd'

For multiple normalized spectra:
    -Generates a sample lsd profile using the first spectrum, and prompts user to enter bounds for bl integration
    -Combines the normalized spectra using veronique's harps_mean.py code and computes an lsd profile at 'mean.lsd'

Then, for all types:
-Runs comp_bl/run_det_many on the working lsd profile (mean.lsd if multiple, [filename].lsd if single) and
saves the output to [filename]_comp_bl_output.txt and [filename]_det_many_output.txt.
-Runs fit_lsd_single 3 times and saves the output to [filename]_fits_output.txt. This step requires user input.

Then, grabs all the information from each .txt file and collects it into a csv file ([filename]_fullmeasurements.csv),
and opens it in excel. The excel output should be directly copy-able from the opened window into the google sheet.

; REVISON HISTORY:
;       written by Erik Stacey, 2020
'''

'''
normalized = True

working_directory = '/Users/stacey/Documents/test_dirs/multiple_norm'
files_to_use = ['hd19400_v_01.s', 'hd19400_v_02.s']
maskname = '14000.mask3'
int_width = [-100,100]
nstars=1
'''

import os, sys
from plot_lsd import plot_LSD
from multiprocessing import Process
from comp_bl_det_many import *
import subprocess
from idl_and_subprocesses import get_displayenv_loc, run_idl_cmd
import logging
import matplotlib.pyplot as pl
from interactive_matplotlib import plot_and_collect_xvals
from spectra_io import import_lsd


def get_ls(ext=None, ifin=None):
    listofstuff = os.listdir()
    if ext is None and ifin is None:
        for element in listofstuff:
            print(f"\t{element}")
    else:
        for element in listofstuff:
            if ext is not None and ext == element[-len(ext):]:
                print(f"\t{element}")
            elif ifin is not None and ifin in element:
                print(f"\t{element}")


def compute_many_LSD(files_to_use, maskname, dv='', ):
    for filename in files_to_use:
        filename_s = filename.replace('.s', '.lsd')
        if dv == '':
            run_idl_cmd(f"run_ilsd, '{filename}', '{maskname}', '{filename_s}', ncpu=4, reg=0.2")
        else:
            run_idl_cmd(f"run_ilsd, '{filename}', '{maskname}', '{filename_s}', ncpu=4, reg=0.2, dv={dv}")


def identify_bounds(lsd_filename, nstars):
    lsd_data = import_lsd(lsd_filename)
    xvals = plot_and_collect_xvals(lsd_data['vel'], lsd_data['stokesI'], nstars)
    pairedxvals = []
    for i in range(len(xvals)):
        if i % 2 == 0:  # Even element; First element
            curpair = [round(xvals[i],1), None]
        else:
            curpair[1] = round(xvals[i],1)
            pairedxvals.append(curpair)
    return pairedxvals

def get_files_to_use():
    currentdir = os.listdir()
    # count number of .sN files
    potentials = []
    for file in currentdir:
        if (len(file) >= 3 and file[-3:] == '.sN') or (len(file) >= 5 and file[-5:] == '.s_Ic'):
            potentials.append(file)
    print(potentials)
    if len(potentials) == 1:
        usefile = input(f"Spectrum file found at {potentials[0]}... use? \n")
        if usefile == 'y':
            return potentials[0]
    elif len(potentials) != 0:
        for i in range(len(potentials)):
            print(f"\t {i}: {potentials[i]}")
        print('\n\n')
        selector = input(f"Select a file above, if none suitable select -1\n")
        if selector == '-1':
            print("Printing whole directory...")
        else:
            return potentials[int(selector)]
    for i in range(len(currentdir)):
        print(f"\t {i}: {currentdir[i]}")
    selector = input(f"Select a spectrum file above\n")
    return currentdir[int(selector)]


def query_use(fname, ftype):
    while True:
        query = input(f'{ftype} file found at {fname}, use? y/n \n')
        if query == 'y':
            return True
        elif query == 'n':
            return False


def get_mask(defaultmask):
    maskfile = defaultmask
    currentdir = os.listdir()
    potentials = []
    for file in currentdir:
        if '.s' not in file and 'mask' in file:
            potentials.append(file)

    if len(potentials) == 1:
        use = query_use(potentials[0], 'Mask')
        if use:
            return potentials[0]
    elif len(potentials) != 0:
        for i in range(len(potentials)):
            print(f"\t{i}: {potentials[i]}")
        print('\n')
        selection = input("Select a mask file to use (-1 if none): ")
        if selection != '-1':
            return potentials[int(selection)]
    while True:
        for i in range(len(currentdir)):
            print(f"\t{i}: {currentdir[i]}")
        print('\n')
        selection = input('Select a mask file to use: ')
        use = query_use(currentdir[int(selection)])
        if use:
            return currentdir[int(selection)]


def get_intrange(defaultrange):
    while True:
        intrangeinp = input("Enter int range (Press enter for default, or use format x1, x2): ")
        if intrangeinp == '':
            return defaultrange
        else:
            intrange = intrangeinp.split(',')
            if intrange == intrangeinp or len(intrange) != 2:
                print("Invalid input...")
                continue
            intrange[1] = intrange[1].strip(' ')
            intrange[0] = float(intrange[0])
            intrange[1] = float(intrange[1])
            return intrange


def get_nstars():
    while True:
        nstars = input('Enter number of stars (int): ')
        try:
            nstars = int(nstars)
            return nstars
        except ValueError:
            print("Invalid input...")

def check_for_lsd(lsdname):
    curdir = os.listdir()
    if lsdname in curdir:
        return query_use(lsdname, 'Lsd')
    else:
        return False



global DISPLAYENV
DISPLAYENV = get_displayenv_loc()

if __name__ == '__main__':

    ##################################################################################################################
    # get information
    get_ls()
    filename = get_files_to_use()
    maskname = get_mask('mask.dat_cln_twk_cln_twk')

    nstars = get_nstars()



    ##################################################################################################################
    ## Make LSD profile
    lsd_nodv_noreg = 'erik_lsd_nodv_noreg.lsd'
    LSDpresent = check_for_lsd(lsd_nodv_noreg)
    if not LSDpresent:
        int_width = get_intrange([-300, 300])
        run_idl_cmd(f"run_ilsd, '{filename}', '{maskname}', '{lsd_nodv_noreg}', ncpu=4, lim={int_width}")
    else:
        temp_lsd = import_lsd('erik_lsd_nodv_noreg.lsd')
        int_width = [temp_lsd['vel'][0], temp_lsd['vel'][-1]]
        print(f'Int range discovered: {int_width}')


    ##################################################################################################################
    ## Fitting routine
    run_fits = input("Run fitting routine? y/n \n")
    if run_fits == 'y':
        os.makedirs('figures', exist_ok=True)
        fits_fname = make_fit_file(lsd_nodv_noreg, nstars=nstars)
        fitsdict = get_fit_params(fits_fname, nstars)
    else:
        fitsdict = None

    ##################################################################################################################
    ## Get comp_bl information

    run_compbl_detmany = input('Get FAP and Bl measurements? y/n \n')
    if run_compbl_detmany == 'y':
        blcomplims = identify_bounds(lsd_nodv_noreg, nstars)


    for i in range(nstars):

        ##################################################################################################################
        ## Get comp_bl information

        if run_compbl_detmany == 'y':
            cblcomplims = blcomplims[i]
            dv = (cblcomplims[1] - cblcomplims[0]) / 20
            clsdname = f'erik_lsd_dvreg_star{i}.lsd'
            run_idl_cmd(
                f"run_ilsd, '{filename}', '{maskname}', '{clsdname}', ncpu=4, reg=0.2, dv={dv}, lim={int_width}")
            plot_LSD(clsdname, vlines = cblcomplims, savename = f'lsdstar{i}')
            bl_fname, det_many_fname = make_info_file(clsdname, bounds=cblcomplims)
            bldict = get_bl(bl_fname)
            bldict.update(get_fap(det_many_fname))
            bldict['int_limits_lower'] = cblcomplims[0]
            bldict['int_limits_upper'] = cblcomplims[1]
            bldict['vel_width'] = dv
        else:
            bldict = None #  write nothing for bl stuff

        write_measurements_dict_2(i, f'fullmeasurements_newroutine_star{i}.csv', fits_dict = fitsdict, bl_dict=bldict)






    for i in range(nstars):
        subprocess.run(['zsh', '-c', f"open fullmeasurements_newroutine_star{i}.csv -a 'Microsoft Excel'"])
