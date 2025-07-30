import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Dobrador de Arame 3D", layout="centered")
st.title("🧰 Dobrador de Arame com Operações Separadas")

if "operacoes" not in st.session_state:
    st.session_state.operacoes = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# Visualização 3D
def desenhar_arame_3d(operacoes):
    x, y, z = [0], [0], [0]
    angulo = 0
    altura = 0

    for op in operacoes:
        tipo = op["tipo"]
        if tipo == "alimentar":
            dist = op["distancia"]
            rad = np.radians(angulo)
            dx = dist * np.cos(rad)
            dy = dist * np.sin(rad)
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
            z.append(altura)
        elif tipo == "dobrar":
            if op["direcao"] == "anti-horário":
                angulo += op["angulo"]
            else:
                angulo -= op["angulo"]

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        line=dict(color='darkorange', width=5),
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
        title="Visualização 3D do Arame"
    )
    st.plotly_chart(fig, use_container_width=True)

# Formulário: operação
st.subheader("➕ Adicionar Operação")

with st.form("form_operacao"):
    tipo = st.selectbox("Tipo de operação", ["alimentar", "dobrar"])

    if tipo == "alimentar":
        distancia = st.number_input("Distância (mm)", 0.0, 1000.0, 100.0)
        op = {"tipo": "alimentar", "distancia": distancia}
    else:
        angulo = st.number_input("Ângulo (°)", -360.0, 360.0, 90.0)
        direcao = st.selectbox("Direção", ["horário", "anti-horário"])
        op = {"tipo": "dobrar", "angulo": angulo, "direcao": direcao}

    salvar = st.form_submit_button("Salvar")

    if salvar:
        if st.session_state.edit_index is None:
            st.session_state.operacoes.append(op)
            st.success("✅ Operação adicionada!")
        else:
            st.session_state.operacoes[st.session_state.edit_index] = op
            st.success("✏️ Operação editada!")
            st.session_state.edit_index = None

# Lista de operações
st.subheader("📋 Lista de Operações")

for i, op in enumerate(st.session_state.operacoes):
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        if op["tipo"] == "alimentar":
            st.markdown(f"**{i+1}.** Alimentar → `{op['distancia']} mm`")
        else:
            st.markdown(f"**{i+1}.** Dobrar → `{op['angulo']}°` ({op['direcao']})")
    with col2:
        if st.button("✏️", key=f"edit_{i}"):
            st.session_state.edit_index = i
    with col3:
        if st.button("❌", key=f"delete_{i}"):
            st.session_state.operacoes.pop(i)
            st.experimental_rerun()

if st.session_state.operacoes:
    desenhar_arame_3d(st.session_state.operacoes)
else:
    st.info("Adicione operações para visualizar o arame.")

# Gerar Código G
def gerar_codigo_g(operacoes):
    linhas = ["; Código G gerado para dobras de arame"]
    for i, op in enumerate(operacoes, 1):
        linhas.append(f"\n; Operação {i}")
        if op["tipo"] == "alimentar":
            linhas.append(f"G1 X{op['distancia']:.2f}")
        else:
            direcao = "G3" if op["direcao"] == "anti-horário" else "G2"
            linhas.append(f"{direcao} A{op['angulo']:.2f}")
    return "\n".join(linhas)

if st.button("📄 Gerar Código G"):
    codigo = gerar_codigo_g(st.session_state.operacoes)
    st.text_area("📄 Código G", value=codigo, height=300)
    st.download_button("📥 Baixar Código G", codigo, file_name="dobras_arame.gcode")

if st.button("🗑️ Limpar tudo"):
    st.session_state.operacoes = []
    st.session_state.edit_index = None
    st.success("Tudo apagado.")
