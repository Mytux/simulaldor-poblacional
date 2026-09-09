import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Simulador Ecológico", layout="wide")
st.title("📊 Simulador Interactivo de Crecimiento Poblacional")

st.markdown("""
Ajusta los parámetros para observar cómo responde la tasa intrínseca de crecimiento $r$ 
y la trayectoria de la población según la fórmula:  
$$r = \\frac{\\ln(R_0)}{T}$$

* **$R_0 > 1.0 \\implies r > 0$**: Crecimiento poblacional.
* **$R_0 = 1.0 \\implies r = 0$**: Población estable (reemplazo exacto).
* **$R_0 < 1.0 \\implies r < 0$**: Declive/Extinción poblacional.
""")

col_control1, col_control2 = st.columns(2)

with col_control1:
    st.subheader("🔴 Escenario 1 (Base)")
    # Permitimos valores de R0 desde 0.01 para generar r negativas
    R0_1 = st.slider(
        "R0 - Tasa Neta de Reproducción", 0.01, 50.0, 31.2, step=0.01, key="r1"
    )
    T_1 = st.slider(
        "T - Tiempo Generacional", 0.1, 20.0, 8.96, step=0.01, key="t1"
    )
    r1 = np.log(R0_1) / T_1
    st.metric("Tasa intrínseca (r1)", f"{r1:.4f}")

with col_control2:
    st.subheader("🔵 Escenario 2 (Comparación)")
    R0_2 = st.slider(
        "R0 - Tasa Neta de Reproducción ",
        0.01,
        50.0,
        0.50,
        step=0.01,
        key="r2",
    )
    T_2 = st.slider(
        "T - Tiempo Generacional ", 0.1, 20.0, 4.5, step=0.01, key="t2"
    )
    r2 = np.log(R0_2) / T_2
    st.metric("Tasa intrínseca (r2)", f"{r2:.4f}")

# Parámetros generales en el panel lateral
N0 = st.sidebar.number_input(
    "Población inicial de hembras (N0)", value=100, min_value=1
)
t_max = st.sidebar.slider("Horizonte de tiempo (t)", 5, 100, 30)

# Cálculos de proyección
t = np.linspace(0, t_max, 300)
N1 = N0 * np.exp(r1 * t)
N2 = N0 * np.exp(r2 * t)

# Gráfico interactivo con Plotly
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=t,
        y=N1,
        mode="lines",
        name=f"Escenario 1 (r={r1:.3f})",
        line=dict(color="red", width=3),
    )
)

fig.add_trace(
    go.Scatter(
        x=t,
        y=N2,
        mode="lines",
        name=f"Escenario 2 (r={r2:.3f})",
        line=dict(color="blue", width=3, dash="dash"),
    )
)

# Línea de referencia si la población se extingue o colapsa a 0
fig.add_hline(
    y=0, line_dash="dot", line_color="gray", annotation_text="Límite de Extinción (N=0)"
)

fig.update_layout(
    xaxis_title="Tiempo (t)",
    yaxis_title="Número de Hembras N(t)",
    template="plotly_white",
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)
