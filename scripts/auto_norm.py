import idl_and_subprocesses as ias
import os



def norm_and_combine_spectra(files_to_use):
    ias.run_idl_cmd((f"meanspec, {files_to_use}"))
    ias.run_idl_cmd(f"norm_gui,'mean.s',file_s = 'mean.sN'")



if __name__ == '__main__':
    files_in_dir = os.listdir()
    files_to_use = [element for element in files_in_dir if '.s' in element and '.sN' not in element and element!='mean.s']
    all_dots = files_to_use
    keeprunning = True
    selectnewfiles = False
    while keeprunning:
        print('\n \n \n \n')
        if len(files_to_use)!=1:
            print('Norming and combining the following files:')
            for i in range(len(files_to_use)):
                print(f'\t {files_to_use[i]}')
            while True:
                choice = input("Proceed? y/n")
                if choice == 'y':
                    selectnewfiles = False
                    keeprunning = False
                    break
                if choice =='n':
                    keeprunning = True
                    selectnewfiles = True
                    break
            if keeprunning == False:
                norm_and_combine_spectra(files_to_use)

        elif len(files_to_use) == 1:

            print('Normalizing this file:')
            print(f"\t {files_to_use[0]}")
            while True:
                choice = input("Proceed? y/n")
                if choice == 'y':
                    selectnewfiles = False
                    keeprunning = False
                    break
                if choice == 'n':
                    selectnewfiles = True
                    keeprunning = True
                    break
            if keeprunning == False:
                ias.run_idl_cmd(f"norm_gui,'{files_to_use[0]}',file_s = '{files_to_use[0]+'N'}'")

        else:
            print("No .s files detected!")
            for element in files_in_dir:
                print(element)
            files_to_use = input("Enter files to use (separate by ,): ")
            files_to_use_split = files_to_use.split(',')
            if files_to_use_split == []:
                pass
            else:
                files_to_use = [element.strip(' ') for element in files_to_use_split]

        if selectnewfiles:
            for i in range(len(all_dots)):
                print(f'\t {i}: {all_dots[i]}')
            selected_indices = input('Enter files to use by number: ')
            if len(selected_indices) == 1:
                files_to_use = [all_dots[int(selected_indices)]]
            else:
                selected_indices = selected_indices.split(',')
                selected_indices = [int(element.strip(' ')) for element in selected_indices]
                files_to_use = []
                for i in range(len(selected_indices)):
                    print(f"current: {selected_indices[i]}")
                    selected_indices[i] = int(selected_indices[i])
                    files_to_use.append(all_dots[selected_indices[i]])
            print('New files to use:', files_to_use)




