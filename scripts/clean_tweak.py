
from idl_and_subprocesses import run_idl_cmd
from process_single_dir import get_intrange, get_mask, get_files_to_use


def clean_tweak_cycle(mask, spectrum, lsdbounds):
    run_idl_cmd(f"run_ilsd, '{spectrum}', '{mask}', 'temp.lsd', ncpu=4, lim={lsdbounds}")
    run_idl_cmd(f"mask_gui, '{mask}', 'temp.lsd', '{spectrum}', 0.1")

if __name__ == "__main__":
    lsdbounds = get_intrange([-300, 300])
    spectrum_to_use = get_files_to_use()

    maskfile = get_mask('mask.dat')

    print(f"Running clean/tweak cycle on {spectrum_to_use} with mask {maskfile} using LSD bounds {lsdbounds}")
    keepclntwking = True

    while keepclntwking:
        clean_tweak_cycle(maskfile,spectrum_to_use, lsdbounds)
        maskfile = maskfile + '_cln_twk'
        while True:
            choice = input("Cont? y/n \n")
            if choice == 'y':
                break
            if choice == 'n':
                keepclntwking = False
                break
