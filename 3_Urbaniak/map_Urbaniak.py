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
import math
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

    return (delta,map);


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
        #for col in range(1,500):
        #    if mapLevels[row,col-1] > mapLevels[row,col]: # cieniowanie na podstawie wysokosci
        #        img[row, col] = gradient_map_shading_higher(mapLevels[row, col])
        #    else:   # cieniowanie na podstawie wysokosci
        #        img[row, col] = gradient_map_shading_lower(mapLevels[row, col])
    return img

def slope(fx, fy):
    return math.atan((fx**2 + fy**2)**(1/2)) * 180 / math.pi

def aspect(fx,fy):
    if fx == 0:
        return 0
    return 270 + math.atan(fy/fx) - 90 * fx / math.fabs(fx)

def gradient_map_final(h, slo, asp):
    #TODO swiatlo jest z polnocnego zachodu, z tamtej strony beda rozjasniane, z drugiej przyciemniane
    if asp > 180:
        sat = 1.0 - 8*slo
        val = 1.0
    else:
        sat = 1.0
        val = 1.0 - 8*slo
    if sat < 0:
        print('sat', sat)
    if val < 0:
        print('val', val)
    return hsv2rgb(160 - h, sat, val)
    #return hsv2rgb(160 - h, 1.0, 1.0 - 5*slo) # - to te 'znosne'

def vecSun(x,y,z):
    sunX = -1000
    sunY = 1000
    sunZ = 10000

    return (sunX - x, sunY - y, sunZ - z)

def angleVectors(x1, y1, z1, x2, y2, z2 ):
    val = math.acos((x1*x2 + y1*y2 + z1*z2)/(x1**2+y1**2+z1**2)**(1/2)/(x2**2+y2**2+z2**2)**(1/2))
    return val

def vecNorm(x,y,z,angle):
    #TODO
    return 0

def createImgFinal(mapLevels, delta):
    #TODO
    img = np.zeros((500, 500, 3))
    aspects = []
    for row in range(0,498):
        for col in range(498):
            fx = mapLevels[row,col] - mapLevels[row + 2,col]
            fx += mapLevels[row,col + 1] - mapLevels[row + 2,col + 1]
            fx += mapLevels[row,col + 2] - mapLevels[row + 2,col + 2]
            fx /= 6 * delta
            fy = mapLevels[row,col + 2] - mapLevels[row,col]
            fy += mapLevels[row + 1,col + 2] - mapLevels[row + 1,col]
            fy += mapLevels[row + 2, col + 2] - mapLevels[row + 2, col]
            fy /= 6 * delta
            img[row, col] = gradient_map_final(mapLevels[row, col], slope(fx,fy), aspect(fx,fy))
    return img


if __name__ == '__main__':
    (delta,mapLevels) = loadMapFromURL('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/kolorowanie_mapy/big.dem')
    fig = plt.figure(figsize=(6, 6))
    #print( mapLevels.shape )
    #print ( np.amax(mapLevels) )
    #print ( np.amin(mapLevels) )

    #img = createImg(mapLevels)
    img = createImgFinal(mapLevels, delta)

    mapPlot = plt.subplot('111')
    mapPlot.imshow(img, aspect='auto')
    mapPlot.tick_params('both', direction='in')


    fig.savefig('map_Urbaniak.pdf')