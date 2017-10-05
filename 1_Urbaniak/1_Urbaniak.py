#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs
import csv
import matplotlib.pyplot as plt

def main():
    urlStream = [ \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/2cel-rs.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/2cel.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/cel-rs.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/cel.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/rsel.csv")]
    seriesNames = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
    plt.figure(figsize=(3, 3))
    for i in range(len(urlStream)):
        csvReader = csv.reader(codecs.iterdecode(urlStream[i], 'utf-8'))
        generation = []
        gamesPlayed = [] #x1000
        gamesPercentWon = []
        next(csvReader, None)
        for row in csvReader:
            generation.append(int(row[0]))
            gamesPlayed.append(float(row[1])/1000)
            suma = 0.0
            for col in range(2,len(row)):
                suma += float(row[col])
            gamesPercentWon.append(suma*100/(len(row) - 2))
        plt.plot(gamesPlayed, gamesPercentWon, label = seriesNames[i])
    plt.legend()
    plt.savefig('1_Urbaniak.pdf')
    plt.close()
        

if __name__ == '__main__':
        main()
