import pandas as pd
import numpy as np
import math
from operator import add
import AnalyseVariables as av
import sys

#%matplotlib inline
eplData = pd.read_csv("~/progs/BettingPredictor/data/EPL20142015Odds.csv")
total = eplData['Result'].count()
wins = eplData[eplData['Result']==1]
draws = eplData[eplData['Result']==0]
loss = eplData[eplData['Result']==-1]
loseordraw = eplData[eplData['Result']!=1]

names = eplData.columns.values.tolist()
infogain = []
entro = []
minvarent = []
cutval = []
cutdir = []
mini = []
maxi = []
effratio = []
effwin = []
efflod = []

count = 0

vrange = av.getRange(eplData['Result'])
resultprob = av.GetValProbs(eplData,'Result',vrange,total)
resultentropy = av.calcentropy(eplData,'Result',vrange,total)

count = 0
for name in names:
    sys.stdout.write("\r" + name + " " + str(count) + ":                     ")
    sys.stdout.flush()
    count = count + 1
    if eplData[name].dtype == np.int64:

        vrange = av.getRange(eplData[name])
        mini.append(vrange[0])
        maxi.append(vrange[1])
        ent = av.ConditionalEntropy(eplData,name,resultentropy,vrange,resultprob)
        infogain.append(ent[0])
        entro.append(ent[1])
        cut = av.bestCut(eplData,name,vrange,resultprob)
        cutval.append(cut[1])
        minvarent.append(cut[0])
        cutdir.append(cut[2])
        effic = av.getEfficiencies(eplData,name,cut[1],cut[2])
        effratio.append(effic[0])
        effwin.append(effic[1])
        efflod.append(effic[2])


    else:
        entro.append(0.0)
        infogain.append(0.0)
        cutval.append(0.0)
        minvarent.append(0.0)
        cutdir.append(0.0)
        mini.append(0.0)
        maxi.append(0.0)
        effratio.append(0.0)
        effwin.append(0.0)
        efflod.append(0.0)

print "DONE"
analysis_results = pd.DataFrame(
    {'Variable Names': names,
     'Information Gain': infogain,
     'Entropy': entro,
     'Minimum Entropy': minvarent,
     'Cut Value': cutval,
     'Cut Direction': cutdir,
     'Minimum': mini,
     'Maximum': maxi,
     'Efficiency Ratio': effratio,
     'Efficiency Win': effwin,
     'Efficiency Lose or Draw': efflod
    })

analysis_results = analysis_results.sort_values('Information Gain')
analysis_results.to_csv('analysis_results.csv')
print(analysis_results)
