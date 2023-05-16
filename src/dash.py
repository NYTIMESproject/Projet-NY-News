import pandas as pd
import plotly.express as px
from dash import *
#import dash_core_components as dcc
#import dash_html_components as html
from jupyter_dash import JupyterDash

df = pd.read_csv('data_brutes/data_articles/2023-01_nyt.csv')
# créer l'instance de JupyterDash
app = JupyterDash(__name__)

# Créer une mise en page
app.layout = html.Div([
    html.H1('Recherche d\'articles du New York Times'),
    dcc.Input(id='mot-recherche', type='text', placeholder='Entrez le mot à rechercher'),
    html.Div(id='total-occurrences'),
    html.Div([
        html.Div([
            dcc.Graph(id='graphique-categories')
        ], className='six columns', style={'display': 'inline-block', 'width': '45%'}),
        html.Div([
            dcc.Graph(id='graphique-abstract')
        ], className='six columns', style={'display': 'inline-block', 'width': '45%', 'float': 'right'})
    ]),
    dcc.Graph(id='graphique')
])


# Définir une fonction de rappel pour mettre à jour les graphiques et le total des occurrences
@app.callback(
    [dash.dependencies.Output('graphique', 'figure'),
     dash.dependencies.Output('graphique-categories', 'figure'),
     dash.dependencies.Output('graphique-abstract', 'figure'),
     dash.dependencies.Output('total-occurrences', 'children')],
    [dash.dependencies.Input('mot-recherche', 'value')])
def update_graph(mot_recherche):
    # Filtrer les articles qui contiennent le mot recherché (ignorer la casse des lettres)
    df_filtre = df[df['keywords'].str.contains(mot_recherche, case=False)]

    # Convertir la colonne pub_date en datetime et extraire la date
    df_filtre['date'] = pd.to_datetime(df_filtre['pub_date']).dt.date

    # Regrouper les articles par date et compter le nombre d'articles pour chaque date
    df_group = df_filtre.groupby('date').size().reset_index(name='count')

    # Calculer le total des occurrences dans le mois
    total_occurrences = df_group['count'].sum()

    # Créer un graphique avec plotly pour les  par jour
    fig = px.line(df_group, x='date', y='count',
                  title='Nombre d\'articles par jour contenant le mot "{}"'.format(mot_recherche))

    # Filtrer les articles par catégorie avec le plus grand nombre d' du mot recherché
    categorie_populaire = df_filtre['categories'].value_counts().idxmax()
    df_categorie = df_filtre[df_filtre['categories'] == categorie_populaire]

    # Créer un graphique avec plotly pour les occurrences par catégorie (en vert)
    fig_categories = px.histogram(df_categorie, x='date',
                                  title='Nombre du mot "{}" dans la catégorie avec le plus d\'occurence"{}"'.format(
                                      mot_recherche, categorie_populaire)
                                  , color_discrete_sequence=['green'])

    # Filtrer les articles par jour et sommer les occurrences dans l'abstract
    df_abstract = df_filtre.groupby('date')['abstract'].count().reset_index()

    # Créer un graphique avec plotly pour la somme des mots dans l'abstract par jour sur le mois (en rouge)
    fig_abstract = px.line(df_abstract, x='date', y='abstract',
                           title='Somme des mots "{}" dans l\'abstract par jour sur le mois'.format(mot_recherche)
                           , color_discrete_sequence=['red'])

    return fig, fig_categories, fig_abstract, "Total des occurrences : {}".format(total_occurrences)


# lancé Dash avec JupyterDash
app.run_server(mode='inline')