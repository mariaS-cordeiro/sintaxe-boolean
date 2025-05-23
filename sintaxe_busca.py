import streamlit as st
import re

st.set_page_config(page_title="Elaboração de Sintaxe de Busca", layout="wide")
st.title("🔍 Elaboração de Sintaxe de Busca")

# Estilo CSS
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

def highlight_syntax(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Proteger trechos entre aspas com placeholders
    placeholder_map = {}
    def substituir_aspas(m):
        chave = f"__ASPAS_{len(placeholder_map)}__"
        placeholder_map[chave] = m.group(0)
        return chave

    text = re.sub(r'"[^"]*"|\'[^\']*\'', substituir_aspas, text)

    # Destaque: Operadores booleanos em azul
    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue; font-weight:bold;">\1</span>', text, flags=re.IGNORECASE)

    # Destaque: Parênteses em verde
    text = re.sub(r'\(', r'<span style="color:green; font-weight:bold;">(</span>', text)
    text = re.sub(r'\)', r'<span style="color:green; font-weight:bold;">)</span>', text)

    # Destaque: Hashtags em laranja
    text = re.sub(r'(#\w+)', r'<span style="color:orange; font-weight:bold;">\1</span>', text)

    # Restaurar os trechos entre aspas em cinza
    for chave, original in placeholder_map.items():
        text = text.replace(chave, f'<span style="color:gray;">{original}</span>')

    return text

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

if query.strip():
    alerta_parenteses, alerta_aspas, alerta_operadores = detectar_problemas(query)

    if alerta_parenteses or alerta_aspas or alerta_operadores:
        st.markdown(
            f"<div style='font-family:Courier New, monospace; font-size:30px;'>{alerta_parenteses}<br>{alerta_aspas}<br>{alerta_operadores}</div>",
            unsafe_allow_html=True
        )

    highlighted = highlight_syntax(query)
    st.markdown("### 💡 Visualização com destaque na sintaxe/regra")
    st.markdown(
        f"<div style='font-family:Courier New, monospace; font-size:40px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )
