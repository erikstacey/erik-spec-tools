from process_single_dir import *




global displayenv_loc
DISPLAYENV = get_displayenv_loc()


if __name__ == '__main__':
    get_ls()
    filename = get_files_to_use()
    maskname = get_mask('mask.dat_cln_twk_cln_twk')
    int_width = get_intrange([-300, 300])
    nstars = get_nstars()



    print(f"Working dir is {os.getcwd()}")
    current_multiprocs = []
    #step 1*: compute init LSD...
    run_idl_cmd(f"run_ilsd, '{filename}', '{maskname}', 'erik_lsd_noreg_nobin.lsd', ncpu=4, lim={int_width}")
    # now look at temp lsd profile, and select appropriate bounds for comp_bl and run_det_many
    fits_fname = make_fit_file(lsd_filename, nstars=nstars)

    for i in range(nstars):
        fit_dict = get_fit_params(fits_fname, 2)


    for i in range(nstars):
        subprocess.run(['zsh', '-c', f"open fullmeasurements_star{i}.csv -a 'Microsoft Excel'"])

