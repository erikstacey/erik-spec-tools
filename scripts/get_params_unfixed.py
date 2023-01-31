from comp_bl_det_many import get_fit_params
from os import listdir

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

current_dir_files = listdir()
if 'erik_fits_output.txt' in current_dir_files:
    filename = 'erik_fits_output.txt'
else:
    for f in current_dir_files:
        if '_fits_output.txt' in f:
            filename = f
            break

length_of_file = file_len(filename)
print(length_of_file)
nstars = (length_of_file - 16) // 42
print(f"Number of stars identified: {nstars}")

fit_params = get_fit_params(filename, nstars)

listparams = []
listparams_fixedrv = []
for i in range(nstars):
    for param in ['depth', 'rv', 'vsini', 'vmac']:
        listparams.append(fit_params[param+str(i)])
        if param == 'rv':
            listparams_fixedrv.append(0)
        else:
            listparams_fixedrv.append(fit_params[param + str(i)])

print(listparams)
print('With fixed RVs:')
print(listparams_fixedrv)
