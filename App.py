#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc



# In[2]:


app = Dash(__name__, use_pages=True, meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=0.5, maximum-scale=1.2, minimum-scale=0.5,'}],
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           )
server = app.server
app.title = 'EffectiveFootball'

app.layout = html.Div(
    [
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)


if __name__ == '__main__':
    app.run_server(debug=False)

