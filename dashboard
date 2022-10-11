import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.graph_objects as go
from dash import dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

final = pd.read_csv('final.csv', sep=';')
player_result = pd.read_csv('player_result.csv', sep=';')
urls = pd.read_csv('urls.csv', sep=';')
df = final.merge(player_result, on = ['Player', 'year', 'Share'])

df['predictions'] = df['predictions'].apply(lambda x : round(x, 3))
df = df[(df['Share'] != 0) | (df['predictions'] > 0.08)]
df = df.merge(urls, on = ['Player', 'year'])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])


# --------------LAYOUT---------------------------------------------------------------------------------------------------------


app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/fr/8/87/NBA_Logo.svg", height="30px")),
                    dbc.Col(dbc.NavbarBrand("NBA PROJECT BY NICOLAS BOERO", className="ms-2"))],
                    align="center",
                    className="g-0")
            ),
            dbc.Row(
                dcc.Dropdown(id='dropdown_year',
                             options=list(set(df['year'].tolist())),
                             value=max(list(set(df['year'].tolist()))),
                             clearable=False,
                             style = {'width' : '200%'}), 
                align = "right")
        ]),
        color="dark",
        dark=True
    ),
    html.Br(),
    dbc.Container(
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dcc.Dropdown(id='dropdown_player',
                                 options=[],
                                 value=[],
                                 clearable=False),
                    dbc.Row([
                        dbc.Col(
                            dbc.CardImg(id='pic'),
                            width = 5), 
                        dbc.Col(
                            dbc.CardBody([
                                dbc.ListGroupItem(id='voting_result'),                             
                                dbc.ListGroupItem(id='model_prediction')
                            ]),
                            width = 7
                        )
                    ])
                ]),
                width = 3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(id='team_result'),
                    dcc.Graph(id='pie_chart')
                ]),
                width = 3
            ),
            dbc.Col(
                dbc.Card([
                    dcc.Dropdown(id='dropdown_player2',
                                 options=[],
                                 value=[],
                                 clearable=False),
                    dbc.Row([
                        dbc.Col(
                            dbc.CardImg(id='pic2'),
                            width = 5), 
                        dbc.Col(
                            dbc.CardBody([
                                dbc.ListGroupItem(id='voting_result2'),                             
                                dbc.ListGroupItem(id='model_prediction2')
                            ]),
                            width = 7
                        )
                    ])
                ]),
                width = 3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(id='team_result2'),
                    dcc.Graph(id='pie_chart2')
                ]),
                width = 3
            )
        ])
    ),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Table(id='per_game_stats')),
            dbc.Col(dbc.Table(id='per_game_stats2'))
            ]),
        dbc.Row([
            dbc.Col(dbc.Table(id='advanced_stats')),
            dbc.Col(dbc.Table(id='advanced_stats2'))
        ])
    ]),
    dbc.Container(
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader('MVP RESULTS'), 
                    dcc.Graph(id='bar_result')
                ])
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader('MODEL PREDICTION'), 
                    dcc.Graph(id='bar_prediction')
                    ])
            )
    ]))              
])




# ----------CALLBACKS-----------------------------------------------------------------------------------------------------------------



# ----------DROPDOWN PLAYER ---------------------------------------------------------------------------------------------------------


@app.callback(
    [Output('dropdown_player', 'options'),
     Output('dropdown_player', 'value')],
    Input('dropdown_year', 'value'))

def get_player1(dropdown_year):
    yeardf = df[df["year"] == dropdown_year]
    options = yeardf['Player'].tolist()
    value = yeardf.loc[yeardf['Share'] == yeardf['Share'].max(), 'Player'].iloc[0]
    return options, value

@app.callback(
    [Output('dropdown_player2', 'options'),
     Output('dropdown_player2', 'value')],
    Input('dropdown_year', 'value'))

def get_player2(dropdown_year):
    yeardf = df[df["year"] == dropdown_year]
    options = yeardf['Player'].tolist()
    value = yeardf.loc[yeardf['predictions'] == yeardf['predictions'].max(), 'Player'].iloc[0]
    return options, value


# ----------PICTURES ---------------------------------------------------------------------------------------------------------


@app.callback(
    Output('pic', 'src'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def get_pic(dropdown_year, dropdown_player):
    url = df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'url'].iloc[0]
    r = requests.get(f'https://www.basketball-reference.com/players/{url}.html')
    soup = BeautifulSoup(r.text, 'html.parser')
    short_url = url[2:]
    pic = soup.find('img', src=f'https://www.basketball-reference.com/req/202106291/images/players/{short_url}.jpg')['src']
    return pic

@app.callback(
    Output('pic2', 'src'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def get_pic2(dropdown_year, dropdown_pred_player):
    url = df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_pred_player), 'url'].iloc[0]
    r = requests.get(f'https://www.basketball-reference.com/players/{url}.html')
    soup = BeautifulSoup(r.text, 'html.parser')
    short_url = url[2:]
    pic = soup.find('img', src=f'https://www.basketball-reference.com/req/202106291/images/players/{short_url}.jpg')['src']
    return pic


# ----------VOTING RESULT & PREDICTIONS---------------------------------------------------------------------------------------------------------


@app.callback(
    Output('voting_result', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def voting_result(dropdown_year, dropdown_player):
    actual_rank =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'actual_rank'].iloc[0]
    Share = df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'Share'].iloc[0]
    return f"MVP Rank: {actual_rank} ({Share})"

@app.callback(
    Output('voting_result2', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def voting_result2(dropdown_year, dropdown_player):
    actual_rank =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'actual_rank'].iloc[0]
    Share =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'Share'].iloc[0]
    return f"MVP Rank : {actual_rank} ({Share})"

@app.callback(
    Output('model_prediction', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def model_prediction(dropdown_year, dropdown_player):
    predicted_rank =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'predicted_rank'].iloc[0]
    predictions =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'predictions'].iloc[0]
    return f"Prediction: {predicted_rank} ({predictions})"

@app.callback(
    Output('model_prediction2', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def model_prediction2(dropdown_year, dropdown_player):
    predicted_rank =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'predicted_rank'].iloc[0]
    predictions =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'predictions'].iloc[0]
    return f"Prediction: {predicted_rank} ({predictions})"


# ----------TEAMS RESULT-----------------------------------------------------------------------------------------------------------------


@app.callback(
    Output('team_result', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def team_result(dropdown_year, dropdown_player):
    team_name =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'Team'].iloc[0]
    return f"{team_name}"

@app.callback(
    Output('team_result2', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def team_result2(dropdown_year, dropdown_player):
    team_name =  df.loc[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player), 'Team'].iloc[0]
    return f"{team_name}"


# ----------PIE CHARTS-----------------------------------------------------------------------------------------------------------------


@app.callback(
    Output('pie_chart', 'figure'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def pie(dropdown_year, dropdown_player):
    pie_stats = df[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player)]
    fig = px.pie(values=[pie_stats['W'].iloc[0], pie_stats['L'].iloc[0]], names=['Wins', 'Losses'], width=300, height=165)
    fig.update_traces(hole=.3, textinfo='value+label', marker=dict(colors=['rgb(88, 158, 58)', 'rgb(168, 54, 39)']))
    fig.add_annotation(text = pie_stats['W/L%'].iloc[0], showarrow=False)
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    return fig

@app.callback(
    Output('pie_chart2', 'figure'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def pie2(dropdown_year, dropdown_player):
    pie_stats = df[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player)]
    pie2 = px.pie(values=[pie_stats['W'].iloc[0], pie_stats['L'].iloc[0]], names=['Wins', 'Losses'], width=300, height=165)
    pie2.update_traces(hole=.3, textinfo='value+label', marker=dict(colors=['rgb(88, 158, 58)', 'rgb(168, 54, 39)']))
    pie2.add_annotation(text = pie_stats['W/L%'].iloc[0], showarrow=False)
    pie2.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend = False)
    return pie2


# ----------PER GAME STAS------------------------------------------------------------------------


@app.callback(
    Output('per_game_stats', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def per_game_stats(dropdown_year, dropdown_player):
    per_game_stats = df[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player)][['Age', 'Pos', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'FG%', '3P%', 'FT%']]
    return dbc.Table.from_dataframe(per_game_stats, bordered =True, size= 'sm')

@app.callback(
    Output('per_game_stats2', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def per_game_stats2(dropdown_year, dropdown_player):
    per_game_stats = df[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player)][['Age', 'Pos', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'FG%', '3P%', 'FT%']]
    return dbc.Table.from_dataframe(per_game_stats, bordered =True, size= 'sm')


# ----------ADVANCED STAS------------------------------------------------------------------------


@app.callback(
    Output('advanced_stats', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player', 'value')])

def advanced_stats(dropdown_year, dropdown_player):
    advanced_stats = df[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player)][['USG%', 'PER', 'OWS', 'DWS', 'WS', 'WS/48', 'BPM','VORP', 'TS%', 'eFG%']]
    return dbc.Table.from_dataframe(advanced_stats, bordered =True, size= 'sm')

@app.callback(
    Output('advanced_stats2', 'children'),
    [Input('dropdown_year', 'value'),
    Input('dropdown_player2', 'value')])

def advanced_stats2(dropdown_year, dropdown_player):
    advanced_stats = df[(df["year"] == dropdown_year) & (df["Player"] == dropdown_player)][['USG%', 'PER', 'OWS', 'DWS', 'WS', 'WS/48', 'BPM','VORP', 'TS%', 'eFG%']]
    return dbc.Table.from_dataframe(advanced_stats, bordered =True, size= 'sm') 



# ----------BAR CHARTS------------------------------------------------------------------------

@app.callback(
    Output('bar_result', 'figure'),
    Input('dropdown_year', 'value'))

def graph_mvp_result(dropdown_year):
    yeardf = df[(df["year"] == dropdown_year) & (df['Share'] != 0)]
    yeardf['Player'] = yeardf['Player'].apply(lambda x : x.split()[0] if x == 'Giannis Antetokounmpo' else x.split()[1])
    fig = px.bar(yeardf, x="Player", y="Share", text='Share', width=600, height=300)
    fig.update_xaxes(categoryorder="total descending")
    fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(l=10, r=10, t=10, b=10)).update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_traces(textposition='outside', textfont_size=8)
    return fig

@app.callback(
    Output('bar_prediction', 'figure'),
    Input('dropdown_year', 'value'))

def graph_pred_mvp_result(dropdown_year):
    yeardf = df[(df["year"] == dropdown_year) & (df['predictions'] > 0.04)]
    yeardf['Player'] = yeardf['Player'].apply(lambda x : x.split()[0] if x == 'Giannis Antetokounmpo' else x.split()[1])
    fig = px.bar(yeardf, x="Player", y="predictions", text='predictions', width=600, height=300)
    fig.update_xaxes(categoryorder="total descending")
    fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(l=10, r=10, t=0, b=10)).update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_traces(textposition='outside', textfont_size=8)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
