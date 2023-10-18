# Libraries
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
    page_title="Cozinhas",
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
# -----------------------------------------------------------------------------------------------
def top_restaurants(df):
    df_aux = df_new.loc[:,['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating', 'votes']].drop_duplicates().sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=False)
    df_aux = df_aux.reset_index(drop=True)
    df_aux = df_aux.head(qtde_rest)
    return df_aux

# -----------------------------------------------------------------------------------------------
def top_cuisines (df, top_asc):
    #função para gerar os gráficos barras de melhor e pior tipos de culinárias

    df_aux = (df.loc[:,['cuisines','aggregate_rating']]
                 .groupby('cuisines')
                 .mean()
                     .sort_values('aggregate_rating', ascending=top_asc).head(qtde_rest).reset_index())
    df_aux = round(df_aux,2)
    if top_asc==True:
        var = 'Piores'
    else:
        var = 'Melhores'
    
    fig = (px.bar(df_aux, x='cuisines', y='aggregate_rating', title=f'Top {qtde_rest} {var} Tipos de Culinárias',
                text_auto=True,
                labels={'aggregate_rating':'Média das Avaliações',
                        'cuisines' : 'Culinária'}))
    
       
    fig.update_layout(title_x=0.2)
    fig.update_layout(title_font_color='black')

    fig.update_traces(textfont_size=10, textangle=1, textposition="outside", cliponaxis=False)
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

col1, col2 = st.sidebar.columns([1, 3])

st.sidebar.markdown('## Filtros')
st.markdown(
    """
    ## Melhores Restaurantes dos Principais tipos Culinários

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

qtde_rest = st.sidebar.slider( 
        'Selecione a quantidade de Restaurantes que deseja visualizar',0,20,10)

cuisines = st.sidebar.multiselect( 
        'Escolha os Paises que Deseja visualizar os Restaurantes',
        df_new.cuisines.unique(),
        default=['Home-made', 'BBQ','Japanese','Brazilian','Arabian','American','Italian',])

# Filtro de País
linhas_selecionadas = df_new['country_name'].isin( paises )
df_new = df_new.loc[linhas_selecionadas, :]

# Filtro de quantidade
df_new = df_new.groupby('country_name').filter(lambda x: x['cuisines'].nunique() >= qtde_rest)


# Filtro de Cozinhas
linhas_selecionadas = df_new['cuisines'].isin( cuisines )
df_new = df_new.loc[linhas_selecionadas, :]



# =======================================
# Layout no Streamlit
# =======================================

st.title( ' 🍽️ Visão Tipos de Cozinhas' )
#with tab1:
with st.container():

    col1, col2, col3, col4, col5 = st.columns( 5, gap='small' )
    with col1:
        df_aux = df_new.loc[:,['restaurant_id', 'cuisines', 'currency', 'restaurant_name',  'aggregate_rating', 'city', 'country_name', 'average_cost_for_two']].drop_duplicates().sort_values(by=['aggregate_rating', 'restaurant_id', 'restaurant_name'], ascending=False)
        st.metric(label=f'{df_aux.cuisines.iloc[0]}: {df_aux.restaurant_name.iloc[0]}', 
                value=f'{df_aux.aggregate_rating.iloc[0]}/5.0',
                help=f"""
                    País: {df_aux.country_name.iloc[0]}\n
                    Cidade: {df_aux.city.iloc[0]} \n
                    Preço para duas pessoas: {df_aux.average_cost_for_two.iloc[0]}({df_aux.currency.iloc[0]})
                    """                
                    )

    with col2:
        df_aux = df_new.loc[:,['restaurant_id', 'cuisines', 'currency', 'restaurant_name',  'aggregate_rating', 'city', 'country_name', 'average_cost_for_two']].drop_duplicates().sort_values(by=['aggregate_rating', 'restaurant_id', 'restaurant_name'], ascending=False)
        st.metric(label=f'{df_aux.cuisines.iloc[1]}: {df_aux.restaurant_name.iloc[1]}', 
                value=f'{df_aux.aggregate_rating.iloc[1]}/5.0',
                help=f"""
                    País: {df_aux.country_name.iloc[1]}\n
                    Cidade: {df_aux.city.iloc[1]} \n
                    Preço para duas pessoas: {df_aux.average_cost_for_two.iloc[1]}({df_aux.currency.iloc[1]})
                    """                
                    )
            
    with col3:
        df_aux = df_new.loc[:,['restaurant_id', 'cuisines', 'currency', 'restaurant_name',  'aggregate_rating', 'city', 'country_name', 'average_cost_for_two']].drop_duplicates().sort_values(by=['aggregate_rating', 'restaurant_id', 'restaurant_name'], ascending=False)
        st.metric(label=f'{df_aux.cuisines.iloc[2]}: {df_aux.restaurant_name.iloc[2]}', 
                    value=f'{df_aux.aggregate_rating.iloc[1]}/5.0',
                    help=f"""
                    País: {df_aux.country_name.iloc[2]}\n
                    Cidade: {df_aux.city.iloc[2]} \n
                    Preço para duas pessoas: {df_aux.average_cost_for_two.iloc[2]}({df_aux.currency.iloc[2]})
                    """                
                    )

    with col4:
        df_aux = df_new.loc[:,['restaurant_id', 'cuisines', 'currency', 'restaurant_name',  'aggregate_rating', 'city', 'country_name', 'average_cost_for_two']].drop_duplicates().sort_values(by=['aggregate_rating', 'restaurant_id', 'restaurant_name'], ascending=False)
        st.metric(label=f'{df_aux.cuisines.iloc[3]}: {df_aux.restaurant_name.iloc[3]}', 
                    value=f'{df_aux.aggregate_rating.iloc[1]}/5.0',
                    help=f"""
                    País: {df_aux.country_name.iloc[3]}\n
                    Cidade: {df_aux.city.iloc[3]} \n
                    Preço para duas pessoas: {df_aux.average_cost_for_two.iloc[3]}({df_aux.currency.iloc[3]})
                    """                
                    )
            
    with col5:
        df_aux = df_new.loc[:,['restaurant_id', 'cuisines', 'currency', 'restaurant_name',  'aggregate_rating', 'city', 'country_name', 'average_cost_for_two']].drop_duplicates().sort_values(by=['aggregate_rating', 'restaurant_id', 'restaurant_name'], ascending=False)
        st.metric(label=f'{df_aux.cuisines.iloc[4]}: {df_aux.restaurant_name.iloc[4]}', 
                    value=f'{df_aux.aggregate_rating.iloc[1]}/5.0',
                    help=f"""
                    País: {df_aux.country_name.iloc[4]}\n
                    Cidade: {df_aux.city.iloc[4]} \n
                    Preço para duas pessoas: {df_aux.average_cost_for_two.iloc[4]}({df_aux.currency.iloc[4]})
                    """                
                    )
            
with st.container():
        # Top Restaurantes
        st.write(f'## Top {qtde_rest} Restaurantes \n')        
        df_aux = top_restaurants(df_new)
        st.dataframe( df_aux )

with st.container():

 col1, col2 = st.columns(2)
with col1:
        fig = top_cuisines (df, top_asc=False)
        st.plotly_chart (fig, use_container_width=True, theme='streamlit')
with col2:
        fig = top_cuisines (df, top_asc=True)
        st.plotly_chart (fig, use_container_width=True, theme='streamlit')

