import streamlit as st
from fpdf import FPDF
import datetime

def calcular_valor_corrigido(valor_inicial, taxa_correcao, juros):
    """Calcula o valor corrigido aplicando a taxa de correcao e juros.

    Args:
        valor_inicial: O valor inicial a ser corrigido.
        taxa_correcao: A taxa de correção em percentual.
        juros: A taxa de juros em percentual.

    Returns:
        O valor corrigido.
    """

    taxa_correcao = taxa_correcao
    juros = juros / 100
    valor_corrigido = valor_inicial * (1 + taxa_correcao) * (1 + juros)
    return valor_corrigido

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for dado in dados:
        pdf.cell(200, 10, txt=f"Data da Atualização: {dado['data_atualizacao']}", ln=True)
        pdf.cell(200, 10, txt=f"Valor Inicial: R$ {dado['valor_inicial']:.2f}", ln=True)
        # ... (outros campos)
        pdf.cell(200, 10, txt=f"Valor Corrigido: R$ {dado['valor_corrigido']:.2f}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)  # Linha em branco para separar os registros

    pdf.output("relatorio.pdf")
# def gerar_pdf(valor_inicial, taxa_correcao, juros, valor_corrigido, data_atualizacao):
#     """Gera um PDF com os dados da simulação.

#     Args:
#         valor_inicial: O valor inicial a ser corrigido.
#         taxa_correcao: A taxa de correção em percentual.
#         juros: A taxa de juros em percentual.
#         valor_corrigido: O valor corrigido.
#         data_atualizacao: A data até onde vai a atualização.
#     """

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt="Relatório de Atualização de Valor", ln=True, align='C')
#     pdf.cell(200, 10, txt=f"Data da Atualização: {data_atualizacao}", ln=True)
#     pdf.cell(200, 10, txt=f"Valor Inicial: R$ {valor_inicial:.2f}", ln=True)
#     pdf.cell(200, 10, txt=f"Taxa de Correção: {taxa_correcao:.2f}%", ln=True)
#     pdf.cell(200, 10, txt=f"Taxa de Juros: {juros:.2f}%", ln=True)
#     pdf.cell(200, 10, txt=f"Valor Corrigido: R$ {valor_corrigido:.2f}", ln=True)
#     pdf.output("relatorio.pdf")

# # Interface do Streamlit
# st.title("Calculadora de Atualização de Valor")

# valor_inicial = st.number_input("Valor Inicial:")
# data_atualizacao = st.date_input("Data da Atualização")
# taxa_correcao = st.number_input("Taxa de Correção (%)")
# juros = st.number_input("Taxa de Juros (%)")

# if st.button("Calcular e Gerar PDF"):
#     valor_corrigido = calcular_valor_corrigido(valor_inicial, taxa_correcao, juros)
#     st.write("Valor Corrigido:", valor_corrigido)
#     gerar_pdf(valor_inicial, taxa_correcao, juros, valor_corrigido, data_atualizacao)
#     st.success("PDF gerado com sucesso!")

# Interface do Streamlit
st.title("Calculadora de Atualização de Valor")

# Lista para armazenar os dados de cada linha
dados = []

# Container para adicionar novas linhas dinamicamente
container = st.container()

# Função para adicionar uma nova linha de campos
def adicionar_linha():
    with container:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            valor_inicial = st.number_input("Valor Inicial:")
        with col2:
            data_atualizacao = st.date_input("Data da Atualização")
        with col3:
            taxa_correcao = st.number_input("Taxa de Correção")
        with col4:
            juros = st.number_input("Taxa de Juros (%)")
        
         # Adiciona os dados da linha à lista
        dados.append({
            'valor_inicial': valor_inicial,
            'data_atualizacao': data_atualizacao,
            'taxa_correcao': taxa_correcao,
            'juros': juros
        })

# Botão para adicionar nova linha
st.button("Adicionar Valor", on_click=adicionar_linha)

# Botão para calcular e gerar PDF
if st.button("Calcular e Gerar PDF"):
    # Coleta os dados de todas as linhas
    # dados = []
    # # ... (lógica para coletar os dados de todas as linhas)
    
    # Calcula os valores corrigidos e gera o PDF
    for dado in dados:
        valor_corrigido = calcular_valor_corrigido(dado['valor_inicial'], dado['taxa_correcao'], dado['juros'])
        # ... (adicionar o valor corrigido aos dados)
        dado['valor_corrigido'] = valor_corrigido
    gerar_pdf(dados)
    st.success("PDF gerado com sucesso!")

# Chamada inicial para adicionar a primeira linha
adicionar_linha()
# Para permitir o download:
with open('relatorio.pdf', 'rb') as pdf_file:
    PDFbytes = pdf_file.read()

st.download_button(
    label="Baixar PDF",
    data=PDFbytes,
    file_name="relatorio.pdf",
    mime='application/octet-stream'
)