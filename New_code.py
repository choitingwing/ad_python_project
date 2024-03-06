#!/usr/bin/env python
# coding: utf-8

"""
This is a file example of using the function_packages for plotting.

Plotting of BLTrackfile format (multiple 2D table type data)

The data file (from Fluka) has the format of
!BLTrackfile 
!x y z Px Py Pz t PDGid EvNum TrkId Parent weight
!cm cm cm GeV/c GeV/c GeV/c ns - - - - -

The function_packages set a structure of a plotting generator for any multiple table like data

"""


# import lib from others
import numpy as np
import pandas as pd
import matplotlib as mpl
# import my lib
from function_packages import *

# # Load files
# Specify the path to your directory 
data_path = './data'
# load data with function
data, file_names = load_raw_data(data_path, mpi=True) # here file_names means the name of the files (name_of_files)

# # close cores other than 0
# if file_names==0:
#     sys.exit()

# or you can rename the file name here (make sure it can be writen as a file name):
file_names = ['wo horn ', 'w horn ']
for i, name in enumerate(file_names):
    print("Renamed file name: ", 'f'+str(i), " ---> ", name)

# edit your column name of the data 
namelist = ['x', 'y', 'z', 'Px', 'Py', 'Pz', 't', 'PDGid', 'EventID', 'TrackID', 'ParentID', 'Weight']

# # Just use pandas to show the data structure but not use it for processing and plotting
# all_data_pd = [pd.DataFrame(d, columns=namelist) for d in data]
# all_data_pd[0]


# # Data processing and selection

# ## Data processing

# if you need to create new columns from the old one, do it here.
## Define variable and constant that I need to change the data.
r_maxmax = 30 # cm
theta_maxmax = 60e-3 # rad
emittance = r_maxmax*1e-2*theta_maxmax/1e-3
print( "(Max) Emittance cut  is ", emittance, "mmrad")
    
# I used a function to help me, open the function and modify it the way you want
all_data = changing_data(data, r_maxmax, theta_maxmax)


# create variables/ or really just naming the column so that the code is less messy below, that's way I don't use panda below
variable_names = ['x', 'y', 'r', 'emission_angle', 'Px', 'Py', 'Pz', 'P', 'PDGid', 'emission_angle_max'] # define your quantities
for i, name in enumerate(variable_names):
    globals()[name] = all_data[:,:,i]  # You can assign any value here
print("Each column has the shape (files, row): ", P.shape)


# ## Data selection (using numpy, because I found doing panda_data['column'] is quite messy)


# preparing for data selection, performing a cut and generate selected data

## low level selection
### select pdgid
particles_pdgid = [12, -13, -14, 211, -211] 
### transform pdgid to some familiar names
particle_variables = ['nu_e', 'mu_plus', 'nu_mu_bar','pion_plus', 'pion_minus'] 
for i, name in enumerate(particle_variables):
    globals()[name] = PDGid == particles_pdgid[i]   # all_data[:,:,8] is PDGid

## higher level selection 
pion720880 = ((P>720)&(P<880))
emit_r_theta = ( (emission_angle < emission_angle_max)  )

## make all selections into a list
cut_list = [pion_plus, pion720880, emit_r_theta]
cut_name_list = [r'$\pi^+$ ',r'720<P<880', r'emit_r_$\theta$'] # create a name list for plotting


# create new columns for the selected data
## using a function to help
All_data_s_c = generate_selected_data(all_data, cut_list)
## create variables/ or really just naming the new columns 
cut_variable_names = ['x_s_c', 'y_s_c', 'r_s_c', 'emission_angle_s_c', 'Px_s_c', 'Py_s_c', 'Pz_s_c', 'P_s_c', 'PDGid_s_c']
for  i, name in enumerate(cut_variable_names): 
    globals()[name] = All_data_s_c[i] # for clear variable



# Now you can use the data by each physics quality , i.e.: x_s_c[cut][number of file]
print('Each physics quantity has ', len(x_s_c), 'cuts and ', len(x_s_c[0]), "files.","\nEach files with a cut has ", x_s_c[0][0].shape, "rows.")


# # Plotting


mpl.rcParams['font.size'] = 16 # define the text size in all plots
plt.rcParams['figure.facecolor'] = 'white' 
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k','pink','brown','olive','orange', 'purple'] # define colors for multiple lines

image_path = './plots/'
# Check if the directory exists
if not os.path.exists(image_path):
    # If it doesn't exist, create it
    os.makedirs(image_path)
# ## 1D plotting

# Take one column and plot histogram, the functions using here are bin_gen_1D and plotting_1D_hist. 

# ### Momentum distribution


# generate histogram binning
bin_min, bin_max, bin_width = 0, 2000, 10
bin_P = bin_gen_1D(bin_min, bin_max, bin_width)

# plotting parameters
figsize = (20,10)
xlabel = 'P(MeV)'
ylabel = f' N/{bin_width} MeV'
title = 'Momentrum distribution of pion with and w/o horn'
save_name = image_path +  f'{data.shape[1]}_pion_momentum_dis.png' # the name of the image if you save it.
fit = 0 # no confidence level fitting

#
plotting_1D_hist(P_s_c, bin_P, figsize, xlabel, ylabel, save_name, title, 
                 colors, fit, file_names, cut_name_list, save=True)

# ### Emission angle distribution


bin_width = 0.01
bin_theta = bin_gen_1D(0, np.pi/2, bin_width)
  
figsize = (15,10)
xlabel = fr'$\theta_{{lab}}$ (rads)'
ylabel = fr' N / {bin_width} rad'
title = 'Emission angle distribution of pion with and w/o horn'
save_name = image_path +  f'pion_emission_angle_dis.png'
fit = 0 #

plotting_1D_hist(emission_angle_s_c, bin_theta, figsize, xlabel, ylabel, save_name , title, 
                 colors, fit, file_names, cut_name_list, save=True)


# ### x distribution with fit

bin_width = 1
bin_x = bin_gen_1D(-200, 200, bin_width)
  
figsize = (20,10)
xlabel = fr'x (cm)'
ylabel = fr' N / {bin_width} rad'
title = 'x distribution of pion with and w/o horn'
save_name = image_path +  f'x_dis.png'
fit = 0.68 # 68% of the data
plotting_1D_hist(x_s_c, bin_x, figsize, xlabel, ylabel, save_name , title, 
                 colors, fit, file_names, cut_name_list, save=True)


# ## 2D plotting

# All plots any two quanities with different cuts and files, with gaussian fit

# ### P-theta heat map
bin_min, bin_max, bin_width = 0, 2000, 10
bin_min2, bin_max2, bin_width2 = 0, np.pi/2, 0.01
bins_P_theta = bin_gen_2D(bin_min, bin_max, bin_width, bin_min2, bin_max2, bin_width2)

xlabel = f"P (MeV)"
ylabel = fr"$\theta$ (rad)" 
title =  fr'P-$\theta$'
save_name = image_path +  'P_theta' # the name of the image if you save it.
figsize = (8,7)
cmap = "Blues"
fit=0 # 0: no gaussian fitting, 1: one std, 2: two std, ..

# That using oPlot is really nice visualising on html.
call_plotting_2D_hist_w_oPlot(P_s_c, emission_angle_s_c, bins_P_theta, figsize, xlabel, ylabel, save_name , title, 
                 cmap, fit, file_names, cut_name_list, save=True)


# ### x-y heat map
bin_min_x, bin_max_x, bin_width_x = -200, 200, 1
bin_min_y, bin_max_y, bin_width_y = -200, 200, 1
bins_xy_xy = bin_gen_2D(bin_min_x, bin_max_x, bin_width_x, bin_min_y, bin_max_y, bin_width_y)

xlabel = f"x (cm)"
ylabel = f"y (cm)"
title =  fr'xy'
save_name = image_path +  'xy'
cmap = "Greens" #"coolwarm" # "BuPu" "YlOrRd"
figsize = (8.2,7)
fit=1 

call_plotting_2D_hist_w_oPlot(x_s_c, y_s_c, bins_xy_xy, figsize, xlabel, ylabel, save_name , title, 
                 cmap, fit, file_names, cut_name_list, save=True)

# !jupyter nbconvert --to html Plot_BL_files

print('\nPlotting is done. Check your path.')


# ## 3D plotting

# - possibility in the future.
# 
# - using GPU
