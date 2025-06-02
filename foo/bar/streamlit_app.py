#Librerias
import streamlit as st
from kagglehub import load_dataset, KaggleDatasetAdapter
import plotly.express as px

df = load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "emmanuelleai/world-marathons-majors",
  "world_marathon_majors.csv",
pandas_kwargs={"encoding": "latin1"}
)

def main():
    st.title('World Marathons Majors 🏃')
    st.header('Dataset')
    st.text('El data set incluye los tiempos y los nombre y su pais de origen de todos los ganadores de los maratones mas importantes del mundo.')
    st.dataframe(df)


    top10atletas = (
        df['winner']
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'winner': 'atleta', 'count': 'victorias'})
    )
    st.subheader('Top 10 Atletas con más Victorias')
    st.bar_chart(top10atletas,x='atleta',y='victorias',x_label='Atletas', y_label='Nro. Victorias', color=['#FF5733'] )
    st.dataframe(top10atletas)

    fig = px.box(
        df.sort_values(by="time"),
        x="marathon",
        y="time",
        labels={
            'time':'Tiempo',
            'marathon': "Maratón"
        }
    )
    fig.update_traces(marker_color='rgba(0,123,255,0.5)',line_color='rgba(144, 12, 63,1)')
    st.subheader('Distribución de Tiempos por Maratón')
    st.plotly_chart(fig, use_container_width=True)

    masculino_df = df[df['gender'] == 'Male']
    femenino_df = df[df['gender'] == 'Female']
    men_time = []
    women_time = []
    for i in masculino_df['time']:
        (hr, _min, sec) = str(i).split(":")
        men_time.append((int(hr) * 3600) + (int(_min) * 60) + (int(sec)))
    for i in femenino_df['time']:
        (hr, _min, sec) = str(i).split(":")
        women_time.append((int(hr) * 3600) + (int(_min) * 60) + (int(sec)))

    masculino_df['Sec_time'] = men_time
    femenino_df['Sec_time'] = women_time

    fig_masculino = px.scatter(masculino_df, x='year', y='Sec_time', labels={'year':'Año','Sec_time':'Tiempo en segundos','country':'País'}, title="Masculino",
               color="country")
    fig_femenino = px.scatter(femenino_df, x='year', y='Sec_time', labels={'year':'Año','Sec_time':'Tiempo en segundos','country':'País'}, title="Femenino",
               color="country")

    st.subheader('Progresión de Récords: Tiempo vs Año')
    st.plotly_chart(fig_masculino,use_container_width=True)
    st.plotly_chart(fig_femenino,use_container_width=True)

main()