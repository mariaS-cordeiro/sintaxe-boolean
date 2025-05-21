import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Elaboração de Sintaxe de busca")

st.markdown("""
Digite sua expressão com operadores booleanos (**AND**, **OR**, **NOT**) e veja o destaque de sintaxe.
""")

query = st.text_area("Escreva sua expressão:", height=200)

def highlight_syntax(text):
    # Escapar caracteres HTML
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Operadores válidos em azul e negrito
    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue;"><strong>\1</strong></span>', text, flags=re.IGNORECASE)

    # Parênteses em verde e **com negrito**
    text = re.sub(r'\(', r'<span style="color:green; font-weight:bold;">(</span>', text)
    text = re.sub(r'\)', r'<span style="color:green; font-weight:bold;">)</span>', text)

    # Verificar parênteses desbalanceados
    if text.count('(') != text.count(')'):
        text += '<br><span style="color:red;"><strong>⚠️ Parênteses desbalanceados!</strong></span>'

    return text

def detectar_operadores_errados(text):
    # Lista dos únicos operadores válidos
    operadores_validos = {"AND", "OR", "NOT"}

    # Encontrar palavras em caixa alta com 2 ou mais letras
    palavras = re.findall(r'\b[A-Z]{2,}\b', text)
    errados = [op for op in palavras if op.upper() not in operadores_validos]

    return errados

if query.strip():
    # Detectar e exibir operadores inválidos
    operadores_errados = detectar_operadores_errados(query)
    if operadores_errados:
        st.markdown(
            f"<span style='color:red; font-family:Courier New; font-size:14px;'>"
            f"⚠️ Operadores inválidos detectados: {', '.join(operadores_errados)}"
            f"</span>", unsafe_allow_html=True
        )

    # Mostrar destaque
    st.markdown("### 💡 Visualização com Destaque de Sintaxe")
    highlighted = highlight_syntax(query)
    st.markdown(
        f"<div style='font-family:Courier New; font-size:14px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )
