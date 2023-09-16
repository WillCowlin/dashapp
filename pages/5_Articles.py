#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__, name='Articles', title='Articles | EffectiveFootball')

layout = dbc.Container([
    dbc.Row([dcc.Markdown(
        '''[Dashboard & Data](https://drive.google.com/file/d/1sCi_azGWUrJAjIWANPSa13wJslnmGc1c/view?usp=drive_link)''',
        style={'color':'white'})]),
])