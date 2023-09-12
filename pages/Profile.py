#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash

from dash import Dash, dcc, html, Input, Output,callback

import pandas as pd

import numpy as np

import plotly.graph_objects as go

from scipy import stats

import dash_bootstrap_components as dbc


# In[2]:


dash.register_page(__name__, path='/')


# In[ ]:


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

dfp=dfp.set_index('Player')

pos = {"cb": dfcb,
       "fb": dffb,
       "6": df6,
       "8": df8,
       "10": df10,
       "w": dfw,
       "9":df9
      }

Pos = {"cb": 'CB',
       "fb": 'FB',
       "6": 'DM',
       "8": 'CM',
       "10": 'AM',
       "w": 'W',
       "9": 'ST'
      }

metrics = ['Aerial','Deep Defending','Tackling','Recovering',
                    'Passing','Short Passing','Medium Passing','Long Passing',
                    'Pass Progression & Control','Dribbling',
                    'Creating & Scoring']


X={'Aerial':'Won/90','Deep Defending':'Clr/1/3','Tackling':'Tkl/oT','Recovering':'Int/oP',
                    'Passing':'P/sP','Short Passing':'SP/sP','Medium Passing':'MP/sP','Long Passing':'LP/sP',
                    'Pass Progression & Control':'PrgP/P','Dribbling':'TOSucc/C',
                    'Creating & Scoring':'xA/T'}
Y={'Aerial':'Won%','Deep Defending':'Blocks/Sh','Tackling':'dTkl%','Recovering':'Recov/90',
                    'Passing':'Pass%','Short Passing':'SPass%','Medium Passing':'MPass%','Long Passing':'LPass%',
                    'Pass Progression & Control':'Mis+Dis/C','Dribbling':'PrgC/C',
                    'Creating & Scoring':'G-PK/90'}
XL={'Aerial':'Frequency','Deep Defending':'Clearances','Tackling':'Frequency','Recovering':'Interceptions',
                    'Passing':'Volume','Short Passing':'Volume','Medium Passing':'Volume','Long Passing':'Volume',
                    'Pass Progression & Control':'Pass Progression','Dribbling':'Take Ons',
                    'Creating & Scoring':'Creating'}
YL={'Aerial':'Success Rate','Deep Defending':'Blocks','Tackling':'Success Rate','Recovering':'Recoveries',
                    'Passing':'Success Rate','Short Passing':'Success Rate','Medium Passing':'Success Rate',
                    'Long Passing':'Success Rate',
                    'Pass Progression & Control':'Control','Dribbling':'Carry Progression',
                    'Creating & Scoring':'Scoring'}
XZ={'Aerial':'AFreq','Deep Defending':'Clearances','Tackling':'TFreq','Recovering':'Interceptions',
                    'Passing':'PFreq','Short Passing':'SFreq','Medium Passing':'MFreq','Long Passing':'LFreq',
                    'Pass Progression & Control':'Pass Progression','Dribbling':'Take Ons',
                    'Creating & Scoring':'Creating'}
YZ={'Aerial':'ASucc','Deep Defending':'Blocks','Tackling':'TSucc','Recovering':'Recoveries',
                    'Passing':'PSucc','Short Passing':'SSucc','Medium Passing':'MSucc',
                    'Long Passing':'LSucc',
                    'Pass Progression & Control':'Control','Dribbling':'Carry Progression',
                    'Creating & Scoring':'Scoring'}


# In[ ]:


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='searchbar1', options=dfp.index, placeholder='Player Search',
                            value='Erling Haaland', clearable=False),
            dcc.Graph(id='radar', config={'displayModeBar':False}),
        ], xs=11, sm=11, md=11, lg=11, xl=5),
        dbc.Col([
            dcc.Dropdown(id='searchbar2', options=metrics, placeholder='Metric',
                           value='Aerial', clearable=False),
            dcc.Graph(id='scatter',config={'displayModeBar':False,'showtips':False}),
        ], xs=11, sm=11, md=11, lg=11, xl=5)
    ], justify="center"),
    dbc.Row([
        dcc.Markdown('''###### Data from Opta via [FBref](https://fbref.com/en/)''',style={'color':'white'})])
],fluid=True)

