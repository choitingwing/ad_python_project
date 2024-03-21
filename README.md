

# Background
In accelerator physics, particles are generated from some source before sending to an accelerator, or it is more like collecting the particles. Here, pions generated from a target are collected. To be able to collect them efficiently, we need to know the pion beam properties. In order to know that, we plot the pion data.

# Introduction
Plotting data is always getting messy at the end.  

In this project, I would like to transform my previously developed code. I aim to create a plotting generator for some table-like data file by transforming the code into a Python library and optimising the code for speed/memory usage.  If you open old_code.html or old_code.ipynb, you can see how messy that is. Everything is explicitly coded inside one file, from loading data, calculations, and 2D and 3D plottings. I will try to transform the code by using everything I learned in the course.

Things that improved:
1. Using functions, packages and Modules.
2. Using docstring and sphinx
3. Better use of fancy indexing to process data
4. The possibility of using mpi to load data (cores can load one file each at the same time.)
5. Better use of matplotlib

# Explaination of the files

old code/:   contain original plotting file

data/:   contain pions data

function_packages/:  a Module that I am using in my new code

plots/:   a file that contain all plots generated from the new code

docs/:   contain everything from sphinx

New_code.ipynb:   a notebook that demonstrates how to use the package (no mpi)

New_code.html:  a sample result from New_code.ipynb

New_code.py:   a Python code that demonstrates how to use the package (with or without mpi)

# How to use this repo

A. For New_code.ipynb, just open it and Run all or line by line.

B. For New_code.py, do  `mpiexec python New_code.py`  in bash shell

# Summary

This is a good start for me to apply and learn advanced Python skills. I think I am becoming a better programmer now.

For this program, there are possibilities to expand it with 3D plotting, x-y plotting and others. 

Aiming to make plotting as easy as possible for researcher, avoiding all unnecessary steps in programming and figuring out how to use libraries.
