#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash

from dash import Dash, dcc, html, State, Input, Output, callback, dash_table

import dash_ag_grid as dag

import pandas as pd

import numpy as np

import plotly.graph_objects as go

from scipy import stats

import dash_bootstrap_components as dbc


# In[2]:
dash.register_page(__name__, name='Filter & Compare', title='Filter & Compare | EffectiveFootball')

#load data

dfp = pd.read_csv (r'https://raw.githubusercontent.com/WillCowlin/dashapp/main/22%2023%20Players.csv', index_col=False)
dfp = dfp.rename(columns=dfp.iloc[0]).drop(dfp.index[0])
dfp.index = range(0,len(dfp))
cols = dfp.columns
cols = cols.drop(['Rk','Player','Position','Nation','Pos','Squad','Comp','Age','Born','Matches'])
for col in cols:
    dfp[col] = dfp[col].astype(float)

dfs = pd.read_csv (r'https://raw.githubusercontent.com/WillCowlin/dashapp/main/22%2023%20squad.csv', index_col=False)
dfs = dfs.rename(columns=dfs.iloc[0]).drop(dfs.index[0])
dfs.index = range(0,len(dfs))
cols = dfs.columns
cols = cols.drop(['Rk','Squad','Comp'])
for col in cols:
    dfs[col] = dfs[col].astype(float)

dfo = pd.read_csv (r'https://raw.githubusercontent.com/WillCowlin/dashapp/main/22%2023%20opponent.csv', index_col=False)
dfo = dfo.rename(columns=dfo.iloc[0]).drop(dfo.index[0])
dfo.index = range(0,len(dfo))
cols = dfo.columns
cols = cols.drop(['Rk','Squad','Comp'])
for col in cols:
    dfo[col] = dfo[col].astype(float)


dfp=dfp.loc[(dfp['Position']!='gk')]
dfp.index = range(0,len(dfp))

dfp['Player/Age']=dfp['Player']+['/']+dfp['Age']
dfp.index = range(0,len(dfp))

#map squad stats to players

dfp['t90s'] = dfp['Squad'].map(dfs.set_index('Squad')['90s'])
dfp.index = range(0,len(dfp))

dfp['tg'] = dfp['Squad'].map(dfs.set_index('Squad')['G-PK'])
dfp.index = range(0,len(dfp))

dfp['o1/3P'] = dfp['Squad'].map(dfo.set_index('Squad')['1/3P'])
dfp.index = range(0,len(dfp))

dfp['oSh'] = dfp['Squad'].map(dfo.set_index('Squad')['Sh'])
dfp.index = range(0,len(dfp))

dfp['oLT'] = dfp['Squad'].map(dfo.set_index('Squad')['LiveTouc'])
dfp.index = range(0,len(dfp))

dfp['oAttT'] = dfp['Squad'].map(dfo.set_index('Squad')['AttT'])
dfp.index = range(0,len(dfp))

dfp['sAttT'] = dfp['Squad'].map(dfs.set_index('Squad')['AttT'])
dfp.index = range(0,len(dfp))

dfp['txA'] = dfp['Squad'].map(dfs.set_index('Squad')['xA'])
dfp.index = range(0,len(dfp))

dfp['TRecov'] = dfp['Squad'].map(dfs.set_index('Squad')['Recov']) + dfp['Squad'].map(dfo.set_index('Squad')['Recov'])
dfp.index = range(0,len(dfp))

#w*x

dfp['o1/3P']=dfp['90s']*dfp['o1/3P']
dfp['oSh']=dfp['90s']*dfp['oSh']
dfp['oLT']=dfp['90s']*dfp['oLT']
dfp['t90s']=dfp['90s']*dfp['t90s']
dfp['oAttT']=dfp['90s']*dfp['oAttT']
dfp['sAttT']=dfp['90s']*dfp['sAttT']
dfp['tg']=dfp['90s']*dfp['tg']
dfp['txA']=dfp['90s']*dfp['txA']
dfp['TRecov']=dfp['90s']*dfp['TRecov']


#aggrigate
dfp=dfp.groupby(dfp['Player/Age'],as_index=False).aggregate({'Player':'first', 'Position':'first','90s':'sum','t90s':'sum',
                                                             'Clr':'sum','o1/3P':'sum','ShBlocked':'sum','oSh':'sum',
                                                             'Lost':'sum','Won':'sum','Tkl':'sum','dTkl':'sum','dTAtt':'sum',
                                                             'oLT':'sum','Recov':'sum','oAttT':'sum','Int':'sum','CmpT':'sum',
                                                             'AttT':'sum','sAttT':'sum','PrgDistT':'sum','PrgDist':'sum',
                                                             'Carries':'sum','Mis':'sum','Dis':'sum','tg':'sum',
                                                             'G-PK':'sum','TOSucc':'sum','TOAtt':'sum','Ast':'sum',
                                                             'xA':'sum','Touches':'sum','txA':'sum','Age':'first','PrgP':'sum',
                                                             'PrgC':'sum','CmpS':'sum','AttS':'sum','CmpM':'sum','AttM':'sum',
                                                             'CmpL':'sum','AttL':'sum','TRecov':'sum'})

dfp=dfp.loc[(dfp['90s']>=13.6)]
dfp.index = range(0,len(dfp))

#calculate weighted means
dfp['t90s']=dfp['t90s']/dfp['90s']
dfp['o1/3P']=dfp['o1/3P']/dfp['90s']
dfp['oSh']=dfp['oSh']/dfp['90s']
dfp['oLT']=dfp['oLT']/dfp['90s']
dfp['oAttT']=dfp['oAttT']/dfp['90s']
dfp['sAttT']=dfp['sAttT']/dfp['90s']
dfp['tg']=dfp['tg']/dfp['90s']
dfp['txA']=dfp['txA']/dfp['90s']
dfp['TRecov']=dfp['TRecov']/dfp['90s']

#calculacte performance metrics
dfp['Clr/1/3']=(dfp['Clr']/dfp['90s'])/(dfp['o1/3P']/dfp['t90s'])
dfp['Blocks/Sh']=(dfp['ShBlocked']/dfp['90s'])/(dfp['oSh']/dfp['t90s'])
dfp['Won%']=dfp['Won']/(dfp['Lost']+dfp['Won'])
dfp['Won/90']=dfp['Won']/dfp['90s']
dfp['dTkl%']=dfp['dTkl']/(dfp['dTAtt'])
dfp['Tkl/oT']=(dfp['Tkl']/dfp['90s'])/(dfp['oLT']/dfp['t90s'])
dfp['Recov/90']=(dfp['Recov']/dfp['90s'])/(dfp['TRecov']/dfp['t90s'])
dfp['Int/oP']=(dfp['Int']/dfp['90s'])/(dfp['oAttT']/dfp['t90s'])
dfp['Pass%']=dfp['CmpT']/dfp['AttT']
dfp['P/sP']=(dfp['CmpT']/dfp['90s'])/(dfp['sAttT']/dfp['t90s'])
dfp['PrgP/P']=dfp['PrgDistT']/dfp['AttT']
dfp['PrgC/C']=dfp['PrgDist']/dfp['Carries']
dfp['Mis+Dis/C']=(dfp['Mis']+dfp['Dis'])/dfp['Carries']
dfp['G-PK/90']=dfp['G-PK']/dfp['90s']
dfp['G%']=dfp['G-PK/90']/(dfp['tg']/dfp['t90s'])
dfp['TO%']=dfp['TOSucc']/dfp['TOAtt']
dfp['TO%']=dfp['TO%'].replace(np.nan, 0)
dfp['TOSucc/C']=dfp['TOSucc']/dfp['Carries']
dfp['xA/T']=dfp['xA']/dfp['Touches']
dfp['Ast/90']=dfp['Ast']/dfp['90s']
dfp['PassF']=dfp['AttT']-dfp['CmpT']
dfp['Lost/T']=(dfp['PassF']+dfp['Mis']+dfp['Dis'])/dfp['Touches']
dfp['g/xA']=dfp['G-PK/90']/(dfp['txA']/dfp['t90s'])
dfp['SPass%']=dfp['CmpS']/dfp['AttS']*100
dfp['SP/sP']=(dfp['CmpS']/dfp['90s'])/(dfp['sAttT']/dfp['t90s'])*500
dfp['MPass%']=dfp['CmpM']/dfp['AttM']*100
dfp['MP/sP']=(dfp['CmpM']/dfp['90s'])/(dfp['sAttT']/dfp['t90s'])*500
dfp['LPass%']=dfp['CmpL']/dfp['AttL']*100
dfp['LP/sP']=(dfp['CmpL']/dfp['90s'])/(dfp['sAttT']/dfp['t90s'])*500

#make position numbers strings
dfp['Position'] = dfp['Position'].apply(str)

#locate ST
df9 = dfp[dfp['Position'].str.contains('9', na=False)]
df9.index = range(0,len(df9))

#locate W
dfw = dfp[dfp['Position'].str.contains('w', na=False)]
dfw.index = range(0,len(dfw))

#locate 10
df10 = dfp[dfp['Position'].str.contains('10', na=False)]
df10.index = range(0,len(df10))

#locate 8
df8 = dfp[dfp['Position'].str.contains('8', na=False)]
df8.index = range(0,len(df8))

#locate 6
df6 = dfp[dfp['Position'].str.contains('6', na=False)]
df6.index = range(0,len(df6))

#Locate FB
dffb = dfp[dfp['Position'].str.contains('fb', na=False)]
dffb.index = range(0,len(dffb))

#Locate CB
dfcb = dfp[dfp['Position'].str.contains('cb', na=False)]
dfcb.index = range(0,len(dfcb))

#Locate gk
dfgk = dfp[dfp['Position'].str.contains('gk', na=False)]
dfgk.index = range(0,len(dfgk))


# In[3]:


df9['Clr/1/3pc'] = stats.zscore(df9['Clr/1/3'])
df9['Blocks/Shpc'] = stats.zscore(df9['Blocks/Sh'])
df9['Deep defending pc'] = (df9[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
df9['Deep defending pc'] = stats.zscore(df9['Deep defending pc'])
df9['Deep Defending'] = [round(stats.percentileofscore(df9['Deep defending pc'].values, i))
                         for i in df9['Deep defending pc'].values]
df9['Clearances'] = [round(stats.percentileofscore(df9['Clr/1/3'].values, i))
                     for i in df9['Clr/1/3'].values]
df9['Blocks'] = [round(stats.percentileofscore(df9['Blocks/Sh'].values, i))
                 for i in df9['Blocks/Sh'].values]
##
df9['Won/90pc'] = stats.zscore(df9['Won/90'])
df9['Won%pc'] = stats.zscore(df9['Won%'])
df9['Aerial pc'] = (df9[['Won/90pc', 'Won%pc']].mean(axis=1))
df9['Aerial pc'] = stats.zscore(df9['Aerial pc'])
df9['Aerial'] = [round(stats.percentileofscore(df9['Aerial pc'].values, i))
                 for i in df9['Aerial pc'].values]
df9['ASucc'] = [round(stats.percentileofscore(df9['Won%'].values, i))
                for i in df9['Won%'].values]
df9['AFreq'] = [round(stats.percentileofscore(df9['Won/90'].values, i))
                for i in df9['Won/90'].values]
##
df9['Tkl/oTpc'] = stats.zscore(df9['Tkl/oT'])
df9['dTkl%pc'] = stats.zscore(df9['dTkl%'])
df9['Tackling pc'] = (df9[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
df9['Tackling pc'] = stats.zscore(df9['Tackling pc'])
df9['Tackling'] = [round(stats.percentileofscore(df9['Tackling pc'].values, i))
                   for i in df9['Tackling pc'].values]
df9['TSucc'] = [round(stats.percentileofscore(df9['dTkl%'].values, i))
                for i in df9['dTkl%'].values]
df9['TFreq'] = [round(stats.percentileofscore(df9['Tkl/oT'].values, i))
                for i in df9['Tkl/oT'].values]
##
df9['Recov/90pc'] = stats.zscore(df9['Recov/90'])
df9['Int/oPpc'] = stats.zscore(df9['Int/oP'])
df9['Anticipating pc'] = (df9[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
df9['Anticipating pc'] = stats.zscore(df9['Anticipating pc'])
df9['Recovering'] = [round(stats.percentileofscore(df9['Anticipating pc'].values, i))
                     for i in df9['Anticipating pc'].values]
df9['Recoveries'] = [round(stats.percentileofscore(df9['Recov/90'].values, i))
                     for i in df9['Recov/90'].values]
df9['Interceptions'] = [round(stats.percentileofscore(df9['Int/oP'].values, i))
                        for i in df9['Int/oP'].values]
##
df9['P/sPpc'] = stats.zscore(df9['P/sP'])
df9['Pass%pc'] = stats.zscore(df9['Pass%'])
df9['Passing pc'] = (df9[['P/sPpc', 'Pass%pc']].mean(axis=1))
df9['Passing pc'] = stats.zscore(df9['Passing pc'])
df9['Passing'] = [round(stats.percentileofscore(df9['Passing pc'].values, i))
                  for i in df9['Passing pc'].values]
df9['PSucc'] = [round(stats.percentileofscore(df9['Pass%'].values, i))
                for i in df9['Pass%'].values]
df9['PFreq'] = [round(stats.percentileofscore(df9['P/sP'].values, i))
                for i in df9['P/sP'].values]
df9['SP/sPpc'] = stats.zscore(df9['SP/sP'])
df9['SPass%pc'] = stats.zscore(df9['SPass%'])
df9['SPassing pc'] = (df9[['SP/sPpc', 'SPass%pc']].mean(axis=1))
df9['SPassing pc'] = stats.zscore(df9['SPassing pc'])
df9['Short Passing'] = [round(stats.percentileofscore(df9['SPassing pc'].values, i))
                        for i in df9['SPassing pc'].values]
df9['SSucc'] = [round(stats.percentileofscore(df9['SPass%'].values, i))
                for i in df9['SPass%'].values]
df9['SFreq'] = [round(stats.percentileofscore(df9['SP/sP'].values, i))
                for i in df9['SP/sP'].values]
df9['MP/sPpc'] = stats.zscore(df9['MP/sP'])
df9['MPass%pc'] = stats.zscore(df9['MPass%'])
df9['MPassing pc'] = (df9[['MP/sPpc', 'MPass%pc']].mean(axis=1))
df9['MPassing pc'] = stats.zscore(df9['MPassing pc'])
df9['Medium Passing'] = [round(stats.percentileofscore(df9['MPassing pc'].values, i))
                         for i in df9['MPassing pc'].values]
df9['MSucc'] = [round(stats.percentileofscore(df9['MPass%'].values, i))
                for i in df9['MPass%'].values]
df9['MFreq'] = [round(stats.percentileofscore(df9['MP/sP'].values, i))
                for i in df9['MP/sP'].values]
df9['LP/sPpc'] = stats.zscore(df9['LP/sP'])
df9['LPass%pc'] = stats.zscore(df9['LPass%'])
df9['LPassing pc'] = (df9[['LP/sPpc', 'LPass%pc']].mean(axis=1))
df9['LPassing pc'] = stats.zscore(df9['LPassing pc'])
df9['Long Passing'] = [round(stats.percentileofscore(df9['LPassing pc'].values, i))
                       for i in df9['LPassing pc'].values]
df9['LSucc'] = [round(stats.percentileofscore(df9['LPass%'].values, i))
                for i in df9['LPass%'].values]
df9['LFreq'] = [round(stats.percentileofscore(df9['LP/sP'].values, i))
                for i in df9['LP/sP'].values]
##
df9['Pass Progression pc'] = stats.zscore(df9['PrgP/P'])
df9['Pass Progression'] = [round(stats.percentileofscore(df9['Pass Progression pc'].values, i))
                           for i in df9['Pass Progression pc'].values]
##
df9['Control pc'] = -stats.zscore(df9['Mis+Dis/C'])
df9['Control'] = [round(stats.percentileofscore(df9['Control pc'].values, i))
                  for i in df9['Control pc'].values]
##
df9['PrgC/Cpc'] = stats.zscore(df9['PrgC/C'])
df9['TOSucc/Cpc'] = stats.zscore(df9['TOSucc/C'])
df9['TO%pc'] = stats.zscore(df9['TO%'])
df9['Dribbling pc'] = (df9[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
df9['Dribbling pc'] = stats.zscore(df9['Dribbling pc'])
df9['Dribbling'] = [round(stats.percentileofscore(df9['Dribbling pc'].values, i))
                    for i in df9['Dribbling pc'].values]
df9['Take Ons'] = [round(stats.percentileofscore(df9['TOSucc/C'].values, i))
                   for i in df9['TOSucc/C'].values]
df9['Carry Progression'] = [round(stats.percentileofscore(df9['PrgC/C'].values, i))
                            for i in df9['PrgC/C'].values]
##
df9['Creating pc'] = stats.zscore(df9['xA/T'])
df9['Creating'] = [round(stats.percentileofscore(df9['Creating pc'].values, i))
                   for i in df9['Creating pc'].values]
##
df9['G-PK/90pc'] = stats.zscore(df9['G-PK/90'])
df9['G%pc'] = stats.zscore(df9['G%'])
df9['Scoring pc'] = (df9[['G-PK/90pc']].mean(axis=1))
df9['Scoring pc'] = stats.zscore(df9['Scoring pc'])
df9['Scoring'] = [round(stats.percentileofscore(df9['Scoring pc'].values, i))
                  for i in df9['Scoring pc'].values]

df9['C&S pc'] = (df9[['Creating pc', 'G-PK/90pc']].mean(axis=1))
df9['C&S pc'] = stats.zscore(df9['C&S pc'])
df9['Creating & Scoring'] = [round(stats.percentileofscore(df9['C&S pc'].values, i))
                             for i in df9['C&S pc'].values]

df9['Pass Progression & Control'] = 'N/A'


# In[4]:


dfw['Clr/1/3pc'] = stats.zscore(dfw['Clr/1/3'])
dfw['Blocks/Shpc'] = stats.zscore(dfw['Blocks/Sh'])
dfw['Deep defending pc'] = (dfw[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
dfw['Deep defending pc'] = stats.zscore(dfw['Deep defending pc'])
dfw['Deep Defending'] = [round(stats.percentileofscore(dfw['Deep defending pc'].values, i))
                         for i in dfw['Deep defending pc'].values]
dfw['Clearances'] = [round(stats.percentileofscore(dfw['Clr/1/3'].values, i))
                     for i in dfw['Clr/1/3'].values]
dfw['Blocks'] = [round(stats.percentileofscore(dfw['Blocks/Sh'].values, i))
                 for i in dfw['Blocks/Sh'].values]
##
dfw['Won/90pc'] = stats.zscore(dfw['Won/90'])
dfw['Won%pc'] = stats.zscore(dfw['Won%'])
dfw['Aerial pc'] = (dfw[['Won/90pc', 'Won%pc']].mean(axis=1))
dfw['Aerial pc'] = stats.zscore(dfw['Aerial pc'])
dfw['Aerial'] = [round(stats.percentileofscore(dfw['Aerial pc'].values, i))
                 for i in dfw['Aerial pc'].values]
dfw['ASucc'] = [round(stats.percentileofscore(dfw['Won%'].values, i))
                for i in dfw['Won%'].values]
dfw['AFreq'] = [round(stats.percentileofscore(dfw['Won/90'].values, i))
                for i in dfw['Won/90'].values]
##
dfw['Tkl/oTpc'] = stats.zscore(dfw['Tkl/oT'])
dfw['dTkl%pc'] = stats.zscore(dfw['dTkl%'])
dfw['Tackling pc'] = (dfw[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
dfw['Tackling pc'] = stats.zscore(dfw['Tackling pc'])
dfw['Tackling'] = [round(stats.percentileofscore(dfw['Tackling pc'].values, i))
                   for i in dfw['Tackling pc'].values]
dfw['TSucc'] = [round(stats.percentileofscore(dfw['dTkl%'].values, i))
                for i in dfw['dTkl%'].values]
dfw['TFreq'] = [round(stats.percentileofscore(dfw['Tkl/oT'].values, i))
                for i in dfw['Tkl/oT'].values]
##
dfw['Recov/90pc'] = stats.zscore(dfw['Recov/90'])
dfw['Int/oPpc'] = stats.zscore(dfw['Int/oP'])
dfw['Anticipating pc'] = (dfw[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
dfw['Anticipating pc'] = stats.zscore(dfw['Anticipating pc'])
dfw['Recovering'] = [round(stats.percentileofscore(dfw['Anticipating pc'].values, i))
                     for i in dfw['Anticipating pc'].values]
dfw['Recoveries'] = [round(stats.percentileofscore(dfw['Recov/90'].values, i))
                     for i in dfw['Recov/90'].values]
dfw['Interceptions'] = [round(stats.percentileofscore(dfw['Int/oP'].values, i))
                        for i in dfw['Int/oP'].values]
##
dfw['P/sPpc'] = stats.zscore(dfw['P/sP'])
dfw['Pass%pc'] = stats.zscore(dfw['Pass%'])
dfw['Passing pc'] = (dfw[['P/sPpc', 'Pass%pc']].mean(axis=1))
dfw['Passing pc'] = stats.zscore(dfw['Passing pc'])
dfw['Passing'] = [round(stats.percentileofscore(dfw['Passing pc'].values, i))
                  for i in dfw['Passing pc'].values]
dfw['PSucc'] = [round(stats.percentileofscore(dfw['Pass%'].values, i))
                for i in dfw['Pass%'].values]
dfw['PFreq'] = [round(stats.percentileofscore(dfw['P/sP'].values, i))
                for i in dfw['P/sP'].values]
dfw['SP/sPpc'] = stats.zscore(dfw['SP/sP'])
dfw['SPass%pc'] = stats.zscore(dfw['SPass%'])
dfw['SPassing pc'] = (dfw[['SP/sPpc', 'SPass%pc']].mean(axis=1))
dfw['SPassing pc'] = stats.zscore(dfw['SPassing pc'])
dfw['Short Passing'] = [round(stats.percentileofscore(dfw['SPassing pc'].values, i))
                        for i in dfw['SPassing pc'].values]
dfw['SSucc'] = [round(stats.percentileofscore(dfw['SPass%'].values, i))
                for i in dfw['SPass%'].values]
dfw['SFreq'] = [round(stats.percentileofscore(dfw['SP/sP'].values, i))
                for i in dfw['SP/sP'].values]
dfw['MP/sPpc'] = stats.zscore(dfw['MP/sP'])
dfw['MPass%pc'] = stats.zscore(dfw['MPass%'])
dfw['MPassing pc'] = (dfw[['MP/sPpc', 'MPass%pc']].mean(axis=1))
dfw['MPassing pc'] = stats.zscore(dfw['MPassing pc'])
dfw['Medium Passing'] = [round(stats.percentileofscore(dfw['MPassing pc'].values, i))
                         for i in dfw['MPassing pc'].values]
dfw['MSucc'] = [round(stats.percentileofscore(dfw['MPass%'].values, i))
                for i in dfw['MPass%'].values]
dfw['MFreq'] = [round(stats.percentileofscore(dfw['MP/sP'].values, i))
                for i in dfw['MP/sP'].values]
dfw['LP/sPpc'] = stats.zscore(dfw['LP/sP'])
dfw['LPass%pc'] = stats.zscore(dfw['LPass%'])
dfw['LPassing pc'] = (dfw[['LP/sPpc', 'LPass%pc']].mean(axis=1))
dfw['LPassing pc'] = stats.zscore(dfw['LPassing pc'])
dfw['Long Passing'] = [round(stats.percentileofscore(dfw['LPassing pc'].values, i))
                       for i in dfw['LPassing pc'].values]
dfw['LSucc'] = [round(stats.percentileofscore(dfw['LPass%'].values, i))
                for i in dfw['LPass%'].values]
dfw['LFreq'] = [round(stats.percentileofscore(dfw['LP/sP'].values, i))
                for i in dfw['LP/sP'].values]
##
dfw['Pass Progression pc'] = stats.zscore(dfw['PrgP/P'])
dfw['Pass Progression'] = [round(stats.percentileofscore(dfw['Pass Progression pc'].values, i))
                           for i in dfw['Pass Progression pc'].values]
##
dfw['Control pc'] = -stats.zscore(dfw['Mis+Dis/C'])
dfw['Control'] = [round(stats.percentileofscore(dfw['Control pc'].values, i))
                  for i in dfw['Control pc'].values]
##
dfw['PrgC/Cpc'] = stats.zscore(dfw['PrgC/C'])
dfw['TOSucc/Cpc'] = stats.zscore(dfw['TOSucc/C'])
dfw['TO%pc'] = stats.zscore(dfw['TO%'])
dfw['Dribbling pc'] = (dfw[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
dfw['Dribbling pc'] = stats.zscore(dfw['Dribbling pc'])
dfw['Dribbling'] = [round(stats.percentileofscore(dfw['Dribbling pc'].values, i))
                    for i in dfw['Dribbling pc'].values]
dfw['Take Ons'] = [round(stats.percentileofscore(dfw['TOSucc/C'].values, i))
                   for i in dfw['TOSucc/C'].values]
dfw['Carry Progression'] = [round(stats.percentileofscore(dfw['PrgC/C'].values, i))
                            for i in dfw['PrgC/C'].values]
##
dfw['Creating pc'] = stats.zscore(dfw['xA/T'])
dfw['Creating'] = [round(stats.percentileofscore(dfw['Creating pc'].values, i))
                   for i in dfw['Creating pc'].values]
##
dfw['G-PK/90pc'] = stats.zscore(dfw['G-PK/90'])
dfw['G%pc'] = stats.zscore(dfw['G%'])
dfw['Scoring pc'] = (dfw[['G-PK/90pc']].mean(axis=1))
dfw['Scoring pc'] = stats.zscore(dfw['Scoring pc'])
dfw['Scoring'] = [round(stats.percentileofscore(dfw['Scoring pc'].values, i))
                  for i in dfw['Scoring pc'].values]

dfw['C&S pc'] = (dfw[['Creating pc', 'G-PK/90pc']].mean(axis=1))
dfw['C&S pc'] = stats.zscore(dfw['C&S pc'])
dfw['Creating & Scoring'] = [round(stats.percentileofscore(dfw['C&S pc'].values, i))
                             for i in dfw['C&S pc'].values]

dfw['Pass Progression & Control'] = 'N/A'


# In[5]:


df10['Clr/1/3pc'] = stats.zscore(df10['Clr/1/3'])
df10['Blocks/Shpc'] = stats.zscore(df10['Blocks/Sh'])
df10['Deep defending pc'] = (df10[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
df10['Deep defending pc'] = stats.zscore(df10['Deep defending pc'])
df10['Deep Defending'] = [round(stats.percentileofscore(df10['Deep defending pc'].values, i))
                         for i in df10['Deep defending pc'].values]
df10['Clearances'] = [round(stats.percentileofscore(df10['Clr/1/3'].values, i))
                     for i in df10['Clr/1/3'].values]
df10['Blocks'] = [round(stats.percentileofscore(df10['Blocks/Sh'].values, i))
                 for i in df10['Blocks/Sh'].values]
##
df10['Won/90pc'] = stats.zscore(df10['Won/90'])
df10['Won%pc'] = stats.zscore(df10['Won%'])
df10['Aerial pc'] = (df10[['Won/90pc', 'Won%pc']].mean(axis=1))
df10['Aerial pc'] = stats.zscore(df10['Aerial pc'])
df10['Aerial'] = [round(stats.percentileofscore(df10['Aerial pc'].values, i))
                 for i in df10['Aerial pc'].values]
df10['ASucc'] = [round(stats.percentileofscore(df10['Won%'].values, i))
                for i in df10['Won%'].values]
df10['AFreq'] = [round(stats.percentileofscore(df10['Won/90'].values, i))
                for i in df10['Won/90'].values]
##
df10['Tkl/oTpc'] = stats.zscore(df10['Tkl/oT'])
df10['dTkl%pc'] = stats.zscore(df10['dTkl%'])
df10['Tackling pc'] = (df10[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
df10['Tackling pc'] = stats.zscore(df10['Tackling pc'])
df10['Tackling'] = [round(stats.percentileofscore(df10['Tackling pc'].values, i))
                   for i in df10['Tackling pc'].values]
df10['TSucc'] = [round(stats.percentileofscore(df10['dTkl%'].values, i))
                for i in df10['dTkl%'].values]
df10['TFreq'] = [round(stats.percentileofscore(df10['Tkl/oT'].values, i))
                for i in df10['Tkl/oT'].values]
##
df10['Recov/90pc'] = stats.zscore(df10['Recov/90'])
df10['Int/oPpc'] = stats.zscore(df10['Int/oP'])
df10['Anticipating pc'] = (df10[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
df10['Anticipating pc'] = stats.zscore(df10['Anticipating pc'])
df10['Recovering'] = [round(stats.percentileofscore(df10['Anticipating pc'].values, i))
                     for i in df10['Anticipating pc'].values]
df10['Recoveries'] = [round(stats.percentileofscore(df10['Recov/90'].values, i))
                     for i in df10['Recov/90'].values]
df10['Interceptions'] = [round(stats.percentileofscore(df10['Int/oP'].values, i))
                        for i in df10['Int/oP'].values]
##
df10['P/sPpc'] = stats.zscore(df10['P/sP'])
df10['Pass%pc'] = stats.zscore(df10['Pass%'])
df10['Passing pc'] = (df10[['P/sPpc', 'Pass%pc']].mean(axis=1))
df10['Passing pc'] = stats.zscore(df10['Passing pc'])
df10['Passing'] = [round(stats.percentileofscore(df10['Passing pc'].values, i))
                  for i in df10['Passing pc'].values]
df10['PSucc'] = [round(stats.percentileofscore(df10['Pass%'].values, i))
                for i in df10['Pass%'].values]
df10['PFreq'] = [round(stats.percentileofscore(df10['P/sP'].values, i))
                for i in df10['P/sP'].values]
df10['SP/sPpc'] = stats.zscore(df10['SP/sP'])
df10['SPass%pc'] = stats.zscore(df10['SPass%'])
df10['SPassing pc'] = (df10[['SP/sPpc', 'SPass%pc']].mean(axis=1))
df10['SPassing pc'] = stats.zscore(df10['SPassing pc'])
df10['Short Passing'] = [round(stats.percentileofscore(df10['SPassing pc'].values, i))
                        for i in df10['SPassing pc'].values]
df10['SSucc'] = [round(stats.percentileofscore(df10['SPass%'].values, i))
                for i in df10['SPass%'].values]
df10['SFreq'] = [round(stats.percentileofscore(df10['SP/sP'].values, i))
                for i in df10['SP/sP'].values]
df10['MP/sPpc'] = stats.zscore(df10['MP/sP'])
df10['MPass%pc'] = stats.zscore(df10['MPass%'])
df10['MPassing pc'] = (df10[['MP/sPpc', 'MPass%pc']].mean(axis=1))
df10['MPassing pc'] = stats.zscore(df10['MPassing pc'])
df10['Medium Passing'] = [round(stats.percentileofscore(df10['MPassing pc'].values, i))
                         for i in df10['MPassing pc'].values]
df10['MSucc'] = [round(stats.percentileofscore(df10['MPass%'].values, i))
                for i in df10['MPass%'].values]
df10['MFreq'] = [round(stats.percentileofscore(df10['MP/sP'].values, i))
                for i in df10['MP/sP'].values]
df10['LP/sPpc'] = stats.zscore(df10['LP/sP'])
df10['LPass%pc'] = stats.zscore(df10['LPass%'])
df10['LPassing pc'] = (df10[['LP/sPpc', 'LPass%pc']].mean(axis=1))
df10['LPassing pc'] = stats.zscore(df10['LPassing pc'])
df10['Long Passing'] = [round(stats.percentileofscore(df10['LPassing pc'].values, i))
                       for i in df10['LPassing pc'].values]
df10['LSucc'] = [round(stats.percentileofscore(df10['LPass%'].values, i))
                for i in df10['LPass%'].values]
df10['LFreq'] = [round(stats.percentileofscore(df10['LP/sP'].values, i))
                for i in df10['LP/sP'].values]
##
df10['Pass Progression pc'] = stats.zscore(df10['PrgP/P'])
df10['Pass Progression'] = [round(stats.percentileofscore(df10['Pass Progression pc'].values, i))
                           for i in df10['Pass Progression pc'].values]
##
df10['Control pc'] = -stats.zscore(df10['Mis+Dis/C'])
df10['Control'] = [round(stats.percentileofscore(df10['Control pc'].values, i))
                  for i in df10['Control pc'].values]
##
df10['PrgC/Cpc'] = stats.zscore(df10['PrgC/C'])
df10['TOSucc/Cpc'] = stats.zscore(df10['TOSucc/C'])
df10['TO%pc'] = stats.zscore(df10['TO%'])
df10['Dribbling pc'] = (df10[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
df10['Dribbling pc'] = stats.zscore(df10['Dribbling pc'])
df10['Dribbling'] = [round(stats.percentileofscore(df10['Dribbling pc'].values, i))
                    for i in df10['Dribbling pc'].values]
df10['Take Ons'] = [round(stats.percentileofscore(df10['TOSucc/C'].values, i))
                   for i in df10['TOSucc/C'].values]
df10['Carry Progression'] = [round(stats.percentileofscore(df10['PrgC/C'].values, i))
                            for i in df10['PrgC/C'].values]
##
df10['Creating pc'] = stats.zscore(df10['xA/T'])
df10['Creating'] = [round(stats.percentileofscore(df10['Creating pc'].values, i))
                   for i in df10['Creating pc'].values]
##
df10['G-PK/90pc'] = stats.zscore(df10['G-PK/90'])
df10['G%pc'] = stats.zscore(df10['G%'])
df10['Scoring pc'] = (df10[['G-PK/90pc']].mean(axis=1))
df10['Scoring pc'] = stats.zscore(df10['Scoring pc'])
df10['Scoring'] = [round(stats.percentileofscore(df10['Scoring pc'].values, i))
                  for i in df10['Scoring pc'].values]

df10['C&S pc'] = (df10[['Creating pc', 'G-PK/90pc']].mean(axis=1))
df10['C&S pc'] = stats.zscore(df10['C&S pc'])
df10['Creating & Scoring'] = [round(stats.percentileofscore(df10['C&S pc'].values, i))
                             for i in df10['C&S pc'].values]

df10['Pass Progression & Control'] = 'N/A'


# In[6]:


df8['Clr/1/3pc'] = stats.zscore(df8['Clr/1/3'])
df8['Blocks/Shpc'] = stats.zscore(df8['Blocks/Sh'])
df8['Deep defending pc'] = (df8[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
df8['Deep defending pc'] = stats.zscore(df8['Deep defending pc'])
df8['Deep Defending'] = [round(stats.percentileofscore(df8['Deep defending pc'].values, i))
                         for i in df8['Deep defending pc'].values]
df8['Clearances'] = [round(stats.percentileofscore(df8['Clr/1/3'].values, i))
                     for i in df8['Clr/1/3'].values]
df8['Blocks'] = [round(stats.percentileofscore(df8['Blocks/Sh'].values, i))
                 for i in df8['Blocks/Sh'].values]
##
df8['Won/90pc'] = stats.zscore(df8['Won/90'])
df8['Won%pc'] = stats.zscore(df8['Won%'])
df8['Aerial pc'] = (df8[['Won/90pc', 'Won%pc']].mean(axis=1))
df8['Aerial pc'] = stats.zscore(df8['Aerial pc'])
df8['Aerial'] = [round(stats.percentileofscore(df8['Aerial pc'].values, i))
                 for i in df8['Aerial pc'].values]
df8['ASucc'] = [round(stats.percentileofscore(df8['Won%'].values, i))
                for i in df8['Won%'].values]
df8['AFreq'] = [round(stats.percentileofscore(df8['Won/90'].values, i))
                for i in df8['Won/90'].values]
##
df8['Tkl/oTpc'] = stats.zscore(df8['Tkl/oT'])
df8['dTkl%pc'] = stats.zscore(df8['dTkl%'])
df8['Tackling pc'] = (df8[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
df8['Tackling pc'] = stats.zscore(df8['Tackling pc'])
df8['Tackling'] = [round(stats.percentileofscore(df8['Tackling pc'].values, i))
                   for i in df8['Tackling pc'].values]
df8['TSucc'] = [round(stats.percentileofscore(df8['dTkl%'].values, i))
                for i in df8['dTkl%'].values]
df8['TFreq'] = [round(stats.percentileofscore(df8['Tkl/oT'].values, i))
                for i in df8['Tkl/oT'].values]
##
df8['Recov/90pc'] = stats.zscore(df8['Recov/90'])
df8['Int/oPpc'] = stats.zscore(df8['Int/oP'])
df8['Anticipating pc'] = (df8[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
df8['Anticipating pc'] = stats.zscore(df8['Anticipating pc'])
df8['Recovering'] = [round(stats.percentileofscore(df8['Anticipating pc'].values, i))
                     for i in df8['Anticipating pc'].values]
df8['Recoveries'] = [round(stats.percentileofscore(df8['Recov/90'].values, i))
                     for i in df8['Recov/90'].values]
df8['Interceptions'] = [round(stats.percentileofscore(df8['Int/oP'].values, i))
                        for i in df8['Int/oP'].values]
##
df8['P/sPpc'] = stats.zscore(df8['P/sP'])
df8['Pass%pc'] = stats.zscore(df8['Pass%'])
df8['Passing pc'] = (df8[['P/sPpc', 'Pass%pc']].mean(axis=1))
df8['Passing pc'] = stats.zscore(df8['Passing pc'])
df8['Passing'] = [round(stats.percentileofscore(df8['Passing pc'].values, i))
                  for i in df8['Passing pc'].values]
df8['PSucc'] = [round(stats.percentileofscore(df8['Pass%'].values, i))
                for i in df8['Pass%'].values]
df8['PFreq'] = [round(stats.percentileofscore(df8['P/sP'].values, i))
                for i in df8['P/sP'].values]
df8['SP/sPpc'] = stats.zscore(df8['SP/sP'])
df8['SPass%pc'] = stats.zscore(df8['SPass%'])
df8['SPassing pc'] = (df8[['SP/sPpc', 'SPass%pc']].mean(axis=1))
df8['SPassing pc'] = stats.zscore(df8['SPassing pc'])
df8['Short Passing'] = [round(stats.percentileofscore(df8['SPassing pc'].values, i))
                        for i in df8['SPassing pc'].values]
df8['SSucc'] = [round(stats.percentileofscore(df8['SPass%'].values, i))
                for i in df8['SPass%'].values]
df8['SFreq'] = [round(stats.percentileofscore(df8['SP/sP'].values, i))
                for i in df8['SP/sP'].values]
df8['MP/sPpc'] = stats.zscore(df8['MP/sP'])
df8['MPass%pc'] = stats.zscore(df8['MPass%'])
df8['MPassing pc'] = (df8[['MP/sPpc', 'MPass%pc']].mean(axis=1))
df8['MPassing pc'] = stats.zscore(df8['MPassing pc'])
df8['Medium Passing'] = [round(stats.percentileofscore(df8['MPassing pc'].values, i))
                         for i in df8['MPassing pc'].values]
df8['MSucc'] = [round(stats.percentileofscore(df8['MPass%'].values, i))
                for i in df8['MPass%'].values]
df8['MFreq'] = [round(stats.percentileofscore(df8['MP/sP'].values, i))
                for i in df8['MP/sP'].values]
df8['LP/sPpc'] = stats.zscore(df8['LP/sP'])
df8['LPass%pc'] = stats.zscore(df8['LPass%'])
df8['LPassing pc'] = (df8[['LP/sPpc', 'LPass%pc']].mean(axis=1))
df8['LPassing pc'] = stats.zscore(df8['LPassing pc'])
df8['Long Passing'] = [round(stats.percentileofscore(df8['LPassing pc'].values, i))
                       for i in df8['LPassing pc'].values]
df8['LSucc'] = [round(stats.percentileofscore(df8['LPass%'].values, i))
                for i in df8['LPass%'].values]
df8['LFreq'] = [round(stats.percentileofscore(df8['LP/sP'].values, i))
                for i in df8['LP/sP'].values]
##
df8['Pass Progression pc'] = stats.zscore(df8['PrgP/P'])
df8['Pass Progression'] = [round(stats.percentileofscore(df8['Pass Progression pc'].values, i))
                           for i in df8['Pass Progression pc'].values]
##
df8['Control pc'] = -stats.zscore(df8['Mis+Dis/C'])
df8['Control'] = [round(stats.percentileofscore(df8['Control pc'].values, i))
                  for i in df8['Control pc'].values]
##
df8['PrgC/Cpc'] = stats.zscore(df8['PrgC/C'])
df8['TOSucc/Cpc'] = stats.zscore(df8['TOSucc/C'])
df8['TO%pc'] = stats.zscore(df8['TO%'])
df8['Dribbling pc'] = (df8[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
df8['Dribbling pc'] = stats.zscore(df8['Dribbling pc'])
df8['Dribbling'] = [round(stats.percentileofscore(df8['Dribbling pc'].values, i))
                    for i in df8['Dribbling pc'].values]
df8['Take Ons'] = [round(stats.percentileofscore(df8['TOSucc/C'].values, i))
                   for i in df8['TOSucc/C'].values]
df8['Carry Progression'] = [round(stats.percentileofscore(df8['PrgC/C'].values, i))
                            for i in df8['PrgC/C'].values]
##
df8['Creating pc'] = stats.zscore(df8['xA/T'])
df8['Creating'] = [round(stats.percentileofscore(df8['Creating pc'].values, i))
                   for i in df8['Creating pc'].values]
##
df8['G-PK/90pc'] = stats.zscore(df8['G-PK/90'])
df8['G%pc'] = stats.zscore(df8['G%'])
df8['Scoring pc'] = (df8[['G-PK/90pc']].mean(axis=1))
df8['Scoring pc'] = stats.zscore(df8['Scoring pc'])
df8['Scoring'] = [round(stats.percentileofscore(df8['Scoring pc'].values, i))
                  for i in df8['Scoring pc'].values]

df8['C&S pc'] = (df8[['Creating pc', 'G-PK/90pc']].mean(axis=1))
df8['C&S pc'] = stats.zscore(df8['C&S pc'])
df8['Creating & Scoring'] = [round(stats.percentileofscore(df8['C&S pc'].values, i))
                             for i in df8['C&S pc'].values]

df8['Pass Progression & Control'] = 'N/A'


# In[7]:


df6['Clr/1/3pc'] = stats.zscore(df6['Clr/1/3'])
df6['Blocks/Shpc'] = stats.zscore(df6['Blocks/Sh'])
df6['Deep defending pc'] = (df6[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
df6['Deep defending pc'] = stats.zscore(df6['Deep defending pc'])
df6['Deep Defending'] = [round(stats.percentileofscore(df6['Deep defending pc'].values, i))
                         for i in df6['Deep defending pc'].values]
df6['Clearances'] = [round(stats.percentileofscore(df6['Clr/1/3'].values, i))
                     for i in df6['Clr/1/3'].values]
df6['Blocks'] = [round(stats.percentileofscore(df6['Blocks/Sh'].values, i))
                 for i in df6['Blocks/Sh'].values]
##
df6['Won/90pc'] = stats.zscore(df6['Won/90'])
df6['Won%pc'] = stats.zscore(df6['Won%'])
df6['Aerial pc'] = (df6[['Won/90pc', 'Won%pc']].mean(axis=1))
df6['Aerial pc'] = stats.zscore(df6['Aerial pc'])
df6['Aerial'] = [round(stats.percentileofscore(df6['Aerial pc'].values, i))
                 for i in df6['Aerial pc'].values]
df6['ASucc'] = [round(stats.percentileofscore(df6['Won%'].values, i))
                for i in df6['Won%'].values]
df6['AFreq'] = [round(stats.percentileofscore(df6['Won/90'].values, i))
                for i in df6['Won/90'].values]
##
df6['Tkl/oTpc'] = stats.zscore(df6['Tkl/oT'])
df6['dTkl%pc'] = stats.zscore(df6['dTkl%'])
df6['Tackling pc'] = (df6[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
df6['Tackling pc'] = stats.zscore(df6['Tackling pc'])
df6['Tackling'] = [round(stats.percentileofscore(df6['Tackling pc'].values, i))
                   for i in df6['Tackling pc'].values]
df6['TSucc'] = [round(stats.percentileofscore(df6['dTkl%'].values, i))
                for i in df6['dTkl%'].values]
df6['TFreq'] = [round(stats.percentileofscore(df6['Tkl/oT'].values, i))
                for i in df6['Tkl/oT'].values]
##
df6['Recov/90pc'] = stats.zscore(df6['Recov/90'])
df6['Int/oPpc'] = stats.zscore(df6['Int/oP'])
df6['Anticipating pc'] = (df6[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
df6['Anticipating pc'] = stats.zscore(df6['Anticipating pc'])
df6['Recovering'] = [round(stats.percentileofscore(df6['Anticipating pc'].values, i))
                     for i in df6['Anticipating pc'].values]
df6['Recoveries'] = [round(stats.percentileofscore(df6['Recov/90'].values, i))
                     for i in df6['Recov/90'].values]
df6['Interceptions'] = [round(stats.percentileofscore(df6['Int/oP'].values, i))
                        for i in df6['Int/oP'].values]
##
df6['P/sPpc'] = stats.zscore(df6['P/sP'])
df6['Pass%pc'] = stats.zscore(df6['Pass%'])
df6['Passing pc'] = (df6[['P/sPpc', 'Pass%pc']].mean(axis=1))
df6['Passing pc'] = stats.zscore(df6['Passing pc'])
df6['Passing'] = [round(stats.percentileofscore(df6['Passing pc'].values, i))
                  for i in df6['Passing pc'].values]
df6['PSucc'] = [round(stats.percentileofscore(df6['Pass%'].values, i))
                for i in df6['Pass%'].values]
df6['PFreq'] = [round(stats.percentileofscore(df6['P/sP'].values, i))
                for i in df6['P/sP'].values]
df6['SP/sPpc'] = stats.zscore(df6['SP/sP'])
df6['SPass%pc'] = stats.zscore(df6['SPass%'])
df6['SPassing pc'] = (df6[['SP/sPpc', 'SPass%pc']].mean(axis=1))
df6['SPassing pc'] = stats.zscore(df6['SPassing pc'])
df6['Short Passing'] = [round(stats.percentileofscore(df6['SPassing pc'].values, i))
                        for i in df6['SPassing pc'].values]
df6['SSucc'] = [round(stats.percentileofscore(df6['SPass%'].values, i))
                for i in df6['SPass%'].values]
df6['SFreq'] = [round(stats.percentileofscore(df6['SP/sP'].values, i))
                for i in df6['SP/sP'].values]
df6['MP/sPpc'] = stats.zscore(df6['MP/sP'])
df6['MPass%pc'] = stats.zscore(df6['MPass%'])
df6['MPassing pc'] = (df6[['MP/sPpc', 'MPass%pc']].mean(axis=1))
df6['MPassing pc'] = stats.zscore(df6['MPassing pc'])
df6['Medium Passing'] = [round(stats.percentileofscore(df6['MPassing pc'].values, i))
                         for i in df6['MPassing pc'].values]
df6['MSucc'] = [round(stats.percentileofscore(df6['MPass%'].values, i))
                for i in df6['MPass%'].values]
df6['MFreq'] = [round(stats.percentileofscore(df6['MP/sP'].values, i))
                for i in df6['MP/sP'].values]
df6['LP/sPpc'] = stats.zscore(df6['LP/sP'])
df6['LPass%pc'] = stats.zscore(df6['LPass%'])
df6['LPassing pc'] = (df6[['LP/sPpc', 'LPass%pc']].mean(axis=1))
df6['LPassing pc'] = stats.zscore(df6['LPassing pc'])
df6['Long Passing'] = [round(stats.percentileofscore(df6['LPassing pc'].values, i))
                       for i in df6['LPassing pc'].values]
df6['LSucc'] = [round(stats.percentileofscore(df6['LPass%'].values, i))
                for i in df6['LPass%'].values]
df6['LFreq'] = [round(stats.percentileofscore(df6['LP/sP'].values, i))
                for i in df6['LP/sP'].values]
##
df6['Pass Progression pc'] = stats.zscore(df6['PrgP/P'])
df6['Pass Progression'] = [round(stats.percentileofscore(df6['Pass Progression pc'].values, i))
                           for i in df6['Pass Progression pc'].values]
##
df6['Control pc'] = -stats.zscore(df6['Mis+Dis/C'])
df6['Control'] = [round(stats.percentileofscore(df6['Control pc'].values, i))
                  for i in df6['Control pc'].values]
##
df6['PrgC/Cpc'] = stats.zscore(df6['PrgC/C'])
df6['TOSucc/Cpc'] = stats.zscore(df6['TOSucc/C'])
df6['TO%pc'] = stats.zscore(df6['TO%'])
df6['Dribbling pc'] = (df6[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
df6['Dribbling pc'] = stats.zscore(df6['Dribbling pc'])
df6['Dribbling'] = [round(stats.percentileofscore(df6['Dribbling pc'].values, i))
                    for i in df6['Dribbling pc'].values]
df6['Take Ons'] = [round(stats.percentileofscore(df6['TOSucc/C'].values, i))
                   for i in df6['TOSucc/C'].values]
df6['Carry Progression'] = [round(stats.percentileofscore(df6['PrgC/C'].values, i))
                            for i in df6['PrgC/C'].values]
##
df6['Creating pc'] = stats.zscore(df6['xA/T'])
df6['Creating'] = [round(stats.percentileofscore(df6['Creating pc'].values, i))
                   for i in df6['Creating pc'].values]
##
df6['G-PK/90pc'] = stats.zscore(df6['G-PK/90'])
df6['G%pc'] = stats.zscore(df6['G%'])
df6['Scoring pc'] = (df6[['G-PK/90pc']].mean(axis=1))
df6['Scoring pc'] = stats.zscore(df6['Scoring pc'])
df6['Scoring'] = [round(stats.percentileofscore(df6['Scoring pc'].values, i))
                  for i in df6['Scoring pc'].values]

df6['C&S pc'] = (df6[['Creating pc', 'G-PK/90pc']].mean(axis=1))
df6['C&S pc'] = stats.zscore(df6['C&S pc'])
df6['Creating & Scoring'] = [round(stats.percentileofscore(df6['C&S pc'].values, i))
                             for i in df6['C&S pc'].values]

df6['Pass Progression & Control'] = 'N/A'


# In[8]:


dffb['Clr/1/3pc'] = stats.zscore(dffb['Clr/1/3'])
dffb['Blocks/Shpc'] = stats.zscore(dffb['Blocks/Sh'])
dffb['Deep defending pc'] = (dffb[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
dffb['Deep defending pc'] = stats.zscore(dffb['Deep defending pc'])
dffb['Deep Defending'] = [round(stats.percentileofscore(dffb['Deep defending pc'].values, i))
                         for i in dffb['Deep defending pc'].values]
dffb['Clearances'] = [round(stats.percentileofscore(dffb['Clr/1/3'].values, i))
                     for i in dffb['Clr/1/3'].values]
dffb['Blocks'] = [round(stats.percentileofscore(dffb['Blocks/Sh'].values, i))
                 for i in dffb['Blocks/Sh'].values]
##
dffb['Won/90pc'] = stats.zscore(dffb['Won/90'])
dffb['Won%pc'] = stats.zscore(dffb['Won%'])
dffb['Aerial pc'] = (dffb[['Won/90pc', 'Won%pc']].mean(axis=1))
dffb['Aerial pc'] = stats.zscore(dffb['Aerial pc'])
dffb['Aerial'] = [round(stats.percentileofscore(dffb['Aerial pc'].values, i))
                 for i in dffb['Aerial pc'].values]
dffb['ASucc'] = [round(stats.percentileofscore(dffb['Won%'].values, i))
                for i in dffb['Won%'].values]
dffb['AFreq'] = [round(stats.percentileofscore(dffb['Won/90'].values, i))
                for i in dffb['Won/90'].values]
##
dffb['Tkl/oTpc'] = stats.zscore(dffb['Tkl/oT'])
dffb['dTkl%pc'] = stats.zscore(dffb['dTkl%'])
dffb['Tackling pc'] = (dffb[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
dffb['Tackling pc'] = stats.zscore(dffb['Tackling pc'])
dffb['Tackling'] = [round(stats.percentileofscore(dffb['Tackling pc'].values, i))
                   for i in dffb['Tackling pc'].values]
dffb['TSucc'] = [round(stats.percentileofscore(dffb['dTkl%'].values, i))
                for i in dffb['dTkl%'].values]
dffb['TFreq'] = [round(stats.percentileofscore(dffb['Tkl/oT'].values, i))
                for i in dffb['Tkl/oT'].values]
##
dffb['Recov/90pc'] = stats.zscore(dffb['Recov/90'])
dffb['Int/oPpc'] = stats.zscore(dffb['Int/oP'])
dffb['Anticipating pc'] = (dffb[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
dffb['Anticipating pc'] = stats.zscore(dffb['Anticipating pc'])
dffb['Recovering'] = [round(stats.percentileofscore(dffb['Anticipating pc'].values, i))
                     for i in dffb['Anticipating pc'].values]
dffb['Recoveries'] = [round(stats.percentileofscore(dffb['Recov/90'].values, i))
                     for i in dffb['Recov/90'].values]
dffb['Interceptions'] = [round(stats.percentileofscore(dffb['Int/oP'].values, i))
                        for i in dffb['Int/oP'].values]
##
dffb['P/sPpc'] = stats.zscore(dffb['P/sP'])
dffb['Pass%pc'] = stats.zscore(dffb['Pass%'])
dffb['Passing pc'] = (dffb[['P/sPpc', 'Pass%pc']].mean(axis=1))
dffb['Passing pc'] = stats.zscore(dffb['Passing pc'])
dffb['Passing'] = [round(stats.percentileofscore(dffb['Passing pc'].values, i))
                  for i in dffb['Passing pc'].values]
dffb['PSucc'] = [round(stats.percentileofscore(dffb['Pass%'].values, i))
                for i in dffb['Pass%'].values]
dffb['PFreq'] = [round(stats.percentileofscore(dffb['P/sP'].values, i))
                for i in dffb['P/sP'].values]
dffb['SP/sPpc'] = stats.zscore(dffb['SP/sP'])
dffb['SPass%pc'] = stats.zscore(dffb['SPass%'])
dffb['SPassing pc'] = (dffb[['SP/sPpc', 'SPass%pc']].mean(axis=1))
dffb['SPassing pc'] = stats.zscore(dffb['SPassing pc'])
dffb['Short Passing'] = [round(stats.percentileofscore(dffb['SPassing pc'].values, i))
                        for i in dffb['SPassing pc'].values]
dffb['SSucc'] = [round(stats.percentileofscore(dffb['SPass%'].values, i))
                for i in dffb['SPass%'].values]
dffb['SFreq'] = [round(stats.percentileofscore(dffb['SP/sP'].values, i))
                for i in dffb['SP/sP'].values]
dffb['MP/sPpc'] = stats.zscore(dffb['MP/sP'])
dffb['MPass%pc'] = stats.zscore(dffb['MPass%'])
dffb['MPassing pc'] = (dffb[['MP/sPpc', 'MPass%pc']].mean(axis=1))
dffb['MPassing pc'] = stats.zscore(dffb['MPassing pc'])
dffb['Medium Passing'] = [round(stats.percentileofscore(dffb['MPassing pc'].values, i))
                         for i in dffb['MPassing pc'].values]
dffb['MSucc'] = [round(stats.percentileofscore(dffb['MPass%'].values, i))
                for i in dffb['MPass%'].values]
dffb['MFreq'] = [round(stats.percentileofscore(dffb['MP/sP'].values, i))
                for i in dffb['MP/sP'].values]
dffb['LP/sPpc'] = stats.zscore(dffb['LP/sP'])
dffb['LPass%pc'] = stats.zscore(dffb['LPass%'])
dffb['LPassing pc'] = (dffb[['LP/sPpc', 'LPass%pc']].mean(axis=1))
dffb['LPassing pc'] = stats.zscore(dffb['LPassing pc'])
dffb['Long Passing'] = [round(stats.percentileofscore(dffb['LPassing pc'].values, i))
                       for i in dffb['LPassing pc'].values]
dffb['LSucc'] = [round(stats.percentileofscore(dffb['LPass%'].values, i))
                for i in dffb['LPass%'].values]
dffb['LFreq'] = [round(stats.percentileofscore(dffb['LP/sP'].values, i))
                for i in dffb['LP/sP'].values]
##
dffb['Pass Progression pc'] = stats.zscore(dffb['PrgP/P'])
dffb['Pass Progression'] = [round(stats.percentileofscore(dffb['Pass Progression pc'].values, i))
                           for i in dffb['Pass Progression pc'].values]
##
dffb['Control pc'] = -stats.zscore(dffb['Mis+Dis/C'])
dffb['Control'] = [round(stats.percentileofscore(dffb['Control pc'].values, i))
                  for i in dffb['Control pc'].values]
##
dffb['PrgC/Cpc'] = stats.zscore(dffb['PrgC/C'])
dffb['TOSucc/Cpc'] = stats.zscore(dffb['TOSucc/C'])
dffb['TO%pc'] = stats.zscore(dffb['TO%'])
dffb['Dribbling pc'] = (dffb[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
dffb['Dribbling pc'] = stats.zscore(dffb['Dribbling pc'])
dffb['Dribbling'] = [round(stats.percentileofscore(dffb['Dribbling pc'].values, i))
                    for i in dffb['Dribbling pc'].values]
dffb['Take Ons'] = [round(stats.percentileofscore(dffb['TOSucc/C'].values, i))
                   for i in dffb['TOSucc/C'].values]
dffb['Carry Progression'] = [round(stats.percentileofscore(dffb['PrgC/C'].values, i))
                            for i in dffb['PrgC/C'].values]
##
dffb['Creating pc'] = stats.zscore(dffb['xA/T'])
dffb['Creating'] = [round(stats.percentileofscore(dffb['Creating pc'].values, i))
                   for i in dffb['Creating pc'].values]
##
dffb['G-PK/90pc'] = stats.zscore(dffb['G-PK/90'])
dffb['G%pc'] = stats.zscore(dffb['G%'])
dffb['Scoring pc'] = (dffb[['G-PK/90pc']].mean(axis=1))
dffb['Scoring pc'] = stats.zscore(dffb['Scoring pc'])
dffb['Scoring'] = [round(stats.percentileofscore(dffb['Scoring pc'].values, i))
                  for i in dffb['Scoring pc'].values]

dffb['C&S pc'] = (dffb[['Creating pc', 'G-PK/90pc']].mean(axis=1))
dffb['C&S pc'] = stats.zscore(dffb['C&S pc'])
dffb['Creating & Scoring'] = [round(stats.percentileofscore(dffb['C&S pc'].values, i))
                             for i in dffb['C&S pc'].values]

dffb['Pass Progression & Control'] = 'N/A'


# In[9]:


dfcb['Clr/1/3pc'] = stats.zscore(dfcb['Clr/1/3'])
dfcb['Blocks/Shpc'] = stats.zscore(dfcb['Blocks/Sh'])
dfcb['Deep defending pc'] = (dfcb[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
dfcb['Deep defending pc'] = stats.zscore(dfcb['Deep defending pc'])
dfcb['Deep Defending'] = [round(stats.percentileofscore(dfcb['Deep defending pc'].values, i))
                         for i in dfcb['Deep defending pc'].values]
dfcb['Clearances'] = [round(stats.percentileofscore(dfcb['Clr/1/3'].values, i))
                     for i in dfcb['Clr/1/3'].values]
dfcb['Blocks'] = [round(stats.percentileofscore(dfcb['Blocks/Sh'].values, i))
                 for i in dfcb['Blocks/Sh'].values]
##
dfcb['Won/90pc'] = stats.zscore(dfcb['Won/90'])
dfcb['Won%pc'] = stats.zscore(dfcb['Won%'])
dfcb['Aerial pc'] = (dfcb[['Won/90pc', 'Won%pc']].mean(axis=1))
dfcb['Aerial pc'] = stats.zscore(dfcb['Aerial pc'])
dfcb['Aerial'] = [round(stats.percentileofscore(dfcb['Aerial pc'].values, i))
                 for i in dfcb['Aerial pc'].values]
dfcb['ASucc'] = [round(stats.percentileofscore(dfcb['Won%'].values, i))
                for i in dfcb['Won%'].values]
dfcb['AFreq'] = [round(stats.percentileofscore(dfcb['Won/90'].values, i))
                for i in dfcb['Won/90'].values]
##
dfcb['Tkl/oTpc'] = stats.zscore(dfcb['Tkl/oT'])
dfcb['dTkl%pc'] = stats.zscore(dfcb['dTkl%'])
dfcb['Tackling pc'] = (dfcb[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
dfcb['Tackling pc'] = stats.zscore(dfcb['Tackling pc'])
dfcb['Tackling'] = [round(stats.percentileofscore(dfcb['Tackling pc'].values, i))
                   for i in dfcb['Tackling pc'].values]
dfcb['TSucc'] = [round(stats.percentileofscore(dfcb['dTkl%'].values, i))
                for i in dfcb['dTkl%'].values]
dfcb['TFreq'] = [round(stats.percentileofscore(dfcb['Tkl/oT'].values, i))
                for i in dfcb['Tkl/oT'].values]
##
dfcb['Recov/90pc'] = stats.zscore(dfcb['Recov/90'])
dfcb['Int/oPpc'] = stats.zscore(dfcb['Int/oP'])
dfcb['Anticipating pc'] = (dfcb[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
dfcb['Anticipating pc'] = stats.zscore(dfcb['Anticipating pc'])
dfcb['Recovering'] = [round(stats.percentileofscore(dfcb['Anticipating pc'].values, i))
                     for i in dfcb['Anticipating pc'].values]
dfcb['Recoveries'] = [round(stats.percentileofscore(dfcb['Recov/90'].values, i))
                     for i in dfcb['Recov/90'].values]
dfcb['Interceptions'] = [round(stats.percentileofscore(dfcb['Int/oP'].values, i))
                        for i in dfcb['Int/oP'].values]
##
dfcb['P/sPpc'] = stats.zscore(dfcb['P/sP'])
dfcb['Pass%pc'] = stats.zscore(dfcb['Pass%'])
dfcb['Passing pc'] = (dfcb[['P/sPpc', 'Pass%pc']].mean(axis=1))
dfcb['Passing pc'] = stats.zscore(dfcb['Passing pc'])
dfcb['Passing'] = [round(stats.percentileofscore(dfcb['Passing pc'].values, i))
                  for i in dfcb['Passing pc'].values]
dfcb['PSucc'] = [round(stats.percentileofscore(dfcb['Pass%'].values, i))
                for i in dfcb['Pass%'].values]
dfcb['PFreq'] = [round(stats.percentileofscore(dfcb['P/sP'].values, i))
                for i in dfcb['P/sP'].values]
dfcb['SP/sPpc'] = stats.zscore(dfcb['SP/sP'])
dfcb['SPass%pc'] = stats.zscore(dfcb['SPass%'])
dfcb['SPassing pc'] = (dfcb[['SP/sPpc', 'SPass%pc']].mean(axis=1))
dfcb['SPassing pc'] = stats.zscore(dfcb['SPassing pc'])
dfcb['Short Passing'] = [round(stats.percentileofscore(dfcb['SPassing pc'].values, i))
                        for i in dfcb['SPassing pc'].values]
dfcb['SSucc'] = [round(stats.percentileofscore(dfcb['SPass%'].values, i))
                for i in dfcb['SPass%'].values]
dfcb['SFreq'] = [round(stats.percentileofscore(dfcb['SP/sP'].values, i))
                for i in dfcb['SP/sP'].values]
dfcb['MP/sPpc'] = stats.zscore(dfcb['MP/sP'])
dfcb['MPass%pc'] = stats.zscore(dfcb['MPass%'])
dfcb['MPassing pc'] = (dfcb[['MP/sPpc', 'MPass%pc']].mean(axis=1))
dfcb['MPassing pc'] = stats.zscore(dfcb['MPassing pc'])
dfcb['Medium Passing'] = [round(stats.percentileofscore(dfcb['MPassing pc'].values, i))
                         for i in dfcb['MPassing pc'].values]
dfcb['MSucc'] = [round(stats.percentileofscore(dfcb['MPass%'].values, i))
                for i in dfcb['MPass%'].values]
dfcb['MFreq'] = [round(stats.percentileofscore(dfcb['MP/sP'].values, i))
                for i in dfcb['MP/sP'].values]
dfcb['LP/sPpc'] = stats.zscore(dfcb['LP/sP'])
dfcb['LPass%pc'] = stats.zscore(dfcb['LPass%'])
dfcb['LPassing pc'] = (dfcb[['LP/sPpc', 'LPass%pc']].mean(axis=1))
dfcb['LPassing pc'] = stats.zscore(dfcb['LPassing pc'])
dfcb['Long Passing'] = [round(stats.percentileofscore(dfcb['LPassing pc'].values, i))
                       for i in dfcb['LPassing pc'].values]
dfcb['LSucc'] = [round(stats.percentileofscore(dfcb['LPass%'].values, i))
                for i in dfcb['LPass%'].values]
dfcb['LFreq'] = [round(stats.percentileofscore(dfcb['LP/sP'].values, i))
                for i in dfcb['LP/sP'].values]
##
dfcb['Pass Progression pc'] = stats.zscore(dfcb['PrgP/P'])
dfcb['Pass Progression'] = [round(stats.percentileofscore(dfcb['Pass Progression pc'].values, i))
                           for i in dfcb['Pass Progression pc'].values]
##
dfcb['Control pc'] = -stats.zscore(dfcb['Mis+Dis/C'])
dfcb['Control'] = [round(stats.percentileofscore(dfcb['Control pc'].values, i))
                  for i in dfcb['Control pc'].values]
##
dfcb['PrgC/Cpc'] = stats.zscore(dfcb['PrgC/C'])
dfcb['TOSucc/Cpc'] = stats.zscore(dfcb['TOSucc/C'])
dfcb['TO%pc'] = stats.zscore(dfcb['TO%'])
dfcb['Dribbling pc'] = (dfcb[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
dfcb['Dribbling pc'] = stats.zscore(dfcb['Dribbling pc'])
dfcb['Dribbling'] = [round(stats.percentileofscore(dfcb['Dribbling pc'].values, i))
                    for i in dfcb['Dribbling pc'].values]
dfcb['Take Ons'] = [round(stats.percentileofscore(dfcb['TOSucc/C'].values, i))
                   for i in dfcb['TOSucc/C'].values]
dfcb['Carry Progression'] = [round(stats.percentileofscore(dfcb['PrgC/C'].values, i))
                            for i in dfcb['PrgC/C'].values]
##
dfcb['Creating pc'] = stats.zscore(dfcb['xA/T'])
dfcb['Creating'] = [round(stats.percentileofscore(dfcb['Creating pc'].values, i))
                   for i in dfcb['Creating pc'].values]
##
dfcb['G-PK/90pc'] = stats.zscore(dfcb['G-PK/90'])
dfcb['G%pc'] = stats.zscore(dfcb['G%'])
dfcb['Scoring pc'] = (dfcb[['G-PK/90pc']].mean(axis=1))
dfcb['Scoring pc'] = stats.zscore(dfcb['Scoring pc'])
dfcb['Scoring'] = [round(stats.percentileofscore(dfcb['Scoring pc'].values, i))
                  for i in dfcb['Scoring pc'].values]

dfcb['C&S pc'] = (dfcb[['Creating pc', 'G-PK/90pc']].mean(axis=1))
dfcb['C&S pc'] = stats.zscore(dfcb['C&S pc'])
dfcb['Creating & Scoring'] = [round(stats.percentileofscore(dfcb['C&S pc'].values, i))
                             for i in dfcb['C&S pc'].values]

dfcb['Pass Progression & Control'] = 'N/A'


# In[16]:


Pos = {"cb": 'CB',
       "fb": 'FB',
       "6": 'DM',
       "8": 'CM',
       "10": 'AM',
       "w": 'W',
       "9": 'ST'
      }

dfp = pd.concat([df9,dfw,df10,df8,df6,dffb,dfcb])
dfp=dfp[['Player','Position','Deep Defending','Aerial','Tackling','Recovering',
                         'Passing','Pass Progression','Control','Dribbling',
                         'Creating','Scoring']]
dfp=dfp.replace({'Position':Pos})
dfp=dfp.sort_values(by='Player')
dfp.index = range(0,len(dfp))








# Sorting operators (https://dash.plotly.com/datatable/filtering)
layout = dbc.Container([
                        dbc.Button(
                            "Filter",
                            id="collapse-button",
                            className="mb-3",
                            color="primary",
                            n_clicks=0,
                            style={'background-color':'rgb(17,17,17)','border-color':'grey'}
                        ),

                        dbc.Collapse([

                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='player', options=dfp['Player'], multi=True, placeholder="Select Player(s)",)),
                            dbc.Col(dcc.Dropdown(id='position',options=['CB','FB','DM','CM','AM','W','ST'], multi=True, placeholder="Select Position(s)",)),
                        ]),

                        dbc.Row([html.Br()]),

                        dbc.Row([
                            dbc.Col([dcc.Markdown('Deep Defending',style={'color':'white','font-size':'12px','text-align': 'center'}), dcc.Slider(0,100,1,value=0,id='dd',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Aerial',style={'color':'white','font-size':'12px','text-align': 'center'}), dcc.Slider(0, 100, 1, value=0,id='aerial',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Tackling',style={'color':'white','font-size':'12px','text-align': 'center'}), dcc.Slider(0, 100, 1, value=0,id='tackling',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Recovering',style={'color':'white','font-size':'12px','text-align': 'center'}), dcc.Slider(0, 100, 1, value=0,id='recovering',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})])
                        ]),

                        dbc.Row([html.Br()]),

                        dbc.Row([
                            dbc.Col([dcc.Markdown('Passing',style={'color':'white','font-size':'12px','text-align': 'center'}),dcc.Slider(0,100,1,value=0,id='passing',
                                                marks=None,tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Pass Progression',style={'color':'white','font-size':'12px','text-align': 'center'}),dcc.Slider(0, 100, 1, value=0,id='pp',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Control',style={'color':'white','font-size':'12px','text-align': 'center'}),dcc.Slider(0, 100, 1, value=0,id='control',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Dribbling',style={'color':'white','font-size':'12px','text-align': 'center'}),dcc.Slider(0, 100, 1, value=0,id='dribbling',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})])
                        ]),

                        dbc.Row([html.Br()]),

                        dbc.Row([
                            dbc.Col([]),
                            dbc.Col([dcc.Markdown('Creating',style={'color':'white','font-size':'12px','text-align': 'center'}),dcc.Slider(0,100,1,value=0,id='creating',
                                                marks=None,tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([dcc.Markdown('Scoring',style={'color':'white','font-size':'12px','text-align': 'center'}),dcc.Slider(0, 100, 1, value=0,id='scoring',
                                                      marks=None,
                                                      tooltip={"placement": "bottom", "always_visible": True})]),
                            dbc.Col([])
                        ])],id="collapse",is_open=False),

                        dbc.Row([html.Br()]),

                        dbc.Row([
                                dag.AgGrid(id='grid',
                                    columnDefs=[{"field": "Player", "pinned": "left", 'width':'300','headerTooltip':'Player',"tooltipField": 'Player',},
                                                {"field": "Position",'headerTooltip':'Position'},
                                                {"field": "Deep Defending",'headerTooltip':'Deep Defending'},
                                                {"field": "Aerial",'headerTooltip':'Aerial'},
                                                {"field": "Tackling",'headerTooltip':'Tackling'},
                                                {"field": "Recovering",'headerTooltip':'Recovering'},
                                                {"field": "Passing",'headerTooltip':'Passing'},
                                                {"field": "Pass Progression",'headerTooltip':'Pass Progression'},
                                                {"field": "Control",'headerTooltip':'Control'},
                                                {"field": "Dribbling",'headerTooltip':'Dribbling'},
                                                {"field": "Creating",'headerTooltip':'Creating'},
                                                {"field": "Scoring",'headerTooltip':'Scoring'},
                                                ],
                                    rowData=dfp.to_dict("records"),
                                    defaultColDef = {
                                        'sortable': True

                                    },
                                    dashGridOptions={
                                                    'sortingOrder': ['desc', 'asc', None],
                                                    "accentedSort": True,
                                                    'suppressCellSelection':True
                                    },

                                    style={"height": 580, "width": 1500},
                                    className = "ag-theme-alpine-dark",
                                    columnSize='sizeToFit'

                                )

                                ],justify='center'),

                        dbc.Row([html.Br()])

                        ],fluid=True,)

@callback(
    Output('grid', 'rowData'),
    Input('player', 'value'),
    Input('position', 'value'),
    Input('dd', 'value'),
    Input('aerial', 'value'),
    Input('tackling', 'value'),
    Input('recovering', 'value'),
    Input('passing', 'value'),
    Input('pp', 'value'),
    Input('control', 'value'),
    Input('dribbling', 'value'),
    Input('creating', 'value'),
    Input('scoring', 'value'),
)

def update_grid(player_v, position_v,
                dd_v, aerial_v, tackling_v, recovering_v,
                passing_v, pp_v, control_v, dribbling_v,
                creating_v, scoring_v):
    dfx = dfp.copy()
    if player_v:
        dfx = dfx[dfx.Player.isin(player_v)]
    if position_v:
        dfx = dfx[dfx.Position.isin(position_v)]
    dfx = dfx[(dfx['Deep Defending'] >= dd_v)]
    dfx = dfx[(dfx['Aerial'] >= aerial_v)]
    dfx = dfx[(dfx['Tackling'] >= tackling_v)]
    dfx = dfx[(dfx['Recovering'] >= recovering_v)]
    dfx = dfx[(dfx['Passing'] >= passing_v)]
    dfx = dfx[(dfx['Pass Progression'] >= pp_v)]
    dfx = dfx[(dfx['Control'] >= control_v)]
    dfx = dfx[(dfx['Dribbling'] >= dribbling_v)]
    dfx = dfx[(dfx['Creating'] >= creating_v)]
    dfx = dfx[(dfx['Scoring'] >= scoring_v)]
    return dfx.to_dict('records')

@callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    State("collapse", "is_open")
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=False)

