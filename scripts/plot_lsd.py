import spectra_io as io
import os
import sys
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit
import numpy as np

def mute():
    f = open(os.devnull, 'w')
    sys.stdout = f

def plot_LSD(filename,bounds='None', vlines='None', savename=False, suppress = False):
    print("VLINES BEING ADDED ARE:", vlines)
    if suppress:
        mute()
    print(f"Plotting {filename}")
    data = io.import_lsd(filename)
    _, axs = pl.subplots(2)
    axs[0].plot(data['vel'], data['stokesI'])
    axs[1].plot(data['vel'], data['stokesV'])
    if not bounds == 'None':
        pl.xlim(bounds[0], bounds[1])
    if not vlines == 'None':
        for element in vlines:
            axs[0].axvline(element, color='red')
            axs[1].axvline(element, color='red')
    if savename != False:
        try:
            os.mkdir('figures')
        except FileExistsError:
            pass
        pl.savefig(f"figures/{savename}")
        pl.clf()
    else:
        pass
        pl.pause(10000)
        pl.clf()

def linmodel(x, m, b):
    return m*x+b

def plot_LSD_fit(LSDfname, nstars, file_s = None, norm=1):
    print(f"Plotting LSD fit with norm = {norm} and saving to {os.getcwd()}/{file_s}")
    data = io.import_lsd(LSDfname)
    # perform linear fit and normalize using the f
    if norm == 1:
        firstlast10_x = np.append(data['vel'][:10], data['vel'][-10:])
        firstlast10_y = np.append(data['stokesI'][:10], data['stokesI'][-10:])
        params, _ = curve_fit(linmodel,firstlast10_x, firstlast10_y)
        model = linmodel(data['vel'],*params)
        #pl.plot(firstlast10_x, firstlast10_y)
        #pl.plot(data['vel'], data['stokesI'])
        data['stokesI'] = data['stokesI'] + (1-model)
        #pl.plot(data['vel'], model, label='linmod')
    if norm == 2:
        firstlast10_x = [max(data['vel'][:10]), max(data['vel'][-10:])]
        firstlast10_y = [max(data['stokesI'][:10]), max(data['stokesI'][-10:])]
        params, _ = curve_fit(linmodel, firstlast10_x, firstlast10_y)
        model = linmodel(data['vel'], *params)
        # pl.plot(firstlast10_x, firstlast10_y)
        # pl.plot(data['vel'], data['stokesI'])
        data['stokesI'] = data['stokesI'] + (1 - model)

    if norm in [1,2]:
        label1 = 'Profile (norm)'
    else:
        label1 = 'Profile'

    pl.plot(data['vel'], data['stokesI'], color='black', label=label1)
    if nstars != 1:
        for i in range(nstars):
            data = io.import_lsd(LSDfname+f"_bin_fit_prof{i}")
            pl.plot(data['vel'], data['stokesI'], label=f'Fit star {i}')

    data = io.import_lsd(LSDfname+"_bin_fit_comb")
    pl.plot(data['vel'], data['stokesI'], color='red', label=f'Combined fit')
    pl.legend()
    pl.xlabel("Vel [km s^-1]")
    if file_s is None:
        pl.show()
    else:
        pl.savefig(file_s)
        pl.clf()

if __name__ == '__main__':
    testpath = '/Users/stacey/Documents/test_dirs/fit_lsd_binary_demo_3'
    LSDfname = testpath + '/lowdensity.lsd'
    fitfname = LSDfname+'_bin_fit_comb'

    data = io.import_lsd(LSDfname)
    fit = io.import_lsd(fitfname)

    #pl.plot(data['vel'], data['stokesI'], '.')
    pl.plot(fit['vel'], fit['stokesI'], marker='.', label='Fit')

    for i in range(len(fit['stokesI'])):
        if fit['stokesI'][i] == min(fit['stokesI']):
            pl.axvline(fit['vel'][i])
            break
    pl.axvline(4.9210507, color='orange', label='rv from fit')
    pl.legend()
    pl.show()