#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('gradienty_Urbaniak.pdf')


# 0 <= h <= 360, 0 <= s,v <= 1
def hsv2rgb(h, s, v):
    c = v * s
    x = c * (1.0 - abs((h/60.0)%2-1.0))
    m = v * (1.0 - s)
    if v == 0:
        r = 0.0
        g = 0.0
        b = 0.0
    else:
        if h < 60:
            r = c
            g = x
            b = 0.0
        elif h < 120:
            r = x
            g = c
            b = 0.0
        elif h < 180:
            r = 0.0
            g = c
            b = x
        elif h < 240:
            r = 0.0
            g = x
            b = c
        elif h < 300:
            r = x
            g = 0.0
            b = c
        else:
            r = c
            g = 0.0
            b = x
    return ((r + m), (g+m), (b+m))

def gradient_rgb_bw(v):
    return (v, v, v)

def gradient_rgb_gbr(v):
    if v <= 0.5:
        r = 0
        g = 1 - v*2
        b = v * 2
    else:
        r = v*2 - 1
        g = 0
        b = 2 - v * 2
    return (r, g, b)


def gradient_rgb_gbr_full(v):
    if v <= 0.25:
        r = 0
        g = 1
        b = v*4
    elif v <= 0.5:
        r = 0
        g = 2 - v*4
        b = 1
    elif v <= 0.75:
        r = 4*v - 2
        g = 0
        b = 1
    else:
        r = 1
        g = 0
        b = 4-v*4
    return (r, g, b)


def gradient_rgb_wb_custom(v):
    if v <= 1/7:
        r = 1
        g = 1 - v*7
        b = 1
    elif v <= 2/7:
        r = 2 - v*7
        g = 0
        b = 1
    elif v <= 3/7:
        r = 0
        g = v*7 - 2
        b = 1
    elif v <= 4/7:
        r = 0
        g = 1
        b = 4 - v*7
    elif v <= 5/7:
        r = v*7 - 4
        g = 1
        b = 0
    elif v <= 6/7:
        r = 1
        g = 6 - v*7
        b = 0
    else:
        r = 7 - v*7
        g = 0
        b = 0
    return (r, g, b)


def gradient_hsv_bw(v):
    return hsv2rgb(0.0, 0.0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb(120 + v * 240, 1.0, 1.0)

def gradient_hsv_unknown(v):
    return hsv2rgb(120 - v * 120, 0.45, 1.0)


def gradient_hsv_custom(v):
    #TODO
    if v < 0.5 :
        s = v
        val = 1 - v
    else:
        s = 1 - v
        val = v
    return hsv2rgb(60 + v * 300, s, val)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])