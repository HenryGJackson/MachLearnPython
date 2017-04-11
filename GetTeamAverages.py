import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from pathlib import Path

def GetAverages(df):
    Av = []
    i = 0
    for column in df:
        count = df[column].count()
        if count == 0:
            return 0
        Av.append(sum(df[column])*(1.0)/count)
        i += 1
    return Av

def GetTeamDFs(fname):
    path = "~/progs/BettingPredictor/data/"
    eplData = pd.read_csv(path + fname)
    Teams = pd.read_csv(path + "EPLNames.csv")
    teamdf = pd.DataFrame()

    names = Teams['Team']

    j = 0
    for x in Teams['Code']:
        # teamdf[j] = eplData

        homeframe = eplData[eplData['HomeTeam']==x]
        homeframe = homeframe[homeframe['HomeOrAway']==0]
        awayframe = eplData[eplData['AwayTeam']==x]
        awayframe = awayframe[awayframe['HomeOrAway']==1]

        average = GetAverages(homeframe)
        teamdf[names[j]+" Home"] = average

        average = GetAverages(awayframe)
        teamdf[names[j]+" Away"] = average

        j += 1
    return teamdf

df2 = GetTeamDFs("EPL20142015Odds.csv")
df1 = GetTeamDFs("EPL20132014Odds.csv")
df3 = GetTeamDFs("EPL20152016Odds.csv")


print df1
# def GetAverages(framelist):
