import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Construtor de Sintaxe de Busca")

# CSS: aplica fonte Courier New tamanho 40 na entrada e saída
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
    return text

def detectar_problemas(text):
    # Verifica parênteses desbalanceados
    parenteses_balanceados = text.count('(') == text.count(')')
    alerta_parenteses = ""
    if not parenteses_balanceados:
        alerta_parenteses = "<span style='color:red; font-weight:bold;'>⚠️ Parênteses desbalanceados!</span>"

    # Detecta operadores inválidos
    operadores_validos = {"AND", "OR", "NOT"}
    palavras_maiusculas = re.findall(r'\b[A-Z]{2,}\b', text)
    operadores_errados = [p for p in palavras_maiusculas if p.upper() not in operadores_validos]

    alerta_operadores = ""
    if operadores_errados:
        alerta_operadores = (
            "<span style='color:red; font-weight:bold;'>"
            f"⚠️ Operadores inválidos detectados: {', '.join(operadores_errados)}"
            "</span>"
        )

    return alerta_parenteses, alerta_operadores

if query.strip():
    # Verifica e exibe alertas
    alerta_parenteses, alerta_operadores = detectar_problemas(query)
    if alerta_parenteses or alerta_operadores:
        st.markdown(f"<div style='font-family:Courier New, monospace; font-size:40px;'>{alerta_parenteses}<br>{alerta_operadores}</div>", unsafe_allow_html=True)

    # Exibe visualização com destaque
    highlighted = highlight_syntax(query)
    st.markdown("### 💡 Visualização com Destaque de Sintaxe")
    st.markdown(
        f"<div style='font-family:Courier New, monospace; font-size:40px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )
