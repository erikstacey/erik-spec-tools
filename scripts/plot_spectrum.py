import spectra_io as io
import matplotlib.pyplot as pl
def plot_spectrum(filename, bounds='None', save=False):
    data = io.import_spectrum(filename)
    pl.errorbar(data['wl'], data['stokesI'], data['error'])
    pl.xlabel('Wavelength')
    pl.ylabel('Flux')
    if not bounds == 'None':
        pl.xlim(bounds[0], bounds[1])
    if save:
        pl.savefig(f"analysis_figures/{filename}.png")
    else:
        pl.show(block=False)
        pl.pause(10000)

def plot_spectra(filenames, bounds='None', save=False):
    if type(filenames)!=list:
        use_filenames = [filenames]
    else:
        use_filenames = filenames
    for filename in use_filenames:
        data = io.import_spectrum(filename)
        pl.plot(data['wl'], data['stokesI'], label=filename)
        pl.xlabel('Wavelength')
        pl.ylabel('Flux')
    if not bounds == 'None':
        pl.xlim(bounds[0], bounds[1])
    if save:
        pl.savefig(f"analysis_figures/numerous_spectra.png")
    else:
        pl.legend()
        pl.show(block=False)
        pl.pause(10000)

def plot_spectra_V(filenames, bounds='None', save=False):
    for filename in filenames:
        data = io.import_spectrum(filename)
        pl.plot(data['wl'], data['stokesV'], label=filename)
        pl.xlabel('Wavelength')
        pl.ylabel('Flux')
    if not bounds == 'None':
        pl.xlim(bounds[0], bounds[1])
    if save:
        pl.savefig(f"analysis_figures/numerous_spectra.png")
    else:
        pl.legend()
        pl.show(block=False)
        pl.pause(10000)

if __name__ == "__main__":
    import sys
    cmdlnargs = sys.argv
    files_to_use = cmdlnargs[2:]
    if sys.argv[1] == '0':
        func = plot_spectra
    if sys.argv[1] == '1':
        func = plot_spectra_V
    print(cmdlnargs)
    if len(files_to_use) == 1:
        print(f"Plotting {files_to_use[0]}")
        func(files_to_use[0])
    else:
        print(f"Plotting {files_to_use}")
        func(files_to_use)