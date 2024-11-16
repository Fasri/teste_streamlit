import streamlit as st
import pandas as pd

# Função para carregar a tabela Excel
def carregar_tabela():
    uploaded_file = st.file_uploader("Escolha o arquivo Excel", type=['xls', 'xlsx'])
    if uploaded_file:
        # Carregar o arquivo Excel em um DataFrame
        df = pd.read_excel(uploaded_file)
        # Filtrar apenas as prioridades legais
        prioridades_legais = df[df['prioridades'].str.contains('Prioridade Legal', case=False, na=False)].copy()

        # Adicionar uma coluna "posição prioridade" numerando apenas as prioridades legais
        prioridades_legais['posição prioridade'] = range(1, len(prioridades_legais) + 1)

        # Juntar essa nova coluna de volta ao DataFrame original
        df = df.merge(prioridades_legais[['processo', 'posição prioridade']], on='processo', how='left')
        
        # Reorganizar para que a coluna "posição prioridade" seja a primeira
        df = df[['posição prioridade'] + [col for col in df.columns if col != 'posição prioridade']]
        
        return df
    return None

# Função para exibir a posição prioridade, número do processo, menu de calculista e cumprimento lado a lado
def exibir_processo_calculista_cumprimento(df):
    for index, row in df.iterrows():
        # Criar quatro colunas: Posição Prioridade, Processo, Calculista, Cumprimento
        cols = st.columns([1, 1, 2, 2])  # Ajustando a largura das colunas

        # Exibir posição prioridade na primeira coluna
        with cols[0]:
            st.write(f"{row['posição prioridade']}" if pd.notnull(row['posição prioridade']) else "")

        # Exibir número do processo na segunda coluna
        with cols[1]:
            st.write(f"{row['processo']}")

        # Exibir menu de calculista na terceira coluna
        with cols[2]:
            df.at[index, 'calculista'] = st.selectbox(
                "Calculista",
                options=['', 'Felipe Ribeiro', 'Big Boss 1', 'Big Boss 2', 'Priscilla'],
                index=['', 'Felipe Ribeiro', 'Big Boss 1', 'Big Boss 2', 'Priscilla'].index(row['calculista']) if row['calculista'] in ['Felipe Ribeiro', 'Big Boss 1', 'Big Boss 2', 'Priscilla'] else 0,
                key=f'calculista_{index}'
            )

        # Exibir menu de cumprimento na quarta coluna
        with cols[3]:
            df.at[index, 'cumprimento'] = st.selectbox(
                "Cumprimento",
                options=['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'],
                index=['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'].index(row['cumprimento']) if row['cumprimento'] in ['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'] else 0,
                key=f'cumprimento_{index}'
            )

# Carregar a tabela Excel
df = carregar_tabela()

if df is not None:
    # Exibir a posição prioridade, número do processo, calculista e cumprimento lado a lado
    exibir_processo_calculista_cumprimento(df)

    # Exibir a tabela final atualizada na barra lateral, incluindo todas as colunas
    st.sidebar.write("Tabela Atualizada")
    st.sidebar.dataframe(df)
