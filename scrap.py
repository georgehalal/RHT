#!/usr/bin/python

#-----------------------------------------------------------------------------------------
#Imports
#-----------------------------------------------------------------------------------------
from __future__ import division
from astropy.io import fits
#from scipy.stats import norm
#from mpl_toolkits.mplot3d import Axes3D
#from mayavi import mlab
#from astropy import wcs
import numpy as np
import scipy.ndimage
import math
import os
import matplotlib.pyplot as plt
import sys
import string
import tempfile 
import shutil
   

def houghnew(image, theta):
    if image.ndim != 2 or theta.ndim != 1:
        raise ValueError('In houghnew, image must be 2-D and theta must be 1-D')

    wy, wx = image.shape 
    wmid = np.floor(wx/2.0) #_____________________________________________TODO??

    # compute the vertical bins (the distances)
    nr_bins = np.ceil(np.hypot(*image.shape))

    # allocate the output data
    out = np.zeros((int(nr_bins), len(theta)), dtype=np.bool_) #TODO______ uint664 datatype?

    # precompute the sin and cos of the angles
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # find the indices of the non-zero values in
    # the input data
    y, x = np.nonzero(image)

    # x and y can be large, so we can't just broadcast to 2D
    # arrays as we may run out of memory. Instead we process
    # one vertical slice at a time.
    for i, (cT, sT) in enumerate(zip(cos_theta, sin_theta)):

        # compute the base distances
        distances = (x - wmid) * cT + (y - wmid) * sT

        # round the distances to the nearest integer
        # and shift them to a nonzero bin
        shifted = np.round(distances) + nr_bins/2

        # cast the shifted values to ints to use as indices
        indices = shifted.astype(np.int)
        
        # use bin count to accumulate the coefficients
        bincount = np.bincount(indices) #TODO______________________ bincount method?

        # finally assign the proper values to the out array
        out[:len(bincount), i] = bincount
        #out.T[i] = bincount

    return out


def all_thetas(window, thetbins):
    wy, wx = window.shape #Parse x/y dimensions
    ntheta = len(thetbins) #Parse height in theta
    nr_bins = int(np.ceil(np.hypot(*window.shape)))
    
    #Makes prism; output has dimensions (x, y, theta)
    out = np.zeros((wy, wx, ntheta), np.int)
    coords = zip( *np.nonzero(window))

    for (j, i) in coords:
        #At each x/y value, create new single-pixel data
        w_1 = np.zeros((wy, wx), np.float_)
        w_1[j,i] = 1
        out[j, i, :] = houghnew(w_1, thetbins)[np.floor(nr_bins/2), :]

    return out 
