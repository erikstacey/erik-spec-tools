from spectra_io import import_lsd
import matplotlib.pyplot as pl
ROOT_LOC = '/Users/stacey/Documents/HD155273/HD155273_spectra 2/2019/'
LSDNAME = '/X2019.lsd'

if __name__ == "__main__":
    lsdprof = import_lsd(ROOT_LOC+LSDNAME)
    combfit = import_lsd(ROOT_LOC+LSDNAME+"_bin_fit_comb")
    fit1 = import_lsd(ROOT_LOC+LSDNAME+"_bin_fit_prof0")
    fit2 = import_lsd(ROOT_LOC + LSDNAME + "_bin_fit_prof1")
    pl.plot(lsdprof['vel'], lsdprof['stokesI'], color='black')
    pl.plot(combfit['vel'], combfit['stokesI'], color='red')
    pl.plot(fit1['vel'], fit1['stokesI'], color='blue', linestyle='--')
    pl.plot(fit2['vel'], fit2['stokesI'], color='green', linestyle='--')
    pl.show()