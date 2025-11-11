import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Ya no necesitamos KMeans o StandardScaler aquí, 
# ¡porque el modelo ya hizo su trabajo!

# --- 1. Título de la App ---
st.set_page_config(layout="wide") # Hace que el dashboard ocupe toda la pantalla
st.title('Dashboard de Segmentación de Clientes (RFM)')

# --- 2. Cargar los Datos ---
# Usamos una función con cache para que Streamlit no recargue el CSV cada vez
@st.cache_data 
def load_data():
    df = pd.read_csv('dataset/rfm_data.csv')
    return df

# Cargamos los datos
df_rfm = load_data()

# --- 3. Mostrar los Datos ---
st.header('Datos de Clientes Segmentados (RFM)')
st.write(f"Los datos contienen {df_rfm.shape[0]} clientes, separados en 3 segmentos.")

# st.dataframe() es para mostrar una tabla interactiva
st.dataframe(df_rfm.head())
