
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


st.set_page_config(
    page_title="Home",
    page_icon="📈"
)

# -------------------------------------
# Funções
# -------------------------------------

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

col1, col2 = st.sidebar.columns([1, 3])

image_path=('logo.png')
image = Image.open( image_path )
col1.image( image, width=35) 
col2.write ('# Fome Zero')

st.sidebar.markdown('## Filtros')
st.write('# Fome Zero!')

st.markdown(
    """
    ## O Melhor lugar para encontrar seu mais novo restaurante favorito!
"""
)

paises = st.sidebar.multiselect( 
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
default=['Brazil', 'England', 'Qatar', 'South Africa',
       'Canada', 'Australia'])

st.sidebar.markdown( '## Dados tratados' )
df.to_csv("your_name.csv")

#-------------------------------------------

def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df_new)

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)

# Filtro de País
linhas_selecionadas = df_new['country_name'].isin( paises )
df_new = df_new.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================

#with tab1:
with st.container():
    st.markdown ('### Temos as seguintes marcas dentro da nossa plataforma:')

    col1, col2, col3, col4, col5 = st.columns( 5, gap='small' )
    with col1:
        # Restaurantes cadastrados
        restaurantes_cadastrados = df_new.loc[:, 'restaurant_name'].nunique()
        col1.metric( 'Restaurantes Cadastrados', restaurantes_cadastrados )


    with col2:
        # Países Cadastrados
        df_pais = df_new.loc[:, 'country_name'].nunique()
        col2.metric( 'Países Cadastrados', df_pais )

    with col3:
        # Cidades Cadastradas
        city = df_new.loc[:, 'city'].nunique()
        col3.metric( 'Cidades Cadastradas', city )

    with col4:
        # Avaliações Feitas na Plataforma
        df_aux= df_new.loc[:,['restaurant_name','votes']].drop_duplicates()
        df_aval = df_aux.votes.sum()
        col4.metric( 'Avaliações Feitas na Plataforma', df_aval )

    with col5:
        # Tipos de Culinárias Oferecidas
        cuisines = df_new.loc[:, 'cuisines'].nunique()
        col5.metric( 'Tipos de Culinárias Oferecidas', cuisines )

st.container()
st.write ('### Mapa com a Localização dos restaurantes:')

df_aux = (df_new.loc[:, ['city', 'aggregate_rating', 'currency', 'cuisines', 'color_name', 'restaurant_id','latitude', 'longitude', 'average_cost_for_two', 'restaurant_name']]
             .groupby(['city', 'cuisines','color_name', 'currency', 'restaurant_id', 'restaurant_name'])
             .median().reset_index())


map1 = folium.Map()
marker_cluster = folium.plugins.MarkerCluster().add_to(map1)

                    
for i in range ( len (df_aux) ):
    popup_html = f'<div style="width: 250px;">' \
                 f"<b>{df_aux.loc[i, 'restaurant_name']}</b><br><br>" \
                 \
                 f"Preço para dois: {df_aux.loc[i, 'average_cost_for_two']:.2f} ( {df_aux.loc[i, 'currency']})<br> " \
                 f"Type: {df_aux.loc[i, 'cuisines']}<br>" \
                 f"Nota: {df_aux.loc[i, 'aggregate_rating']}/5.0" \
                 f'</div>'
    folium.Marker ([df_aux.loc[i, 'latitude'], df_aux.loc[i, 'longitude']],
                   popup=popup_html, width=500, height=500, tooltip='clique aqui', parse_html=True,  
                   zoom_start=30, tiles= 'Stamen Toner', 
                   icon=folium.Icon(color=df_aux.loc[i, 'color_name'] , icon='home')).add_to(marker_cluster)
    
folium_static(map1)
