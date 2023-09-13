#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row([dcc.Markdown(
        '''[Twitter](https://twitter.com/EffectiveFball)''',
        style={'color':'white'})]),
    dbc.Row([dcc.Markdown(
        '''[LinkedIn](https://www.linkedin.com/in/will-cowlin-49b689270/)''',
        style={'color':'white'})]),
])