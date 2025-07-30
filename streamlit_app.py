import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Gerador de Código G com Visualização", layout="centered")

st.title("🧰 Gerador de Código G com Visualização da Dobra")

if "instrucoes" not in st.session_state:
    st.session_state.instrucoes = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Função para gerar visualização do arame
def desenhar_arame(instrucoes):
    x, y = [0], [0]
    angulo_atual = 0

    for ang, dist, dir_ in instrucoes:
        if dir_ == "anti-horário":
            angulo_atual += ang
        else:
            angulo_atual -= ang

        rad = np.radians(angulo_atual)
        dx = dist * np.cos(rad)
        dy = dist * np.sin(rad)

        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    fig, ax = plt.subplots()
    ax.plot(x, y, '-o', color='steelblue')
    ax.set_aspect('equal')
    ax.set_title("Visualização das dobras")
    ax.grid(True)
    st.pyplot(fig)


# Formulário de instrução
st.subheader("➕ Adicionar Instrução")

with st.form("form_dobra"):
    col1, col2 = st.columns(2)
    with col1:
        angulo = st.number_input("Ângulo da dobra (°)", -360.0, 360.0, 90.0)
    with col2:
        distancia = st.number_input("Distância (mm)", 0.0, 1000.0, 100.0)

    direcao = st.selectbox("Direção", ["horário", "anti-horário"])
    enviar = st.form_submit_button("Salvar")

    if enviar:
        if st.session_state.edit_index is None:
            st.session_state.instrucoes.append((angulo, distancia, direcao))
            st.success("✅ Instrução adicionada!")
        else:
            st.session_state.instrucoes[st.session_state.edit_index] = (angulo, distancia, direcao)
            st.success("✏️ Instrução editada!")
            st.session_state.edit_index = None


# Mostrar instruções com opções de editar/apagar
st.subheader("📋 Instruções")

for i, (ang, dist, dir_) in enumerate(st.session_state.instrucoes):
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.markdown(f"**{i+1}.** Distância: `{dist} mm`, Ângulo: `{ang}°`, Direção: `{dir_}`")
    with col2:
        if st.button("✏️", key=f"edit_{i}"):
            angulo = ang
            distancia = dist
            direcao = dir_
            st.session_state.edit_index = i
    with col3:
        if st.button("❌", key=f"delete_{i}"):
            st.session_state.instrucoes.pop(i)
            st.experimental_rerun()

if st.session_state.instrucoes:
    desenhar_arame(st.session_state.instrucoes)
else:
    st.info("Adicione instruções para ver a visualização.")

# Geração de Código G
def gerar_codigo_g(instrs):
    linhas = ["; Código G gerado para dobras de arame"]
    for i, (ang, dist, dir_) in enumerate(instrs, 1):
        linhas.append(f"\n; Instrução {i}")
        linhas.append(f"G1 X{dist:.2f}")
        if dir_ == "horário":
            linhas.append(f"G2 A{ang:.2f}")
        else:
            linhas.append(f"G3 A{ang:.2f}")
    return "\n".join(linhas)

if st.button("📄 Gerar Código G"):
    codigo = gerar_codigo_g(st.session_state.instrucoes)
    st.text_area("📄 Código G", value=codigo, height=300)
    st.download_button("📥 Baixar Código G", codigo, file_name="dobras_arame.gcode")

if st.button("🗑️ Limpar tudo"):
    st.session_state.instrucoes = []
    st.session_state.edit_index = None
    st.success("Tudo apagado.")
