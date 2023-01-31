from spectra_io import import_lsd, save_lsd

def sub_stokesI(filename1, filename2, file_s):
    data1 = import_lsd(filename1)
    data2 = import_lsd(filename2)
    data1['stokesI'] = data2['stokesI']
    save_lsd(data1, file_s=file_s)