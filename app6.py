import streamlit as st
import pandas as pd
from datetime import datetime

st.title('CENTRAL DE CONTADORIA REMOTA')

# Carregar o DataFrame com tratamento de erros
try:
    df = pd.read_csv('/home/felipe/Projetos/live_streamlit/ Consolidacao.csv')
except FileNotFoundError:
    st.error("Erro: O arquivo CSV não foi encontrado.")
    st.stop()  # Interrompe a execução se o arquivo não for encontrado

# Título da páginas
st.title('Busca Interativa da posição do Processo')

# Caixa de texto para entrada do usuário
texto_busca = st.text_input('Digite o número do processo:')

# Função para calcular a diferença média de dias entre a data de remessa e a data de conclusão
def calcular_media_dias(df, data_remessa_col, data_conclusao_col):
   # Convertendo as datas no formato dia/mês/ano (dayfirst=True)
    df = df.dropna(subset=[data_remessa_col, data_conclusao_col])  # Remover linhas com valores nulos nas colunas de datas
    datas_remessa = pd.to_datetime(df[data_remessa_col], dayfirst=True)
    datas_conclusao = pd.to_datetime(df[data_conclusao_col], dayfirst=True)
    diferenca_dias = (datas_conclusao - datas_remessa).dt.days
    return diferenca_dias.mean()

# Filtrar os dados e exibir as informações relevantes
if texto_busca:
    if 'Número do processo' in df.columns:
        df_filtrado = df[df['Número do processo'].str.contains(texto_busca, case=False)]
        
        if not df_filtrado.empty:
            # Extrair informações
            data_chegada = df_filtrado['DataRemessaContadoria'].values[0]
            nucleo = df_filtrado['Núcleo'].values[0]
            posicao_geral = df_filtrado['Posicao'].values[0]
            prioridade_legal = df_filtrado['Prioridade'].values[0] if 'Prioridade' == 'Prioridade Legal' else False
            posicao_prioridade = df_filtrado['Posicaoprioridade'].values[0] if 'Posicaoprioridade' in df_filtrado.columns else "N/A"

            # Calcular a média de dias no núcleo
            media_dias_nucleo = calcular_media_dias(df, 'DataRemessaContadoria', 'Data da conclusão')

            # Montar a mensagem de saída
            mensagem = (
                f"O processo **{texto_busca}** chegou no dia **{data_chegada}**, está no núcleo **{nucleo}**, "
                f"e está na posição geral **{posicao_geral}**.\n"
                f"A média de dias que o processo fica no núcleo é de **{media_dias_nucleo:.2f} dias**."
            )

            # Adicionar informações sobre prioridade, se aplicável
            if prioridade_legal:
                mensagem += f"\nEste é um processo de **prioridade legal**, ocupando a posição de prioridade **{posicao_prioridade}**."

            # Exibir a mensagem final
            st.write(mensagem)

        else:
            # Caso o processo não seja encontrado
            st.warning(f"O processo **{texto_busca}** não foi encontrado. Pode haver vários motivos: o processo foi devolvido à vara ou ainda não foi enviado à Contadoria Remota.")
    else:
        st.error("Erro: Coluna 'Número do processo' não encontrada no arquivo.")
