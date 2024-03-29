import base64

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

# import warnings


# warnings.filterwarnings('ignore')


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

# Configuração do tamanho dos textos principais
def texto_diversos():
        st.markdown(
        """
        <style>

        .st-emotion-cache-q4lvki p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 18px;
        }
        .css-176rrwg {
            min-height: 1.5rem;
        }

        .css-q4lvki p {
            font-size: 18px;
        }

        .css-atw1qn p {
            font-size: 18px;
        }

        .st-af {
            font-size: 1.1rem;
        }

        </style>
        """,
        unsafe_allow_html=True)



## --- Versão 5 -----

# Função para carregar os dados
@st.cache_data
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
selected_classes = st.sidebar.multiselect('**Demonstrativos de Resultado:**', 
                                          classes, 
                                          default=classes)

unique_questionadores = data['QUESTIONADOR'].unique()
selected_questionadores = st.sidebar.multiselect('**Escolha os Questionadores:**', 
                                                 unique_questionadores, 
                                                 default=unique_questionadores)


# https://colorhunt.co/
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


aba1, aba2, aba3 = st.tabs(["Perguntas e Respostas", "Quantidade de Questionamentos", "Atas Reuniões Comitês"])

with aba1:

    # Aplica as modificações dos textos
    texto_diversos()
    
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
                st.caption(f"**Nome:** :orange[**{row['NOME'].strip()}**]")
        else:
            st.write("Nenhuma informação disponível para esses filtros selecionados.")

with aba2:

    stilo_abre = "<h1 style=color:#61677A;font-size:18px;>"
    stilo_fecha = "</h1>"

    spam_abre = f"<span style='color:#0766AD'>"
    spam_abre2 = f"<span style='color:#31304D'>"
    spam_fecha = "</span>"


    # https://colorhunt.co/

    
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
                        "color:#265073;
                        font-size:30px;
                        ">Total de questões: {total_questionamentos}</h1>""", 
                        unsafe_allow_html=True)
        
        for index in quantidades_totais.index:
            # print(f'{index} {quantidades_totais[index]}')
            st.markdown(f"""<h1 style=
                        "color:#265073;
                        font-size:30px;
                        ">{index}: {quantidades_totais[index]}</h1>""", 
                        unsafe_allow_html=True)
            
    with col2:
        st.subheader('Total por questionador')
        for index in questionador_totais.index:
            # print(f'{index} {questionador_totais[index]}')
            st.markdown(f"""<h1 style=
                        "color:#265073;
                        font-size:30px;
                        ">{index}: {questionador_totais[index]}</h1>""", 
                        unsafe_allow_html=True)

with aba3:

        # stilo_abre = "<h1 style=color:#61677A;font-size:20px;>"
        # stilo_fecha = "</h1>"
        
        st.markdown(""" 
                    📝 **Acesso às Atas das Reuniões com os Comitês**

                    Para garantir total transparência e facilitar o acesso à informação, disponibilizamos todas as atas das reuniões realizadas com os comitês. Esses documentos são essenciais para entender as decisões e discussões que impactam a direção da empresa.

                    🔍 **Como Acessar:**
                    - **As atas estão organizadas abaixo e podem ser visualizadas ou baixadas diretamente do nosso site.**
                    - Clique na ata desejada para abrir o documento, onde você pode ler online ou optar por fazer o download.

                    📥 **Download:**
                    - **Para baixar uma ata, clique no ícone de download na parte superior presente no documento. O arquivo será salvo em formato PDF em seu dispositivo.**

                    👥 Público-Alvo:
                    Esta seção é especialmente útil para acionistas, membros dos comitês, funcionários e qualquer parte interessada em acompanhar as atividades e decisões da empresa.

                    Acreditamos que o acesso facilitado a essas informações fortalece a confiança e a transparência entre a empresa e todos os seus stakeholders.""")
        
        st.divider()

        
        # def displayPDF(file):
        #     # Opening file from file path
        #     with open(file, "rb") as f:
        #         base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        #     # Embedding PDF in HTML
        #     pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1100" height="1000" type="application/pdf">'

        #     # Displaying File
        #     st.markdown(pdf_display, unsafe_allow_html=True)


        # def displayPDF(file):
        #     # Opening file from file path
        #     with open(file, "rb") as f:
        #         base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        #     # Embedding PDF in HTML
        #     pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1100" height="1000" type="application/pdf"></iframe>'

        #     # Displaying File
        #     st.markdown(pdf_display, unsafe_allow_html=True)


        # pdf_1 = './res/12-2023/52ª REUNIÃO ORDINÁRIA DO COMITÊ DE OPERAÇÃO E MANUTENÇÃO.pdf'
        # pdf_2 = './res/12-2023/Ata 164ª Reunião Ordinária do CRC - em análise pelos membros do CRC.pdf'
        # pdf_3 = './res/12-2023/Ata da 102ª Reunião do Comitê de Gestão - 14.12.23.pdf'
        # pdf_4 = './res/12-2023/ATA DA 114ª REUNIÃO DO COMITÊ DE AUDITORIA - somente orçamento.pdf'
        # pdf_5 = './res/12-2023/ATA DA 192ª REUNIÃO DO COMITÊ FINANCEIRO - orçamento.pdf'
        # pdf_6 = './res/12-2023/Ata_146ª Reunião ordinária do CT - 14.12.2023 - em análise pelos membros.pdf'
        # pdf_7 = './res/12-2023/Minuta da Ata da 172ª Reunião do CMA 13.12.2023 - orçamento.pdf'


        # https://discuss.streamlit.io/t/problems-displaying-pdf-in-streamlit-cloud/35555

        def displayPDF2(link):
            pdf_display = link
            st.markdown(pdf_display, unsafe_allow_html=True)


        # link calameo
            
        link1 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=005631827143ab67d94d2&mode=mini" width="800" height="680" frameborder="1" scrolling="yes" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""

        link2 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=005631827c55f2773760e&mode=mini" width="800" height="680" frameborder="0" scrolling="no" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""

        link3 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=005631827d9b85f7e011a&mode=mini" width="800" height="680" frameborder="0" scrolling="no" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""
        
        link4 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=005631827571460f2d32b&mode=mini" width="800" height="680" frameborder="0" scrolling="no" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""
        
        link5 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=005631827f48f3117aad9&mode=mini" width="800" height="680" frameborder="0" scrolling="no" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""
        
        link6 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=0056318274e89fa6ab377&mode=mini" width="800" height="680" frameborder="0" scrolling="no" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""
        
        link7 = """<div style="text-align:center;"><iframe src="//v.calameo.com/?bkcode=005631827ded0c40c559b&mode=mini" width="800" height="680" frameborder="0" scrolling="no" allowtransparency allowfullscreen style="margin:0 auto;"></iframe></div>"""
        
        # links expirados    
             
        # link1 = """<iframe src="https://publuu.com/flip-book/348588/798957/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""

        # link2 = """<iframe src="https://publuu.com/flip-book/348588/798987/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""

        # link3 = """<iframe src="https://publuu.com/flip-book/348588/799002/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""
        
        # link4 = """<iframe src="https://publuu.com/flip-book/348588/799004/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""
        
        # link5 = """<iframe src="https://publuu.com/flip-book/348588/799005/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""
        
        # link6 = """<iframe src="https://publuu.com/flip-book/348588/799006/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""
        
        # link7 = """<iframe src="https://publuu.com/flip-book/348588/799007/page/1?embed" width="100%" height="1620" scrolling="no" frameborder="0" allowfullscreen="" allow="clipboard-write" class="publuuflip"></iframe>"""
        

        
        with st.expander('Reunião 52ª Comitê de Operação e Manutenção'):
            # displayPDF(pdf_1)
            displayPDF2(link1)

        st.divider()
        
        with st.expander('Ata 164ª Reunião Ordinária do CRC'):
            # displayPDF(pdf_2)
            displayPDF2(link2)

        st.divider()

        with st.expander('Ata da 102ª Reunião do Comitê de Gestão'):
            # displayPDF(pdf_3)
            displayPDF2(link3)

        st.divider()

        with st.expander('Ata da 114ª Reunião do Comitê de Auditoria'):
            # displayPDF(pdf_4)
            displayPDF2(link4)

        st.divider()

        with st.expander('Ata da 192ª Reunião do Comitê Financeiro'):
            # displayPDF(pdf_5)
            displayPDF2(link5)

        st.divider()

        with st.expander('Ata 146ª Reunião Ordinária do CT'):
            # displayPDF(pdf_6)
            displayPDF2(link6)

        st.divider()

        with st.expander('Minuta da Ata da 172ª Reunião do CMA'):
            # displayPDF(pdf_7)
            displayPDF2(link7)

