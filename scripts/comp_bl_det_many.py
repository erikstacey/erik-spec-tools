
import numpy as np
from idl_and_subprocesses import run_idl_cmd
import shutil
import os
from plot_lsd import plot_LSD_fit


def make_info_file(filename, bounds):
    # make the det_many and comp_bl files
    stripped_fname = filename.strip('.lsd')
    det_many_fname = f"{stripped_fname}_det_many_output.txt"
    print(f"Running run_det_many on {filename} and saving to {det_many_fname}")
    run_idl_cmd(f"run_det_many, '{filename}',vel={bounds}", file_s = det_many_fname)

    comp_bl_fname = f"{stripped_fname}_comp_bl_output.txt"
    print(f"Running comp_bl on {filename} and saving to {comp_bl_fname}")
    run_idl_cmd(f"comp_bl, '{filename}', 1.2, 500, lim_inp ={bounds}, norm = 1",file_s = comp_bl_fname)
    return comp_bl_fname, det_many_fname

def query_fixed_params(nstars):
    while True:
        fixed_params = input("Fix any parameters? y/n\n")
        if fixed_params == 'n':
            fixed_params = [0, 0, 0, 0]*nstars
            return fixed_params
        elif fixed_params == 'y':
            while True:
                fixed_params = input('Enter parameters (depth, RV, vsini, vmac..., 0 for unfixed)\n')
                fixed_params = fixed_params.strip(']').strip('[').split(',')
                fixed_params = [float(element.strip(' ')) for element in fixed_params]
                return fixed_params
            break

def make_fit_file(filename, nstars, fixed_params = None):
    fixed_params = input("Enter fixed params: (n if none):")

    if fixed_params is None or fixed_params == 'n':
        fixed_params = [0,0,0,0] * nstars
    stripped_fname = filename.strip('.lsd')
    fits_fname = stripped_fname + f"_fits_output.txt"
    temp_fits_fname = "fits_temp.txt"
    while True:
        while True:
            norm = input("Norm: ")
            if norm in ['0', '1', '2']:
                norm = int(norm)
                print(f"Norm set to {norm}")
                break
        with open(fits_fname, 'w') as f:
            f.write(f"Set of 3 fits to the LSD profile in {filename} - Generated using idl fit_lsd_binary,"
                    f" controlled by python script\n")
        for i in range(1,4):
            while True:
                print(f"Temporarily copying {fits_fname} to {temp_fits_fname}")
                shutil.copy(fits_fname, temp_fits_fname)
                print(f'Running fit {i}')
                run_idl_cmd(f"fit_lsd_binary, '{filename}', norm={norm}, nstars={nstars}, write_synth=1, fixa = {fixed_params}  & t=DIALOG_MESSAGE('Press OK to continue', center=1)",
                            file_s = fits_fname, append=True)
                #redo_fit = input("Redo fit? y/n")
                redo_fit = 'n'
                if redo_fit == 'y':
                    print(f"Restoring previous fit results from {temp_fits_fname}")
                    shutil.copy(temp_fits_fname,fits_fname)
                elif redo_fit == 'n':
                    # save the figure
                    plot_LSD_fit(filename,nstars,file_s = f"figures/fit_{i}", norm=norm)
                    break

        runagain = input("Run again? (y/n) \n")
        if runagain =='n':
            break
        os.remove(temp_fits_fname)
        print("3 fits performed and written to ", fits_fname)
    return fits_fname



def get_bl(fname):
    print(f"Retrieving bl measurement from {fname}")
    out_dict = {}
    with open(fname, 'r') as f:
        while True:
            currentline = f.readline()
            if not currentline:
                break
            if 'LSD Bl=' in currentline:
                splitline = currentline.split(' ')
                splitline = [element for element in splitline if element not in ['', ' ']]
                out_dict['Bl'] = float(splitline[2])
                out_dict['Bl_sigma'] = float(splitline[4])
                return out_dict
def get_fap(fname):
    print(f"Retrieving FAP measurement from {fname}")
    out_dict = {'fap_outside': None, 'fap': None}
    with open(fname, 'r') as f:
        count = 0
        while count<5:
            currentline = f.readline()
            if not currentline:
                count+=1
            if 'fap =' in currentline:
                splitline = currentline.split(' ')
                splitline = [element for element in splitline if element not in ['', ' ']]
                for i in range(len(splitline)):
                    if splitline[i]=='=':
                        currentfap = splitline[i+1]
                        if out_dict['fap_outside'] is None:
                            out_dict['fap_outside'] = float(currentfap)
                        else:
                            out_dict['fap'] = float(currentfap)
                            return out_dict

def get_fit_params(fname, nstars):
    print(f"Retrieving fit parameters from {fname}")
    out_dict = {}
    for i in range(nstars):
        for param in ['depth','rv', 'vsini','vmac']:
            out_dict[param+str(i)] = []
            out_dict[param+str(i)+'_std'] = 0.0
    with open(fname, 'r') as f:
        while True:
            currentline = f.readline()
            if currentline == '':
                for i in range(5):
                    currentline = f.readline()
                    endoffile = True
                    if currentline != '':
                        endoffile = False
                if endoffile:
                    break
            if "Fit for profile" in currentline:
                # identify which profile
                splitline = currentline.strip('\n').split(' ')
                currentprofile = int(splitline[-1].strip(' '))
                for param in ['depth', 'rv', 'vsini', 'vmac']:
                    currentline = f.readline()
                    splitline = currentline.split(' ')
                    splitline = [element for element in splitline if element not in [' ', '']]
                    measurement = float(splitline[2])
                    out_dict[param+str(currentprofile)].append(measurement)
                    print(f"Identified {param} for star{currentprofile} of {measurement}")
    # now convert to mean and std
    for i in range(nstars):
        for param in ['depth','rv', 'vsini', 'vmac']:
            out_dict[param+str(i)+'_std'] = np.std(out_dict[param+str(i)])
            out_dict[param+str(i)] = np.mean(out_dict[param+str(i)])

    return out_dict

def get_hjds():
    listofdicts = []
    # crawl current directory for .out files and collect some information from them
    filesindir = os.listdir()
    for file in filesindir:
        if file[-4:] == '.out':
            with open(file, 'r') as f:
                keepreading = True
                while keepreading:
                    currentline = f.readline()
                    if currentline == '':
                        for i in range(5):
                            currentline = f.readline()
                            if currentline != '':
                                keepreading = True
                                break
                            else:
                                keepreading = False

                    if 'Time of observations :' in currentline:
                        splitline = currentline.split(' ')
                        splitline = [element for element in splitline if element not in ['', ' ']]
                        cyear, cmonth, cday, ctime = splitline[4], splitline[5], splitline[6], splitline[9]
                        cdict = {'file': file, 'day': cday, 'month':cmonth, 'year':cyear, 'time': ctime}
                    if 'Heliocentric Julian date (UTC)' in currentline:
                        splitline = currentline.split(' ')
                        splitline = [element for element in splitline if element not in ['', ' ']]
                        chjd = splitline[5].strip('\n')
                        cdict['hjd'] = chjd
                listofdicts.append(cdict)
    if listofdicts == []:
        print("No .out files found... no HJDs/dates extracted")
        return None
    return listofdicts

def make_measurements_dict(int_limits, dv, bl_fname,det_many_fname, fitparams_fname, nstars):
    measurements_dict = {'int_limits_lower':int_limits[0],'int_limits_upper':int_limits[1],'vel_width':dv,}
    bl_dict = get_bl(bl_fname)
    fap_dict = get_fap(det_many_fname)
    measurements_dict.update(bl_dict)
    measurements_dict.update(fap_dict)
    measurements_dict.update(get_fit_params(fitparams_fname, nstars))

    hjd_dicts = get_hjds()

    return measurements_dict, hjd_dicts

def make_measurements_dict_blendedbinary(int_limits, dv, bl_fname,det_many_fname, nstars):
    measurements_dict = {'int_limits_lower':int_limits[0],'int_limits_upper':int_limits[1],'vel_width':dv,}
    bl_dict = get_bl(bl_fname)
    fap_dict = get_fap(det_many_fname)
    measurements_dict.update(bl_dict)
    measurements_dict.update(fap_dict)

    hjd_dicts = get_hjds()

    return measurements_dict, hjd_dicts



def write_measurements_dict(mdict, hjddicts, file_s, currentstar):
    print(f'Writing measurements to {file_s}...')
    with open(file_s, 'w') as f:
        f.write('Int limits,Int limits,Bl,sigma,FA prob,Vel width,Reg,v_rad,stdev,vsini,stdev,v_mac,stdev,v_tot,stdev\n')
        f.write(f"{mdict['int_limits_lower']:f},")
        f.write(f"{mdict['int_limits_upper']:f},")
        f.write(f"{mdict['Bl']:f},")
        f.write(f"{mdict['Bl_sigma']:f},")
        f.write(f"{mdict['fap']},")
        f.write(f"{mdict['vel_width']:f},")
        f.write("0.2,")
        f.write(f"{mdict[f'rv{currentstar}']:f},")
        f.write(f"{mdict[f'rv{currentstar}_std']:f},")
        f.write(f"{mdict[f'vsini{currentstar}']:f},")
        f.write(f"{mdict[f'vsini{currentstar}_std']:f},")
        f.write(f"{mdict[f'vmac{currentstar}']:f},")
        f.write(f"{mdict[f'vmac{currentstar}_std']:f},")
        f.write(f"{(mdict[f'vmac{currentstar}']**2 + mdict[f'vsini{currentstar}']**2)**0.5:f}")

        if hjddicts != None:
            # now write hjddicts stuff
            f.write('\n \n')
            for cdict in hjddicts:
                for key in cdict.keys():
                    f.write(cdict[key]+',')
                f.write('\n')
            # now write avg hjd
            numkeys = len(hjddicts[0].keys())
            numdicts = len(hjddicts)
            sumhjdtemp = 0.0
            for cdict in hjddicts:
                sumhjdtemp += float(cdict['hjd'])
            avg_hjd = sumhjdtemp/numdicts
            for i in range(numkeys-1):
                f.write(' ,')
            f.write(str(avg_hjd))
            f.write('\n')

    print('Complete')

def write_measurements_dict_2(currentstar, file_s, fits_dict = None, bl_dict = None):
    print(fits_dict)
    print(bl_dict)

    with open(file_s, 'w') as f:
        f.write(
            'Int limits,Int limits,Bl,sigma,FA prob,Vel width,Reg,v_rad,stdev,vsini,stdev,v_mac,stdev,v_tot,stdev\n')
        if bl_dict is not None:
            f.write(f"{bl_dict['int_limits_lower']:f},")
            f.write(f"{bl_dict['int_limits_upper']:f},")
            f.write(f"{bl_dict['Bl']:f},")
            f.write(f"{bl_dict['Bl_sigma']:f},")
            f.write(f"{bl_dict['fap']},")
            f.write(f"{bl_dict['vel_width']:f},")
            f.write("0.2,")
        else:
            f.write(', , , , , , ,')

        if fits_dict is not None:
            f.write(f"{fits_dict[f'rv{currentstar}']:f},")
            f.write(f"{fits_dict[f'rv{currentstar}_std']:f},")
            f.write(f"{fits_dict[f'vsini{currentstar}']:f},")
            f.write(f"{fits_dict[f'vsini{currentstar}_std']:f},")
            f.write(f"{fits_dict[f'vmac{currentstar}']:f},")
            f.write(f"{fits_dict[f'vmac{currentstar}_std']:f},")
            f.write(f"{(fits_dict[f'vmac{currentstar}'] ** 2 + fits_dict[f'vsini{currentstar}'] ** 2) ** 0.5:f}")

        else:
            f.write(', , , , , , ,')




def make_fit_file_bin(filename, nstars, fixed_params=None):
    if fixed_params is None:
        fixed_params = [0,0,0,0]*nstars

    stripped_fname = filename.strip('.lsd')
    fits_fname = stripped_fname + f"_fits_output.txt"
    temp_fits_fname = "fits_temp.txt"
    while True:
        while True:
            norm = input("Norm: ")
            if norm in ['0', '1', '2']:
                norm = int(norm)
                print(f"Norm set to {norm}")
                break
        with open(fits_fname, 'w') as f:
            f.write(f"Set of 3 fits to the LSD profile in {filename} - Generated using idl fit_lsd_binary,"
                    f" controlled by python script\n")
        for i in range(1,4):
            while True:
                print(f"Temporarily copying {fits_fname} to {temp_fits_fname}")
                shutil.copy(fits_fname, temp_fits_fname)
                print(f'Running fit {i}')
                run_idl_cmd(f"fit_lsd_binary, '{filename}', norm={norm}, nstars={nstars}, write_synth=1, fixa = {fixed_params}  & t=DIALOG_MESSAGE('Press OK to continue')",
                            file_s = fits_fname, append=True)
                #redo_fit = input("Redo fit? y/n")
                redo_fit = 'n'
                if redo_fit == 'y':
                    print(f"Restoring previous fit results from {temp_fits_fname}")
                    shutil.copy(temp_fits_fname,fits_fname)
                elif redo_fit == 'n':
                    # save the figure
                    plot_LSD_fit(filename,nstars,file_s = f"figures/fit_{i}", norm=norm)
                    break

        runagain = input("Run again? (y/n) \n")
        if runagain =='n':
            break
        os.remove(temp_fits_fname)
        print("3 fits performed and written to ", fits_fname)
    return fits_fname



if __name__ == "__main__":
    test = query_fixed_params(2)
    print(type(test))
    print(test)