import pandas as pd
import numpy as np
import math
from operator import add
# import matplotlib.pyplot as plt


def getRange(data):
    minv = min(data)
    maxv = max(data)
    return (minv, maxv)

def getEntropyVals(probabilities):
    # entropy = [0,0,0]
    entropy = [0]*len(probabilities)
    for i,val in enumerate(probabilities):
        if val == 0:
            entropy[i] = 0.0
        else:
            entropy[i] = (-1)*val*math.log(val,2)

    return entropy

def GetValProbs(data,variable,myrange,total):
    number = myrange[1] - myrange[0]
    probs = [0.0]*(number+1)
    for x in range(0,number):
        for y in data[variable]:
            if y == x + myrange[0]:
                probs[x] = probs[x] + 1;

    probs = [x*(1.0)/total for x in probs]

    return probs

def calcentropy(data,variable,myrange,total):
    probs = GetValProbs(data,variable,myrange,total)
    entropyvals = getEntropyVals(probs)
    entropy = sum(entropyvals)

    return entropy

# "Conditional Entropy Formula" 
def CondEntForm(probXY,probY):
    if isinstance(probXY, list):
        lengthi = len(probXY)
        temp = [0]*lengthi
        for i in range(0,lengthi):
                if probY <= 0.0 or probXY[i] <= 0.0:
                    # print "Error: Probability less than 0. ", probY, probXY
                    temp[i] = 0
                else:
                    temp[i] = probXY[i]*(math.log(probY)-math.log(probXY[i]))
        entropy = sum(temp)
    else:
        if probY <= 0.0 or probXY <= 0.0:
            # print "Error: Probability less than 0. ", probY, probXY
            entropy = 0
        else:
            entropy = probXY*(math.log(probY)-math.log(probXY))
    return entropy

def ConditionalEntropy(data,variable,totentropy,myrange,resultprob):
    length = (myrange[1]-myrange[0])
    valprob = [0]*(length+1)
    winandvalprob = [0]*(length+1)
    drawandvalprob = [0]*(length+1)
    losandvalprob = [0]*(length+1)
    entropy = [0.0]*(length+1)
    total = data[variable].count()
    for i in range(0,len(data[variable])):
        for j in range(0,length+1):
            cutval = myrange[0] + j
            if data[variable][i] == cutval:
                valprob[j] = valprob[j] + 1
                if data['Result'][i] == 1:
                    winandvalprob[j] = winandvalprob[j] + 1
                elif data['Result'][i] == 0:
                    drawandvalprob[j] = drawandvalprob[j] + 1
                else:
                    losandvalprob[j] = losandvalprob[j] + 1

    for i in range(0,length+1):
        if total > 0:
            losandvalprob[i] = losandvalprob[i]*1.0/total
            winandvalprob[i] = winandvalprob[i]*(1.0)/total
            drawandvalprob[i] = drawandvalprob[i]*(1.0)/total
            valprob[i] = valprob[i]*(1.0)/total

        else:
            winandvalprob[i] = 1.0
            losandvalprob[i] = 1.0
            drawandvalprob[i] = 1.0
            valprob[i] = 1.0

    # print valprob, winandvalprob
    # print winandvalprob, resultprob
    entropy = CondEntForm(winandvalprob,resultprob[0])
    entropy = entropy + CondEntForm(losandvalprob,resultprob[2])
    entropy = entropy + CondEntForm(drawandvalprob,resultprob[1])
    # print entropy
    infogain = totentropy - entropy
    # print infogain
    return infogain, entropy

def bestCut(data,variable,myrange,resultprob):
    count = 1+myrange[1]-myrange[0]

    probs = [0]*count
    for x in data[variable]:
        for i in range(0,count):
            if x == i + myrange[0]:
                # print variable, " - x = i + myrange[0] = ", i, " + ", myrange[0], " = ", x
                probs[i] = probs[i] + 1


    total = data[variable].count()
    probs = [x*(1.0)/total for x in probs]
    mysum = 0
    cutval = 0
    entropy = [0]*count
    minentropy = 1000
    cutdirection = -1
    # print probs
    for i in range(0,count):
        entropy[i] = CondEntForm(probs[i],resultprob[0])
        entropy[i] = entropy[i] + CondEntForm(probs[i],resultprob[1])
        entropy[i] = entropy[i] + CondEntForm(probs[i],resultprob[2])
        # print entropy[i]
    sument = [[0]*2 for i in range(0,count)]
    # print variable, entropy
    for i in range(0,count):
        for j in range(0,i):
            sument[i][0] = sument[i][0] + entropy[j]
        for j in range(i,count):
            sument[i][1] = sument[i][1] + entropy[j]

    minentropy = 1000
    for i in range(0,count):
        for j in range(0,2):
            if sument[i][j] < minentropy and sument[i][j] != 0.0:
                minentropy = sument[i][j]
                cutdirection = j
                cutval = i+myrange[0]
    return minentropy, cutval, cutdirection


def getEfficiencies(data,variable,cut,direction):

    if direction == -1:
        print "No Viable cut on ", variable
        return 1.0, 1.0

    dat = data[variable]
    total = dat.count()
    wincount = 0
    for i,x in enumerate(dat):
        if x < cut:
            if data['Result'][i] == 1:
                wincount = wincount + 1

    wineff = (wincount*1.0)/total
    lodeff = 1.0 - wineff

    ratio = wineff/lodeff
    return ratio, wineff, lodeff
