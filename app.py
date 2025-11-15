import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px # Usaremos Plotly para gráficos interactivos

# --- 1. Configuración de la Página y Carga de Datos ---
st.set_page_config(layout="wide") # Ocupa toda la pantalla
st.title('Dashboard de Segmentación de Clientes (RFM)')

@st.cache_data # Carga los datos una sola vez
def load_data():
    df = pd.read_csv('dataset/rfm_data.csv')
    # Asegurarnos de que cluster_id sea categórico para los gráficos
    df['cluster_id'] = df['cluster_id'].astype(str) 
    return df

df_rfm = load_data()

# --- 2. Perfil Promedio (La Tabla de Interpretación) ---
st.header('Perfiles Promedio de los Segmentos')
st.write("""
Aquí vemos los perfiles promedio de cada segmento. Esto nos permite 
definir a cada grupo basándonos en su comportamiento (R, F, M).
""")

# Calculamos la tabla de perfiles (la "hoja de respuestas")
cluster_profile = df_rfm.groupby('cluster_id')[['amount', 'frequency', 'recency']].mean().reset_index()

# Renombramos para claridad en el dashboard
cluster_profile = cluster_profile.rename(columns={
    'amount': 'Gasto Promedio (M)',
    'frequency': 'Frecuencia Promedio (F)',
    'recency': 'Recencia Promedia (R)'
})
st.dataframe(cluster_profile, use_container_width=True)

# --- 3. Justificación del Modelo (Elbow & Silhouette) ---
st.header('Justificación del Modelo: ¿Por qué K=3?')
st.write("""
Para decidir el número óptimo de clusters (K), usamos dos métodos estadísticos:
1.  **Método del Codo (Inercia):** Busca el "codo" donde la mejora del modelo se aplana (K=3).
2.  **Análisis de Silueta:** Busca el puntaje más alto de "separación" (K=3 tiene un puntaje casi perfecto de 0.60).
""")

# Mostramos la imagen que guardamos desde el notebook
st.image('justificacion_clusters.png', use_column_width=True)


# --- 4. Validación Visual (Boxplots) ---
st.header('Validación Visual de los Segmentos (Boxplots)')
st.write("Confirmamos visualmente que los grupos están bien separados en las tres métricas.")

col1, col2, col3 = st.columns(3)

with col1:
    fig_r = px.box(df_rfm, x='cluster_id', y='recency', title='Recencia (R) por Segmento', color='cluster_id')
    st.plotly_chart(fig_r, use_container_width=True)

with col2:
    fig_f = px.box(df_rfm, x='cluster_id', y='frequency', title='Frecuencia (F) por Segmento', color='cluster_id')
    st.plotly_chart(fig_f, use_container_width=True)

with col3:
    fig_m = px.box(df_rfm, x='cluster_id', y='amount', title='Gasto (M) por Segmento', color='cluster_id')
    st.plotly_chart(fig_m, use_container_width=True)


# --- 5. Exploración Avanzada (Pairplot) ---
st.header('Separación de Clusters (Pairplot)')
st.write("""
Este gráfico confirma que los 3 segmentos son poblaciones distintas. 
Nota cómo el grupo 'Superiores' (1) se separa claramente en Gasto y Frecuencia, 
mientras que 'Riesgo' (2) se separa por su alta Recencia.
""")

# Mostramos la imagen del Pairplot que guardamos
st.image('pairplot_segmentos.png', use_container_width=True)

# --- 6. Explorar los Datos Crudos ---
st.header('Explorar Datos de Clientes')
st.write("Datos finales de RFM con el segmento asignado.")
st.dataframe(df_rfm, use_container_width=True)