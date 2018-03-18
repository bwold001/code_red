import numpy as np
import h5py

with h5py.File('model/model_100.h5','r') as hdf:
    ls = list(hdf.keys())
    print(ls)
    data = hdf.get('dense_31')
    dataset1 = np.array(data)
    print (dataset1.shape)
