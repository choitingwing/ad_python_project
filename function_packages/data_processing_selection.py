# changing columns of the data
import numpy as np

def changing_data(data, r_maxmax=30, theta_maxmax=60e-3):
    """ 
    This function is to tranforming the original data column to the data column you want.
    It also served a transitional data to hold some data column which just for data selection until data selection

    Parameters
    ----------
    data: np.array
        original data
    r_maxmax: float
        just a value for the calculation you want, here it set the maxiumn radius
        theta_maxmax has the same function, you can add more.

    Returns
    -------
    all_data: a numpy array/matrix
    
    Examples
    --------
    >>> all_data = changing_data(data, r_maxmax, theta_maxmax)

    """
    total_number_of_files =len(data)
    line = len(data[1])
    all_data = np.empty([total_number_of_files, line, 10])

    # add the new variables (columns) you want
    variable_names = ['x', 'y', 'r', 'emission_angle', 'Px', 'Py', 'Pz', 'P', 'PDGid', 'emission_angle_max']
    print( '\n Change the data columns into' , variable_names)
    
    for i, name in enumerate(variable_names):
        globals()[name] = all_data[:,:,i]  # You can assign any value here, create variable based on variable_names
    
    #  calculating the values for each new column    
    for i in range(total_number_of_files):
        factor = 1000 
        Px[i], Py[i], Pz[i]= data[i,:,3]*factor, data[i,:,4]*factor, data[i,:,5]*factor
        P[i] = np.sqrt(Pz[i]**2+Px[i]**2+Py[i]**2)

        x[i], y[i] = data[i,:,0], data[i,:,1]
   
        r[i] = np.sqrt(x[i]**2 + y[i]**2)
        emission_angle[i]  = np.arctan( np.sqrt(Px[i]**2+Py[i]**2)/Pz[i] )

        emission_angle_max[i] = theta_maxmax * np.sqrt( 1-(r[i]/r_maxmax)**2 ) # this column is transitional , set the maxiumn emission angle for each r
        PDGid[i] =  data[i,:,7]
    emission_angle_max[np.isnan(emission_angle_max)] = 0 
    return all_data
    

def generate_selected_data(all_data, cut_list):
    """ 
    This function is to generating data column with selection of data (fancing indexing).
    It also served a transitional data to hold some data column which just for data selection until data selection

    Parameters
    ----------
    all_data: np.array 
        original data/ changed data using the changing_data function
    cut_list: a list of TF array
        each element has the size of all_data

    Returns
    -------
    x_s_c, y_s_c, r_s_c, emission_angle_s_c, Px_s_c, Py_s_c, Pz_s_c, P_s_c, PDGid_s_c : float, x_s_c[number of cut][number of file] 

        len(x_s_c) is the number of cuts in cut_list, x_s_c is a list
        len(x_s_c[0]) is the number of file, x_s_c[0] is a list inside x_s_c
        x_s_c[0][0].shape is number of row in the column, np.array inside x_s_c[0] 


    
    Examples
    --------
    >>> x_s_c[0][0]
    >>> n, bins, patches = ax.hist(P_s_c[0][1])

    """

    total_number_of_files = len(all_data)
    selected_variables = ['x_s_c', 'y_s_c', 'r_s_c', 'emission_angle_s_c', 'Px_s_c', 'Py_s_c', 'Pz_s_c', 'P_s_c', 'PDGid_s_c'] # variable for saving selected column of all files, return at the end
    for  name in selected_variables: 
        globals()[name] = [] # for clear variable
    
    for cut in cut_list:
        selected_data = [all_data[i][cut[i]] for i in range(total_number_of_files)]
        dummy = ['x_s', 'y_s', 'r_s', 'emission_angle_s', 'Px_s', 'Py_s', 'Pz_s', 'P_s', 'PDGid_s'] # intermideiate variable for saving selected column from different files, will be abandoned.
        
        for  name in dummy: # for clear variable
            globals()[name] = []
        for i in range(total_number_of_files):
            for j, name in enumerate(dummy):
                globals()[name].append( selected_data[i][:,j] )
                """ equalivant to : 
                                        x_s.append(selected_data[i][:,0])
                                        y_s.append(selected_data[i][:,1])
                                        r_s.append(selected_data[i][:,2])
                                        emission_angle_s.append(selected_data[i][:,3])
                                        Px_s.append(selected_data[i][:,4])
                                        Py_s.append(selected_data[i][:,5])
                                        Pz_s.append(selected_data[i][:,6])
                                        P_s.append(selected_data[i][:,7])
                                        PDGid_s.append(selected_data[i][:,8])
                                                                                                """
        for k, name in enumerate(selected_variables):
            globals()[name].append(globals()[dummy[k]])
            """ equalivant to : 
                                        x_s_c.append(x_s)
                                        y_s_c.append(y_s)
                                        r_s_c.append(r_s)
                                        emission_angle_s_c.append(emission_angle_s)
                                        Px_s_c.append(Px_s)
                                        Py_s_c.append(Py_s)
                                        Pz_s_c.append(Pz_s)
                                        P_s_c.append(P_s)
                                        PDGid_s_c.append(PDGid_s) 
                                                                                        """
    return x_s_c, y_s_c, r_s_c, emission_angle_s_c, Px_s_c, Py_s_c, Pz_s_c, P_s_c, PDGid_s_c
