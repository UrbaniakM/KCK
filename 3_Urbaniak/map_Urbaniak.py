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
    delta = int(firstRow[2])/100
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


def createImg(mapLevels, delta):
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

def slope(fx, fy): # bedzie prawdopodobnie niepotrzebne
    return math.atan((fx**2 + fy**2)**(1/2)) * 180 / math.pi

def aspect(fx,fy): # bedzie prwadopodobnei niepotrzebne
    if fx == 0:
        return 0
    return 270 + math.atan(fy/fx) - 90 * fx / math.fabs(fx)

def gradient_map_final(h, angle, position, normalize_vector):
    sat = 1
    val = 1
    position -= 0.5
    if position < 0:
        sat -= np.sin(angle)*abs(position)*1.25
    else:
        val -= np.sin(angle)*abs(position)/2
    if normalize_vector < 0:
        sat = (1+normalize_vector + sat)/2
    else:
        val = (1-normalize_vector + val)/2
    val += 0.20
    return hsv2rgb(160 - h, sat, val)

def vecToSun(x,y,z):
    sunX = 200
    sunY = 100
    sunZ = 2500

    retX = sunZ - z
    retY = sunX - x
    retZ = sunZ - z
    #normalizacja
    vecLenght = abs(retX) + abs(retY) + abs(retZ)
    retX /= vecLenght
    retY /= vecLenght
    retZ /= vecLenght
    return (retX, retY, retZ)

def angle_between_vectors(x1, y1, z1, x2, y2, z2 ):
    val = math.acos((x1*x2 + y1*y2 + z1*z2)/(x1**2+y1**2+z1**2)**(1/2)/(x2**2+y2**2+z2**2)**(1/2))
    return val

def vecNorm(fx,fy):
    retX = -fx
    retY = -fy
    retZ = 1
    vecLenght = abs(retX) + abs(retY) + abs(retZ)
    retX /= vecLenght
    retY /= vecLenght
    retZ /= vecLenght
    return (retX, retY, retZ)

def calculateAngles():
    angles = np.zeros([500, 500])
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
            (xs,ys,zs) = vecToSun(row,col,mapLevels[row,col])
            xsl, ysl, zsl = vecNorm(fx,fy)
            angles[row,col] = angle_between_vectors( xs,ys,zs, xsl,ysl,zsl )
    return angles
  

def createImgFinal(mapLevels, delta):
    img = np.zeros((500, 500, 3))
    for row in range(500):
        for col in range(500):
            img[row, col] = gradient_map_base(mapLevels[row, col]) # bazowy import
    angles = calculateAngles()
    anglesVector = np.sort(np.reshape(angles,-1))
    minAngles = min(anglesVector)
    maxAngles = max(anglesVector)
    for row in range(0,498):
        for col in range(0,498):
            normalize_vector = ((angles[row][col]-minAngles)/(maxAngles-minAngles))*2 - 1
            position = np.where(anglesVector == angles[row][col])[0]
            position = position[0]/len(angles)**2
            img[row,col] = gradient_map_final(mapLevels[row,col], angles[row,col], position, normalize_vector)  
    return img


if __name__ == '__main__':
    (delta,mapLevels) = loadMapFromURL('http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/kolorowanie_mapy/big.dem')
    fig = plt.figure(figsize=(6, 6))

    #img = createImg(mapLevels)
    img = createImgFinal(mapLevels, delta)
    mapPlot = plt.subplot('111')
    mapPlot.imshow(img, aspect='auto')
    mapPlot.tick_params('both', direction='in')


fig.savefig('map_Urbaniak.pdf')
