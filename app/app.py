# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pickle as pck
import praw

username, password, app_client_id, app_client_secret = 'Grade1503', 'Raffels1503', 'jljZhDDYjJNGEA', 'jmX3k3a38suV2HBDCwBsBRBNmv0'
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
                [dcc.Input(id='userInput',
                           placeholder='r/',
                           type='text',
                           value=''
                           ), dbc.Button('Submit', id="btnSubmit", color="dark", className="mr-1")
                 ]
            ),

            dcc.RadioItems(
                options=[
                    {'label': 'Hot', 'value': 'Hot'},
                    {'label': 'New', 'value': 'New'}

                ],
                value='',
                labelStyle={'display': 'inline-block'}
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
    [dash.dependencies.Input('btnSubmit', 'n_clicks')],
    [dash.dependencies.State('userInput', 'value')])
def update_output(n_clicks, value):
    if value is '':
        return "Please insert"
    else:
        subreddit = reddit.subreddit(value)
        posts = subreddit.new(limit=10)
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


if __name__ == "__main__":
    app.run_server(debug=True, port=9989)
