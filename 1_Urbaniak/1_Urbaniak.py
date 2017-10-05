#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs
import csv
#import matplotlib.pyplot as plt

def main():
    urlStream = [ \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/2cel-rs.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/2cel.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/cel-rs.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/cel.csv"), \
        urllib.request.urlopen("http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/labs/python/ipd-choices-9-005/rsel.csv")]
    series = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
    for i in range(len(urlPath)):
        csvReader = csv.reader(codecs.iterdecode(urlStream[i], 'utf-8'))
        pokolenie = []
        for row in csvReader:
            pokolenie.append(row[0])

if __name__ == '__main__':
        main()
