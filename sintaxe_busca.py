import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Elaboração de Sintaxe de Busca")

# CSS global para fonte e tamanho
st.markdown("""
    <style>
    textarea {
        font-family: 'Courier New', monospace !important;
        font-size: 30px !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stMarkdownContainer"] > div {
        font-family: 'Courier New', monospace;
        font-size: 40px;
        line-height: 1.2;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("Digite sua sintaxe/regra com operadores booleanos (**AND**, **OR**, **NOT**) e veja os destaques na sintaxe.")

query = st.text_area("Escreva sua sintaxe de busca:", height=400)

# Função de destaque visual com placeholders para aspas
def highlight_syntax(text):
    # Escapar HTML
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Protege trechos entre aspas com placeholders
    aspas_duplas = re.findall(r'"[^"]*"', text)
    aspas_simples = re.findall(r"'[^']*'", text)

    placeholder_map = {}
    for i, trecho in enumerate(aspas_duplas + aspas_simples):
        chave = f"__ASPAS_{i}__"
        placeholder_map[chave] = trecho
        text = text.replace(trecho, chave, 1)

    # Operadores booleanos em azul
    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue; font-weight:bold;">\1</span>', text, flags=re.IGNORECASE)

    # Parênteses em verde
    text = re.sub(r'\(', r'<span style="color:green; font-weight:bold;">(</span>', text)
    text = re.sub(r'\)', r'<span style="color:green; font-weight:bold;">)</span>', text)

    # Hashtags em laranja
    text = re.sub(r'(#\w+)', r'<span style="color:orange; font-weight:bold;">\1</span>', text)

    # Restaura trechos entre aspas em cinza
    for chave, original in placeholder_map.items():
        cinza = f'<span style="color:gray; font-weight:bold;">{original}</span>'
        text = text.replace(chave, cinza)

    return text

# Função de verificação de problemas
def detectar_problemas(text):
    alerta_parenteses = ""
    if text.count('(') != text.count(')'):
        alerta_parenteses = "<span style='color:red; font-weight:bold;'>⚠️ Parênteses abertos!</span>"

    alerta_aspas = ""
    if text.count('"') % 2 != 0 or text.count("'") % 2 != 0:
        alerta_aspas = "<span style='color:red; font-weight:bold;'>⚠️ Aspas abertas sem fechamento!</span>"

    operadores_validos = {"AND", "OR", "NOT"}
    palavras = re.findall(r'\b\w{2,}\b', text)
    operadores_suspeitos = [p for p in palavras if p.upper() in operadores_validos and p.upper() != p]
    operadores_incorretos = [p for p in palavras if p.upper() not in operadores_validos and p.lower() in {"and", "or", "not"}]
    erros = operadores_suspeitos + operadores_incorretos

    alerta_operadores = ""
    if erros:
        alerta_operadores = (
            "<span style='color:red; font-weight:bold;'>"
            f"⚠️ Operadores inválidos detectados (grafia incorreta): {', '.join(erros)}"
            "</span>"
        )

    return alerta_parenteses, alerta_aspas, alerta_operadores

# Execução principal
if query.strip():
    alerta_parenteses, alerta_aspas, alerta_operadores = detectar_problemas(query)

    if alerta_parenteses or alerta_aspas or alerta_operadores:
        st.markdown(
            f"<div style='font-family:Courier New, monospace; font-size:40px;'>{alerta_parenteses}<br>{alerta_aspas}<br>{alerta_operadores}</div>",
            unsafe_allow_html=True
        )

    highlighted = highlight_syntax(query)
    st.markdown("### 💡 Visualização com destaque na sintaxe/regra")
    st.markdown(
        f"<div style='font-family:Courier New, monospace; font-size:40px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )
