#  ------------------------------------------------------------------------
#  File Name   : magritek2py.py
#  Description : Loading and Plotting 1D Data of Magritek NMR Spectrometer
#  Developer   : Dr. Kosuke Ohgo
#  ULR         : https://github.com/ohgo1977/Magritek_NMR_Gadgets
#  Version     : 1.1.0
# 
#  ------------------------------------------------------------------------
# 
# MIT License
#
# Copyright (c) 2025 Kosuke Ohgo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Version 1.1.0 on 9/22/2025
# Revised on 9/22/2025
# - loadImage() and plotImage() were added.
#
# Version 1.0.0 on 3/29/2024


import struct
import matplotlib.pyplot as plt
import numpy as np

def load1d(fname):
    # Load a binary file for a spectrum (spectrum.1d or spectrum_processed.1d) or an FID (data.1d).
    # Outputs are
    # ax1d: a list including x-axis values. Chemical shift for a spectrum and time for an FID.
    # data_r: a list including a real part of a spectrum or FID.
    # data_i: a list including a imaginary part of a spectrum or FID.
    # Example:
    # time, data_r, data_i = magritek2py.load1d('spectrum_processed.1d')

    fid = open(fname,'rb')

    # Header
    # int32 => 32 bit => 4 bytes
    owner_pros = struct.unpack('<i', fid.read(4))[0]
    format_data = struct.unpack('<i', fid.read(4))[0]
    version_v1_1 = struct.unpack('<i', fid.read(4))[0]
    dataType_504 = struct.unpack('<i', fid.read(4))[0]
    xDim = struct.unpack('<i', fid.read(4))[0]
    yDim = struct.unpack('<i', fid.read(4))[0]
    zDim = struct.unpack('<i', fid.read(4))[0]
    qDim = struct.unpack('<i', fid.read(4))[0]

    # Data size
    xlen = xDim*yDim*zDim*qDim

    # float32 => 32 bit => 4 bytes
    ax1d = [struct.unpack('f', fid.read(4))[0] for i in range(xlen)]
    data = [struct.unpack('f', fid.read(4))[0] for i in range(2*xlen)]# r1, i1, r2, i2, ...
    data_r = data[0::2]# Real part
    data_i = data[1::2]# Imaginary part

    return ax1d, data_r, data_i

def plot1d(ax1d, data_r, **kwargs):
    # Plot a spectrum (spectrum.1d or spectrum_processed.1d) or an FID (data.1d). 
    # ax1d: a list including x-axis values. Chemical shift for a spectrum and time for an FID.
    # data_r: a list including y-axis values. Spectrum or FID. Usually, real part of a spectrum or FID from load1d is used. 
    # There are otpional parameters.
    # plot_ragnge: range to display a spectrum. Default is a full range of data.
    # max_range: range to determine the max value of y-axis. The range of y-axis is between -0.05 and 1.05 of the highest intensity in max_range. Default is a full range of data.
    # major_tick: interval of major tick. The default is 1.
    # minor_tick: interval of minor tick. The default is 0.1. 
    #
    # Example:
    # magritek2py.plot1d(time, data_r, plot_range = [0, 225], max_range = [0, 200], major_tick = 10, minor_tick = 1)

    if 'plot_range' not in kwargs:
        plot_range = [ax1d[0], ax1d[:]]
    else:
        plot_range = kwargs['plot_range']
    
    if 'max_range' not in kwargs:
        max_range =  [ax1d[0], ax1d[:]]
    else:
        max_range = kwargs['max_range']

    if 'major_tick' not in kwargs:
        major_tick = 1
    else:
        major_tick = kwargs['major_tick']
    
    if 'minor_tick' not in kwargs:
        minor_tick = 0.1
    else:
        minor_tick = kwargs['minor_tick']

    # Obtaining indeces of ax1d corresponding to max_range
    max_range_id = []
    for ii in range(2):
        max_range_tmp = max_range[ii]
        id_tmp = min(range(len(ax1d)), key=lambda i: abs(ax1d[i] - max_range_tmp))
        max_range_id.append(id_tmp)

    # Obtaining maximum value in max_range
    data_tmp = data_r[max_range_id[0]:max_range_id[1]]
    max_value_y = max(data_tmp)

    # Generate a figure
    fig = plt.figure(figsize = (9, 5))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(ax1d, data_r)

    # Create major and minor ticks
    major_ticks_x = np.arange(plot_range[0], plot_range[1], major_tick)
    minor_ticks_x = np.arange(plot_range[0], plot_range[1], minor_tick)
    ax.set_xticks(major_ticks_x)
    ax.set_xticks(minor_ticks_x, minor=True)

    # And a corresponding grid
    ax.grid(which='both')

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    ax.set_xlabel('Chemical shift (ppm)')
    ax.set_xlim(plot_range[0], plot_range[1])
    ax.set_ylim(-0.05*max_value_y, 1.05*max_value_y)
    ax.invert_xaxis()
    plt.savefig('temp')
    plt.show()


def loadImage(fname):
    # Load a binary file for an image (usually, 'iData.2d').
    # Output is
    # data: numpy ndarray with the dimensions of xDim and yDim.
    # Example:
    # data = magritek2py.loadImaga('iData.2d')

    fid = open(fname,'rb')

    # Header
    # int32 => 32 bit => 4 bytes
    owner_pros = struct.unpack('<i', fid.read(4))[0]
    format_data = struct.unpack('<i', fid.read(4))[0]
    version_v1_1 = struct.unpack('<i', fid.read(4))[0]
    dataType_504 = struct.unpack('<i', fid.read(4))[0]
    xDim = struct.unpack('<i', fid.read(4))[0]
    yDim = struct.unpack('<i', fid.read(4))[0]
    zDim = struct.unpack('<i', fid.read(4))[0]
    qDim = struct.unpack('<i', fid.read(4))[0]

    # Data size
    xlen = xDim*yDim*zDim*qDim

    # float32 => 32 bit => 4 bytes
    data = [struct.unpack('f', fid.read(4))[0] for i in range(xlen)]# real part only
    data = np.asarray(data).reshape((yDim,xDim))
    return data

def plotImage(data, FOV0, FOV1, **kwargs):
    # Plot image data. 
    # data: numpy ndarray obtained by loadImage()
    # FOV0: Field of View of Read Gradient axis in mm.
    # FOV1: Field of View of Phase Gradient axis in mm.
    # There are otpional parameters.
    # plane: plane of the image. The default is 'xy'
    # major_tick: interval of major tick. The default is 1.
    # minor_tick: interval of minor tick. The default is 0.1.
    # Example:
    # magritek2py.loadImage(data,8,8,plane='xz',major_tick = 2, minor_tick = 0.5)
    
    if 'plane' not in kwargs:
        plane = 'xy'
    else:
        plane = kwargs['plane']

    if 'major_tick' not in kwargs:
        major_tick = 1
    else:
        major_tick = kwargs['major_tick']
    
    if 'minor_tick' not in kwargs:
        minor_tick = 0.1
    else:
        minor_tick = kwargs['minor_tick']
    fig = plt.figure(figsize = (9, 5))
    ax = fig.add_subplot(1, 1, 1)
    dims = data.shape
    xDim = dims[1]# Need to be considered
    yDim = dims[0]# Need to be considered
    # https://neuraldatascience.io/8-mri/read_viz.html
    # https://matplotlib.org/stable/users/explain/colors/colormaps.html
    # https://stackoverflow.com/questions/20069545/2d-plot-of-a-matrix-with-colors-like-in-a-spectrogram
    data_plot = np.flipud(data)# Keep consistency of images between Magritek and Python
    plt.imshow(data_plot,cmap='turbo', extent=[0,FOV0,0,FOV1])
    major_ticks_x = np.arange(0, FOV0+major_tick, major_tick)
    minor_ticks_x = np.arange(0, FOV0+minor_tick, minor_tick)
    ax.set_xticks(major_ticks_x)
    ax.set_xticks(minor_ticks_x, minor=True)
    ax.set_xlabel(plane[0]+' (mm) ('+str(round(FOV0/xDim*1000))+' um/pixel)')

    major_ticks_y = np.arange(0, FOV1+major_tick, major_tick)
    minor_ticks_y = np.arange(0, FOV1+minor_tick, minor_tick)
    ax.set_yticks(major_ticks_y)
    ax.set_yticks(minor_ticks_y, minor=True)
    ax.set_ylabel(plane[1]+' (mm) ('+str(round(FOV1/yDim*1000))+' um/pixel)')

    plt.show()
