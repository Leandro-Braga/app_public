import warnings

import pandas as pd
import streamlit as st
from PIL import Image

warnings.filterwarnings('ignore')


image_logo = Image.open('./img/logo_nesa_branco.png')
image_logo_simpes = Image.open('./img/logo_simples.png')


# ----- Configuração da página --------- #

st.set_page_config(
    page_title="Questões Acionistas",
    page_icon=image_logo_simpes,
    layout='wide', # opções (wide, centered)
    initial_sidebar_state='auto', # opções de tela inicial (auto, expanded, collapsed)
    menu_items={
        'Get Help': 'https://www.norteenergiasa.com.br/pt-br/',
        'About': 'Esta aplicação foi desenvolvida pela equipe de Orçamento',
        'Report a bug': "https://www.norteenergiasa.com.br/pt-br/contato"
    }
)

#---------------------------------------#

st.sidebar.image(image_logo) ## Imagem Norte no sidebar

bar = st.sidebar

## ---- Titulos e nome do usuário ---- ##

filtro = "Selecionar os filtros:"

bar.markdown(f"""<h1 style=
                "color:#FAF8F1;
                font-size:20px;
                ">{filtro}</h1>""", 
                unsafe_allow_html=True)


## --- Versão 5 -----

# Função para carregar os dados
def load_data(filepath):
    return pd.read_excel(filepath)

df_qestao_acionista = load_data('./res/Questao_Acionista.xlsx')

# Carregar os dados
data = df_qestao_acionista

# Estrutura de seções
classes = [
    "Receita Operacional",
    "Custo Operacional",
    "Lucro Operacional",
    "Resultado Financeiro",
    "Investimentos",
    "Provisão Socioambiental",
    "Estoques",
    "CAPEX",
    "Intangíveis",
    "Outros",
    "Fluxo de Caixa"
]

# Inicializar a aplicação Streamlit
st.title(':grey[Perguntas e Respostas]')
st.subheader(":grey[Demonstrativo de Resultado – DRE 24-26]")

# Filtros na barra lateral para selecionar classes e questionadores
selected_classes = st.sidebar.multiselect('**Escolha os Demonstrativos de Resultado:**', 
                                          classes, 
                                          default=classes)

unique_questionadores = data['QUESTIONADOR'].unique()
selected_questionadores = st.sidebar.multiselect('**Escolha os Questionadores:**', 
                                                 unique_questionadores, 
                                                 default=unique_questionadores)



# https://colorhunt.co/
# bar.markdown(f"""<h1 style=
#                 "color:#FAF8F1;
#                 font-size:30px;
#                 ">{menu_bar}</h1>""", 
#                 unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid=stSidebar] {background-color: #0099A8;}
    </style> """, unsafe_allow_html=True)

# -------------------------------------------------------------------------- #


# Função para filtrar os dados
def filter_data_by_class_questionador(dataframe,
                                       classe, 
                                       selected_questionadores):
    
    return dataframe[
        (dataframe['CLASSE'] == classe) 
        &
        dataframe['QUESTIONADOR'].isin(selected_questionadores)
    ]

# Iterar sobre as classes selecionadas e exibir as perguntas e respostas
for classe in selected_classes:

    st.subheader(f':grey[{classe}]')
    
    # Filtrar os dados para a classe e questionadores selecionados
    class_filtered_data = filter_data_by_class_questionador(data, 
                                                            classe, 
                                                            selected_questionadores)
    
    if not class_filtered_data.empty:

        for idx, row in class_filtered_data.iterrows():
            st.write(f":blue[**Pergunta:**] {row['PERGUNTA']}")
            st.write(f":green[**Resposta:**] {row['RESPOSTA']}")
            st.caption(f"**Questionador:** :orange[**{row['QUESTIONADOR']}**]")
    else:
        st.write("Nenhuma informação disponível para esses filtros selecionados.")
