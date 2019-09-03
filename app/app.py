# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pickle as pck
import praw
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

username = config['User']['username']
password = config['User']['password']
app_client_id = config['Keys']['client_id']
app_client_secret = config['Keys']['client_secret']

reddit = praw.Reddit(client_id=app_client_id,
                     client_secret=app_client_secret,
                     user_agent=username,
                     username=username,
                     password=password)

navbar = dbc.NavbarSimple(
    brand="Meme Feeder",
    brand_href="#",
    sticky="top",
)

input = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.InputGroup(
                        [
                            dbc.InputGroupAddon("r/", addon_type="prepend"),
                            dbc.Input(id='userInput', value="dankmemes"),
                        ]
                    ),
                    dbc.Button('Submit', id="btnSubmit",
                               color="dark", className="mr-1")
                ]
            ),

            dbc.RadioItems(
                id='radioInput',
                options=[
                    {'label': 'Hot', 'value': 'hot'},
                    {'label': 'New', 'value': 'new'}],
                value='hot',
                labelStyle={'display': 'inline-block'}
            ),

            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': '10', 'value': '10'},
                    {'label': '100', 'value': '100'},
                    {'label': '1000', 'value': '1000'}
                ],
                value='amount'
            )


        ]
    )

]
)

body = dbc.Container(
    [
        dbc.Row(
            [
                html.Div(id='output')
            ]
        )
    ],
    className="mt-4",
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([navbar, input, body])
app.config.suppress_callback_exceptions = True


@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('btnSubmit', 'n_clicks'),
     dash.dependencies.Input('userInput', 'n_submit')],
    [dash.dependencies.State('userInput', 'value'),
     dash.dependencies.State('radioInput', 'value'),
     dash.dependencies.State('dropdown', 'value')])
def update_output(n_clicks_submit, n_enters, text, choice, amount):
    print(n_clicks_submit, n_enters, text, choice, amount)
    if (n_clicks_submit is not None) or (n_enters is not None):
        subreddit = reddit.subreddit(text)
        if choice == 'new':
            posts = subreddit.new(limit=int(amount))
        else:
            posts = subreddit.hot(limit=int(amount))
        cards = []
        for post in posts:
            url = post.url
            cards.append(dbc.Card(
                [dbc.CardBody(
                    [
                        html.H4("Card title",
                                className="card-title"),
                        html.P(
                            url
                        )
                    ]
                ),
                    dbc.CardImg(src=url, top=True)

                ]
            ))
        return cards
    else:
        return ''


if __name__ == "__main__":
    app.run_server(debug=True)
