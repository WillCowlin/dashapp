#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Glossary', title='Glossary | EffectiveFootball')

layout = dbc.Container([
    dbc.Row([dcc.Markdown(
        '''Soon...''',
        style={'color':'white'})]),
])