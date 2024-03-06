import numpy as np
import matplotlib.pyplot as plt
from .help_functions import *

def bin_gen_2D(bin_min, bin_max, bin_width, bin_min2, bin_max2, bin_width2):
    """ 
    This is for bin boundaries generation of 2D data

    Parameters
    ----------
    bin_min, bin_min2: float
        lowest bound of each physics quantity
    bin_max, bin_max2: float
        highest bound of each physics quantity
    bin_width, bin_width2: float
        bin width of each physics quantity
           
    Returns
    -------
    bins: float
        a numpy array/matrix
    bins2: float
        a numpy array/matrix

    Examples
    --------
    >>> bin_min, bin_max, bin_width = 0, 2000, 10
    >>> bin_min2, bin_max2, bin_width2 = 0, np.pi/2, 0.01
    >>> bins_P_theta = bin_gen_2D(bin_min, bin_max, bin_width, bin_min2, bin_max2, bin_width2)

    """

    bins_number = int( (bin_max-bin_min)/bin_width+1)
    bins = np.linspace(bin_min, bin_max, bins_number)

    bins_number2 = int( (bin_max2-bin_min2)/bin_width2+1)
    bins2 = np.linspace(bin_min2, bin_max2, bins_number2)
    return bins, bins2

def plotting_2D_hist(hist_data, hist_data2, bins, figsize, xlabel, ylabel, save_name, title, cmap, fit, file_names, cut_name_list, oPlot, save=False):
    """ 
    This is for plotting 1D histogram on one physics quantity (column), but multiple files and selection

    Parameters
    ----------
    hist_data: float
        data shpae from generate_selected_data()
    hist_data2: float
        data shpae from generate_selected_data()
    bins: a list of two floar np.array
        bins boundaries from bin_gen_2D
    figsize: (float, float)
    xlabel: string
    ylabel: string
    save_name: string
    title: string
    cmap: cmap string 
        i.e.: "Blues"
    fit: float
        0: no gaussian fitting, 1: one std, 2: two std, ..
    file_names: string list
        list of the files' name
    cut_name_list: string list
        list of the name of the selection
    oPlot: input oPlot class for plotting help in html
    save: True/False
        save an image or not, default False
           
    Returns
    -------
    no return values
    
    Examples
    --------
    >>> xlabel = f"P (MeV)"
    >>> ylabel = fr" $\theta$ (rad)" 
    >>> title =  fr'P-$\theta$'
    >>> save_name = image_path +'P_theta' # the name of the image if you save it.
    >>> figsize = (8,7)
    >>> cmap = "Blues"
    >>> fit=0 
    
    >>> plotting_2D_hist(P_s_c, emission_angle_s_c, bins_P_theta, figsize, xlabel, ylabel, save_name, title, cmap, fit, file_names, cut_name_list, oPlot, save)

    """
    total_number_of_cut = len(hist_data)
    total_number_of_files = len(hist_data[0])
    
    for i in range(total_number_of_files):
        for ic in range(len(cut_name_list)):
            plot_title = fr"Heatmap of {title} of {file_names[i]}, {cut_name_list[ic]}"+"\n" +f"Total number is {hist_data[ic][i].shape[0]}"
            cscale = "linear"
            fig, ax, im = get_histogram2d(hist_data[ic][i], hist_data2[ic][i],
                                          title=plot_title, xlabel=xlabel, ylabel=ylabel, bins=bins, 
                                          cmap=cmap, cscale=cscale, figsize=figsize)
            
            if fit==True:
                confidence_ellipse(hist_data[ic][i], hist_data2[ic][i], ax, n_std=fit, label=r'$1\sigma$', edgecolor='red')
            plt.tight_layout()
            if save == True:
                save_name2 = save_name + f'_{file_names[i]}_{cut_name_list[ic]}_2Ddis.png'
                plt.savefig(save_name2, dpi=300)

            oPlot.add_plot(ax) # pass it to the FlowLayout to save as an image
            plt.close() # this gets rid of the plot so it doesn't appear in the cell

def call_plotting_2D_hist_w_oPlot(hist_data, hist_data2, bins, figsize, xlabel, ylabel, save_name, title, cmap, fit, file_names, cut_name_list, save=False):
    """ 
    This is a function to call plotting_2D_hist with oPlot

    Parameters
    ----------
    same as plotting_2D_hist

    Returns
    -------
    no return values

    Examples
    --------
    >>> call_plotting_2D_hist_w_oPlot(P_s_c, emission_angle_s_c, bins_P_theta, figsize, xlabel, ylabel, save_name, title, 
                 cmap, fit, file_names, cut_name_list, save=True)
                 
    """
    oPlot = FlowLayout() # create an empty FlowLayout
    plotting_2D_hist(hist_data, hist_data2, bins, figsize, xlabel, ylabel, save_name, title, cmap, fit, file_names, cut_name_list, oPlot, save)
    oPlot.PassHtmlToCell()

