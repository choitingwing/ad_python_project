# background
In accelerator physics, particles are generated from some source before sending to an accelerator, or it is more like collecting the particles. Here, pions generated from a target are collected. To be able to collect them efficiently, we need to know the pion beam properties. In order to know that, we plot the pion data.

# Introduction
Plotting data is always getting messy at the end.  

In this project, I would like to transform my previously developed code. I aim to create a plotting generator for a specific type of data file by transforming your code into a Python library and optimising your code for speed/memory usage.  If you open old_code.html or old_code.ipynb, you can see how messy that is. Everything is explicitly coded inside one file, from loading data, calculations, and 2D and 3D plottings. I will try to transform the code by using everything I learned in the course.

Things that improved:
1. Using functions, packages and Modules.
2. Using docstring and sphinx
3. Better use of fancy indexing to process data
4. The possibility of using mpi to load data ( one core can load one file at the same time.)
5. Better use of matplotlib

# Explaination of the files

old code/: contain original plotting file
data/: contain pions data
function_packages/: Module that I am using in my new code
plots/: a file that contain all plots generated from the new code
docs/: contain everything from sphinx

New_code.ipynb: a notebook that domonstrate how to use the package (no mpi)
New_code.py: a python code that domonstrate how to use the package (with or without mpi)

# How to use this repo

For New_code.ipynb, just open it and Run all or line by line.
For New_code.py, do " mpiexec python New_code.py " in bash shell
