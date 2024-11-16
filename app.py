import streamlit as st
import pandas as pd

st.title('CENTRAL DE CONTADORIA REMOTA')

# Carregar o DataFrame
df = pd.read_csv('/home/felipe/Projetos/live_streamlit/ Consolidacao.csv')

# Título da página
st.title('Busca Interativa da posição do Processo')

# Caixa de texto para entrada do usuário
texto_busca = st.text_input('Digite o numero do processo:')

# Filtrar os dados e exibir a tabela
if texto_busca:
    df_filtrado = df[df['Número do processo'].str.contains(texto_busca, case=False)]
    st.dataframe(df_filtrado)