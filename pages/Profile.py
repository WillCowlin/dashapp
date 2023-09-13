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

card_radar = dbc.Card([
    dbc.CardHeader(
        dcc.Dropdown(id='searchbar1', options=dfp.index, placeholder='Player Search',
                            value='Erling Haaland', clearable=False, style={"width": "550px"})
    ),
    dbc.CardBody(
        dcc.Graph(id='radar', config={'displayModeBar':False})
    )
],color='rgb(17,17,17)',style={"width": "650px", 'height':'650px'},className="align-items-center")

card_scatter = dbc.Card([
    dbc.CardHeader(
        dcc.Dropdown(id='searchbar2', options=metrics, placeholder='Metric',
                     value='Aerial', clearable=False, style={"width": "550px"})
    ),
    dbc.CardBody(
        dcc.Graph(id='scatter',config={'displayModeBar':False,'showtips':False})
    )
],color='rgb(17,17,17)',style={"width": "650px", 'height':'650px'},className="align-items-center ")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(card_radar,width="auto"), dbc.Col(card_scatter,width="auto")
    ],justify="center")

],fluid=True)


@callback(
    Output('radar', 'figure'),
    Input('searchbar1', 'value')
)
def radar(Player):
    Position = dfp.loc[Player, 'Position']

    dfx = pos[Position]

    dfx['Clr/1/3pc'] = stats.zscore(dfx['Clr/1/3'])
    dfx['Blocks/Shpc'] = stats.zscore(dfx['Blocks/Sh'])
    dfx['Deep defending pc'] = (dfx[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
    dfx['Deep defending pc'] = stats.zscore(dfx['Deep defending pc'])
    dfx['Deep Defending'] = [round(stats.percentileofscore(dfx['Deep defending pc'].values, i))
                             for i in dfx['Deep defending pc'].values]

    ##
    dfx['Won/90pc'] = stats.zscore(dfx['Won/90'])
    dfx['Won%pc'] = stats.zscore(dfx['Won%'])
    dfx['Aerial pc'] = (dfx[['Won/90pc', 'Won%pc']].mean(axis=1))
    dfx['Aerial pc'] = stats.zscore(dfx['Aerial pc'])
    dfx['Aerial'] = [round(stats.percentileofscore(dfx['Aerial pc'].values, i))
                     for i in dfx['Aerial pc'].values]

    ##
    dfx['Tkl/oTpc'] = stats.zscore(dfx['Tkl/oT'])
    dfx['dTkl%pc'] = stats.zscore(dfx['dTkl%'])
    dfx['Tackling pc'] = (dfx[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
    dfx['Tackling pc'] = stats.zscore(dfx['Tackling pc'])
    dfx['Tackling'] = [round(stats.percentileofscore(dfx['Tackling pc'].values, i))
                       for i in dfx['Tackling pc'].values]

    ##
    dfx['Recov/90pc'] = stats.zscore(dfx['Recov/90'])
    dfx['Int/oPpc'] = stats.zscore(dfx['Int/oP'])
    dfx['Anticipating pc'] = (dfx[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
    dfx['Anticipating pc'] = stats.zscore(dfx['Anticipating pc'])
    dfx['Recovering'] = [round(stats.percentileofscore(dfx['Anticipating pc'].values, i))
                         for i in dfx['Anticipating pc'].values]

    ##
    dfx['P/sPpc'] = stats.zscore(dfx['P/sP'])
    dfx['Pass%pc'] = stats.zscore(dfx['Pass%'])
    dfx['Passing pc'] = (dfx[['P/sPpc', 'Pass%pc']].mean(axis=1))
    dfx['Passing pc'] = stats.zscore(dfx['Passing pc'])
    dfx['Passing'] = [round(stats.percentileofscore(dfx['Passing pc'].values, i))
                      for i in dfx['Passing pc'].values]
    ##
    dfx['Pass Progression pc'] = stats.zscore(dfx['PrgP/P'])
    dfx['Pass Progression'] = [round(stats.percentileofscore(dfx['Pass Progression pc'].values, i))
                               for i in dfx['Pass Progression pc'].values]
    ##
    dfx['Control pc'] = -stats.zscore(dfx['Mis+Dis/C'])
    dfx['Control'] = [round(stats.percentileofscore(dfx['Control pc'].values, i))
                      for i in dfx['Control pc'].values]
    ##
    dfx['PrgC/Cpc'] = stats.zscore(dfx['PrgC/C'])
    dfx['TOSucc/Cpc'] = stats.zscore(dfx['TOSucc/C'])
    dfx['TO%pc'] = stats.zscore(dfx['TO%'])
    dfx['Dribbling pc'] = (dfx[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
    dfx['Dribbling pc'] = stats.zscore(dfx['Dribbling pc'])
    dfx['Dribbling'] = [round(stats.percentileofscore(dfx['Dribbling pc'].values, i))
                        for i in dfx['Dribbling pc'].values]
    ##
    dfx['Creating pc'] = stats.zscore(dfx['xA/T'])
    dfx['Creating'] = [round(stats.percentileofscore(dfx['Creating pc'].values, i))
                       for i in dfx['Creating pc'].values]
    ##
    dfx['G-PK/90pc'] = stats.zscore(dfx['G-PK/90'])
    dfx['G%pc'] = stats.zscore(dfx['G%'])
    dfx['Scoring pc'] = (dfx[['G-PK/90pc']].mean(axis=1))
    dfx['Scoring pc'] = stats.zscore(dfx['Scoring pc'])
    dfx['Scoring'] = [round(stats.percentileofscore(dfx['Scoring pc'].values, i))
                      for i in dfx['Scoring pc'].values]

    dfx = dfx.set_index('Player')

    fig1 = go.Figure(data=go.Barpolar(r=[dfx.loc[Player, 'Scoring'], dfx.loc[Player, 'Aerial'],
                                         dfx.loc[Player, 'Deep Defending'],
                                         dfx.loc[Player, 'Tackling'],
                                         dfx.loc[Player, 'Recovering'],
                                         dfx.loc[Player, 'Passing'],
                                         dfx.loc[Player, 'Pass Progression'],
                                         dfx.loc[Player, 'Control'],
                                         dfx.loc[Player, 'Dribbling'],
                                         dfx.loc[Player, 'Creating']

                                         ],
                                      theta=['Scoring', 'Aerial', 'Deep Defending', 'Tackling', 'Recovering',
                                             'Passing', 'Pass Progression', 'Control', 'Dribbling',
                                             'Creating'],
                                      marker_color=['lime', 'red', 'red', 'red', 'red', 'dodgerblue', 'dodgerblue',
                                                    'dodgerblue', 'dodgerblue', 'lime'],

                                      opacity=0.5, hoverinfo='none', base=40

                                      ))

    fig1.update_layout(
        polar=dict(radialaxis=dict(visible=True, showticklabels=False, range=(0, 150), showline=False, dtick=20,
                                   griddash='dot', gridcolor='white'),
                   angularaxis=dict(direction='clockwise', griddash='longdash', gridcolor='white', linecolor='white'),
                   ),
        showlegend=False, dragmode=False, margin=dict(l=50, r=90, t=85, b=50), height=550, width=550,
        font_color='white', template="plotly_dark",
        title=dict(
            text="Data from Opta via <a href=\"https://fbref.com/en/\">FBref</a>",
            x=0, y=0.99,
            font=dict(size=14)
        )

    )

    fig1.add_trace(
        go.Scatterpolar(r=[0], theta=['Scoring'], marker_color='rgb(17,17,17)', marker_size=111, hoverinfo='none',
                        mode='text+markers', textfont_color='white', text='<b>' + Pos[Position] + '</b>',
                        textfont_size=40))

    fig1.add_trace(go.Scatterpolar(r=[dfx.loc[Player, 'Scoring'] + 40, dfx.loc[Player, 'Aerial'] + 40,
                                      dfx.loc[Player, 'Deep Defending'] + 40,
                                      dfx.loc[Player, 'Tackling'] + 40,
                                      dfx.loc[Player, 'Recovering'] + 40,
                                      dfx.loc[Player, 'Passing'] + 40,
                                      dfx.loc[Player, 'Pass Progression'] + 40,
                                      dfx.loc[Player, 'Control'] + 40,
                                      dfx.loc[Player, 'Dribbling'] + 40,
                                      dfx.loc[Player, 'Creating'] + 40

                                      ],
                                   theta=['Scoring', 'Aerial', 'Deep Defending', 'Tackling', 'Recovering',
                                          'Passing', 'Pass Progression', 'Control', 'Dribbling',
                                          'Creating'],

                                   opacity=1, marker_size=25, marker_color='white', textfont_color='rgb(17,17,17)',
                                   hoverinfo='none', mode='text+markers',
                                   text=(dfx.loc[Player, 'Scoring'], dfx.loc[Player, 'Aerial'],
                                         dfx.loc[Player, 'Deep Defending'],
                                         dfx.loc[Player, 'Tackling'],
                                         dfx.loc[Player, 'Recovering'],
                                         dfx.loc[Player, 'Passing'],
                                         dfx.loc[Player, 'Pass Progression'],
                                         dfx.loc[Player, 'Control'],
                                         dfx.loc[Player, 'Dribbling'],
                                         dfx.loc[Player, 'Creating']
                                         )))

    return fig1


@callback(
    Output('scatter', 'figure'),
    Input('searchbar1', 'value'),
    Input('searchbar2', 'value')
)
def scatter(Player, Metric):
    Position2 = dfp.loc[Player, 'Position']

    dfX = pos[Position2]
    dfY = dfX[dfX['Player'] == Player]

    x = X[Metric]
    y = Y[Metric]
    xl = XL[Metric]
    yl = YL[Metric]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=dfX[x], y=dfX[y], mode='markers', hovertemplate=dfX['Player'],
                              marker_size=10, marker_color='darkgrey', marker_symbol='circle-open-dot', name=''))

    fig2.add_trace(go.Scatter(x=dfY[x], y=dfY[y], mode='markers', hovertemplate=dfY['Player'],
                              marker_size=10, marker_color='red', marker_symbol='circle-open-dot',
                              name=''))
    fig2.update_xaxes(showgrid=False,
                      linecolor='white',
                      zeroline=False, showticklabels=False)
    fig2.update_yaxes(showgrid=False,
                      linecolor='white',
                      zeroline=False, showticklabels=False)

    fig2.update_layout(paper_bgcolor='rgb(17,17,17)', plot_bgcolor='rgb(17,17,17)',
                       font_color='white', title={'x': 0.5}, template="plotly_dark",
                       margin=dict(l=50, r=50, t=85, b=50), height=550, width=550,
                       showlegend=False, dragmode=False, xaxis_title='', yaxis_title='')

    if Metric == 'Pass Progression & Control':
        fig2.update_yaxes(autorange="reversed")

    fig2.add_shape(type="line",
                   x0=np.percentile(dfX[x], 50, interpolation='midpoint'), y0=dfX[y].min(),
                   x1=np.percentile(dfX[x], 50, interpolation='midpoint'), y1=dfX[y].max(),
                   line=dict(color="white", width=1, dash='dot'))

    fig2.add_shape(type="line",
                   x0=dfX[x].min(), y0=np.percentile(dfX[y], 50, interpolation='midpoint'),
                   x1=dfX[x].max(), y1=np.percentile(dfX[y], 50, interpolation='midpoint'),
                   line=dict(color="white", width=1, dash='dot'))

    dfz = pos[Position2]

    dfz['Clr/1/3pc'] = stats.zscore(dfz['Clr/1/3'])
    dfz['Blocks/Shpc'] = stats.zscore(dfz['Blocks/Sh'])
    dfz['Deep defending pc'] = (dfz[['Clr/1/3pc', 'Blocks/Shpc']].mean(axis=1))
    dfz['Deep defending pc'] = stats.zscore(dfz['Deep defending pc'])
    dfz['Deep Defending'] = [round(stats.percentileofscore(dfz['Deep defending pc'].values, i))
                             for i in dfz['Deep defending pc'].values]
    dfz['Clearances'] = [round(stats.percentileofscore(dfz['Clr/1/3'].values, i))
                         for i in dfz['Clr/1/3'].values]
    dfz['Blocks'] = [round(stats.percentileofscore(dfz['Blocks/Sh'].values, i))
                     for i in dfz['Blocks/Sh'].values]
    ##
    dfz['Won/90pc'] = stats.zscore(dfz['Won/90'])
    dfz['Won%pc'] = stats.zscore(dfz['Won%'])
    dfz['Aerial pc'] = (dfz[['Won/90pc', 'Won%pc']].mean(axis=1))
    dfz['Aerial pc'] = stats.zscore(dfz['Aerial pc'])
    dfz['Aerial'] = [round(stats.percentileofscore(dfz['Aerial pc'].values, i))
                     for i in dfz['Aerial pc'].values]
    dfz['ASucc'] = [round(stats.percentileofscore(dfz['Won%'].values, i))
                    for i in dfz['Won%'].values]
    dfz['AFreq'] = [round(stats.percentileofscore(dfz['Won/90'].values, i))
                    for i in dfz['Won/90'].values]
    ##
    dfz['Tkl/oTpc'] = stats.zscore(dfz['Tkl/oT'])
    dfz['dTkl%pc'] = stats.zscore(dfz['dTkl%'])
    dfz['Tackling pc'] = (dfz[['Tkl/oTpc', 'dTkl%pc']].mean(axis=1))
    dfz['Tackling pc'] = stats.zscore(dfz['Tackling pc'])
    dfz['Tackling'] = [round(stats.percentileofscore(dfz['Tackling pc'].values, i))
                       for i in dfz['Tackling pc'].values]
    dfz['TSucc'] = [round(stats.percentileofscore(dfz['dTkl%'].values, i))
                    for i in dfz['dTkl%'].values]
    dfz['TFreq'] = [round(stats.percentileofscore(dfz['Tkl/oT'].values, i))
                    for i in dfz['Tkl/oT'].values]
    ##
    dfz['Recov/90pc'] = stats.zscore(dfz['Recov/90'])
    dfz['Int/oPpc'] = stats.zscore(dfz['Int/oP'])
    dfz['Anticipating pc'] = (dfz[['Recov/90pc', 'Int/oPpc']].mean(axis=1))
    dfz['Anticipating pc'] = stats.zscore(dfz['Anticipating pc'])
    dfz['Recovering'] = [round(stats.percentileofscore(dfz['Anticipating pc'].values, i))
                         for i in dfz['Anticipating pc'].values]
    dfz['Recoveries'] = [round(stats.percentileofscore(dfz['Recov/90'].values, i))
                         for i in dfz['Recov/90'].values]
    dfz['Interceptions'] = [round(stats.percentileofscore(dfz['Int/oP'].values, i))
                            for i in dfz['Int/oP'].values]
    ##
    dfz['P/sPpc'] = stats.zscore(dfz['P/sP'])
    dfz['Pass%pc'] = stats.zscore(dfz['Pass%'])
    dfz['Passing pc'] = (dfz[['P/sPpc', 'Pass%pc']].mean(axis=1))
    dfz['Passing pc'] = stats.zscore(dfz['Passing pc'])
    dfz['Passing'] = [round(stats.percentileofscore(dfz['Passing pc'].values, i))
                      for i in dfz['Passing pc'].values]
    dfz['PSucc'] = [round(stats.percentileofscore(dfz['Pass%'].values, i))
                    for i in dfz['Pass%'].values]
    dfz['PFreq'] = [round(stats.percentileofscore(dfz['P/sP'].values, i))
                    for i in dfz['P/sP'].values]
    dfz['SP/sPpc'] = stats.zscore(dfz['SP/sP'])
    dfz['SPass%pc'] = stats.zscore(dfz['SPass%'])
    dfz['SPassing pc'] = (dfz[['SP/sPpc', 'SPass%pc']].mean(axis=1))
    dfz['SPassing pc'] = stats.zscore(dfz['SPassing pc'])
    dfz['Short Passing'] = [round(stats.percentileofscore(dfz['SPassing pc'].values, i))
                            for i in dfz['SPassing pc'].values]
    dfz['SSucc'] = [round(stats.percentileofscore(dfz['SPass%'].values, i))
                    for i in dfz['SPass%'].values]
    dfz['SFreq'] = [round(stats.percentileofscore(dfz['SP/sP'].values, i))
                    for i in dfz['SP/sP'].values]
    dfz['MP/sPpc'] = stats.zscore(dfz['MP/sP'])
    dfz['MPass%pc'] = stats.zscore(dfz['MPass%'])
    dfz['MPassing pc'] = (dfz[['MP/sPpc', 'MPass%pc']].mean(axis=1))
    dfz['MPassing pc'] = stats.zscore(dfz['MPassing pc'])
    dfz['Medium Passing'] = [round(stats.percentileofscore(dfz['MPassing pc'].values, i))
                             for i in dfz['MPassing pc'].values]
    dfz['MSucc'] = [round(stats.percentileofscore(dfz['MPass%'].values, i))
                    for i in dfz['MPass%'].values]
    dfz['MFreq'] = [round(stats.percentileofscore(dfz['MP/sP'].values, i))
                    for i in dfz['MP/sP'].values]
    dfz['LP/sPpc'] = stats.zscore(dfz['LP/sP'])
    dfz['LPass%pc'] = stats.zscore(dfz['LPass%'])
    dfz['LPassing pc'] = (dfz[['LP/sPpc', 'LPass%pc']].mean(axis=1))
    dfz['LPassing pc'] = stats.zscore(dfz['LPassing pc'])
    dfz['Long Passing'] = [round(stats.percentileofscore(dfz['LPassing pc'].values, i))
                           for i in dfz['LPassing pc'].values]
    dfz['LSucc'] = [round(stats.percentileofscore(dfz['LPass%'].values, i))
                    for i in dfz['LPass%'].values]
    dfz['LFreq'] = [round(stats.percentileofscore(dfz['LP/sP'].values, i))
                    for i in dfz['LP/sP'].values]
    ##
    dfz['Pass Progression pc'] = stats.zscore(dfz['PrgP/P'])
    dfz['Pass Progression'] = [round(stats.percentileofscore(dfz['Pass Progression pc'].values, i))
                               for i in dfz['Pass Progression pc'].values]
    ##
    dfz['Control pc'] = -stats.zscore(dfz['Mis+Dis/C'])
    dfz['Control'] = [round(stats.percentileofscore(dfz['Control pc'].values, i))
                      for i in dfz['Control pc'].values]
    ##
    dfz['PrgC/Cpc'] = stats.zscore(dfz['PrgC/C'])
    dfz['TOSucc/Cpc'] = stats.zscore(dfz['TOSucc/C'])
    dfz['TO%pc'] = stats.zscore(dfz['TO%'])
    dfz['Dribbling pc'] = (dfz[['TOSucc/Cpc', 'PrgC/Cpc']].mean(axis=1))
    dfz['Dribbling pc'] = stats.zscore(dfz['Dribbling pc'])
    dfz['Dribbling'] = [round(stats.percentileofscore(dfz['Dribbling pc'].values, i))
                        for i in dfz['Dribbling pc'].values]
    dfz['Take Ons'] = [round(stats.percentileofscore(dfz['TOSucc/C'].values, i))
                       for i in dfz['TOSucc/C'].values]
    dfz['Carry Progression'] = [round(stats.percentileofscore(dfz['PrgC/C'].values, i))
                                for i in dfz['PrgC/C'].values]
    ##
    dfz['Creating pc'] = stats.zscore(dfz['xA/T'])
    dfz['Creating'] = [round(stats.percentileofscore(dfz['Creating pc'].values, i))
                       for i in dfz['Creating pc'].values]
    ##
    dfz['G-PK/90pc'] = stats.zscore(dfz['G-PK/90'])
    dfz['G%pc'] = stats.zscore(dfz['G%'])
    dfz['Scoring pc'] = (dfz[['G-PK/90pc']].mean(axis=1))
    dfz['Scoring pc'] = stats.zscore(dfz['Scoring pc'])
    dfz['Scoring'] = [round(stats.percentileofscore(dfz['Scoring pc'].values, i))
                      for i in dfz['Scoring pc'].values]

    dfz['C&S pc'] = (dfz[['Creating pc', 'G-PK/90pc']].mean(axis=1))
    dfz['C&S pc'] = stats.zscore(dfz['C&S pc'])
    dfz['Creating & Scoring'] = [round(stats.percentileofscore(dfz['C&S pc'].values, i))
                                 for i in dfz['C&S pc'].values]

    dfz['Pass Progression & Control'] = 'N/A'

    dfz = dfz.set_index('Player')

    fig2.add_annotation(text="<span style='color:rgb(17,17,17)'> Pass Progression & Control </span>"+ '<br>' + xl + '<br>' + str(dfz.loc[Player, XZ[Metric]])+ '<br>'+' ',
                        align='center',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.9,
                        y=1.2,

                        bordercolor='white',
                        borderwidth=1,
                        font=dict(color="white", size=12))

    fig2.add_annotation(text="<span style='color:rgb(17,17,17)'> Pass Progression & Control </span>"+ '<br>' +yl + '<br>' + str(dfz.loc[Player, YZ[Metric]])+ '<br>'+' ',
                        align='center',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.1,
                        y=1.2,

                        bordercolor='white',
                        borderwidth=1,
                        font=dict(color="white", size=12))

    fig2.add_annotation(text=xl,
                        align='center',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=-0.01,
                        yanchor='top',
                        font=dict(color="white", size=12))

    fig2.add_annotation(text=yl,
                        align='center',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=-0.01,
                        y=0.5,
                        xanchor='right',
                        textangle=-90,
                        font=dict(color="white", size=12))

    return fig2