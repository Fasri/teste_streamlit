import streamlit as st
from fpdf import FPDF
import pandas as pd

# Função para calcular o valor corrigido
def calcular_valor_corrigido(valor_inicial, taxa_correcao, juros):
    """Calcula o valor corrigido aplicando a taxa de correcao e juros."""
    taxa_correcao = taxa_correcao / 100  # Converter porcentagem
    juros = juros / 100  # Converter porcentagem
    valor_corrigido = valor_inicial * (1 + taxa_correcao) * (1 + juros)
    return valor_corrigido

# Função para gerar o PDF em formato de planilha
def gerar_pdf(dados):
    """Gera um PDF com os dados fornecidos em formato de planilha."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Atualização de Valor", ln=True, align='C')

    # Cabeçalhos da "planilha"
    pdf.set_font("Arial", 'B', size=10)
    pdf.cell(40, 10, txt="Valor Inicial (R$)", border=1, align='C')
    pdf.cell(40, 10, txt="Data de Atualização", border=1, align='C')
    pdf.cell(40, 10, txt="Taxa de Correção (%)", border=1, align='C')
    pdf.cell(40, 10, txt="Taxa de Juros (%)", border=1, align='C')
    pdf.cell(40, 10, txt="Valor Corrigido (R$)", border=1, align='C')
    pdf.ln()

    # Conteúdo das linhas da "planilha"
    pdf.set_font("Arial", size=10)
    for _, dado in dados.iterrows():
        pdf.cell(40, 10, txt=f"{dado['valor_inicial']:.2f}", border=1, align='C')
        pdf.cell(40, 10, txt=str(dado['data_atualizacao']), border=1, align='C')
        pdf.cell(40, 10, txt=f"{dado['taxa_correcao']:.2f}", border=1, align='C')
        pdf.cell(40, 10, txt=f"{dado['juros']:.2f}", border=1, align='C')
        pdf.cell(40, 10, txt=f"{dado['valor_corrigido']:.2f}", border=1, align='C')
        pdf.ln()

    pdf.output("relatorio.pdf")

# Interface do Streamlit
st.title("Calculadora de Atualização de Valor")

# DataFrame inicial para armazenar as linhas de dados
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=['valor_inicial', 'data_atualizacao', 'taxa_correcao', 'juros', 'valor_corrigido'])

# Função para adicionar uma nova linha
def adicionar_linha(valor_inicial, data_atualizacao, taxa_correcao, juros):
    novo_dado = pd.DataFrame({
        'valor_inicial': [valor_inicial],
        'data_atualizacao': [data_atualizacao],
        'taxa_correcao': [taxa_correcao],
        'juros': [juros],
        'valor_corrigido': [calcular_valor_corrigido(valor_inicial, taxa_correcao, juros)]
    })

    # Usar pd.concat em vez de append
    st.session_state.dados = pd.concat([st.session_state.dados, novo_dado], ignore_index=True)

# Função para excluir uma linha
def excluir_linha(indice):
    st.session_state.dados = st.session_state.dados.drop(indice).reset_index(drop=True)

# Inputs em forma de "linha" da planilha
st.subheader("Insira os dados como em uma planilha:")

col1, col2, col3, col4 = st.columns(4)
with col1:
    valor_inicial = st.number_input("Valor Inicial:", key="valor_inicial")
with col2:
    data_atualizacao = st.date_input("Data da Atualização", key="data_atualizacao")
with col3:
    taxa_correcao = st.number_input("Taxa de Correção (%)", key="taxa_correcao")
with col4:
    juros = st.number_input("Taxa de Juros (%)", key="juros")

# Botão para adicionar a nova linha
if st.button("Adicionar Linha"):
    adicionar_linha(valor_inicial, data_atualizacao, taxa_correcao, juros)
    st.success("Linha adicionada com sucesso!")

# Exibir as entradas já adicionadas em forma de tabela
if not st.session_state.dados.empty:
    st.subheader("Dados Adicionados")

    # Exibição de linhas com botão para excluir cada uma
    for i, row in st.session_state.dados.iterrows():
        cols = st.columns(6)
        cols[0].write(f"R$ {row['valor_inicial']:.2f}")
        cols[1].write(row['data_atualizacao'])
        cols[2].write(f"{row['taxa_correcao']:.2f}%")
        cols[3].write(f"{row['juros']:.2f}%")
        cols[4].write(f"R$ {row['valor_corrigido']:.2f}")
        if cols[5].button("Excluir", key=f"excluir_{i}"):
            excluir_linha(i)
            st.success(f"Linha {i+1} excluída com sucesso!")
            st.experimental_rerun()  # Atualiza a página após a exclusão

# Botão para calcular e gerar PDF
if st.button("Calcular e Gerar PDF"):
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
