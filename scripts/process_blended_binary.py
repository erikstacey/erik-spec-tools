from spectra_io import import_lsd, save_lsd
from process_single_dir import *
from comp_bl_det_many import *
from sub_stokesI import sub_stokesI

global displayenv_loc
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
    for i in range(nstars):

        ##################################################################################################################
        ## Get comp_bl information

        if run_compbl_detmany == 'y':
            dv = 0.0
            clsdname = f'erik_lsd_star{i}_fitforcompbl.lsd'
            sub_stokesI('erik_lsd_nodv_noreg.lsd', f'erik_lsd_nodv_noreg.lsd_bin_fit_prof{i}', clsdname)
            cblcomplims = identify_bounds(f'erik_lsd_star{i}_fitforcompbl.lsd', 1)
            cblcomplims = cblcomplims[0]
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
