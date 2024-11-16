import streamlit as st
from fpdf import FPDF
import datetime

# Função para calcular o valor corrigido
def calcular_valor_corrigido(valor_inicial, taxa_correcao, juros):
    """Calcula o valor corrigido aplicando a taxa de correcao e juros."""
    taxa_correcao = taxa_correcao / 100  # Converter porcentagem
    juros = juros / 100  # Converter porcentagem
    valor_corrigido = valor_inicial * (1 + taxa_correcao) * (1 + juros)
    return valor_corrigido

# Função para gerar o PDF
def gerar_pdf(dados):
    """Gera um PDF com os dados fornecidos."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Atualização de Valor", ln=True, align='C')
    
    for dado in dados:
        pdf.cell(200, 10, txt=f"Data da Atualização: {dado['data_atualizacao']}", ln=True)
        pdf.cell(200, 10, txt=f"Valor Inicial: R$ {dado['valor_inicial']:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Taxa de Correção: {dado['taxa_correcao']:.2f}%", ln=True)
        pdf.cell(200, 10, txt=f"Taxa de Juros: {dado['juros']:.2f}%", ln=True)
        pdf.cell(200, 10, txt=f"Valor Corrigido: R$ {dado['valor_corrigido']:.2f}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)  # Linha em branco para separar os registros

    pdf.output("relatorio.pdf")

# Interface do Streamlit
st.title("Calculadora de Atualização de Valor")

# Lista para armazenar os dados de cada linha
if 'dados' not in st.session_state:
    st.session_state.dados = []

# Função para adicionar uma nova linha de campos e exibi-la
def adicionar_linha():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        valor_inicial = st.number_input("Valor Inicial:", key=f'valor_inicial-{len(st.session_state.dados)}')
    with col2:
        data_atualizacao = st.date_input("Data da Atualização", key=f'data_atualizacao-{len(st.session_state.dados)}')
    with col3:
        taxa_correcao = st.number_input("Taxa de Correção (%)", key=f'taxa_correcao-{len(st.session_state.dados)}')
    with col4:
        juros = st.number_input("Taxa de Juros (%)", key=f'juros-{len(st.session_state.dados)}')
    
    if st.button("Adicionar Valor", key=f'botao_adicionar-{len(st.session_state.dados)}'):
        # Adiciona os dados da linha à lista na sessão
        st.session_state.dados.append({
            'valor_inicial': valor_inicial,
            'data_atualizacao': data_atualizacao,
            'taxa_correcao': taxa_correcao,
            'juros': juros
        })

# Exibe os campos para adicionar uma nova linha
adicionar_linha()

# Exibe os dados já adicionados
if st.session_state.dados:
    st.subheader("Valores Adicionados")
    for i, dado in enumerate(st.session_state.dados):
        st.write(f"Registro {i+1}:")
        st.write(f"Valor Inicial: R$ {dado['valor_inicial']:.2f}")
        st.write(f"Data da Atualização: {dado['data_atualizacao']}")
        st.write(f"Taxa de Correção: {dado['taxa_correcao']}%")
        st.write(f"Taxa de Juros: {dado['juros']}%")

# Botão para calcular e gerar PDF
if st.button("Calcular e Gerar PDF"):
    for dado in st.session_state.dados:
        valor_corrigido = calcular_valor_corrigido(dado['valor_inicial'], dado['taxa_correcao'], dado['juros'])
        dado['valor_corrigido'] = valor_corrigido
    gerar_pdf(st.session_state.dados)
    st.success("PDF gerado com sucesso!")

    # Para permitir o download:
    with open('relatorio.pdf', 'rb') as pdf_file:
        PDFbytes = pdf_file.read()

    st.download_button(
        label="Baixar PDF",
        data=PDFbytes,
        file_name="relatorio.pdf",
        mime='application/octet-stream'
    )
