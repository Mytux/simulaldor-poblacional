import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Simulador Ecológico", layout="wide")
st.title("📊 Simulador Interactivo de Crecimiento Poblacional")

st.markdown("""
Visualización cartesiana del modelo en cuadrantes:
$$r = \\frac{\\ln(|R_0|)}{T} \\cdot \\text{signo}(R_0)$$
""")

col_control1, col_control2 = st.columns(2)

with col_control1:
    st.subheader("🔴 Escenario 1 (Positivo)")
    R0_1 = st.slider("R0 - Tasa Neta", -50.0, 50.0, 31.2, step=0.1, key="r1")
    T_1 = st.slider("T - Tiempo Generacional", 0.1, 20.0, 8.96, step=0.01, key="t1")
    r1 = (np.log(abs(R0_1)) / T_1) if R0_1 != 0 else 0
    if R0_1 < 0:
        r1 = -r1
    st.metric("Tasa intrínseca (r1)", f"{r1:.4f}")

with col_control2:
    st.subheader("🔵 Escenario 2 (Negativo / Control)")
    R0_2 = st.slider("R0 - Tasa Neta ", -50.0, 50.0, -20.0, step=0.1, key="r2")
    T_2 = st.slider("T - Tiempo Generacional ", 0.1, 20.0, 4.5, step=0.01, key="t2")
    r2 = (np.log(abs(R0_2)) / T_2) if R0_2 != 0 else 0
    if R0_2 < 0:
        r2 = -r2
    st.metric("Tasa intrínseca (r2)", f"{r2:.4f}")

N0 = st.sidebar.number_input("Población inicial (N0)", value=10, min_value=1)
t_max = st.sidebar.slider("Rango Tiempo (Eje X)", 10, 100, 60)

# Puntos discontinuos tipo GeoGebra para armar los cuadrantes
t_puntos = np.linspace(0, t_max, 25)

# Calculamos trayectoria positiva y espejo negativo si r < 0
if r1 >= 0:
    y1 = N0 * np.exp(r1 * (t_puntos / 10)) - N0
else:
    y1 = -(N0 * np.exp(abs(r1) * (t_puntos / 10)) - N0)

if r2 >= 0:
    y2 = N0 * np.exp(r2 * (t_puntos / 10)) - N0
else:
    y2 = -(N0 * np.exp(abs(r2) * (t_puntos / 10)) - N0)

fig = go.Figure()

# Trazo Escenario 1 con marcadores tipo GeoGebra
fig.add_trace(
    go.Scatter(
        x=t_puntos,
        y=y1,
        mode="lines+markers",
        name=f"Escenario 1 (r={r1:.3f})",
        line=dict(color="blue", width=2),
        marker=dict(size=8, symbol="circle", color="blue"),
    )
)

# Trazo Escenario 2 (Cuadrante Inferior)
fig.add_trace(
    go.Scatter(
        x=t_puntos,
        y=y2,
        mode="lines+markers",
        name=f"Escenario 2 (r={r2:.3f})",
        line=dict(color="darkblue", width=2),
        marker=dict(size=8, symbol="circle", color="royalblue"),
    )
)

# Estilizado para simular la rejilla exacta de GeoGebra
fig.update_xaxes(
    range=[-2, t_max],
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor="black",
    showgrid=True,
    gridwidth=1,
    gridcolor="lightgray",
    dtick=10,
)

fig.update_yaxes(
    range=[-25, 45],
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor="black",
    showgrid=True,
    gridwidth=1,
    gridcolor="lightgray",
    dtick=10,
)

fig.update_layout(
    template="plotly_white",
    height=650,
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis_title="Tiempo (t)",
    yaxis_title="Magnitud / Crecimiento (dN/dt)",
)

st.plotly_chart(fig, use_container_width=True)
