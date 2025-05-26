# Visualização e validação
if query.strip():
    alerta_parenteses, alerta_aspas, alerta_operadores = detectar_problemas(query)

    if alerta_parenteses or alerta_aspas or alerta_operadores:
        st.markdown(
            f"<div style='font-family:Courier New, monospace; font-size:20px;'>{alerta_parenteses}<br>{alerta_aspas}<br>{alerta_operadores}</div>",
            unsafe_allow_html=True
        )

    highlighted = highlight_syntax(query)
    st.markdown("### 💡 Visualização com destaque na sintaxe/regra")
    st.markdown(
        f"<div style='font-family:Courier New, monospace; font-size:40px;'>{highlighted}</div>",
        unsafe_allow_html=True
    )

# ⬇️ Mostrar botão mesmo que o query esteja vazio
if st.button("💾 Salvar sintaxe de busca"):
    if not tematica or not aluno or not query:
        st.warning("⚠️ Preencha todos os campos antes de salvar.")
    else:
        nova_entrada = pd.DataFrame({
            "temática da sintaxe": [tematica],
            "aluno/aluna": [aluno],
            "sintaxe de busca": [query],
            "data/hora": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })

        if os.path.exists(csv_path):
            existente = pd.read_csv(csv_path)
            df_total = pd.concat([existente, nova_entrada], ignore_index=True)
        else:
            df_total = nova_entrada

        df_total.to_csv(csv_path, index=False)
        st.success("✅ Sintaxe salva com sucesso!")
