#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


# In[ ]:


dash.register_page(__name__, name='Search', title='Search | EffectiveFootball')

layout = dbc.Container([
    dbc.Row([dcc.Markdown(
        '''Soon...''',
        style={'color':'white'})]),
])
