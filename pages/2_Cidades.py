
# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import inflection
import folium
import pandas as pd
import streamlit as st
from PIL import Image
import datetime
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config( page_title='Cidades', page_icon='📈', layout='wide' )


# =======================================
# Funções
# =======================================

def clean_code( df ): 
    """ Esta funcao tem a responsabilidade de limpar o dataframe 
    
        Tipos de limpeza:
        1. Preenchimento do nome dos países
        2. Criação do Tipo de Categoria de Comida
        3. Criação do nome das Cores
        4. Renomear as colunas do DataFrame
        5. Categorizar por tipo de culinária
        6. Selecionar somente algumas colunas
        7. Excluir linhas com dados ausentes
        8. Excluir linhas duplicados
        9. Excluir linhas cujo valor do prato para duas pessoas está com o valor zerado
        
        Input: Dataframe
        Output: Dataframe
    """
    # 1. Preenchimento do nome dos países
 
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }

    def country_name(country_id):
        return COUNTRIES[country_id]
    
    df['country_name'] = df.loc[:, 'Country Code'].apply(lambda x: country_name (x))

    # 2. Criação do Tipo de Categoria de Comida

    def create_price_tye(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"
    
    df['price_range_name'] = df.loc[:, 'Price range'].apply(lambda x: create_price_tye (x))

    # 3. Criação do nome das Cores
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    def color_name(color_code):
        return COLORS[color_code]

    df['color_name'] = df.loc[:, 'Rating color'].apply(lambda x: color_name (x))

    # 4. Renomear as colunas do DataFrame

    def rename_columns(dataframe):
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(df.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df.columns = cols_new
        return df
    df= rename_columns(df)

    # 5. Categorizar por tipo de culinária
    df["cuisines"]=df["cuisines"].fillna("")
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

     # 6. Selecionar somente algumas colunas
    df_new = df.loc[:, ['restaurant_id', 'restaurant_name', 'city', 'address',
       'locality', 'locality_verbose', 'longitude', 'latitude', 'cuisines',
       'average_cost_for_two', 'currency', 'has_table_booking',
       'has_online_delivery', 'is_delivering_now', 'aggregate_rating', 'rating_text',
       'votes', 'country_name', 'price_range_name', 'color_name']]

    # 7. Excluir linhas com dados ausentes
    df_new = df_new.dropna(axis=0)

    # 8. Excluir linhas duplicados
    df_new = df_new.drop_duplicates()

    # 9. Excluir linhas cujo valor do prato para duas pessoas está com o valor zerado
    df_new = df_new.loc[df_new.average_cost_for_two!=0,:]

    return df_new

# -----------------------------------------------------------------------------------------------
def restaurant_of_city( df ):
    # selecao de linhas
    df_aux= df.loc[:,  ['city','country_name','restaurant_name']].drop_duplicates().groupby(by= ['city','country_name']).count().reset_index().sort_values(by='restaurant_name', ascending=False)
    df_aux = df_aux.rename(columns={'city': "Cidades", 'restaurant_name':'Quantidade de Restaurantes', 'country_name': 'País'})
    df_aux = df_aux.iloc[0:10,:]
    # desenhar o gráfico de linhas
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de Restaurantes', color = 'País', text_auto=True, title='Top 10 Cidades com mais Restaurantes na Base de Dados')
    fig.update_layout(title_x=0.2)
    return fig

# -----------------------------------------------------------------------------------------------
def restaurant_of_city_media_maior( df ):
    # selecao de linhas
    df_aux= df_new.loc[df_new.aggregate_rating>4, ['country_name','city', 'restaurant_name']].drop_duplicates().groupby(by=['city','country_name']).count().reset_index().sort_values(by='restaurant_name', ascending=False)
    df_aux=df_aux.iloc[0:7,:]
    df_aux = df_aux.rename(columns={'city': "Cidades", 'restaurant_name':'Quantidade de Restaurantes', 'country_name': 'País'})
    # desenhar o gráfico de linhas
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de Restaurantes', color = 'País', text_auto=True, title='Cidades com média maior que 4')
    fig.update_layout(title_x=0.2)
    fig.update_xaxes(tickangle=45)
    return fig

# -----------------------------------------------------------------------------------------------
def restaurant_of_city_media_menor( df ):
    # selecao de linhas
    df_aux= df_new.loc[df_new.aggregate_rating<2, ['country_name','city', 'restaurant_name']].drop_duplicates().groupby(by=['city','country_name']).count().reset_index().sort_values(by='restaurant_name', ascending=False)
    df_aux=df_aux.iloc[0:7,:]
    df_aux = df_aux.rename(columns={'city': "Cidades", 'restaurant_name':'Quantidade de Restaurantes', 'country_name': 'País'})
    # desenhar o gráfico de linhas
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de Restaurantes', color = 'País', text_auto=True, title='Cidades com média menor que 2')
    fig.update_layout(title_x=0.3)
    return fig

# -----------------------------------------------------------------------------------------------
def city_cuisines( df ):
    # selecao de linhas
    df_aux= df_new.loc[:, ['country_name','city', 'cuisines']].drop_duplicates().groupby(by=['city', 'country_name']).count().reset_index().sort_values(by='cuisines', ascending=False)
    df_aux=df_aux.iloc[0:10,:]
    df_aux = df_aux.rename(columns={'city': "Cidades", 'cuisines':'Quantidade de Tipo Culinários Únicos', 'country_name': 'País'})
    # desenhar o gráfico de linhas
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de Tipo Culinários Únicos', color = 'País', text_auto=True, title='Top 10 Cidades com mais Restaurantes com Tipos de Culinária Únicos')
    fig.update_layout(title_x=0.1)
    fig.update_xaxes(tickangle=0)
    return fig



# --------------------------- Inicio da Estrutura lógica do código --------------------------
# ------------------------
# Import dataset
# ------------------------
df = pd.read_csv( 'zomato.csv' )

# ------------------------
# Limpando os dados
# ------------------------
df_new = clean_code( df )

# =======================================
# Barra Lateral
# =======================================

st.sidebar.markdown('## Filtros')

paises = st.sidebar.multiselect( 
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
default=['Brazil', 'England', 'Qatar', 'South Africa',
       'Canada', 'Australia'])
# Filtro de País
linhas_selecionadas = df_new['country_name'].isin( paises )
df_new = df_new.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================

st.markdown( '# 🌃 Visão Cidades' )

with st.container():
    fig = restaurant_of_city( df_new)
    st.plotly_chart(fig,use_container_width=True)

with st.container():
    col1, col2= st.columns( 2, gap='large' )
    with col1:
        fig = restaurant_of_city_media_maior( df_new)
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = restaurant_of_city_media_menor( df_new)
        st.plotly_chart(fig,use_container_width=True)

with st.container():
    fig = city_cuisines( df_new)
    st.plotly_chart(fig,use_container_width=True)