#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs
import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    urlStream = [ \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/2cel-rs.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/2cel.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/cel-rs.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/cel.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/rsel.csv")]
    seriesNames = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
    boxPlotData = []
    plt.figure(figsize=(7, 6))
    scattPlot = plt.subplot('121')
    boxPlot = plt.subplot('122')
    fontSize = 8
    for i in range(len(urlStream)):
        csvReader = csv.reader(codecs.iterdecode(urlStream[i], 'utf-8'))
        gamesPlayed = [] #x1000
        gamesPercentWon = []
        gamesWon = []
        next(csvReader, None)
        for row in csvReader:
            gamesPlayed.append(float(row[1])/1000)
            suma = 0.0
            for col in range(2,len(row)):
                suma += float(row[col])
                gamesWon.append(float(row[col])*100)
            gamesPercentWon.append(suma*100/(len(row) - 2))
        scattPlot.plot(gamesPlayed, gamesPercentWon, label = seriesNames[i])
        boxPlotData.append(gamesWon)
    boxPlot.boxplot(boxPlotData)
    boxPlot.yaxis.tick_right()
    boxPlot.set_ylim(60,100)
    boxPlot.tick_params('both',direction = 'in', labelsize = fontSize)
    boxPlot.grid(color='#D3D3D3', linestyle='dotted', linewidth=1)
    scattPlot.legend()
    scattPlot.tick_params('both',direction = 'in', labelsize = fontSize)
    scattPlot.set_xticks([x*100 for x in range(0, 6)])
    scattPlot.set_yticks([x*5 for x in range(12, 21)])
    scattPlot.set_ylim(60, 100)
    scattPlot.set_xlim(0, 500)
    scattPlot.set_xlabel("Rozegranych gier (×1000)", fontsize = fontSize)
    scattPlot.set_ylabel("Odsetek wygranych gier [%]",multialignment='center', fontsize = fontSize)
    scattPlot.grid(color='#D3D3D3', linestyle='dotted', linewidth=1)
    topAxis = scattPlot.twiny()
    topAxis.set_xlim(0,200)
    topAxis.set_xticks([x*40 for x in range(0, 6)])
    topAxis.set_xlabel('Pokolenie', fontsize = fontSize)
    topAxis.tick_params('both',direction = 'in', labelsize = fontSize)
    plt.savefig('1_Urbaniak.pdf')
    plt.close()
        

if __name__ == '__main__':
        main()
