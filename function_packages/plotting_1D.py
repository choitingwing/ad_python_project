# bin generator 1D
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import norm

def bin_gen_1D(bin_min, bin_max, bin_width):
    """ 
    This is for bin boundaries generation of 1D data

    Parameters
    ----------
    bin_min: float
        lowest bound
    bin_max: float
        highest bound
    bin_width: float
        bin width
           
    Returns
    -------
    bins: float
        a numpy array/matrix
    
    Examples
    --------
    >>> bin_min, bin_max, bin_width = 0, 2000, 10
    >>> bin_P = bin_gen_1D(bin_min, bin_max, bin_width)

    """
    bins_number = int( (bin_max-bin_min)/bin_width+1)
    bins = np.linspace(bin_min, bin_max, bins_number)
    return bins

def plotting_1D_hist(hist_data, bins, figsize, xlabel, ylabel, save_name, title, colors, fit, file_names, cut_name_list, save=False):
    """ 
    This is for plotting 1D histogram on one physics quantity (column), but multiple files and selection

    Parameters
    ----------
    hist_data: float
        data shpae from generate_selected_data()
    bins: float np.array
        bins boundaries from bin_gen_1D
    figsize: (float, float)
    xlabel: string
    ylabel: string
    save_name: string
    title: string
    colors: string list
    fit: float
        0 - 1
    file_names: string list
        list of the files' name
    cut_name_list: string list
        list of the name of the selection
    save: True/False
        save an image or not, default False
           
    Returns
    -------
    no return values
    
    Examples
    --------
    
    >>> figsize = (20,10)
    >>> xlabel = 'P(MeV)'
    >>> ylabel = f' N/{bin_width} MeV'
    >>> title = 'Momentrum distribution of pion with and w/o horn'
    >>> save_name = image_path +f'{data.shape[1]}_pion_momentum_dis.png' # the name of the image if you save it.
    >>> fit = 0 # no confidence level fitting

    >>> plotting_1D_hist(P_s_c, bin_P, figsize, xlabel, ylabel, save_name, title, 
                     colors, fit, file_names, cut_name_list, save=True)

    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    fontsize = 18
    # linestyle = "-"
    total_number_of_cut = len(hist_data)
    total_number_of_files = len(hist_data[0])

    ## plot type
    for i in range(total_number_of_files): 
        for ic in range(total_number_of_cut):
            
            n, bins, patches = ax.hist(hist_data[ic][i], bins=bins, histtype='step', 
                # linestyle=linestyle,
                                       color = colors[total_number_of_cut*i +ic], 
                                       label=f'{file_names[i]} {cut_name_list[ic]} : Total number is {hist_data[ic][i].shape[0]}' )

            if fit > 0:
                ci = norm(*norm.fit(hist_data[ic][i])).interval(fit)  # fit a normal distribution and get 95% c.i.
                plt.fill_betweenx([0, n.max()], ci[0], ci[1], color=colors[total_number_of_cut*i +ic], alpha=0.1)  # Mark between 0 and the highest bar in the histogram
    

    ## optional config
    plt.legend(loc='upper right')
    plt.xlabel(xlabel,fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    plt.title(title, fontsize=fontsize) 

    if save == True:
        save_name = save_name
        plt.savefig(save_name, dpi=300)