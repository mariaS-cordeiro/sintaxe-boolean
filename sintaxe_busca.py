def highlight_syntax(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    placeholder_map = {}

    def substituir_aspas(m):
        chave = f"__ASPAS_{len(placeholder_map)}__"
        placeholder_map[chave] = m.group(0)
        return chave

    # CORRIGIDO AQUI
    text = re.sub(r'"[^"]*"|\'[^\']*\'', substituir_aspas, text)

    text = re.sub(r'\b(AND|OR|NOT)\b', r'<span style="color:blue; font-weight:bold;">\1</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'\(', r'<span style="color:green; font-weight:bold;">(</span>', text)
    text = re.sub(r'\)', r'<span style="color:green; font-weight:bold;">)</span>', text)
    text = re.sub(r'(#\w+)', r'<span style="color:orange; font-weight:bold;">\1</span>', text)

    for chave, original in placeholder_map.items():
        text = text.replace(chave, f'<span style="color:gray;">{original}</span>')

    return text
