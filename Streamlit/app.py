#---------------------------------------------------------------IMPORTACIÓN DE LIBRERÍAS-----------------------------------------------------------------------------
#Importamos las librerías que vamos a utilizar
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import datetime
import geopandas as gpd
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit.components.v1 as components
from PIL import Image
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
      
#Paleta de colores
#colores = ['#f07167', '#fed9b7', '#fdfcdc', '#00afb9', '#0081a7', '#13315c']
#https://coolors.co/palette/0081a7-00afb9-fdfcdc-fed9b7-f07167

#------------------------------------------------------------------LECTURA DE ARCHIVOS-----------------------------------------------------------------------------
#Leemos los documentos csv que vamos a utilizar para este análisis
cards = pd.read_csv("../Datasets/cards.txt", sep="|", decimal=',') 
weather = pd.read_csv("../Datasets/weather.csv", sep=";", decimal='.') 
dataframe_geojson = gpd.read_file("../Datasets/almeria_localizaciones.geojson")

#------------------------------------------------------------------PREPARACIÓN DE LOS DATOS-------------------------------------------------------------------------
#Conversión tipo de datos archivo CARDS
cards['CP_CLIENTE'] = cards['CP_CLIENTE'].astype(str) #Tipo categórico
cards['CP_COMERCIO'] = cards['CP_COMERCIO'].astype(str) #Tipo categórico
cards['SECTOR'] = cards['SECTOR'].astype(str) #Tipo categórico
cards['DIA'] = pd.to_datetime(cards['DIA'], format="%Y/%m/%d") #Tipo fecha
cards['FRANJA_HORARIA'] = cards['FRANJA_HORARIA'].astype(str) #Tipo categórico
cards['IMPORTE'] = cards['IMPORTE'].astype(float) #Tipo real
cards['NUM_OP'] = cards['NUM_OP'].astype(int) #Tipo entero

#Eliminación de columnas irrelevantes archivo WEATHER
weather = weather.drop(columns= 'TMax')
weather = weather.drop(columns= 'HTMax')
weather = weather.drop(columns= 'TMin')
weather = weather.drop(columns= 'HTMin')
weather = weather.drop(columns= 'HumMax')
weather = weather.drop(columns= 'HumMin')
weather = weather.drop(columns= 'HumMed')
weather = weather.drop(columns= 'VelViento')
weather = weather.drop(columns= 'DirViento')
weather = weather.drop(columns= 'Rad')
weather = weather.drop(columns= 'ETo')

#Conversión tipo de datos archivo WEATHER
weather['FECHA'] = pd.to_datetime(weather['FECHA'], format="%Y/%m/%d") #Tipo fecha
weather['DIA'] = weather['DIA'].astype(int) #Tipo entero
weather['TMed'] = weather['TMed'].astype(float) #Tipo real
weather['Precip'] = weather['Precip'].astype(float) #Tipo real

#Columna DIA a FECHA en el archivo CARDS
cards.columns = ['CP_CLIENTE', 'CP_COMERCIO', 'SECTOR', 'FECHA', 'FRANJA_HORARIA', 'IMPORTE', 'NUM_OP']

#Dataset final CARDS-WEATHER
dataset = cards.merge(weather, on="FECHA", how="inner")

#Archivo geojson
dataframe_geojson = dataframe_geojson.dissolve(by='COD_POSTAL').reset_index()
dataframe_geojson['COD_POSTAL'] = dataframe_geojson['COD_POSTAL'].astype(str) #Tipo categórico
dataframe_geojson['COD_POSTAL'] = dataframe_geojson['COD_POSTAL'].str[1:]

#-----------------------------------------------------------------------------PÁGINA WEB-------------------------------------------------------------------------
#Título de la página web
st.set_page_config(page_title="PBDII - Julieta Benítez", page_icon = Image.open('../Imagenes/icono.png'), layout='wide', initial_sidebar_state='expanded')

#Menú
with st.sidebar:
    selected = option_menu(
        menu_title="Manú principal",
        options = ["Análisis por sectores", "Influencia de la climatología", "Análisis por zonas", "Modelo de IA"],
        icons=["basket2-fill", "cloud-lightning-rain", "geo-fill", "robot"],
        menu_icon="list",
    )

#Secciones de la página web y su contenido
#---------------------------------------------------------------PRIMERA SECCIÓN: ANÁLISIS POR SECTORES---------------------------------------------------------------
if selected == "Análisis por sectores":
    
    st.title(f"Has seleccionado {selected}")

    st.markdown(
            """
            <style>
            .divider {
                width: 100%;
                height: 1px;
                background-color: white;
                border: none;
                border-top: 1px dashed white;
                margin: 20px 0;
            }
            </style>
            """
            , unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.title(f" ")
    
    #FILTROS
    #Posiciones de los filtros
    dia, franja_horaria = st.columns([5, 5])

    #Filtro de fecha
    with dia:
        initial_dia_choice, final_dia_choice = st.slider(
            "¿Qué rangos de días del 2015 te gustaría filtrar?",
            min_value=1, #Desde el 7 para que salgan todos los donuts dibujados de cada semana
            max_value=365,
            step=1,
            value=(1, 365),
        )

    #Ayuda para saber que fecha corresponde a cada día en el primer filtro
    #st.markdown(
        #"""
        #<p style="text-align: center;">
            #<small>* Puedes consultar la fecha a la que corresponde cada día del 2015 en el siguiente <a href="https://www.calendario-365.es/numeros-de-dias/2015.html"> enlace</a></small>
        #</p>
        #""",
        #unsafe_allow_html=True
    #)
    
    #Filtro de franja horaria
    with franja_horaria:
        franja_horaria_choice = st.selectbox(
            "¿Por qué franja horaria te gustaría filtrar?",
            ("Todas", '08-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24', '00-02', '02-04', '04-06', '06-08'),
        )
    
    #Elección del cliente: Todas las franjas horarias o una específica -> En el primer caso, filtramos por el rango de días seleccionado
    # y en el segundo caso por el rango de días y franja horaria seleccionados .> Actualización del dataset que se utilizará en los gráficos (filtered_dataset)
    if franja_horaria_choice == "Todas":
        filtered_dataset = dataset[(initial_dia_choice <= dataset['DIA']) & (dataset['DIA'] <= final_dia_choice)]
    if franja_horaria_choice != "Todas":
        filtered_dataset = dataset[(initial_dia_choice <= dataset['DIA']) & (dataset['DIA'] <= final_dia_choice)]
        filtered_dataset = filtered_dataset[filtered_dataset['FRANJA_HORARIA'] == franja_horaria_choice]

    #Fecha inicial seleccionada por el usuario, para poder imprimirla
    fecha_filtrada_inicial = filtered_dataset.loc[filtered_dataset['DIA'] == initial_dia_choice, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada_inicial = np.datetime_as_string(fecha_filtrada_inicial, unit='s')
    fecha_filtrada_inicial = datetime.datetime.strptime(fecha_filtrada_inicial, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada_inicial = fecha_filtrada_inicial.strftime("%Y-%m-%d")

    #Fecha final seleccionada por el usuario, para poder imprimirla
    fecha_filtrada_final = filtered_dataset.loc[filtered_dataset['DIA'] == final_dia_choice, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada_final = np.datetime_as_string(fecha_filtrada_final, unit='s')
    fecha_filtrada_final = datetime.datetime.strptime(fecha_filtrada_final, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada_final = fecha_filtrada_final.strftime("%Y-%m-%d")

    #Franja horaria elegida por el usuario
    franja_horaria_filtrada = franja_horaria_choice

    #Imprimimos la el rango de fechas según la elecciónde días por parte del usuario 
    st.markdown(
    f"<p style='text-align: center;'>Rango de fechas seleccionadas: <b><span style='color: #d45d5d;'>{fecha_filtrada_inicial} - {fecha_filtrada_final}</span></b> en la Franja Horaria: <b><span style='color: #d45d5d;'>{franja_horaria_filtrada}</span></b></p>",
    unsafe_allow_html=True
    )   
    st.markdown("---")


    #****************************************************************************GRÁFICOS 0 Y 0.2*********************************************************************
    #*******************************************************GRÁFICO 0: Vista temporal general de gastos por sector****************************************************
    #Agrupamos por Fecha y Sector y realizamos la suma de IMPORTE
    importe_fecha_sector = filtered_dataset[["FECHA","SECTOR","IMPORTE"]].groupby(["FECHA","SECTOR"]).sum().reset_index()

    # GRÁFICO 0: Utilizaremos librería plotly
    fig0 = px.line(importe_fecha_sector, x="FECHA", y="IMPORTE", color='SECTOR')

    fig0.update_layout(
        legend=dict(
            x=0,  # Leyenda empieza en la posición 1/4 del ancho total
            y=1.1,  # Colocar arriba (valor mayor a 1)
            orientation="h"  # Orientación horizontal
        )
        )
    
    #Creamos dos columnas para colocar los gráficos 0 y 0.2, en una proporción 2 y 0.7
    colGraf0, colGraf02 = st.columns([2, 0.7])

    #Pintamos Gráfico 0 en página web: Top 5 sectores con más gastos según el día de la semana
    with colGraf0:
        st.markdown("<h3 style='font-size: 23px; text-align: center; margin-left: 35%;'>Línea de tiempo de los gastos por sector en 2015</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig0, use_container_width=True)


    #-------------------------GRÁFICO 0.2 para visualizar mejor el ranking de sectores con mayores gastos---------------------------
    importe_por_sector = filtered_dataset[["SECTOR","IMPORTE"]].groupby(["SECTOR"]).sum().reset_index().sort_values('IMPORTE', ascending=True)
    
    fig02 = go.Figure(data=[go.Bar(x=importe_por_sector['IMPORTE'], y=importe_por_sector['SECTOR'],
                hovertext=importe_por_sector['IMPORTE'], orientation='h')])
    # Customize aspect
    fig02.update_traces(marker_color='rgba(246, 126, 126, 0.3)', marker_line_color='#FD6060',
                    marker_line_width=1.5, opacity=0.8)
    

    #Pintamos Gráfico 0.2 en página web: Ranking de sectores con mayores gastos
    with colGraf02:
        st.plotly_chart(fig02, use_container_width=True)

    #***************************************************************************GRÁFICOS 1 Y 1.2*******************************************************************
    #*******************************************************GRÁFICO 1: Sectores con más gastos según el día de la semana*******************************************
    #Asignamos los nombres de los días de la semana a los números correspondientes
    nombres_dias_semana = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }

    #Obtenemos número de día de la semana y los mapeamos en nueva columna nombres_dias_semana
    filtered_dataset['DIA_SEMANA'] = filtered_dataset['FECHA'].dt.dayofweek.map(nombres_dias_semana)

    #Calculamos suma de los importes por cada combinación de día de la semana y sector
    importe_por_sector = filtered_dataset.groupby(['DIA_SEMANA','SECTOR'])['IMPORTE'].sum().reset_index()

    #Hacemos un DataFrame por cada día de la semana 
    lunes = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Lunes'].sort_values(["IMPORTE"], ascending=False).head(5).copy()
    martes = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Martes'].sort_values(["IMPORTE"], ascending=False).head(5).copy()
    miercoles = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Miércoles'].sort_values(["IMPORTE"], ascending=False).head(5).copy()
    jueves = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Jueves'].sort_values(["IMPORTE"], ascending=False).head(5).copy()
    viernes = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Viernes'].sort_values(["IMPORTE"], ascending=False).head(5).copy()
    sabado = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Sábado'].sort_values(["IMPORTE"], ascending=False).head(5).copy()
    domingo = importe_por_sector[importe_por_sector['DIA_SEMANA'] == 'Domingo'].sort_values(["IMPORTE"], ascending=False).head(5).copy()

    # GRÁFICO 1: Utilizaremos librería plotly
    # Crear subparcelas
    fig1 = make_subplots(rows=1, cols=7, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, 
                                                {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

    fig1.add_trace(go.Pie(labels=lunes['SECTOR'], values=lunes['IMPORTE'], name="Lunes"), 1, 1)
    fig1.add_trace(go.Pie(labels=martes['SECTOR'], values=martes['IMPORTE'], name="Martes"),1, 2)
    fig1.add_trace(go.Pie(labels=miercoles['SECTOR'], values=miercoles['IMPORTE'], name="Miércoles"),1,3)
    fig1.add_trace(go.Pie(labels=jueves['SECTOR'], values=jueves['IMPORTE'], name="Jueves"),1,4)
    fig1.add_trace(go.Pie(labels=viernes['SECTOR'], values=viernes['IMPORTE'], name="Viernes"),1,5)
    fig1.add_trace(go.Pie(labels=sabado['SECTOR'], values=sabado['IMPORTE'], name="Sábado"),1,6)
    fig1.add_trace(go.Pie(labels=domingo['SECTOR'], values=domingo['IMPORTE'], name="Domingo"),1,7)

    #Crear un gráfico circular en forma de donut
    fig1.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig1.update_layout(
        legend=dict(
            x=0.25,  # Leyenda empieza en la posición 1/4 del ancho total
            y=1.1,  # Colocar arriba (valor mayor a 1)
            orientation="h"  # Orientación horizontal
        ),
        #Añadir anotaciones en el centro de los donuts
        annotations=[dict(text='Lunes', x=0.045, y=0.95, font_size=15, showarrow=False),
                    dict(text='Martes', x=0.19, y=0.95, font_size=15, showarrow=False),
                    dict(text='Miércoles', x=0.355, y=0.95, font_size=15, showarrow=False),
                    dict(text='Jueves', x=0.50, y=0.95, font_size=15, showarrow=False),
                    dict(text='Viernes', x=0.65, y=0.95, font_size=15, showarrow=False),
                    dict(text='Sábado', x=0.81, y=0.95, font_size=15, showarrow=False),
                    dict(text='Domingo', x=0.96, y=0.95, font_size=15, showarrow=False)])

    #-------------------------GRÁFICO 1.2 para visualizar mejor el gasto por sectores según día de la semana---------------------------
    #Generamos los días de la semana pero en versión numérica (La que ya viene por defecto en la función dayofweek)
    filtered_dataset['NUM_SEMANA'] = filtered_dataset['FECHA'].dt.dayofweek + 1

    #Agrupamos por Número de la semana y Sector y realizamos la suma de IMPORTE
    importe_numsemana_sector = filtered_dataset[["NUM_SEMANA","SECTOR","IMPORTE"]].groupby(["NUM_SEMANA","SECTOR"]).sum().reset_index()

    # GRÁFICO 1.2: Utilizaremos librería plotly
    fig12 = px.line(importe_numsemana_sector, x="NUM_SEMANA", y="IMPORTE", color='SECTOR')

    fig12.update_layout(
        legend=dict(
            x=0.05,  # Leyenda empieza en la posición 1/4 del ancho total
            y=1.1,  # Colocar arriba (valor mayor a 1)
            orientation="h"  # Orientación horizontal
        ))
    
    #Pintamos Gráfico 1 en página web: Top 5 sectores con más gastos según el día de la semana
    st.markdown("---")
    st.markdown("<h3 style='font-size: 23px; text-align: center;'>Top 5 sectores con más gastos según el día de la semana</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)

    #Pintamos Gráfico 1.2 en página web: Gastos por sector según el día de la semana
    st.plotly_chart(fig12, use_container_width=True)
    st.markdown("---")

    #************************************************GRÁFICO 2: Sectores con más gastos según sea día laboral o fin de semana********************************************
    # Definimos una lista denominada dias_laborables, que contiene los números de los días que no son fines de semana
    dias_laborables = [0, 1, 2, 3, 4]

    #Creamos nueva columna con el día de la semana a la que corresponde cada fecha
    filtered_dataset['DIA_SEMANA_NUMERO'] = filtered_dataset['FECHA'].dt.dayofweek

    #Creamos nueva columna basada en los valores de la anterior columna, comprobando si es día laboral o fin de semana
    filtered_dataset['TIPO_DIA'] = filtered_dataset['DIA_SEMANA_NUMERO'].apply(lambda x: 'Laboral' if x in dias_laborables else 'Fin de semana')

    #Eliminamos la columna DIA_SEMANA_NUMERO al ser irrelevante
    filtered_dataset = filtered_dataset.drop(columns= 'DIA_SEMANA_NUMERO')

    #Filtramos dataset por días laborables y fines de semana, creando dos nuevos dataframes
    Laboral = filtered_dataset[filtered_dataset['TIPO_DIA'] == 'Laboral']
    Fin_de_semana = filtered_dataset[filtered_dataset['TIPO_DIA'] == 'Fin de semana']

    #Agrupamos datos por sector, calculando la suma de los importes, en ambos dataframes nuevos 
    gasto_dias_laborables = Laboral.groupby('SECTOR')['IMPORTE'].sum().reset_index()
    gasto_dias_laborables = pd.DataFrame(gasto_dias_laborables)
    gasto_dias_laborables["TIPO_DIA"] = "Laboral"

    gasto_fines_semana = Fin_de_semana.groupby('SECTOR')['IMPORTE'].sum().reset_index()
    gasto_fines_semana = pd.DataFrame(gasto_fines_semana)
    gasto_fines_semana["TIPO_DIA"] = "Fin de semana"

    #Unimos ambos dataframes en uno solo
    gasto_laborables_fines_semana = pd.concat([gasto_dias_laborables, gasto_fines_semana], axis=0)

    #GRÁFICO 2: Utilizaremos librería plotly
    colores = ['#FF6262', '#68D263']
    fig2 = px.sunburst(gasto_laborables_fines_semana, path=['TIPO_DIA', 'SECTOR'], values='IMPORTE', color_discrete_sequence=colores)
    fig2.update_layout(
        width=800,  # Ancho del gráfico en píxeles
        height=600  # Altura del gráfico en píxeles
    )
    fig2.update_traces(textfont_color='white')

    #Pintamos Gráfico 2 en página web: Sectores con más gastos según sea día laboral o fin de semana
    st.markdown("<h3 style='font-size: 23px; text-align: center;'>Sectores con más gastos según sea día laboral o fin de semana</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)

    #************FOOTER PRIMERA SECCIÓN*************
    st.markdown(
    """
    <style>
    .divider {
        width: 100%;
        height: 1px;
        background-color: white;
        border: none;
        border-top: 1px dashed white;
        margin: 20px 0;
    }
    </style>
    """
    , unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1Footer, col2Footer, col3Footer, col4Footer, col5Footer = st.columns(5)

    with col3Footer:
        st.title(f" ")
        st.image("../Imagenes/logo_footer.png", width=270)

#---------------------------------------------------------------SEGUNDA SECCIÓN: INFLUENCIA DE LA CLIMATOLOGÍA-----------------------------------------------------------
if selected == "Influencia de la climatología":
    st.title(f"Has seleccionado {selected}")

    st.markdown(
            """
            <style>
            .divider {
                width: 100%;
                height: 1px;
                background-color: white;
                border: none;
                border-top: 1px dashed white;
                margin: 20px 0;
            }
            </style>
            """
            , unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.title(f" ")

    #**************************************************************************GRÁFICOS 3 Y 4***************************************************************************
    #-------FILTRO DE FECHA PARA EL GRÁFICO 3 Y 4------
    initial_dia_choice1, final_dia_choice1 = st.slider(
        "¿Qué rangos de días del 2015 te gustaría filtrar?",
        min_value=1, #Desde el 7 para que salgan todos los donuts dibujados de cada semana
        max_value=365,
        step=1,
        value=(1, 365),
    )

    #Elección del cliente: Rango de días seleccionados -> Actualización del dataset que se utilizará en los gráficos (filtered_dataset)
    filtered_dataset = dataset[(initial_dia_choice1 <= dataset['DIA']) & (dataset['DIA'] <= final_dia_choice1)]

    #Fecha inicial seleccionada por el usuario, para poder imprimirla
    fecha_filtrada_inicial1 = filtered_dataset.loc[filtered_dataset['DIA'] == initial_dia_choice1, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada_inicial1 = np.datetime_as_string(fecha_filtrada_inicial1, unit='s')
    fecha_filtrada_inicial1 = datetime.datetime.strptime(fecha_filtrada_inicial1, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada_inicial1 = fecha_filtrada_inicial1.strftime("%Y-%m-%d")

    #Fecha final seleccionada por el usuario, para poder imprimirla
    fecha_filtrada_final1 = filtered_dataset.loc[filtered_dataset['DIA'] == final_dia_choice1, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada_final1 = np.datetime_as_string(fecha_filtrada_final1, unit='s')
    fecha_filtrada_final1 = datetime.datetime.strptime(fecha_filtrada_final1, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada_final1 = fecha_filtrada_final1.strftime("%Y-%m-%d")

    #Imprimimos la el rango de fechas según la elecciónde días por parte del usuario 
    st.markdown(
    f"<p style='text-align: center;'>Rango de fechas seleccionadas: <b><span style='color: #d45d5d;'>{fecha_filtrada_inicial1} - {fecha_filtrada_final1}</span></b>",
    unsafe_allow_html=True
    )

    #Aviso de posibilidad de filtrar por rangos
    st.markdown(
        """
        <p style="text-align: center;">
            <small>Puedes filtrar por rangos, seleccionándolos o deseleccionándolos, en las leyendas correspondientes</small>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")   
    
    #Gráficos 3 y 4 irán colocados en 2 columnas 
    colGraf3, colGraf4 = st.columns([5, 5])

    #*********************************GRÁFICO 3: Influencia del número de precipitaciones en los gastos de los clientes*********************************
    #El gráfico 3 irá en la primera columna
    with colGraf3:
        #Dividimos el número de precipitaciones por 5 rangos
        precip_min = filtered_dataset['Precip'].min()
        precip_max = filtered_dataset['Precip'].max()
        num_rangos_precip = 5

        rangos_precipitaciones = np.linspace(precip_min,
                                        precip_max, 
                                        num_rangos_precip+1)

        #Aplicamos los rangos
        filtered_dataset['Rango_Precip'] = pd.cut(filtered_dataset['Precip'], bins=rangos_precipitaciones, duplicates='drop', include_lowest=True)

        #Calculamos la suma de IMPORTE por cada combinación de Rango_Precip y SECTOR
        importe_por_precip = filtered_dataset.groupby(['Rango_Precip','SECTOR'])['IMPORTE'].sum().reset_index()

        #GRÁFICO 3: Utilizaremos librería plotly
        #Creamos radar chart
        radar_chart_Precip = pd.DataFrame({
            'r':importe_por_precip['IMPORTE'],
            'theta': importe_por_precip['SECTOR'],
            'color': importe_por_precip['Rango_Precip']
        })

        fig3 = px.line_polar(radar_chart_Precip, r='r', theta='theta', line_close=True , color='color')

        fig3.update_layout(
            polar=dict(bgcolor='rgba(0, 0, 0, 0)'),  # Establecer el fondo transparente
            legend_title_text='Rango de precipitaciones existentes', #Nombre de la leyenda
            width=800,  # Ancho del gráfico en píxeles
            height=470  # Altura del gráfico en píxeles
        )

        fig3.update_polars(
        radialaxis=dict(
            linecolor='rgba(255, 255, 255, 0.3)',  # Establecer el color de la línea del eje radial en blanco
            gridcolor='rgba(255, 255, 255, 0.3)'  # Establecer el color de la cuadrícula del eje radial en blanco
        ),
        angularaxis=dict(
            linecolor='rgba(255, 255, 255, 0.3)',  # Establecer el color de la línea del eje angular en blanco
        )
        )
            
        fig3.update_traces(fill='toself')
 
        #Imprimimos gráfico 3
        st.markdown("<h3 style='font-size: 18px; text-align: center;'>Influencia del número de precipitaciones en los gastos de los clientes</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)

    #*********************************GRÁFICO 4: Influencia de la temperatura en los gastos de los clientes*********************************
    #El gráfico 4 irá en la segunda columna
    with colGraf4:
        #Dividimos las temperaturas por 5 rangos
        TMed_min = filtered_dataset['TMed'].min()
        TMed_max = filtered_dataset['TMed'].max()
        num_rangos_TMed = 5

        rangos_TMed = np.linspace(TMed_min,
                                        TMed_max, 
                                        num_rangos_TMed+1)

        #Aplicamos los rangos
        filtered_dataset['Rango_TMed'] = pd.cut(filtered_dataset['TMed'], bins=rangos_TMed, duplicates='drop', include_lowest=True)

        #Calculamos la suma de IMPORTE por cada combinación de Rango_TMed y SECTOR
        importe_por_TMed = filtered_dataset.groupby(['Rango_TMed','SECTOR'])['IMPORTE'].sum().reset_index()

        #GRÁFICO 4: Utilizaremos librería plotly
        #Creamos radar chart
        radar_chart_TMed = pd.DataFrame({
            'r':importe_por_TMed['IMPORTE'],
            'theta': importe_por_TMed['SECTOR'],
            'color': importe_por_TMed['Rango_TMed']
        })

        fig4 = px.line_polar(radar_chart_TMed, r='r', theta='theta', line_close=True , color='color')

        fig4.update_layout(
            polar=dict(bgcolor='rgba(0, 0, 0, 0)'),  # Establecer el fondo transparente
            legend_title_text='Rango de temperaturas existentes', #Nombre de la leyenda
            width=800,  # Ancho del gráfico en píxeles
            height=470  # Altura del gráfico en píxeles
        )

        fig4.update_polars(
        radialaxis=dict(
            linecolor='rgba(255, 255, 255, 0.3)',  # Establecer el color de la línea del eje radial en blanco
            gridcolor='rgba(255, 255, 255, 0.3)'  # Establecer el color de la cuadrícula del eje radial en blanco
        ),
        angularaxis=dict(
            linecolor='rgba(255, 255, 255, 0.3)',  # Establecer el color de la línea del eje angular en blanco
        )
        )
            
        fig4.update_traces(fill='toself')

        #Imprimimos gráfico 4
        st.markdown("<h3 style='font-size: 18px; text-align: center;'>Influencia del la temperatura en los gastos de los clientes</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)

    #************FOOTER SEGUNDA SECCIÓN*************
    st.markdown(
    """
    <style>
    .divider {
        width: 100%;
        height: 1px;
        background-color: white;
        border: none;
        border-top: 1px dashed white;
        margin: 20px 0;
    }
    </style>
    """
    , unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1Footer, col2Footer, col3Footer, col4Footer, col5Footer = st.columns(5)

    with col3Footer:
        st.title(f" ")
        st.image("../Imagenes/logo_footer.png", width=270)

#---------------------------------------------------------------TERCERA SECCIÓN: ANÁLISIS POR ZONAS-----------------------------------------------------------
if selected == "Análisis por zonas":
    st.title(f"Has seleccionado {selected}")

    st.markdown(
            """
            <style>
            .divider {
                width: 100%;
                height: 1px;
                background-color: white;
                border: none;
                border-top: 1px dashed white;
                margin: 20px 0;
            }
            </style>
            """
            , unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.title(f" ")

    #FILTROS
    #Posiciones de los filtros
    dia, franja_horaria = st.columns([5, 5])

    #Filtro de fecha
    with dia:
        initial_dia_choice, final_dia_choice = st.slider(
            "¿Qué rangos de días del 2015 te gustaría filtrar?",
            min_value=1, #Desde el 7 para que salgan todos los donuts dibujados de cada semana
            max_value=365,
            step=1,
            value=(1, 365),
        )
    
    #Filtro de franja horaria
    with franja_horaria:
        franja_horaria_choice = st.selectbox(
            "¿Por qué franja horaria te gustaría filtrar?",
            ("Todas", '08-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24', '00-02', '02-04', '04-06', '06-08'),
        )
    
    #Elección del cliente: Todas las franjas horarias o una específica -> En el primer caso, filtramos por el rango de días seleccionado
    # y en el segundo caso por el rango de días y franja horaria seleccionados .> Actualización del dataset que se utilizará en los gráficos (filtered_dataset)
    if franja_horaria_choice == "Todas":
        filtered_dataset = dataset[(initial_dia_choice <= dataset['DIA']) & (dataset['DIA'] <= final_dia_choice)]
    if franja_horaria_choice != "Todas":
        filtered_dataset = dataset[(initial_dia_choice <= dataset['DIA']) & (dataset['DIA'] <= final_dia_choice)]
        filtered_dataset = filtered_dataset[filtered_dataset['FRANJA_HORARIA'] == franja_horaria_choice]

    #Fecha inicial seleccionada por el usuario, para poder imprimirla
    fecha_filtrada_inicial = filtered_dataset.loc[filtered_dataset['DIA'] == initial_dia_choice, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada_inicial = np.datetime_as_string(fecha_filtrada_inicial, unit='s')
    fecha_filtrada_inicial = datetime.datetime.strptime(fecha_filtrada_inicial, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada_inicial = fecha_filtrada_inicial.strftime("%Y-%m-%d")

    #Fecha final seleccionada por el usuario, para poder imprimirla
    fecha_filtrada_final = filtered_dataset.loc[filtered_dataset['DIA'] == final_dia_choice, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada_final = np.datetime_as_string(fecha_filtrada_final, unit='s')
    fecha_filtrada_final = datetime.datetime.strptime(fecha_filtrada_final, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada_final = fecha_filtrada_final.strftime("%Y-%m-%d")

    #Franja horaria elegida por el usuario
    franja_horaria_filtrada = franja_horaria_choice

    #Imprimimos la el rango de fechas según la elecciónde días por parte del usuario 
    st.markdown(
    f"<p style='text-align: center;'>Rango de fechas seleccionadas: <b><span style='color: #d45d5d;'>{fecha_filtrada_inicial} - {fecha_filtrada_final}</span></b> en la Franja Horaria: <b><span style='color: #d45d5d;'>{franja_horaria_filtrada}</span></b></p>",
    unsafe_allow_html=True
    )   
    st.markdown("---")

    #Gráficos 5 y 6 irán colocados en 2 columnas 
    colGraf5, colGraf6 = st.columns([5, 5])

    #************************************************GRÁFICO 5: Códigos postales con más gastos por sectores*****************************************************
    #El gráfico 5 irá en la primera columna
    with colGraf5:
        #Agrupamos por CP_COMERCIO y SECTOR y calculamos la suma del importe
        gastos_por_sector_cpcomercio = filtered_dataset.groupby(['CP_COMERCIO', 'SECTOR'])['IMPORTE'].sum().reset_index()

        #Cogemos las filas que tengan mayor IMPORTE por SECTOR
        max_gastos = gastos_por_sector_cpcomercio.groupby('SECTOR')['IMPORTE'].idxmax()

        #Creamos un dataframe con los resultados, filtrando por los índices resultantes de la anterior consulta
        cpcomercio_max_gastos_sector = gastos_por_sector_cpcomercio.loc[max_gastos, ['SECTOR', 'CP_COMERCIO', 'IMPORTE']]

        #Creamos un Choropleth map usando Plotly
        fig5 = px.choropleth_mapbox(cpcomercio_max_gastos_sector, geojson=dataframe_geojson, color='SECTOR',
                                locations="CP_COMERCIO", featureidkey="properties.COD_POSTAL",
                                color_continuous_scale = 'viridis',
                                opacity = 0.5,
                                center={"lat": 36.841709, "lon": -2.456918},
                                mapbox_style="carto-positron", zoom=9)

        fig5.update_layout(
            height=600  # Altura del gráfico en píxeles
        )

        fig5.update_traces(visible="legendonly") #Deseleccionar todos los sectores

        fig5.data[0].visible=True   #Seleccionar solo el primero

        #Imprimimos gráfico 5
        st.markdown("<h3 style='font-size: 18px; text-align: center;'>Códigos postales con más gastos por sectores</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig5, use_container_width=True)

    #************************************************GRÁFICO 6: Códigos postales de las personas con más gastos*****************************************************
    #El gráfico 6 irá en la segunda columna
    with colGraf6:
        #Suma de los importes agrupados por los códigos postales de los clientes
        gastos_por_cpcliente = filtered_dataset.groupby('CP_CLIENTE')['IMPORTE'].sum().reset_index()

        #Creamos un Choropleth map usando Plotly
        fig6 = px.choropleth_mapbox(gastos_por_cpcliente, geojson=dataframe_geojson, color='IMPORTE',
                                locations="CP_CLIENTE", featureidkey="properties.COD_POSTAL",
                                center={"lat": 36.841709, "lon": -2.456918},
                                mapbox_style="carto-positron", zoom=9, color_continuous_scale="RdYlGn_r", opacity = 0.5)

        fig6.update_layout(
            height=600  # Altura del gráfico en píxeles
        )

        #Imprimimos gráfico 6
        st.markdown("<h3 style='font-size: 18px; text-align: center;'> Códigos postales de las personas con más gastos</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("---")

    #Gráficos 7 y 7.2 irán colocados en 2 columnas 
    colGraf7, colGraf7_2 = st.columns([7, 3])

    #************************************************GRÁFICO 7: Zonas con más compras de clientes que residen en otras**************************************************
    with colGraf7:
        #Filas de cards que cuentan con un CP_CLIENTE diferente a CP_COMERCIO, que resulta en ninguna
        cpcliente_desigual_cpcomercio = filtered_dataset[filtered_dataset['CP_CLIENTE'] != filtered_dataset['CP_COMERCIO']]

        #Suma del número de operaciones en cada combinación de CP_COMERCIO y CP_CLIENTE
        transacciones_por_zona = cpcliente_desigual_cpcomercio.groupby(['CP_COMERCIO', 'CP_CLIENTE'])['NUM_OP'].sum().reset_index(name='Transacciones')

        #Por cada código de comercio, realizamos la suma de las transacciones
        zonas_con_mas_transacciones = transacciones_por_zona.groupby('CP_COMERCIO')['Transacciones'].sum().reset_index()

        #Creamos un Choropleth map usando Plotly
        fig7 = px.choropleth_mapbox(zonas_con_mas_transacciones, geojson=dataframe_geojson, color='Transacciones',
                                locations="CP_COMERCIO", featureidkey="properties.COD_POSTAL",
                                center={"lat": 36.841709, "lon": -2.456918},
                                mapbox_style="carto-positron", zoom=9, color_continuous_scale="RdYlGn_r", opacity = 0.5)
        
        fig7.update_layout(
                height=550  # Altura del gráfico en píxeles
            )
        
        #Imprimimos gráfico 7
        st.markdown("<h3 style='font-size: 18px; text-align: center;'> Zonas con más compras de clientes que residen en otras</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig7, use_container_width=True)

    #-------------------------GRÁFICO 7.2 para visualizar mejor el ranking de sectores con mayores gastos---------------------------
    with colGraf7_2:
        #Guardamos el CP_COMERCIO con más operaciones de códigos postales diferentes al propio
        cp_comercio_mas_transacciones = zonas_con_mas_transacciones.sort_values('Transacciones', ascending=False).iloc[0]['CP_COMERCIO']

        #Calculamos el número de operaciones por sector en ese código de comercio concreto
        num_op_cp_comercio_max = cards[cards['CP_COMERCIO'] == cp_comercio_mas_transacciones].groupby('SECTOR')['NUM_OP'].sum().reset_index()

        num_op_cp_comercio_max = num_op_cp_comercio_max.sort_values('NUM_OP', ascending=True)
        
        fig7_2 = go.Figure(data=[go.Bar(x=num_op_cp_comercio_max['NUM_OP'], y=num_op_cp_comercio_max['SECTOR'],
                    hovertext=num_op_cp_comercio_max['NUM_OP'], orientation='h')])
        # Customize aspect
        fig7_2.update_traces(marker_color='rgba(246, 126, 126, 0.3)', marker_line_color='#FD6060',
                        marker_line_width=1.5, opacity=0.8)
        
        fig7_2.update_layout(
                height=500  # Altura del gráfico en píxeles
            )


        #Imprimimos gráfico 7
        st.markdown(f"<h3 style='font-size: 15px; text-align: center;'> Detalle de las proporciones de transacciones por cada sector, \nen la zona con mayores compras (CP: <b><span style='color: #d45d5d;'>{cp_comercio_mas_transacciones}</span></b>)</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig7_2, use_container_width=True)

    #************FOOTER TERCERA SECCIÓN*************
    st.markdown(
    """
    <style>
    .divider {
        width: 100%;
        height: 1px;
        background-color: white;
        border: none;
        border-top: 1px dashed white;
        margin: 20px 0;
    }
    </style>
    """
    , unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1Footer, col2Footer, col3Footer, col4Footer, col5Footer = st.columns(5)

    with col3Footer:
        st.title(f" ")
        st.image("../Imagenes/logo_footer.png", width=270)

#---------------------------------------------------------------CUARTA SECCIÓN: MODELO DE IA-----------------------------------------------------------
if selected == "Modelo de IA":
    st.title(f"Has seleccionado {selected}")

    st.markdown(
                """
                <style>
                .divider {
                    width: 100%;
                    height: 1px;
                    background-color: white;
                    border: none;
                    border-top: 1px dashed white;
                    margin: 20px 0;
                }
                </style>
                """
                , unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown(
    f"<p style='text-align: center;'>Nuestro modelo de IA te permite conocer el importe que tendría una transacción, según el día en el que se realiza, el número de operaciones que conlleva, el sector al que pertenece el comercio, y la temperatura media y cantidad de precipitaciones existentes.\n <b><span style='color: #d45d5d;'>¡Pruébalo!</span></b></p>",
    unsafe_allow_html=True
    ) 

    st.markdown(
            """
            <style>
            .divider {
                width: 100%;
                height: 1px;
                background-color: white;
                border: none;
                border-top: 1px dashed white;
                margin: 20px 0;
            }
            </style>
            """
            , unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.title(f" ")

    #FILTROS
    #Posiciones de los filtros
    dia, num_op, sector, TMed, Precip = st.columns([5, 5, 5, 5, 5])

    #Filtro de fecha
    with dia:
        dia_choice = st.slider(
            "¿En qué día del año se realiza la transacción?",
            min_value=1, 
            max_value=365,
            step=1,
            value=365,
        )

    #Filtro de número de operaciones
    with num_op:
        num_op_choice = st.slider(
            "¿Cuántas operaciones se realizan en la transacción?",
            min_value=1, 
            max_value=200,
            step=1,
            value=2,
        )

    #Filtro de sector
    with sector:
        sector_choice = st.selectbox(
            "Selecciona el sector al que pertenece la tienda",
            ("ALIMENTACIÓN", 'AUTO', 'BELLEZA', 'HOGAR', 'MODA Y COMPLEMENTOS', 'OCIO Y TIEMPO LIBRE', 'OTROS', 'RESTAURACIÓN', 'SALUD', 'TECNOLOGÍA'),
        )

    #Filtro de temperatura media
    with TMed:
        TMed_choice = st.slider(
            "¿Qué temperatura media hay el día de la transacción?",
            min_value=0, 
            max_value=40,
            step=1,
            value=15,
        )

    #Filtro de cantidad de precipitaciones
    with Precip:
        Precip_choice = st.slider(
            "¿Cuántas precipitaciones hay el día de la transacción?",
            min_value=0, 
            max_value=40,
            step=1,
            value=0,
        )

    #Elección del cliente
    #SECTOR
    if sector_choice == "ALIMENTACIÓN":
        num_sector_choice = 0
    if sector_choice == "AUTO":
        num_sector_choice = 1
    if sector_choice == "BELLEZA":
        num_sector_choice = 2
    if sector_choice == "HOGAR":
        num_sector_choice = 3
    if sector_choice == "MODA Y COMPLEMENTOS":
        num_sector_choice = 4
    if sector_choice == "OCIO Y TIEMPO LIBRE":
        num_sector_choice = 5
    if sector_choice == "OTROS":
        num_sector_choice = 6
    if sector_choice == "RESTAURACIÓN":
        num_sector_choice = 7
    if sector_choice == "SALUD":
        num_sector_choice = 8
    if sector_choice == "TECNOLOGÍA":
        num_sector_choice = 9

    #Fecha seleccionada por el usuario, para poder imprimirla
    fecha_filtrada = dataset.loc[dataset['DIA'] == dia_choice, 'FECHA'].values[0]
        #Convertimos a formato segundos y luego a datetime para asegurarnos de poder quitar los 0 que quedan al final
    fecha_filtrada = np.datetime_as_string(fecha_filtrada, unit='s')
    fecha_filtrada = datetime.datetime.strptime(fecha_filtrada, "%Y-%m-%dT%H:%M:%S")
        # Formatear la fecha sin ceros finales
    fecha_filtrada = fecha_filtrada.strftime("%Y-%m-%d")


    #Imprimimos la el rango de fechas según la elecciónde días por parte del usuario 
    st.markdown("---")
    st.markdown(
    f"<p style='text-align: center;'><b>CARACTERÍSTICAS SELECCIONADAS DE LA TRANSACCIÓN</b></p>",
    unsafe_allow_html=True
    )  
    st.markdown(
    f"<p style='text-align: center;'>Fecha seleccionada: <b><span style='color: #d45d5d;'>{fecha_filtrada}</span></b></p>",
    unsafe_allow_html=True
    )
    st.markdown(
    f"<p style='text-align: center;'>Número de operaciones seleccionadas: <b><span style='color: #d45d5d;'>{num_op_choice}</span></b></p>",
    unsafe_allow_html=True
    )
    st.markdown(
    f"<p style='text-align: center;'>Sector seleccionado: <b><span style='color: #d45d5d;'>{sector_choice}</span></b></p>",
    unsafe_allow_html=True
    )  
    st.markdown(
    f"<p style='text-align: center;'>Temperatura media seleccionada: <b><span style='color: #d45d5d;'>{TMed_choice}</span></b></p>",
    unsafe_allow_html=True
    )
    st.markdown(
    f"<p style='text-align: center;'>Cantidad de precipitaciones seleccionadas: <b><span style='color: #d45d5d;'>{Precip_choice}</span></b></p>",
    unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown(
    f"<p style='font-size: 20px; text-align: center;'><b>LA TRANSACCIÓN TENDRÁ UN IMPORTE DE...</b></p>",
    unsafe_allow_html=True
    )
    st.markdown(
    f"<p style='font-size: 14px; text-align: center;'><b>Esto puede llevar unos segundos...</b></p>",
    unsafe_allow_html=True
    )

    #MODELO DE IA
    # Crear un diccionario de mapeo de categorías a números, en este caso el SECTOR
    mapeo = {}
    for i, sector in enumerate(dataset['SECTOR'].unique()):
        mapeo[sector] = i

    # Aplicar la codificación de etiquetas a la columna SECTOR
    dataset['NUM_SECTOR'] = dataset['SECTOR'].map(mapeo)

    target_col = 'IMPORTE'

    #Variables de características
    X = dataset[['NUM_SECTOR', 'DIA', 'NUM_OP', 'TMed','Precip']]
    #Variable objetivo
    y = dataset[target_col]

    #Dividimos conjunto de datos en entrenamiento y test, con un proporción del 80% y 20% respectivamente.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

    # Primer DecisionTreeRegressor
    inner_tree = DecisionTreeRegressor(max_depth=10, min_samples_leaf=15, min_samples_split=12)
    inner_tree.fit(X_train, y_train)

    # Obtener las predicciones del primer DecisionTreeRegressor
    predictions_inner = inner_tree.predict(X_train)

    # Segundo DecisionTreeRegressor utilizando las predicciones del primero como entrada
    outer_tree = DecisionTreeRegressor(max_depth=7, min_samples_leaf=3, min_samples_split=4)
    outer_tree.fit(X_train, predictions_inner)

    # Hacer predicciones en el conjunto de prueba
    predictions_outer = outer_tree.predict(X_test)

    row = [[num_sector_choice, dia_choice, num_op_choice, TMed_choice, Precip_choice]]
    yhat = outer_tree.predict(row)
    prediccion = yhat[0]
    prediccion = round(prediccion, 2)

    st.markdown(
    f"<p style='font-size: 60px; text-align: center;'><b><span style='color: #d45d5d;'>{prediccion}€</span></b></p>",
    unsafe_allow_html=True
    )
  
    #************FOOTER CUARTA SECCIÓN*************
    st.markdown(
    """
    <style>
    .divider {
        width: 100%;
        height: 1px;
        background-color: white;
        border: none;
        border-top: 1px dashed white;
        margin: 20px 0;
    }
    </style>
    """
    , unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1Footer, col2Footer, col3Footer, col4Footer, col5Footer = st.columns(5)

    with col3Footer:
        st.title(f" ")
        st.image("../Imagenes/logo_footer.png", width=270)