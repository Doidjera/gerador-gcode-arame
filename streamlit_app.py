import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Gerador de Código G 3D", layout="centered")
st.title("🧰 Gerador de Código G com Visualização 3D")

if "instrucoes" not in st.session_state:
    st.session_state.instrucoes = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# VISUALIZAÇÃO 3D
def desenhar_arame_3d(instrucoes):
    x, y, z = [0], [0], [0]
    angulo = 0
    altura = 0  # você pode mudar isso para simular mudanças no eixo Z

    for ang, dist, direcao in instrucoes:
        if direcao == "anti-horário":
            angulo += ang
        else:
            angulo -= ang

        rad = np.radians(angulo)
        dx = dist * np.cos(rad)
        dy = dist * np.sin(rad)

        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
        z.append(altura)

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        line=dict(color='royalblue', width=5),
        marker=dict(size=4)
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=30),
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        title="Visualização 3D das dobras"
    )
    st.plotly_chart(fig, use_container_width=True)

# FORMULÁRIO
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

# LISTA DE INSTRUÇÕES
st.subheader("📋 Instruções")
for i, (ang, dist, dir_) in enumerate(st.session_state.instrucoes):
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.markdown(f"**{i+1}.** Distância: `{dist} mm`, Ângulo: `{ang}°`, Direção: `{dir_}`")
    with col2:
        if st.button("✏️", key=f"edit_{i}"):
            st.session_state.edit_index = i
    with col3:
        if st.button("❌", key=f"delete_{i}"):
            st.session_state.instrucoes.pop(i)
            st.experimental_rerun()

if st.session_state.instrucoes:
    desenhar_arame_3d(st.session_state.instrucoes)
else:
    st.info("Adicione instruções para visualizar em 3D.")

# G-CODE
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
