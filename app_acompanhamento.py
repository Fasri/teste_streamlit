import streamlit as st
import pandas as pd
from datetime import datetime

# Dados simulados para a tabela
data = {
    'núcleo': ['Núcleo 1', 'Núcleo 2', 'Núcleo 3'],
    'processo': ['12345', '67890', '54321'],
    'vara': ['Vara 1', 'Vara 2', 'Vara 3'],
    'prioridade': ['Alta', 'Média', 'Baixa'],
    'calculista': [None, None, None],
    'data de atribuição': [None, None, None],
    'cumprimento': ['pendente', 'pendente', 'pendente'],
    'data de conclusão': [None, None, None]
}

# Convertemos os dados em um DataFrame
df = pd.DataFrame(data)

# Função para exibir o menu suspenso para o calculista
def exibir_menu_calculista(index):
    calculista = st.selectbox(
        "Calculista",
        options=['', 'Felipe Ribeiro', 'Big Boss 1', 'Big Boss 2', 'Priscilla'],
        key=f'calculista_{index}'
    )
    return calculista

# Função para exibir o menu suspenso para o cumprimento
def exibir_menu_cumprimento(index):
    cumprimento = st.selectbox(
        "Cumprimento",
        options=['pendente', 'cálculo realizado', 'cálculo atualizado', 'devolvido para esclarecimentos'],
        key=f'cumprimento_{index}'
    )
    return cumprimento

# Função para atualizar a tabela com base nas seleções
def atualizar_tabela():
    for index, row in df.iterrows():
        # Exibir campos para cada linha da tabela
        st.write(f"Processo: {row['processo']}")
        
        # Exibir menu de calculista
        df.at[index, 'calculista'] = exibir_menu_calculista(index)
        
        # Data de atribuição: só exibe se houver calculista
        if df.at[index, 'calculista']:
            df.at[index, 'data de atribuição'] = st.date_input(
                "Data de Atribuição", 
                value=datetime.today(), 
                key=f'data_atribuicao_{index}'
            )
        
        # Exibir menu de cumprimento
        df.at[index, 'cumprimento'] = exibir_menu_cumprimento(index)
        
        # Data de conclusão: só exibe se o cumprimento for diferente de "pendente"
        if df.at[index, 'cumprimento'] != 'pendente':
            df.at[index, 'data de conclusão'] = st.date_input(
                "Data de Conclusão", 
                value=datetime.today(), 
                key=f'data_conclusao_{index}'
            )
        
        st.write("---")  # Separador entre linhas

# Chamar a função para exibir e atualizar a tabela
atualizar_tabela()

# Exibir a tabela final atualizada
st.write("Tabela Atualizada")
st.dataframe(df)
