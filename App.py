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

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                    #style={'color':'white', 'background-color':'rgb(17,17,17'},
                    #className="page-link"
                )
                for page in dash.page_registry.values()
            ],
            vertical=False,
            pills=True,
            fill=True,
            justified=True,
            style={'background-color':'rgb(17,17,17)'}
)

app.layout = dbc.Container([
    dbc.Row([sidebar],justify="center"),
    html.Hr(),
    dbc.Row([dash.page_container])
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=False)

