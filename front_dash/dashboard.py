import json

import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import *
import dash_table
import requests

url_api = "http://127.0.0.1:8000/"

def get_all_data():
    response = requests.get(url_api + f"get_time_bdd/")
    reponse_get_time_bdd = json.loads(response.content.decode())

    response = requests.get(url_api + f"get_last_news/")
    reponse_get_last_news = json.loads(response.content.decode())

    response = requests.get(url_api + f"get_top_ten_categorie/")
    reponse_get_top10 = json.loads(response.content.decode())

    return reponse_get_top10, reponse_get_last_news, reponse_get_time_bdd


reponse_get_top10, reponse_get_last_news, reponse_get_time_bdd = get_all_data()

min_datetime = datetime.strptime(reponse_get_time_bdd["min_time"], "%Y-%m-%dT%H:%M:%S")

max_datetime = datetime.strptime(reponse_get_time_bdd["max_time"], "%Y-%m-%dT%H:%M:%S")
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
app.config.suppress_callback_exceptions = True
colors = {
    'background': '#0D75FA',
    'text': '#FFFFFF'
}
style = {
    'TextAlign': "center",
    "colors": "#FFFFF"
}

logo = html.Img(src="https://i0.wp.com/datascientest.com/wp-content/uploads/2020/08/new-logo.png", height="70px",
                className="position-absolute top-0 end-60")
# titre
header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(href="#")),
    ],
    brand=html.Div([
        html.Span(" New-York Time Dashboard", className="font-roboto",
                  style={'font-size': '36px', 'text-align': 'center', "font-weight": "bold"})
    ]),
    brand_href="#",
    color="#472ADE",
    dark=True,
    links_left=True,
    class_name='mb-3'
)
footer = html.Footer(
    dbc.Container(
        dbc.Row(
            dbc.Col(
                html.P(
                    "Projet réalisé par Alexis Peron, Edouard Loiseau et Louis Petat Lenoir dans le cadre de la formation @Datascientest."),
                style={'text-align': 'center'}
            )
        ),
        fluid=True
    ),
    className="footer py-3 mt-5 bg-light"
)

footer2 = html.Footer(html.P("LOL"))

# bouton: mot de recherche, sélection catégorie, date
selector2 = dbc.Row([
    dbc.Card(
        dbc.Row(children=[
            dbc.Col(dbc.Input
                    (id='mot_recherche', placeholder="Entrez le mot à rechercher", type="text"), width=12,
                    className="mb-2 rounded"),
            dbc.Col(dcc.DatePickerRange
                    (id='my_date_picker_range_1', min_date_allowed=min_datetime - timedelta(days=150),
                     max_date_allowed=max_datetime, initial_visible_month=min_datetime, className="rounded"))

        ], className="flex-column"), className="rounded shadow-sm p-4"),
], className="p-3")

selector3 = dbc.Row([
    dbc.Card(
        dbc.Row(children=[
            dbc.Col(dcc.Dropdown
                    (id='dropdown_categories',
                     options=[{'label': category, 'value': category} for category in reponse_get_top10["Keyword"]],
                     style={'width': '100%'}, className='mb-2', placeholder="Sélectionnez une catégorie")),
            dbc.Col(dcc.DatePickerRange
                    (id='my_date_picker_range_2', min_date_allowed=min_datetime - timedelta(days=75),
                     max_date_allowed=max_datetime + timedelta(days=75),
                     initial_visible_month=min_datetime, className="rounded"))

        ], className="flex-column"), className="rounded shadow-sm p-4"),
], className="p-3")


selector1 = dbc.Row([
    dbc.Card(
        dbc.Row(children=[
            dbc.Col(dcc.DatePickerRange
                    (id='my_date_picker_range_3', min_date_allowed=min_datetime - timedelta(days=75),
                     max_date_allowed=max_datetime + timedelta(days=75),
                     initial_visible_month=min_datetime, className="rounded"))
        ], className="flex-column"), className="rounded shadow-sm p-4"),
], className="p-3")

# tableau 1 titres et liens
tab_Titres = dbc.Col(
    dbc.Table(
        [
            html.Thead(
                html.Tr([html.Th("Derniers Articles enregistrés")]),
                style={"background-color": "#f8f9fa"}
            ),
            html.Tbody([
                html.Tr([
                    html.Td(html.A(t, href=lien, target="_blank", )),
                ])
                for t, lien in zip(reponse_get_last_news["Title"], reponse_get_last_news["Url"])
            ]),
        ],
        bordered=True,
        responsive=True,
        hover=True,
        striped=True,class_name="rounded "
    ),class_name='m-3'
)
# graph 1 categories
graph_2 = dcc.Tab(id='graph',
                  label="Graphique 2", value="tab_2",
                  children=[
                      dbc.Card(
                          dbc.CardBody(dcc.Graph(id='graphique-2')), className="shadow bg-white rounded")
                  ]
                  )
# graph 2 abstract
graph_3 = dcc.Tab(
    label="Graphique 3", value="tab_3",
    children=[
        dbc.Card(
            dbc.CardBody(dcc.Graph(id='graphique-3')), className="shadow bg-white rounded")
    ]
)

#graph 3 total articles par jours

graph_1 = dcc.Tab(
    label="Graphique 1", value="tab_1",
    children=[
        dbc.Card(
            dbc.CardBody(dcc.Graph(id='graphique-1')), className="shadow bg-white rounded")
    ]
)

# tableau 2 Titres
tableau_2 = dbc.Col(
    html.Table([
        html.Thead(html.Tr([html.Th("Titres")]), style={'background-color': '#f8f9fa'}),
        html.Tbody([html.Tr([html.Td(element)]) for element in reponse_get_last_news["Title"]])
    ], className="table")
    , width=4)

# tableau 1 liens
tableau_liens_2 = dbc.Col(
    html.Table([
        html.Thead(html.Tr([html.Th("Liens")]), style={'background-color': '#f8f9fa'}),
        html.Tbody([html.Tr([html.Td(html.A(href=lien, children=lien))]) for lien in reponse_get_last_news["Url"]])
    ], className="table")
    , width=4)

tabs = dcc.Tabs(id="tabs_select", value="tab_1", children=
[graph_1,graph_2, graph_3, ],
                className="mb-3"
                )

# créer une mise en page
app.layout = html.Div(children=[
    header,
    logo,
    # selector,
    dbc.Row([
        dbc.Col(width=2, className="p-3", id="selector"),
        dbc.Col(tabs, className="p-3"),
        dbc.Col(tab_Titres,width=3, className="mr-6"),
    ]),
    footer

])

def get_total_count_article(min_date,max_date):
    response = requests.get(url_api + f"get_total_count_article/?min_date={min_date}&max_date={max_date}")
    reponse_parse = json.loads(response.content.decode())
    df = pd.DataFrame(reponse_parse)
    return df
def get_count_filter_article(filter, min_date, max_date):
    response = requests.get(url_api + f"get_count_filter_article/?param={filter}&min_date={min_date}&max_date={max_date}")
    reponse_parse = json.loads(response.content.decode())
    df = pd.DataFrame(reponse_parse)
    return df


def get_categories_count_by_day(filter, start_date, end_date):
    response = requests.get(url_api + f"get_categories_count_by_day/?param={filter}&min_date={start_date}&max_date={end_date}")
    response_get_cat_by_day = json.loads(response.content.decode())
    df = pd.DataFrame(response_get_cat_by_day)
    return df


def display_category(selected_category):
    if selected_category:
        return html.H3(f"Vous avez sélectionné la catégorie : {selected_category}")
    else:
        return html.H3("Sélectionnez une catégorie")


@app.callback(dash.dependencies.Output('selector', 'children'),
              dash.dependencies.Input('tabs_select', 'value'), prevent_initial_call=False)
def update_selector(value):
    if value == "tab_1":
        selector = selector1
    elif value == "tab_2" :
        selector = selector2
    else :
        selector = selector3
    return selector


# definir une fonction de rappel pour mettre à jour le graphique en fonction du mot de recherche
@app.callback(
    dash.dependencies.Output('graphique-2', 'figure'),
    [dash.dependencies.Input('mot_recherche', 'value'),
     dash.dependencies.Input('my_date_picker_range_1', 'start_date'),
     dash.dependencies.Input('my_date_picker_range_1', 'end_date')], prevent_initial_call=False)
# update du choix de catagory
def update_graph2(mot_recherche, start_date, end_date):
    if mot_recherche == None:
        mot_recherche = "France"
    data_article = get_count_filter_article(mot_recherche, start_date, end_date)
    # graphique avec plotly
    fig_keywords = px.line(data_article, x='Date', y='Count',
                           title='Nombre d\'articles publiés contenant le mot "{}"'.format(mot_recherche))
    get_all_data()
    total_occurrences = 0

    return fig_keywords


@app.callback(
    dash.dependencies.Output('graphique-3', 'figure'),
    [dash.dependencies.Input('dropdown_categories', 'value'),
     dash.dependencies.Input('my_date_picker_range_2', 'start_date'),
     dash.dependencies.Input('my_date_picker_range_2', 'end_date')], prevent_initial_call=False)
def update_graph3(dropdown_categories, start_date, end_date):
    data_categories = get_categories_count_by_day(dropdown_categories, start_date, end_date)
    display_category(dropdown_categories)
    fig_categories = px.line(data_categories, x='Date', y='Count',
                             title='Nombre d\'articles publiés dans la categories "{}"'.format(dropdown_categories),
                             color_discrete_sequence=['green'])
    get_all_data()
    return fig_categories


@app.callback(
    dash.dependencies.Output('graphique-1', "figure"),
    [dash.dependencies.Input('my_date_picker_range_3','start_date'),
     dash.dependencies.Input('my_date_picker_range_3','end_date')], prevent_initial_call = False)
def update_graph1(start_date,end_date):
    if start_date == None and end_date == None:
        start_date = min_datetime.date()
        end_date = max_datetime.date()
    data = get_total_count_article(start_date,end_date)
    fig_total_article = px.line(data, x='Date', y='Count',
                             title="Evolution du nombre d'article publiés dans le NY-Times",
                             color_discrete_sequence=['green'])
    get_all_data()
    return fig_total_article

def create_dashboard():
    app.run_server()


# lancé Dash 
create_dashboard()
