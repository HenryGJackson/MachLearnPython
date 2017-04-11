import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from pathlib import Path


def entropyTerm(prob):
    if prob <= 0.0:
        return 0.0
    else:
        return (-1.0)*prob*math.log(prob)

def getEntropy(fname):

    path = "~/progs/BettingPredictor/data/"
    outname = "Entropy_" + fname
    my_file = Path(path+outname)
    if my_file.is_file():
        df = pd.read_csv(path + outname)
        return df
    else:
        eplData = pd.read_csv(path + fname)
        wins = eplData[eplData['Result']==1]
        lods = eplData[eplData['Result']!=1]
        if wins['Result'].count() < 1:
            print "There are no winning events."
            exit()
        if lods['Result'].count() < 1:
            print "There are no losing or drawing events."
            exit()

        names = eplData.columns.values.tolist()
        numvals = []
        frames = []
        for var in names:
            print var
            i = 0
            eventlistW = []
            eventlistLD = []
            entropy = []
            #INT
            if eplData[var].dtype == np.int64:
                length = eplData[var].max() - eplData[var].min()
                if length == 0:
                    length += 1
                efficienciesW = [0]*(length+1)
                efficienciesLD = [0]*(length+1)
                for x in range(eplData[var].min(),eplData[var].min()+length+1):

                    winsubset = wins[wins[var] == x]
                    efficienciesW[i] = winsubset[var].count()*1.0/wins[var].count()
                    if efficienciesW[i] > 0.0:
                        eventlistW.append(1)
                    else:
                        eventlistW.append(-1)

                    lodsubset = lods[lods[var] == x]
                    efficienciesLD[i] = lodsubset[var].count()*1.0/lods[var].count()
                    if efficienciesLD[i] > 0.0:
                        eventlistLD.append(1)
                    else:
                        eventlistLD.append(-1)

                    entropy.append(entropyTerm(efficienciesW[i])+entropyTerm(efficienciesLD[i]))
                    i += 1
                numvals.append(i-1)
            #end of if integer
            #DOUBLE
            elif eplData[var].dtype == np.float64:
                length = 40
                efficienciesW = [0]*(length+1)
                efficienciesLD = [0]*(length+1)
                myrange = eplData[var].max() - eplData[var].min()
                interval = myrange/length
                for i in range(0,length+1):
                    myval = eplData[var].min() + i*interval

                    winsubset = wins[wins[var] > myval-0.5*interval]
                    winsubset = winsubset[winsubset[var] < myval+0.5*interval]
                    efficienciesW[i] = winsubset[var].count()*1.0/wins[var].count()
                    if efficienciesW[i] > 0.0:
                        eventlistW.append(1)
                    else:
                        eventlistW.append(-1)

                    lodsubset = lods[lods[var] > myval-0.5*interval]
                    lodsubset = lodsubset[lodsubset[var] < myval+0.5*interval]
                    efficienciesLD[i] = lodsubset[var].count()*1.0/lods[var].count()
                    if efficienciesLD[i] > 0.0:
                        eventlistLD.append(1)
                    else:
                        eventlistLD.append(-1)

                    entropy.append(entropyTerm(efficienciesW[i])+entropyTerm(efficienciesLD[i]))
                numvals.append(length+1)
            #end of if Double
            analysis_results = pd.DataFrame(
                {'Entropy': entropy,
                 'WinEventList': eventlistW,
                 'WinEfficiency': efficienciesW,
                 'LoseDrawEventList': eventlistLD,
                 'LoseDrawEfficiency': efficienciesLD
                })
            frames.append(analysis_results)

        AverageEntropy = []
        i = 0
        for frame in frames:
            AverageEntropy.append(sum(frame['Entropy'])/numvals[i])
            i += 1

        variable_entropy = pd.DataFrame(
        {'Name': names,
         'Entropy': AverageEntropy
        })
        # variable_entropy = variable_entropy.sort_values('Entropy')
        variable_entropy.to_csv(path + outname)
        return variable_entropy

df = getEntropy("EPL20142015Odds.csv")
df2 = getEntropy("EPL20152016Odds.csv")
df3 = getEntropy("EPL20132014Odds.csv")

EntSum = []
for i in range(0,len(df)):
    EntSum.append(df['Entropy'][i]+df2['Entropy'][i]+df3['Entropy'][i])

Fdf = pd.DataFrame({
'Name': df['Name'],
'Entropy2013/14': df3['Entropy'],
'Entropy2014/15': df['Entropy'],
'Entropy2015/16': df2['Entropy'],
'SumOfEntropy': EntSum
})
Fdf = Fdf.sort_values('SumOfEntropy')
print Fdf
