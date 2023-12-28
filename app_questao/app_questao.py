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

filtro = "Seleção dos filtros:"

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


aba1, aba2 = st.tabs(["Perguntas e Respostas", "Quantidade de Questionamentos"])

with aba1:
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

with aba2:

    stilo_abre = "<h1 style=color:#61677A;font-size:20px;>"
    stilo_fecha = "</h1>"

    spam_abre = f"<span style='color:#0766AD'>"
    spam_abre2 = f"<span style='color:#31304D'>"
    spam_fecha = "</span>"



    
    st.markdown(f"""{stilo_abre}
                📊 Análise de Comunicações: Demonstrativo de Resultado (DRE) 2023-2026.
                {stilo_fecha}""", unsafe_allow_html=True)
    
    st.markdown(f"""{stilo_abre} 
                    {spam_abre}Período de Análise:{spam_fecha} 13 de Outubro de 2023 a 26 de Dezembro de 2023.
                    {stilo_fecha}""", unsafe_allow_html=True)
    
    st.markdown(f"""{stilo_abre} 
                    {spam_abre2}E-mails Recebidos:{spam_fecha}
                    {stilo_fecha}
                    """, unsafe_allow_html=True)
    
    st.markdown(f"""{stilo_abre}
            {spam_abre}Lado Direito:{spam_fecha} Quantidade de e-mails relacionados a cada Demonstrativo de Resultado (DRE).
                {stilo_fecha}
                """, unsafe_allow_html=True)
    st.markdown(f"""{stilo_abre}
            {spam_abre}Lado Esquerdo:{spam_fecha} Quantidade de e-mails recebidos de acionistas.
                {stilo_fecha}
                """, unsafe_allow_html=True)
    st.markdown(f"""{stilo_abre}
            🔍 Objetivo: Proporcionar uma visão clara da interação dos acionistas com os Demonstrativos de Resultado ao longo do período especificado.
                {stilo_fecha}
                """, unsafe_allow_html=True)

    st.divider()

    total_questionamentos = data['CLASSE'].count()
    quantidades_totais = data['CLASSE'].value_counts()
    questionador_totais = data['QUESTIONADOR'].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Total de perguntas')
        st.markdown(f"""<h1 style=
                        "color:#2D9596;
                        font-size:30px;
                        ">Total de questões: {total_questionamentos}</h1>""", 
                        unsafe_allow_html=True)
        
        for index in quantidades_totais.index:
            print(f'{index} {quantidades_totais[index]}')
            st.markdown(f"""<h1 style=
                        "color:#265073;
                        font-size:30px;
                        ">{index}: {quantidades_totais[index]}</h1>""", 
                        unsafe_allow_html=True)
            
    with col2:
        st.subheader('Total por questionador')
        for index in questionador_totais.index:
            print(f'{index} {questionador_totais[index]}')
            st.markdown(f"""<h1 style=
                        "color:#265073;
                        font-size:30px;
                        ">{index}: {questionador_totais[index]}</h1>""", 
                        unsafe_allow_html=True)


    # https://colorhunt.co/