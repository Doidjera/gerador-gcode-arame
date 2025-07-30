import streamlit as st

st.set_page_config(page_title="Gerador de Código G para Dobra de Arame", layout="centered")

st.title("🧰 Gerador de Código G para Dobra de Arame")

if "instrucoes" not in st.session_state:
    st.session_state.instrucoes = []

with st.form("form_dobra"):
    col1, col2 = st.columns(2)
    with col1:
        angulo = st.number_input("Ângulo da dobra (°)", min_value=-360.0, max_value=360.0, value=90.0, step=1.0)
    with col2:
        distancia = st.number_input("Distância linear (mm)", min_value=0.0, value=100.0, step=1.0)

    direcao = st.selectbox("Direção da dobra", ["horário", "anti-horário"])
    adicionar = st.form_submit_button("Adicionar instrução")

    if adicionar:
        st.session_state.instrucoes.append((angulo, distancia, direcao))
        st.success("✅ Instrução adicionada!")

st.subheader("📋 Instruções Adicionadas")
if st.session_state.instrucoes:
    for i, (ang, dist, dir_) in enumerate(st.session_state.instrucoes, 1):
        st.markdown(f"**{i}.** Distância: `{dist}mm`, Ângulo: `{ang}°`, Direção: `{dir_}`")
else:
    st.info("Nenhuma instrução adicionada ainda.")

def gerar_codigo_g(instrucoes):
    linhas = ["; Código G gerado para dobras de arame"]
    for i, (ang, dist, dir_) in enumerate(instrucoes, 1):
        linhas.append(f"\n; Instrução {i}")
        linhas.append(f"G1 X{dist:.2f} ; Avança {dist:.2f} mm")
        if dir_ == "horário":
            linhas.append(f"G2 A{ang:.2f} ; Dobra {ang:.2f}° sentido horário")
        else:
            linhas.append(f"G3 A{ang:.2f} ; Dobra {ang:.2f}° sentido anti-horário")
    return "\n".join(linhas)

if st.button("Gerar Código G"):
    codigo = gerar_codigo_g(st.session_state.instrucoes)
    st.text_area("📄 Código G Gerado", value=codigo, height=300)
    st.download_button("📥 Baixar Código G", codigo, file_name="dobras_arame.gcode")

if st.button("🗑️ Limpar Instruções"):
    st.session_state.instrucoes = []
    st.success("Instruções apagadas.")
