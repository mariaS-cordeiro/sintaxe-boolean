import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Construtor de Sintaxe de Busca")

st.markdown("""
Digite sua expressão com operadores booleanos (**AND**, **OR**, **NOT**) e veja o destaque de sintaxe.
""")

query = st.text_area("Escreva sua expressão:", height=200)

def highlight_syntax(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue;"><strong>\1</strong></span>', text, flags=re.IGNORECASE)
    text = re.sub(r'\(', r'<span style="color:green;"><strong>(</strong></span>', text)
    text = re.sub(r'\)', r'<span style="color:green;"><strong>)</strong></span>', text)
    if text.count('(') != text.count(')'):
        text += '<br><span style="color:red;"><strong>⚠️ Parênteses desbalanceados!</strong></span>'
    return text

if query.strip():
    st.markdown("### 💡 Visualização com Destaque de Sintaxe")
    highlighted = highlight_syntax(query)
    st.markdown(f"<div style='font-family: monospace; font-size: 16px;'>{highlighted}</div>", unsafe_allow_html=True)
