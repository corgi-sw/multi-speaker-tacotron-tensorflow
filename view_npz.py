import numpy as np
import os

path = "./datasets/teacher/data/"
file_list = sorted(os.listdir(path))

idx = 1
for file_name in file_list:
    #npz = np.load(path + file_name)
    s = file_name.split('.')[1]
    if str(idx).zfill(4) != s:
        print(idx)
        break
    idx += 1

    # print(file_name)

    #tokens = npz['tokens']
    #linear = npz['linear']
    #loss_coeff = npz['loss_coeff']

    #if (file_name == 'Raw.0001.npz' or file_name == 'Raw.0004.npz' or file_name == 'Raw.0010.npz' or file_name == 'Raw.0007.npz'):
    #print(file_name)
    #print(loss_coeff)

#    print(file_name)
#    print(tokens)
#    print(len(tokens))
    
    #npz.close()
    # break