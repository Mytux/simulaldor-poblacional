
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Simulador Ecológico & Sensibilidad", layout="wide"
)
st.title("📊 Simulador Interactivo y Análisis de Sensibilidad Demográfica")

# Definición de pestañas principales
tab1, tab2, tab3 = st.tabs([
    "📈 Simulador de Cuadrantes",
    "🔬 Análisis de Sensibilidad y Elasticidad",
    "📚 Marco Teórico",
])

# ==========================================
# PESTAÑA 1: SIMULADOR INTERACTIVO
# ==========================================
with tab1:
    st.markdown("""
    ### Dinámica Poblacional en Plano Cartesiano
    Ajusta los parámetros para observar el comportamiento de $r$ y la velocidad de cambio $dN/dt$:
    $$r = \\frac{\\ln(|R_0|)}{T} \\cdot \\text{signo}(R_0)$$
    """)

    col_control1, col_control2 = st.columns(2)

    with col_control1:
        st.subheader("🔴 Escenario 1 (Base / Positivo)")
        R0_1 = st.slider(
            "R0 - Tasa Neta", -50.0, 50.0, 31.2, step=0.1, key="r1"
        )
        T_1 = st.slider(
            "T - Tiempo Generacional", 0.1, 20.0, 8.96, step=0.01, key="t1"
        )
        r1 = (np.log(abs(R0_1)) / T_1) if R0_1 != 0 else 0
        if R0_1 < 0:
            r1 = -r1
        st.metric("Tasa intrínseca (r1)", f"{r1:.4f}")

    with col_control2:
        st.subheader("🔵 Escenario 2 (Control / Negativo)")
        R0_2 = st.slider(
            "R0 - Tasa Neta ", -50.0, 50.0, -20.0, step=0.1, key="r2"
        )
        T_2 = st.slider(
            "T - Tiempo Generacional ", 0.1, 20.0, 4.5, step=0.01, key="t2"
        )
        r2 = (np.log(abs(R0_2)) / T_2) if R0_2 != 0 else 0
        if R0_2 < 0:
            r2 = -r2
        st.metric("Tasa intrínseca (r2)", f"{r2:.4f}")

    N0 = st.sidebar.number_input(
        "Población inicial (N0)", value=10, min_value=1
    )
    t_max = st.sidebar.slider("Rango Tiempo (Eje X)", 10, 100, 60)

    t_puntos = np.linspace(0, t_max, 30)

    if r1 >= 0:
        y1 = N0 * np.exp(r1 * (t_puntos / 10)) - N0
    else:
        y1 = -(N0 * np.exp(abs(r1) * (t_puntos / 10)) - N0)

    if r2 >= 0:
        y2 = N0 * np.exp(r2 * (t_puntos / 10)) - N0
    else:
        y2 = -(N0 * np.exp(abs(r2) * (t_puntos / 10)) - N0)

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=t_puntos,
            y=y1,
            mode="lines+markers",
            name=f"Escenario 1 (r={r1:.3f})",
            line=dict(color="red", width=2.5),
            marker=dict(size=8, symbol="circle", color="crimson"),
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=t_puntos,
            y=y2,
            mode="lines+markers",
            name=f"Escenario 2 (r={r2:.3f})",
            line=dict(color="blue", width=2.5, dash="dash"),
            marker=dict(size=8, symbol="circle", color="royalblue"),
        )
    )

    fig1.update_xaxes(
        range=[0, t_max],
        autorange=False,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        showgrid=True,
        gridwidth=1,
        gridcolor="lightgray",
        dtick=10,
    )

    fig1.update_yaxes(
        autorange=True,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        showgrid=True,
        gridwidth=1,
        gridcolor="lightgray",
    )

    fig1.update_layout(
        template="plotly_white",
        height=600,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title="Tiempo (t)",
        yaxis_title="Magnitud / Crecimiento (dN/dt)",
    )

    st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# PESTAÑA 2: ANÁLISIS DE SENSIBILIDAD Y ELASTICIDAD (CÓDIGO R EN PLOTLY)
# ==========================================
with tab2:
    st.header(
        "🔬 Análisis de Sensibilidad y Elasticidad de la Tasa Intrínseca"
    )

    col_r1, col_r2 = st.columns(2)

    # 1. Gráfica r vs R (Acotada a R < 50)
    with col_r1:
        st.subheader("1. r vs R (Acotado a R < 50)")
        R_vals = np.linspace(1.01, 50, 500)
        T_levels = [1, 2, 5, 10, 20, 50]

        fig_r_R = go.Figure()

        for T_val in T_levels:
            r_vals = np.log(R_vals) / T_val
            fig_r_R.add_trace(
                go.Scatter(
                    x=R_vals, y=r_vals, mode="lines", name=f"T = {T_val}"
                )
            )

        # Línea vertical e = 2.718
        fig_r_R.add_vline(
            x=np.e,
            line_dash="dash",
            line_color="green",
            annotation_text="R = e (e_R = 1)",
        )
        fig_r_R.add_vline(x=50, line_dash="dot", line_color="red")

        fig_r_R.update_layout(
            xaxis_title="Tasa Neta de Reproducción (R)",
            yaxis_title="Tasa Intrínseca de Crecimiento (r)",
            template="plotly_white",
            height=400,
        )
        st.plotly_chart(fig_r_R, use_container_width=True)

    # 2. Gráfica de Caída de Elasticidad
    with col_r2:
        st.subheader("2. Caída de la Elasticidad de R")
        elasticidad_R = 1 / np.log(R_vals)

        fig_ela = go.Figure()
        fig_ela.add_trace(
            go.Scatter(
                x=R_vals,
                y=elasticidad_R,
                mode="lines",
                name="Elasticidad ε_R",
                line=dict(color="purple", width=2.5),
            )
        )

        fig_ela.add_hline(
            y=1,
            line_dash="dash",
            line_color="black",
            annotation_text="Umbral Inelástico (ε = 1)",
        )
        fig_ela.add_vline(
            x=np.e,
            line_dash="dash",
            line_color="green",
            annotation_text="R = e",
        )

        fig_ela.update_layout(
            xaxis_title="Tasa Neta de Reproducción (R)",
            yaxis_title="Elasticidad de R (ε_R = 1 / ln R)",
            yaxis_range=[0, 3],
            template="plotly_white",
            height=400,
        )
        st.plotly_chart(fig_ela, use_container_width=True)

    st.markdown("---")

    col_sens3, col_sens4 = st.columns(2)

    # 3. Mapa de calor: Razón de Sensibilidades
    with col_sens3:
        st.subheader("3. Razón de Sensibilidades (S_T / S_R)")
        R_grid = np.linspace(1.1, 200, 150)
        T_grid = np.linspace(1, 250, 150)
        R_mesh, T_mesh = np.meshgrid(R_grid, T_grid)

        ratio_mesh = (R_mesh * np.log(R_mesh)) / T_mesh

        fig_heat = go.Figure(
            data=go.Heatmap(
                z=ratio_mesh,
                x=R_grid,
                y=T_grid,
                colorscale="Viridis",
                colorbar=dict(title="S_T / S_R"),
            )
        )

        R_line = np.linspace(1.1, 60, 100)
        T_line = R_line * np.log(R_line)
        fig_heat.add_trace(
            go.Scatter(
                x=R_line,
                y=T_line,
                mode="lines",
                name="R ln(R) = T",
                line=dict(color="red", dash="dash", width=2),
            )
        )

        fig_heat.update_layout(
            xaxis_title="R0",
            yaxis_title="T",
            template="plotly_white",
            height=400,
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # 4. Superficie 3D
    with col_sens4:
        st.subheader("4. Superficie 3D: r = ln(R) / T")
        R_3d = np.linspace(1, 1600, 80)
        T_3d = np.linspace(10, 250, 80)
        R_m3d, T_m3d = np.meshgrid(R_3d, T_3d)
        r_3d = np.log(R_m3d) / T_m3d

        fig_3d = go.Figure(
            data=[
                go.Surface(z=r_3d, x=R_m3d, y=T_m3d, colorscale="Viridis")
            ]
        )
        fig_3d.update_layout(
            scene=dict(
                xaxis_title="R0",
                yaxis_title="T",
                zaxis_title="r",
                aspectratio=dict(x=1, y=1, z=0.7),
            ),
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_3d, use_container_width=True)

# ==========================================
# PESTAÑA 3: MARCO TEÓRICO
# ==========================================
with tab3:
    st.header("📚 Justificación Matemática y Biológica")
    st.markdown("""
    ### 1. Definición de Elasticidad
    La elasticidad mide el cambio porcentual en la tasa $r$ producido por un cambio del $1\\%$ en los parámetros:
    * **Elasticidad de $T$:** $\\epsilon_T = -1$ (Siempre elástica, impacto proporcional directo de $1:1$).
    * **Elasticidad de $R$:** $\\epsilon_R = \\frac{1}{\\ln R}$ (Cae por debajo de $1$ en cuanto $R > e \\approx 2.718$).

    ### 2. Conclusión Demográfica
    Para cualquier especie con $R > 2.718$ (la inmensa mayoría de los insectos y plagas), **el parámetro $R$ es inelástico**. Un esfuerzo enfocado en prolongar el tiempo generacional $T$ o aumentar la mortalidad pre-reproductiva es matemáticamente superior a intentar reducir la camada de huevos.
    """)
