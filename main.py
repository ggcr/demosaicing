from matplotlib import pyplot as plt
import cv2
import numpy as np
from scipy.signal import convolve2d
from PIL import Image

# Read CFA Raw data
def pull_image():
    """
    In order to extract the CFA data from Digital Negative (.DNG) files we use dcraw.c
    http://www.dechifro.org/dcraw/dcraw.c
    """
    raw_data = Image.open('sample.tiff')
    raw = np.array(raw_data).astype(np.double)
    return raw


# Normalization
def normalize_uint8(img, maxval, minval):
    """
    img: uint16 2d raw image
    out: uint8 2d normalized 0-255 image
    https://en.wikipedia.org/wiki/Normalization_(image_processing)
    """
    return (np.rint((img - img.min()) * ((maxval - minval) / (img.max() - img.min())) + minval)).astype(dtype='uint8')

def min_max_normalization(img, maxval, minval):
    """
    https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
    """
    return (img - minval) / (maxval-minval)


# White balancing
def whitebalance(im, rgbScales):

    # generate the white balancing matrix
    scalematrix = rgbScales[1] * np.ones(im.shape)
    
    # rggb
    scalematrix[0::2, 0::2] = rgbScales[0]
    scalematrix[1::2, 1::2] = rgbScales[2]
    
    return np.multiply(im, scalematrix)
    

# Color filtering: `rggb`
def bayer(im):
    r = np.zeros(im.shape[:2])
    g = np.zeros(im.shape[:2])
    b = np.zeros(im.shape[:2])
    r[0::2, 0::2] += im[0::2, 0::2]
    g[0::2, 1::2] += im[0::2, 1::2]
    g[1::2, 0::2] += im[1::2, 0::2]
    b[1::2, 1::2] += im[1::2, 1::2]
    return r, g, b


# Demosaicing
def bilinear(im):
    r, g, b = bayer(im)

    # green interpolation
    k_g = 1/4 * np.array([[0,1,0],[1,0,1],[0,1,0]])
    convg =convolve2d(g, k_g, 'same')
    g = g + convg

    # red interpolation
    k_r_1 = 1/4 * np.array([[1,0,1],[0,0,0],[1,0,1]])
    convr1 =convolve2d(r, k_r_1, 'same')
    convr2 =convolve2d(r+convr1, k_g, 'same')
    r = r + convr1 + convr2

    # blue interpolation
    k_b_1 = 1/4 * np.array([[1,0,1],[0,0,0],[1,0,1]])
    convb1 =convolve2d(b, k_b_1, 'same')
    convb2 =convolve2d(b+convb1, k_g, 'same')
    b = b + convb1 + convb2
    
    return r, g, b


# Demosaicing: Gradient Correction Interpolation
def gradient_correction(im):
    r, g, b = bayer(im)
    
    # each channel has the same dimension
    rows = g.shape[0]
    cols = g.shape[1]
    
    # green interpolation
    GatRB = np.array([
        [   0,   0,  -1,   0,   0],
        [   0,   0,   2,   0,   0],
        [  -1,   2,   4,   2,  -1],
        [   0,   0,   2,   0,   0],
        [   0,   0,  -1,   0,   0]
    ])

    out_g = np.zeros(g.shape)
    out_g[:] = g
    for i in range(rows - 5):
        for j in range(cols - 5):
            if g[i+2, j+2] == 0:
                gx = g[i:i+5, j:j+5]
                if r[i+2, j+2] != 0:
                    # G at R location
                    rx = r[i:i+5, j:j+5]
                    out_g[i+2, j+2] = np.average(gx * GatRB + rx * GatRB)
                elif b[i+2, j+2] != 0:
                    # G at B location
                    bx = b[i:i+5, j:j+5]
                    out_g[i+2, j+2] = np.average(gx * GatRB + bx * GatRB)
        
    # red interpolation
    RatGrow = np.array([
        [   0,   0, 1/2,   0,   0],
        [   0,  -1,   0,  -1,   0],
        [  -1,   4,   5,   4,  -1],
        [   0,  -1,   0,  -1,   0],
        [   0,   0, 1/2,   0,   0]
    ])
    
    RatGcol = np.array([
        [   0,   0,  -1,   0,   0],
        [   0,  -1,   4,  -1,   0],
        [ 1/2,   0,   5,   0, 1/2],
        [   0,  -1,   4,  -1,   0],
        [   0,   0,  -1,   0,   0]
    ])
    
    RatB = np.array([
        [   0,   0,-3/2,   0,   0],
        [   0,   2,   0,   2,   0],
        [-3/2,   0,   6,   0,-3/2],
        [   0,   2,   0,   2,   0],
        [   0,   0,-3/2,   0,   0]
    ])
    
    out_r = np.zeros(g.shape)
    out_r[:] = r
    for i in range(rows - 5):
        for j in range(cols - 5):
            if r[i+2, j+2] == 0:
                rx = r[i:i+5, j:j+5]
                if g[i+2, j+2] != 0 and (r[i+2, j+1] != 0 and r[i+2, j+3] != 0):
                    # R at G, R row
                    gx = g[i:i+5, j:j+5]
                    out_r[i+2, j+2] = np.average(gx * RatGrow + rx * RatGrow)
                elif g[i+2, j+2] != 0 and (r[i+1, j+2] != 0 and r[i+3, j+2] != 0):
                    # R at G, R col
                    gx = g[i:i+5, j:j+5]
                    out_r[i+2, j+2] = np.average(gx * RatGcol + rx * RatGcol)
                elif b[i+2, j+2] != 0:
                    # R at B
                    bx = b[i:i+5, j:j+5]
                    out_r[i+2, j+2] = np.average(bx * RatB + rx * RatB)
    
    BatGrow = RatGrow
    BatGcol = RatGcol
    BatR = RatB
    
    out_b = np.zeros(g.shape)
    out_b[:] = b
    for i in range(rows - 5):
        for j in range(cols - 5):
            if b[i+2, j+2] == 0:
                bx = b[i:i+5, j:j+5]
                if g[i+2, j+2] != 0 and (b[i+2, j+1] != 0 and b[i+2, j+3] != 0):
                    # R at G, R row
                    gx = g[i:i+5, j:j+5]
                    out_b[i+2, j+2] = np.average(gx * BatGrow + bx * BatGrow)
                elif g[i+2, j+2] != 0 and (b[i+1, j+2] != 0 and b[i+3, j+2] != 0):
                    # R at G, R col
                    gx = g[i:i+5, j:j+5]
                    out_b[i+2, j+2] = np.average(gx * BatGcol + bx * BatGcol)
                elif r[i+2, j+2] != 0:
                    # B at R
                    rx = r[i:i+5, j:j+5]
                    out_b[i+2, j+2] = np.average(bx * BatR + rx * BatR)
    
    return out_r, out_g, out_b


if __name__ == "__main__":
    """
    Scaling with darkness <black>, saturation <white>,
    and multipliers <r_scale> <g_scale> <b_scale> <g_scale>

    Scaling with darkness 44, saturation 16383, and
    multipliers 2.264263 1.000000 1.195190 1.000000
    """

    black = 0
    white = 16383
    R_scale = 2.217041
    G_scale = 1.000000
    B_scale = 1.192484

    im = pull_image()

    im_norm = min_max_normalization(im, white, black)

    im_wb = whitebalance(im_norm, rgbScales = [R_scale, G_scale, B_scale])

    r, g, b = bilinear(im_wb)
    # r, g, b = gradient_correction(im_wb)

    image = np.stack((r,g,b), axis=2)
    plt.axis('off')
    plt.title("Bilinear interpolation demosaicing")
    plt.imshow(image)
    plt.show()

