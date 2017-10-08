#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import urllib.request
import csv
import codecs
from matplotlib import colors

def loadMapFromURL(url):
    urlStream = urllib.request.urlopen(url)
    csvReader = csv.reader(codecs.iterdecode(urlStream, 'utf-8'), delimiter=' ')
    firstRow = next(csvReader)
    width = int(firstRow[0])
    height = int(firstRow[1])
    delta = int(firstRow[2])
    map = np.empty([width,height])
    row = 0
    for line in csvReader:
        for col in range(width):
            map[row,col] = float(line[col])
        row += 1

    return map;


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

def gradient_map_base(v):
    return hsv2rgb(160-v, 1.0, 0.85)

def gradient_map_shading_lower(v):
    return hsv2rgb(160-v,0.75, 0.95)

def gradient_map_shading_higher(v):
    return hsv2rgb(160-v,1.0, 0.75)

def createImg(mapLevels):
    img = np.zeros((500, 500, 3))

    for row in range(500):
        for col in range(500):
            img[row, col] = gradient_map_base(mapLevels[row, col]) # bazowy import
        for col in range(1,500):
            if mapLevels[row,col-1] > mapLevels[row,col]: # cieniowanie na podstawie wysokosci
                img[row, col] = gradient_map_shading_higher(mapLevels[row, col])
            else:   # cieniowanie na podstawie wysokosci
                img[row, col] = gradient_map_shading_lower(mapLevels[row, col])

    return img


if __name__ == '__main__':
    mapLevels = loadMapFromURL('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/kolorowanie_mapy/big.dem')
    fig = plt.figure(figsize=(6, 6))
    #print( mapLevels.shape )
    #print ( np.amax(mapLevels) )
    #print ( np.amin(mapLevels) )

    img = createImg(mapLevels)

    mapPlot = plt.subplot('111')
    mapPlot.imshow(img, aspect='auto')
    mapPlot.tick_params('both', direction='in')


    fig.savefig('map_Urbaniak.pdf')