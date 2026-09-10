import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Simulador Ecológico", layout="wide")
st.title("📊 Simulador Interactivo de Crecimiento Poblacional")

st.markdown("""
Ajusta los parámetros para observar la respuesta de la tasa intrínseca $r$ y la dinámica poblacional:
$$r = \\frac{\\ln(R_0)}{T}$$

* **$R_0 > 1.0 \\implies r > 0$**: Crecimiento positivo.
* **$R_0 = 1.0 \\implies r = 0$**: Población estable.
* **$R_0 < 1.0 \\implies r < 0$**: Tasa de cambio negativa (declive/extinción).
""")

# Menú lateral para elegir qué graficar
tipo_grafico = st.sidebar.radio(
    "Selecciona la variable del Eje Y:",
    ("Número de Hembras N(t)", "Tasa de Cambio dN/dt (Permite Cuadrante Negativo)")
)

col_control1, col_control2 = st.columns(2)

with col_control1:
    st.subheader("🔴 Escenario 1 (Base)")
    # Se reduce el límite inferior a 0.0001 para permitir valores de r altamente negativos
    R0_1 = st.slider("R0 - Tasa Neta de Reproducción", 0.0001, 50.0, 31.2, step=0.01, key="r1")
    T_1 = st.slider("T - Tiempo Generacional", 0.1, 20.0, 8.96, step=0.01, key="t1")
    r1 = np.log(R0_1) / T_1
    st.metric("Tasa intrínseca (r1)", f"{r1:.4f}")

with col_control2:
    st.subheader("🔵 Escenario 2 (Comparación)")
    R0_2 = st.slider("R0 - Tasa Neta de Reproducción ", 0.0001, 50.0, 0.05, step=0.01, key="r2")
    T_2 = st.slider("T - Tiempo Generacional ", 0.1, 20.0, 4.5, step=0.01, key="t2")
    r2 = np.log(R0_2) / T_2
    st.metric("Tasa intrínseca (r2)", f"{r2:.4f}")

# Parámetros generales
N0 = st.sidebar.number_input("Población inicial de hembras (N0)", value=100, min_value=1)
t_max = st.sidebar.slider("Horizonte de tiempo (t)", 5, 100, 30)

# Cálculos
t = np.linspace(0, t_max, 300)
N1 = N0 * np.exp(r1 * t)
N2 = N0 * np.exp(r2 * t)

# Cálculo de la velocidad de crecimiento (dN/dt = r * N)
dN_dt1 = r1 * N1
dN_dt2 = r2 * N2

fig = go.Figure()

if tipo_grafico == "Número de Hembras N(t)":
    y1, y2 = N1, N2
    titulo_y = "Número de Hembras N(t)"
else:
    y1, y2 = dN_dt1, dN_dt2
    titulo_y = "Tasa de Crecimiento (dN/dt) [Individuos / Tiempo]"

fig.add_trace(go.Scatter(x=t, y=y1, mode='lines', name=f'Escenario 1 (r={r1:.3f})', line=dict(color='red', width=3)))
fig.add_trace(go.Scatter(x=t, y=y2, mode='lines', name=f'Escenario 2 (r={r2:.3f})', line=dict(color='blue', width=3, dash='dash')))

# Eje horizontal cero visible
fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=1.5, annotation_text="Eje X (Límite Cero)")

fig.update_layout(
    xaxis_title="Tiempo (t)",
    yaxis_title=titulo_y,
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
