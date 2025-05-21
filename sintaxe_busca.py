import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Elaboração de Sintaxe de busca")

# CSS global para aplicar a fonte e tamanho
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

st.markdown("Digite sua sintaxe/regra com operadores booleanos (**AND**, **OR**, **NOT**) e veja os destaques na sintaxe")

query = st.text_area("Escreva sua sintaxe de busca:", height=400)

def highlight_syntax(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue; font-weight:bold;">\1</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'\(', r'<span style="color:green; font-weight:bold;">(</span>', text)
    text = re.sub(r'\)', r'<span style="color:green; font-weight:bold;">)</span>', text)
    return text

def detectar_problemas(text):
    # Parênteses desbalanceados
    alerta_parenteses = ""
    if text.count('(') != text.count(')'):
        alerta_parenteses = "<span style='color:red; font-weight:bold;'>⚠️ Parênteses desbalanceados!</span>"

    # Detectar operadores inválidos (grafia incorreta)
    operadores_validos = {"AND", "OR", "NOT"}
    palavras = re.findall(r'\b\w{2,}\b', text)  # pega todas as palavras com 2 ou mais letras
    operadores_suspeitos = [p for p in palavras if p.upper() in operadores_validos and p.upper() != p]
    operadores_incorretos = [p for p in palavras if p.upper() not in operadores_validos and p.lower() in {"and", "or", "not"}]

    # Exibe erro se for um operador válido escrito de forma errada
    erros = operadores_suspeitos + operadores_incorretos
    alerta_operadores = ""
    if erros:
        alerta_operadores = (
            "<span style='color:red; font-weight:bold;'>"
            f"⚠️ Operadores inválidos detectados (grafia incorreta): {', '.join(erros)}"
            "</span>"
        )

    return alerta_parenteses, alerta_operadores

if query.strip():
    alerta_parenteses, alerta_operadores = detectar_problemas(query)

    if alerta_parenteses or alerta_operadores:
        st.markdown(
            f"<div style='font-family:Courier New, monospace; font-size:40px;'>{alerta_parenteses}<br>{alerta_operadores}</div>",
            unsafe_allow_html=True
        )

    highlighted = highlight_syntax(query)
    st.markdown("### 💡 Visualização com Destaque de Sintaxe")
    st.markdown(
        f"<div style='font-family:Courier New, monospace; font-size:40px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )
    
# Hashtags em laranja
text = re.sub(r'(#\w+)', r'<span style="color:orange; font-weight:bold;">\1</span>', text)

