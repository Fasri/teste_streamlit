import streamlit as st
import pandas as pd
from datetime import datetime

# Função para carregar a tabela Excel
def carregar_tabela():
    uploaded_file = st.file_uploader("Escolha o arquivo Excel", type=['xls', 'xlsx'])
    if uploaded_file:
        # Carregar o arquivo Excel em um DataFrame
        df = pd.read_excel(uploaded_file)
        return df
    return None

# Função para exibir o menu suspenso para o calculista
def exibir_menu_calculista(index, current_value):
    calculista = st.selectbox(
        "Calculista",
        options=['', 'Felipe Ribeiro', 'Big Boss 1', 'Big Boss 2', 'Priscilla'],
        index=current_value if current_value in ['Felipe Ribeiro', 'Big Boss 1', 'Big Boss 2', 'Priscilla'] else 0,
        key=f'calculista_{index}'
    )
    return calculista

# Função para exibir o menu suspenso para o cumprimento
def exibir_menu_cumprimento(index, current_value):
    cumprimento = st.selectbox(
        "Cumprimento",
        options=['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'],
        index=['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'].index(current_value) if current_value in ['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'] else 0,
        key=f'cumprimento_{index}'
    )
    return cumprimento

# Função para atualizar a tabela com base nas seleções
def atualizar_tabela(df):
    for index, row in df.iterrows():
        st.write(f"Processo: {row['processo']}")
        
        # Exibir menu de calculista
        df.at[index, 'calculista'] = exibir_menu_calculista(index, row['calculista'])
        
        # Data de atribuição: só exibe se houver calculista
        if df.at[index, 'calculista']:
            df.at[index, 'data de atribuição'] = st.date_input(
                "Data de Atribuição", 
                value=pd.to_datetime(row['data de atribuição']) if pd.notnull(row['data de atribuição']) else datetime.today(), 
                key=f'data_atribuicao_{index}'
            )
        
        # Exibir menu de cumprimento
        df.at[index, 'cumprimento'] = exibir_menu_cumprimento(index, row['cumprimento'])
        
        # Data de conclusão: só exibe se o cumprimento for diferente de "pendente"
        if df.at[index, 'cumprimento'] != 'pendente':
            df.at[index, 'data de conclusão'] = st.date_input(
                "Data de Conclusão", 
                value=pd.to_datetime(row['data de conclusão']) if pd.notnull(row['data de conclusão']) else datetime.today(), 
                key=f'data_conclusao_{index}'
            )
        
        st.write("---")  # Separador entre linhas

# Interface do Streamlit
st.title("Sistema de Acompanhamento de Processos")

# Carregar a tabela Excel
df = carregar_tabela()

if df is not None:
    # Exibir e atualizar a tabela
    atualizar_tabela(df)

    # Exibir a tabela final atualizada
    st.write("Planilha de Acompanhamento Atualizada")
    st.dataframe(df)
