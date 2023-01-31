import spectra_io as io

def avg_LSDs(filenames, file_s):
    averaged_dict = {}
    numfiles = len(filenames)
    for filename in filenames:
        currentdata = io.import_lsd(filename)
        try:
            for key in ['vel', 'stokesI', 'sigmaI', 'stokesV', 'sigmaV',
                        'null1', 'null1sigma', 'nullV', 'nullVsigma']:
                averaged_dict[key] += currentdata[key] / numfiles
        except KeyError:
            for key in ['vel', 'stokesI', 'sigmaI', 'stokesV','sigmaV',
                        'null1', 'null1sigma', 'nullV', 'nullVsigma']:
                averaged_dict[key] = currentdata[key] / numfiles
            for key in ['header1','header2']:
                averaged_dict[key] = currentdata[key]
    io.save_lsd(averaged_dict, file_s)

if __name__ == '__main__':
    working_dir = '/Users/stacey/Documents/normal_B_stragglers/hd19400/erik_analysis/15dec11'
    filenames_to_avg = ['hd19400_v_01.lsd', 'hd19400_v_02.lsd']
    avg_LSDs([f"{working_dir}/{filenames_to_avg[0]}", f"{working_dir}/{filenames_to_avg[0]}"], f"{working_dir}/avg.lsd")
