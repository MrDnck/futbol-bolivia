import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch

# Cargar el dataset
data = pd.read_csv('soccer-players3.0.1.csv')
data_cleaned = data.drop(columns=['Unnamed: 0'])
data_cleaned = data_cleaned.dropna(subset=['age', 'number', 'date born'])

st.markdown("""
### Fuente de Datos
Los datos se obtuvieron de la plataforma Kaggle: [Jugadores del Fútbol Boliviano](https://www.kaggle.com/datasets/gersontorrez/jugadores-del-futbol-boliviano)

### Código Fuente
Puedes ver y modificar el código en el siguiente repositorio de GitHub: [Repositorio de GitHub](https://github.com/MrDnck/futbol-bolivia)

### Autor
Cristian Catari
            
Celular: +591 70562921  
Correo electrónico: cristian.catari.ma@gmail.com
""")

# Configuración de Streamlit
st.title('Análisis de Jugadores de Fútbol')

# Segmentadores
selected_nationality = st.selectbox('Selecciona la Nacionalidad', options=['Todos'] + list(data_cleaned['nationality'].unique()))
selected_club = st.selectbox('Selecciona el Club', options=['Todos'] + list(data_cleaned['club'].unique()))
selected_position = st.selectbox('Selecciona la Posición', options=['Todos'] + list(data_cleaned['pos'].unique()))

# Filtrar los datos según los segmentadores
filtered_data = data_cleaned
if selected_nationality != 'Todos':
    filtered_data = filtered_data[filtered_data['nationality'] == selected_nationality]
if selected_club != 'Todos':
    filtered_data = filtered_data[filtered_data['club'] == selected_club]
if selected_position != 'Todos':
    filtered_data = filtered_data[filtered_data['pos'] == selected_position]

# Calcular distribuciones y estadísticas
nationality_distribution = filtered_data['nationality'].value_counts()
club_distribution = filtered_data['club'].value_counts()
position_distribution = filtered_data['pos'].value_counts()

# Gráfico de posiciones con mplsoccer
st.header('Distribución de Posiciones en el Campo')
pitch = Pitch(pitch_type='statsbomb', pitch_color='#aabb97', line_color='white', stripe=True)
fig, ax = pitch.draw(figsize=(10, 6))

positions = {
    'Portero': (5, 30),
    'Defensa': (20, 40),
    'Centrocampista': (50, 50),
    'Delantero': (80, 40)
}

for pos, count in position_distribution.items():
    if pos in positions:
        x, y = positions[pos]
        pitch.scatter(x, y, s=count*10, ax=ax, label=f'{pos} ({count})', alpha=0.6)

ax.legend()
st.pyplot(fig)

# Distribución de Nacionalidades
st.header('Distribución de Nacionalidades')
st.bar_chart(nationality_distribution)

# Distribución de Clubes
st.header('Distribución de Clubes')
st.bar_chart(club_distribution)

# Gráficos de dispersión
st.header('Relación entre Edad, Altura y Peso')
fig, ax = plt.subplots()
ax.scatter(filtered_data['age'], filtered_data['height'], alpha=0.5)
ax.set_title('Relación entre Edad y Altura')
ax.set_xlabel('Edad')
ax.set_ylabel('Altura (cm)')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.scatter(filtered_data['age'], filtered_data['weight'], alpha=0.5)
ax.set_title('Relación entre Edad y Peso')
ax.set_xlabel('Edad')
ax.set_ylabel('Peso (kg)')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.scatter(filtered_data['height'], filtered_data['weight'], alpha=0.5)
ax.set_title('Relación entre Altura y Peso')
ax.set_xlabel('Altura (cm)')
ax.set_ylabel('Peso (kg)')
st.pyplot(fig)


