# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash_html_components import Div as D, Img as I

IMG_SRC = 'https://www.todaysparent.com/wp-content/uploads/2017/06/when-your-kid-becomes-a-meme-1024x576-1497986561.jpg'

external_stylesheets = ['https://bootswatch.com/4/darkly/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = D(children=[
    html.H1(children='Memes-4-Africa'),
    D(D(D(D(children= ['Google', I(src=IMG_SRC, width='100%')],
            className='card-header'),
          className='bs-component'),
        className='col-lg-6'),
      className='row')

])

if __name__ == '__main__':
    app.run_server(debug=True)
