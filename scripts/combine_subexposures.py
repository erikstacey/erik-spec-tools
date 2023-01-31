import numpy as np
from spectra_io import import_subexposure

def combine_subexposures(filenames):
    datasets = []
    N = len(datasets[0]['wl'])
    curmeanI = np.zeros(N)
    curmeanV = np.zeros(N)
    for file in filenames:
        cdataset = import_subexposure(file)
        curmeanI += cdataset['stokesI']
        curmeanV += cdataset['stokesV']
    curmeanI /= len(filenames)
    curmeanV /= len(filenames)
    mean_dict = {'wl':cdataset['wl'], 'stokesI':curmeanI, 'stokesV':curmeanV,
                 }




if __name__ == '__main__':
    cdir = '/Users/stacey/Documents/normal_b_stars/kevin_stuff_erik/hd29248/27sep07_cadc/subexposures/'
    filenames = [cdir+'945935i.fits.s', cdir+'945936i.fits.s', cdir+'945937i.fits.s']
    combine_subexposures(filenames)
    curmeanV = np.zeros()
