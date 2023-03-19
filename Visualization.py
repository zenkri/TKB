# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import base64
import ssl
import pickle as pkl

ssl._create_default_https_context = ssl._create_unverified_context

encoded_image = base64.b64encode(open('./logo.png', 'rb').read())

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="35px")),
                        dbc.Col(dbc.NavbarBrand("Technische Kunden-Begleitung", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="#AFE1AF",
    dark=False,
    sticky="top",
)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

with open('./dataset.pkl', 'rb') as f:
    df = pkl.load(f)
    f.close()

fig1 = px.pie(df, values='event', names='location', color_discrete_sequence=px.colors.sequential.Blugrn,
              title='Anzahl Besucher')
fig2 = px.pie(df, values='duration', names='location', color_discrete_sequence=px.colors.sequential.Blugrn,
              title='Durchn. Aufenthalsdauer')
fig3 = px.pie(df, values='wait_time', names='location', color_discrete_sequence=px.colors.sequential.Blugrn,
              title='Durchn. Wartezeit')
# fig3.update_layout(showlegend=False)
fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, entrywidth=70, xanchor="right", x=1))
fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, entrywidth=70, xanchor="right", x=1))
fig3.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, entrywidth=70, xanchor="right", x=1))

fig4 = px.histogram(df, x="time_h", y="duration", color='location',
                    labels={'time_h': 'Uhrzeit', 'duration': 'Dauer [s]'},
                    color_discrete_sequence=px.colors.sequential.Blugrn, title='Verteitung Aufenthaltsdauer')
fig4.update_layout(bargap=0.2)
fig4.update_layout({'plot_bgcolor': 'rgba(255, 255, 255, 1.0)', 'paper_bgcolor': 'rgba(255, 255, 255, 1.0)'})

fig5 = px.histogram(df, x="time_h", y="wait_time", color='location',
                    labels={'time_h': 'Uhrzeit', 'wait_time': 'Dauer [s]'},
                    color_discrete_sequence=px.colors.sequential.Blugrn, title='Verteitung Wartezeit')
fig5.update_layout(bargap=0.2)
fig5.update_layout({'plot_bgcolor': 'rgba(255, 255, 255, 1.0)', 'paper_bgcolor': 'rgba(255, 255, 255, 1.0)'})

fig6 = px.histogram(df, x="day", y="wait_time", color='location', labels={'day': 'Wochentag', 'wait_time': 'Dauer [s]'},
                    color_discrete_sequence=px.colors.sequential.Blugrn, title='Verteitung Aufenthaltsdauer')
fig6.update_layout(bargap=0.2)
fig6.update_layout({'plot_bgcolor': 'rgba(255, 255, 255, 1.0)', 'paper_bgcolor': 'rgba(255, 255, 255, 1.0)'})
fig6.update_xaxes(categoryorder='array', categoryarray=['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])

app.layout = html.Div([

    navbar,

    html.Div(
        dbc.Row(
            dbc.Col([
                dbc.Row(
                    html.H2('Tageswerte')
                ),
                dbc.Row(
                    html.Hr(
                        style={
                            "borderWidth": "0.2vh",
                            "width": "100%",
                            "borderColor": "#097969",
                            "opacity": "unset",
                        }
                    )),
                # width={"size": 10, "offset": 0},
            ])), style={'margin-left': '2%', 'margin-right': '2%', 'margin-top': '1%'}),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig1,
                    style={'width': '100%', 'display': 'inline-block'}
                )]),
            dbc.Col([
                dcc.Graph(
                    id='pop-vs-gdp',
                    figure=fig2,
                    style={'width': '100%', 'display': 'inline-block'}
                )]),
            dbc.Col([
                dcc.Graph(
                    id='pop-vs-gdp',
                    figure=fig3,
                    style={'width': '100%', 'display': 'inline-block'}
                )])
        ]),
    ], style={'margin-left': '2%', 'margin-right': '2%', 'margin-top': '-1%'}),
    html.Div(
        dbc.Row(
            dbc.Col([
                dbc.Row(
                    html.H2('Tagesverlauf', style={'margin-top': '1%'})
                ),
                dbc.Row(
                    html.Hr(
                        style={
                            "borderWidth": "0.2vh",
                            "width": "100%",
                            "borderColor": "#097969",
                            "opacity": "unset",
                        }
                    )),
                # width={"size": 10, "offset": 0},
            ])), style={'margin-left': '2%', 'margin-right': '2%', 'margin-top': '1%'}
    ),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig4,
                    style={'width': '100%', 'display': 'inline-block'}
                )]),
            dbc.Col([
                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig5,
                    style={'width': '100%', 'display': 'inline-block'}
                )]),
        ], style={'margin-left': '2%', 'margin-right': '2%'})]),

    html.Div(
        dbc.Row(
            dbc.Col([
                dbc.Row(
                    html.H2('Wochenverlauf', style={'margin-top': '1%'})
                ),
                dbc.Row(
                    html.Hr(
                        style={
                            "borderWidth": "0.2vh",
                            "width": "100%",
                            "borderColor": "#097969",
                            "opacity": "unset",
                        }
                    )),
                # width={"size": 10, "offset": 0},
            ])), style={'margin-left': '2%', 'margin-right': '2%', 'margin-top': '1%'}
    ),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure=fig6,
                    style={'width': '100%', 'display': 'inline-block'}
                )]),
        ], style={'margin-left': '2%', 'margin-right': '2%'})]),

])

if __name__ == '__main__':
    app.run_server(debug=False)
