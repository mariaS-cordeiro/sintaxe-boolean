import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Construtor de Sintaxe de Busca")

# CSS para aplicar fonte e tamanho na entrada e saída
st.markdown("""
    <style>
    textarea {
        font-family: 'Courier New', monospace !important;
        font-size: 40px !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stMarkdownContainer"] > div {
        font-family: 'Courier New', monospace;
        font-size: 40px;
        line-height: 1.2;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("Digite sua expressão com operadores booleanos (**AND**, **OR**, **NOT**) e veja o destaque de sintaxe.")

query = st.text_area("Escreva sua expressão:", height=300)

def highlight_syntax(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue; font-weight:bold;">\1</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'\(', r'<span style="color:green; font-weight:bold;">(</span>', text)
    text = re.sub(r'\)', r'<span style="color:green; font-weight:bold;">)</span>', text)
    if text.count('(') != text.count(')'):
        text += '<br><span style="color:red; font-weight:bold;">⚠️ Parênteses desbalanceados!</span>'
    return text

def detectar_operadores_errados(text):
    operadores_validos = {"AND", "OR", "NOT"}
    palavras = re.findall(r'\b[A-Z]{2,}\b', text)
    errados = [op for op in palavras if op.upper() not in operadores_validos]
    return errados

if query.strip():
    operadores_errados = detectar_operadores_errados(query)
    if operadores_errados:
        st.markdown(
            f"<div style='color:red; font-family:Courier New, monospace; font-size:40px;'>"
            f"⚠️ Operadores inválidos detectados: {', '.join(operadores_errados)}"
            f"</div>", unsafe_allow_html=True
        )

    highlighted = highlight_syntax(query)
    st.markdown("### 💡 Visualização com Destaque de Sintaxe")
    st.markdown(
        f"<div style='font-family:Courier New, monospace; font-size:40px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )
