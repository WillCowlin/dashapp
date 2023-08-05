#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dash import Dash, dcc, html, Input, Output,callback

import pandas as pd

import numpy as np

import plotly.graph_objects as go

from scipy import stats


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

dfp

#w*x

dfp['o1/3P']=dfp['90s']*dfp['o1/3P']
dfp['oSh']=dfp['90s']*dfp['oSh']
dfp['oLT']=dfp['90s']*dfp['oLT']
dfp['t90s']=dfp['90s']*dfp['t90s']
dfp['oAttT']=dfp['90s']*dfp['oAttT']
dfp['sAttT']=dfp['90s']*dfp['sAttT']
dfp['tg']=dfp['90s']*dfp['tg']
dfp['txA']=dfp['90s']*dfp['txA']

#aggrigate 
dfp=dfp.groupby(dfp['Player/Age'],as_index=False).aggregate({'Player':'first', 'Position':'first','90s':'sum','t90s':'sum',
                                                             'Clr':'sum','o1/3P':'sum','ShBlocked':'sum','oSh':'sum',
                                                             'Lost':'sum','Won':'sum','Tkl':'sum','dTkl':'sum','dTAtt':'sum',
                                                             'oLT':'sum','Recov':'sum','oAttT':'sum','Int':'sum','CmpT':'sum',
                                                             'AttT':'sum','sAttT':'sum','PrgDistT':'sum','PrgDist':'sum',
                                                             'Carries':'sum','Mis':'sum','Dis':'sum','tg':'sum',
                                                             'G-PK':'sum','TOSucc':'sum','TOAtt':'sum','Ast':'sum',
                                                             'xA':'sum','Touches':'sum','txA':'sum','Age':'first','PrgP':'sum',
                                                             'PrgC':'sum'})

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

#calculacte performance metrics
dfp['Clr/1/3']=(dfp['Clr']/dfp['90s'])/(dfp['o1/3P']/dfp['t90s'])
dfp['Blocks/Sh']=(dfp['ShBlocked']/dfp['90s'])/(dfp['oSh']/dfp['t90s'])
dfp['Won%']=dfp['Won']/(dfp['Lost']+dfp['Won'])
dfp['Won/90']=dfp['Won']/dfp['90s']
dfp['dTkl%']=dfp['dTkl']/(dfp['dTAtt'])
dfp['Tkl/oT']=(dfp['Tkl']/dfp['90s'])/(dfp['oLT']/dfp['t90s'])
dfp['Recov/90']=dfp['Recov']/dfp['90s']
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


# In[ ]:


app = Dash(__name__)
server = app.server


app.layout = html.Div([ 
    
    html.Div([dcc.Dropdown(id='searchbar', options=dfp.index, placeholder='Player Search', 
                           value='Erling Haaland', clearable=False,style={'width':'50%','left':140,'font_size':50})]),
    
    html.Div([dcc.Graph(id='radar', config={'displayModeBar':False})])    
])

@app.callback(
    Output('radar','figure'),
    Input('searchbar','value')
)
    

def radar(Player):
    

    
    Position = dfp.loc[Player,'Position']

    dfx = pos[Position]




    dfx['Clr/1/3pc'] = stats.zscore(dfx['Clr/1/3'])
    dfx['Blocks/Shpc'] = stats.zscore(dfx['Blocks/Sh'])
    dfx['Deep defending pc'] = (dfx[['Clr/1/3pc','Blocks/Shpc']].mean(axis=1))
    dfx['Deep defending pc'] = stats.zscore(dfx['Deep defending pc'])
    dfx['Deep Defending'] = [round(stats.percentileofscore(dfx['Deep defending pc'].values, i)) 
                                        for i in dfx['Deep defending pc'].values]
    ##
    dfx['Won/90pc'] = stats.zscore(dfx['Won/90'])
    dfx['Won%pc'] = stats.zscore(dfx['Won%'])
    dfx['Aerial pc'] = (dfx[['Won/90pc','Won%pc']].mean(axis=1))
    dfx['Aerial pc'] = stats.zscore(dfx['Aerial pc'])
    dfx['Aerial'] = [round(stats.percentileofscore(dfx['Aerial pc'].values, i)) 
                                        for i in dfx['Aerial pc'].values]
    ##
    dfx['Tkl/oTpc'] = stats.zscore(dfx['Tkl/oT'])
    dfx['dTkl%pc'] = stats.zscore(dfx['dTkl%'])
    dfx['Tackling pc'] = (dfx[['Tkl/oTpc','dTkl%pc']].mean(axis=1))
    dfx['Tackling pc'] = stats.zscore(dfx['Tackling pc'])
    dfx['Tackling'] = [round(stats.percentileofscore(dfx['Tackling pc'].values, i)) 
                                        for i in dfx['Tackling pc'].values]
    ##
    dfx['Recov/90pc'] = stats.zscore(dfx['Recov/90'])
    dfx['Int/oPpc'] = stats.zscore(dfx['Int/oP'])
    dfx['Anticipating pc'] = (dfx[['Recov/90pc','Int/oPpc']].mean(axis=1))
    dfx['Anticipating pc'] = stats.zscore(dfx['Anticipating pc'])
    dfx['Recovering'] = [round(stats.percentileofscore(dfx['Anticipating pc'].values, i)) 
                                        for i in dfx['Anticipating pc'].values]
    ##
    dfx['P/sPpc'] = stats.zscore(dfx['P/sP'])
    dfx['Pass%pc'] = stats.zscore(dfx['Pass%'])
    dfx['Passing pc'] = (dfx[['P/sPpc','Pass%pc']].mean(axis=1))
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
    dfx['Dribbling pc'] = (dfx[['TOSucc/Cpc','PrgC/Cpc']].mean(axis=1))
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


    dfx=dfx.set_index('Player')
    
    


    fig = go.Figure(data=go.Barpolar(r=[dfx.loc[Player,'Scoring'],dfx.loc[Player,'Aerial'],
             dfx.loc[Player,'Deep Defending'],
             dfx.loc[Player,'Tackling'],
             dfx.loc[Player,'Recovering'],
             dfx.loc[Player,'Passing'],
             dfx.loc[Player,'Pass Progression'],
             dfx.loc[Player,'Control'],
             dfx.loc[Player,'Dribbling'],
             dfx.loc[Player,'Creating']
             
                    ],
          theta=['Scoring','Aerial','Deep Defending','Tackling','Recovering',
                    'Passing','Pass Progression','Control','Dribbling',
                    'Creating'],
            marker_color=['lime','red','red','red','red','dodgerblue','dodgerblue','dodgerblue','dodgerblue','lime'],

                                     opacity=0.5, hoverinfo='none',base=40

        ))

    fig.update_layout(
          polar=dict(radialaxis=dict(visible=True, showticklabels=False, range=(0,150),showline=False, dtick=20,
                                     griddash='dot',gridcolor='white'),
                     angularaxis=dict(direction='clockwise',griddash='longdash',gridcolor='white',linecolor='white')

                    ),
        showlegend=False,dragmode=False, height=650,width=650,font_color='white',template = "plotly_dark"
        )

    fig.add_trace(go.Scatterpolar(r=[0],theta=['Scoring'],marker_color='rgb(17,17,17)',marker_size=127,hoverinfo='none',
                                  mode='text+markers',textfont_color='white',text='<b>'+Pos[Position]+'</b>',textfont_size=40))
    
    fig.add_trace(go.Scatterpolar(r=[dfx.loc[Player,'Scoring']+40,dfx.loc[Player,'Aerial']+40,
             dfx.loc[Player,'Deep Defending']+40,
             dfx.loc[Player,'Tackling']+40,
             dfx.loc[Player,'Recovering']+40,
             dfx.loc[Player,'Passing']+40,
             dfx.loc[Player,'Pass Progression']+40,
             dfx.loc[Player,'Control']+40,
             dfx.loc[Player,'Dribbling']+40,
             dfx.loc[Player,'Creating']+40
             
                    ],
          theta=['Scoring','Aerial','Deep Defending','Tackling','Recovering',
                    'Passing','Pass Progression','Control','Dribbling',
                    'Creating'],

                                     opacity=1,marker_size=25,marker_color='white',textfont_color='rgb(17,17,17)',
                                  hoverinfo='none',mode='text+markers',
        text=(dfx.loc[Player,'Scoring'],dfx.loc[Player,'Aerial'],                                                              
             dfx.loc[Player,'Deep Defending'],
             dfx.loc[Player,'Tackling'],
             dfx.loc[Player,'Recovering'],
             dfx.loc[Player,'Passing'],
             dfx.loc[Player,'Pass Progression'],
             dfx.loc[Player,'Control'],
             dfx.loc[Player,'Dribbling'],
             dfx.loc[Player,'Creating']
             )))
    
    

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)

