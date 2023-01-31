import numpy as np
from copy import copy
import os

def harps_mean(file, output):
    os.getcwd()
    # Using the first spectrum in the list as the template
    with open( file[0],'r') as f:
        title = f.readline().strip('\n')
    data1 = np.genfromtxt( file[0], names='wave, flux, V, N1, N2, err_I', skip_header=2 )
    order1 = np.where( data1[1:]['wave'] < data1[:-1]['wave'] )
    order1 = order1[0]
    order1 = np.append([0], order1)
    order1 = np.append(order1, data1.size)

    final = copy(data1)
    # weighted mean.
    # Sum_i  d_i / sig_i**2
    # ---------------------------
    #    Sum_i  1/sig_i**2

    # For the propagation of the error bars:
    #  e_i = sqrt( 1 / ( Sum_i 1 / sig_i**2 )  )

    final['flux'] = final['flux'] / data1['err_I']**2
    final['V'] = final['V'] / data1['err_I']**2
    final['N1'] = final['N1'] / data1['err_I']**2
    final['N2'] = final['N2'] / data1['err_I']**2

    # To keep track of the normalization factor in the mean
    weight_sum = 1.0 / data1['err_I']**2

    #fig, ax = plt.subplots(1,1)

    for d in range(1,len(file)):

        data = np.genfromtxt( file[d], names='wave, flux, V, N1, N2, err_I', skip_header=3 )
        order = np.where( data[1:]['wave'] < data[:-1]['wave'] )
        order = order[0]
        order = np.append([0], order)
        order = np.append(order, data.size)
        print(data.size)
        print(order)

        for o in range(0,order1.size-1):
        #for o in range(0,1):
    
            k1i = order1[o] # first index of order for data1
            k1f = order1[o+1] # last index of order for data 1
            #print('order {}: {} ({}) to {} ({})'.format(o, k1i,data1[k1i]['wave'], k1f, data1[k1f-1]['wave'] ))

            ki = order[o] # first index of order for the current data to add
            kf = order[o+1] # last index of order for the current data to add

            # Interpolate the err_I on the wavescale of the first data
            err = np.interp(data1[k1i:k1f]['wave'], data[ki:kf]['wave'], data[ki:kf]['err_I'])
            # Keep track of the sum of the weigths
            weight_sum[k1i:k1f] = weight_sum[k1i:k1f] + 1.0 / err**2

            # Interpolate the flux to the wavescale of the first data,
            # multiply by interpolated weigth,
            # and add to the summation
            final[k1i:k1f]['flux'] = ( final[k1i:k1f]['flux'] +
                    np.interp(data1[k1i:k1f]['wave'], data[ki:kf]['wave'], data[ki:kf]['flux']) /
                    err**2)
            # Do the same with the other columns
            final[k1i:k1f]['V'] = ( final[k1i:k1f]['V'] +
                    np.interp(data1[k1i:k1f]['wave'], data[ki:kf]['wave'], data[ki:kf]['V']) /
                    err**2)
            final[k1i:k1f]['N1'] = ( final[k1i:k1f]['N1'] +
                    np.interp(data1[k1i:k1f]['wave'], data[ki:kf]['wave'], data[ki:kf]['N1']) /
                    err**2)
            final[k1i:k1f]['N2'] = ( final[k1i:k1f]['N2'] +
                    np.interp(data1[k1i:k1f]['wave'], data[ki:kf]['wave'], data[ki:kf]['N2']) /
                    err**2)

            # Just for testing.
            #ax.plot(data1[k1i:k1f]['wave'], data1[k1i:k1f]['flux'])
            #ax.plot(data[ki:kf]['wave'], data[ki:kf]['flux'])
            #ax.plot(final[k1i:k1f]['wave'], final[k1i:k1f]['flux']/weight_sum[k1i:k1f], label='mean')

            #ax.plot(data1[k1i:k1f]['wave'], data1[k1i:k1f]['err_I'])
            #ax.plot(data[ki:kf]['wave'], data[ki:kf]['err_I'])
            #ax.plot(final[k1i:k1f]['wave'], 1/weight_sum[k1i:k1f]**0.5, label='mean')

    ## Making the normalization
    final['flux'] = final['flux'] / weight_sum
    final['V'] = final['V'] / weight_sum
    final['N1'] = final['N1'] / weight_sum
    final['N2'] = final['N2'] / weight_sum

    # overriding the error with the new weigthed error
    final['err_I'] = 1.0 / weight_sum**0.5

    #ax.plot(data1['wave'], data1['flux'])
    #ax.plot(final['wave'], final['flux'], label='final')
    #ax.legend()
    #plt.show()

    f = open(output, 'w')
    f.write('{}\r'.format(title) )
    f.write('{} {}\r'.format(final.size, 6))
    for i in range(0, final.size):
        f.write('{} {} {} {} {} {}\r'.format(final[i]['wave'], final[i]['flux'],final[i]['V'],final[i]['N1'],final[i]['N2'], final[i]['err_I']  ) )

    f.close()

def gen_diagnostic_spectrum(file_s, sectionlens, section1, section2, sigma):
    with open(file_s,'w') as f:
        f.write('*** Reduced spectrum of nothing\n')
        f.write(f'3*{sectionlens}')
        for i in range(sectionlens):
            f.write("{} {} {} {} {} {}\n".format(i, section1, section2, section1, section1, sigma))
        for i in range(sectionlens, 2*sectionlens):
            f.write("{} {} {} {} {} {}\n".format(i, section1, section2, section1, section1, 3*sigma))
        for i in range(2*sectionlens, 3*sectionlens):
            f.write("{} {} {} {} {} {}\n".format(i, section2, section1, section1, section1, 2*sigma))

if __name__ == "__main__":
    from sys import argv
    files_to_use = argv[1:]
    harps_mean(files_to_use, 'mean.s')


