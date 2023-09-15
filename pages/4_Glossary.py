#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Glossary', title='Glossary | EffectiveFootball')

card_1 = dbc.Card([
    dbc.CardHeader(html.H4("Aerial",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.H5("Success Rate"),
                    html.P("Percentage of aerial duels won"),
                    html.H5("Frequency"),
                    html.P("Aerials won per 90"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_2 = dbc.Card([
    dbc.CardHeader(html.H4("Deep Defending",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.H5("Blocks"),
                    html.P("Shots blocked per opposition shot"),
                    html.H5("Clearances"),
                    html.P("Clearances per opposition final third pass"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_3 = dbc.Card([
    dbc.CardHeader(html.H4("Tackling",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.H5("Success Rate"),
                    html.P("Percentage of opposing dribblers tackled"),
                    html.H5("Frequency"),
                    html.P("Tackles per opposition live touch"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_4 = dbc.Card([
    dbc.CardHeader(html.H4("Recovering",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.H5("Recoveries"),
                    html.P("Loose ball recovered per loose ball"),
                    html.H5("Interceptions"),
                    html.P("Aerials won per 90"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_5 = dbc.Card([
    dbc.CardHeader(html.H4("Passing",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.H5("Success Rate"),
                    html.P("Percentage of passes completed"),
                    html.H5("Frequency"),
                    html.P("Passes per team pass"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_6 = dbc.Card([
    dbc.CardHeader(html.H4("Pass Progression",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.P("Progressive pass distance per completed pass"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_7 = dbc.Card([
    dbc.CardHeader(html.H4("Control",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.P("Miscontrols and dispossessions per carry"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_8 = dbc.Card([
    dbc.CardHeader(html.H4("Dribbling",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.H5("Carry Progression"),
                    html.P("Progressive carry distance per carry"),
                    html.H5("Take Ons"),
                    html.P("Take ons per carry"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_9 = dbc.Card([
    dbc.CardHeader(html.H4("Creating",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.P("Expected assists per touch"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

card_10 = dbc.Card([
    dbc.CardHeader(html.H4("Scoring",style={'color':'white'})),
    dbc.CardBody(
            [
                    html.P("Goals per 90"),
            ],style={'color':'white'}
    ),
],color='rgb(17,17,17)',style={"width": "250px", 'height':'250px'},className="align-items-center")

layout = dbc.Container([
    dbc.Row([card_1,card_2,card_3,card_4,card_5,card_6,card_7,card_8,card_9,card_10],justify="center"),

])