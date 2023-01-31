import numpy as np

def import_spectrum(filename):
    print(f'Importing {filename}...')
    wl, stokesI, stokesV, N1, N2, error = [],[],[],[],[],[]
    with open(filename, 'r') as f:
        # skip header
        f.readline()
        f.readline()
        while True:
            currentline = f.readline().strip('\n')
            # check to see we haven't reached the end of the file
            if not currentline:
                break
            splitline = currentline.split(' ')
            splitline = [element for element in splitline if element not in ['',' ']]
            cwl = float(splitline[0])
            cstokesI = float(splitline[1])
            cstokesV = float(splitline[2])
            cN1 = float(splitline[3])
            cN2 = float(splitline[4])
            cerror = float(splitline[5])

            wl.append(cwl)
            stokesI.append(cstokesI)
            stokesV.append(cstokesV)
            N1.append(cN1)
            N2.append(cN2)
            error.append(cerror)
    print('Successfully imported')
    return {'wl': wl, 'stokesI': stokesI, 'stokesV': stokesV, 'error':error}

def import_subexposure(filename):
    print(f'Importing {filename}...')
    wl, stokesI, stokesV, N1, N2, error = [],[],[],[],[],[]
    with open(filename, 'r') as f:
        # skip header
        f.readline()
        f.readline()
        while True:
            currentline = f.readline().strip('\n')
            # check to see we haven't reached the end of the file
            if not currentline:
                break
            splitline = currentline.split(' ')
            splitline = [element for element in splitline if element not in ['',' ']]
            cwl = float(splitline[0])
            cstokesI = float(splitline[1])
            cstokesV = float(splitline[2])

            wl.append(cwl)
            stokesI.append(cstokesI)
            stokesV.append(cstokesV)

    print('Successfully imported')
    return {'wl': wl, 'stokesI': stokesI, 'stokesV': stokesV, 'error':error}

def import_lsd(filename):
    print(f'Importing {filename}...')
    with open(filename, 'r') as f:
        header1 = f.readline()
        header2 = f.readline()
        data = {'vel':[],
                'stokesI':[],'sigmaI':[],
                'stokesV':[],'sigmaV':[],
                'null1':[],'null1sigma':[],
                'nullV':[],'nullVsigma':[],
                'header1':header1, 'header2':header2}
        while True:
            currentline = f.readline().strip('\n').strip(' ')
            if currentline == '':
                break
            line_elements = currentline.split(' ')
            line_elements = [element for element in line_elements if element!='']
            for i in range(len(line_elements)):
                line_elements[i] = float(line_elements[i].strip(' '))
            data['vel'].append(line_elements[0])
            data['stokesI'].append(line_elements[1])
            data['sigmaI'].append(line_elements[2])
            data['stokesV'].append(line_elements[3])
            data['sigmaV'].append(line_elements[4])
            data['null1'].append(line_elements[5])
            data['null1sigma'].append(line_elements[6])
            data['nullV'].append(line_elements[7])
            data['nullVsigma'].append(line_elements[8])
        for key in data.keys():
            if key not in ['header1', 'header2']:
                data[key]=np.array(data[key])
        return data

def save_spectrum(stokesdict, fname):
    print(f'Writing to {fname}')
    with open(fname, 'w') as f:
        f.write('This file was written from a python script')
        f.write(' ')
        for i in range(len(stokesdict['wl'])):
            f.write(f"{stokesdict['wl'][i]} ")
            f.write(f"{stokesdict['stokesI'][i]} ")
            f.write(f"{stokesdict['stokesIerr'][i]} ")
            f.write(f"{stokesdict['stokesV'][i]} ")
            f.write(f"{stokesdict['stokesVerr'][i]}\n")
    print('Successfully written')

def save_lsd(data, file_s):
    print(f'Writing to {file_s}')
    with open(file_s, 'w') as f:
        f.write(data['header1'])
        f.write(data['header2'])
        for i in range(len(data['vel'])):
            f.write(f"{data['vel'][i]} ")
            f.write(f"{data['stokesI'][i]} ")
            f.write(f"{data['sigmaI'][i]} ")
            f.write(f"{data['stokesV'][i]} ")
            f.write(f"{data['sigmaV'][i]} ")
            f.write(f"{data['null1'][i]} ")
            f.write(f"{data['null1sigma'][i]} ")
            f.write(f"{data['nullVsigma'][i]} ")
            f.write(f"{data['nullVsigma'][i]}\n")