import time
import numpy as np
import os
import sys

def load_raw_data(data_path, mpi=False):
    """ 
    This file contain one function only.
    The load_raw_data function is used to load data from a directory using np.loadtxt, with or without mpi.
    
    Often loading massive data and with multiple files is slow, with multiple cores, one can load multiple data at the same time or even split your data

    If you use mpi, core 0 will do merging of data, other cores will load data from file evenly. 
    (except the last core will take one more per total number of core  if you have number of file more than total number of cores.)

    Parameters
    ----------
    data_path: directory where the data is located
    mpi: True/False 
            True if you want to use mpi.

    Returns
    -------
    data: a numpy array/matrix
    file_names:str array 
        the names of all files.

    Examples
    --------
    >>> data_path = './data'
    >>> data, file_names = load_raw_data(data_path)
    >>> data, file_names = load_raw_data(data_path, mpi = True)

    """

    # Get a list of all file names in the directory
    file_names = os.listdir(data_path)
    # Get each file name into a list
    number_of_files = [os.path.join(data_path, name) for name in file_names]

    data = []
    if mpi==True:
        # load mpi
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        total_ranks = comm.Get_size()
        # distributing files to cores almost evenly
        for i, filename in enumerate(number_of_files): 
            j = np.mod(i, total_ranks) 
            if j == 0: # never get 0
                j = total_ranks - 1 # distribute it to the last core
            if rank == j:
                print(f'\ncore {rank} is loading "{filename}" ...')
                t0 = time.time()
                rankload = np.loadtxt(filename)
                t1 = time.time()
                t = int(t1 - t0)
                print(f' loaded "{filename}" ..., it took: {t}s')
                comm.send(rankload, dest=0) # send the data to 0
            elif rank == 0: # core 0 for merging data only
                rankload = comm.recv(source=j)
                data.append(rankload)
                print("core", rank, "is merging files")
    else:
        rank = 0 # just a value convenience for not using mpi
        for filename in number_of_files:
            print(f' \nloading "{filename}" ...')
            t0 = time.time()
            data.append(np.loadtxt(filename))
            print('This file has' , np.loadtxt(filename).shape[0], 'number of pions')
            t1 = time.time()
            t = int(t1-t0)
            print(f' loaded "{filename}" ..., it took:{t}s')

       
    # Cut to the minimum row and merge data
    # same code below for both mpi and non-mpi
    if rank == 0:
        print("\n merging all files")
        min_line = min(len(d) for d in data)
        data_np = np.stack([d[:min_line, :] for d in data], axis=0)
        data = np.array(data_np)
        print("The data is in numpy format and with the shape of (files, row, column)", data.shape)
        for i, name in enumerate(file_names):
            file_names[i]='f'+str(i)
            print("Renamed file name: ", name, " ---> ", file_names[i])
    else:
        sys.exit() # close all other cpus


    return data, file_names