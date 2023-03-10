import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import cufflinks as cf
import time as time
import datetime
import chart_studio

cf.set_config_file(sharing='public',theme='white',offline=False)

# configuracion de la pagina del dash 

st.set_page_config (
    page_title = "Dasboard Test",
    page_icon = "📊",
    # Disposión del contenido 
    layout = "wide",
    initial_sidebar_state = "expanded", 
    menu_items={'about':'Extramilla Carlos'}
    

)

with st.sidebar:
       st.title ("Dashboard Extramilla Carlos")
       st.write ("Dashboard python")
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
##chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    ##chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

with st.spinner('Wait for it...'):
    time.sleep(5)
    st.success('Done!')


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.

data = pd.read_csv('./data_performance_alk.csv')
data = data.dropna()
data['CampaignId'] = data['CampaignId'].astype(str)
data['Date'] = pd.to_datetime(data['Date'], format = "%Y-%m-%d")
data = data.drop(columns = ['Engagements','VideoQuartile100Rate','VideoQuartile75Rate','VideoQuartile50Rate','VideoQuartile25Rate','VideoViews'])
data = data.drop(data[data['Device'] == 'Other'].index)
data['Objetivo'] = np.where(data['CampaignName'].str.contains('AWN'), 'Awareness', np.where(data['CampaignName'].str.contains('PEF'), 'Performance', 'Asignar'))

condiciones = [
    data['CampaignName'].str.contains('_TV_'), 
    data['CampaignName'].str.contains('_COMP_'),
    data['CampaignName'].str.contains('_LB_'),
    data['CampaignName'].str.contains('_PQ_'),
    data['CampaignName'].str.contains('_CEL_'),
    data['CampaignName'].str.contains('_HG_'),
    data['CampaignName'].str.contains('_AU_'),
    data['CampaignName'].str.contains('_LL_'),
    data['CampaignName'].str.contains('_VJ_'),
    data['CampaignName'].str.contains('_DEP_'),
    data['CampaignName'].str.contains('_MR_'),
    data['CampaignName'].str.contains('_CM_'),
    data['CampaignName'].str.contains('_ACC_'),
    data['CampaignName'].str.contains('_TCA_'),
    data['CampaignName'].str.contains('_INT_'),
    data['CampaignName'].str.contains('_TLP_')
]

valores = [
    'Televisores',
    'Computadores',
    'Grandes',
    'Pequeños',
    'Celulares',
    'Hogar',
    'Audio',
    'Llantas',
    'Videojuegos',
    'Deportes',
    'Mercado',
    'Cámaras',
    'Accesorios',
    'TCA',
    'Intangibles',
    'Todos los productos'
]

data['Categoría'] = np.select(condiciones, valores, default='Other')
##st.write(data)


with st.container():
     st.title(':blue[Dashboard Extramilla]')
     
with st.container():
     filtro_fecha, filtro_objetivo, filtro_categoria, filtro_dispositivo  = st.columns(4)

     with filtro_fecha:
        fecha_inicio, fecha_final = st.date_input('Fecha',[datetime.date(2023,2,1),datetime.date(2023,2,28)])
        if fecha_inicio < fecha_final:
            pass
        else:
            st.error('Error: End date must fall after start date.')
          

     with filtro_dispositivo:
          Dispositivos = data['Device'].unique()
          sub_container = st.container()
          todos_dispositivos = st.checkbox('Seleccionar todo', value=True)
          if todos_dispositivos : 
               Dispositivo_fil=sub_container.multiselect('Dispositivo',Dispositivos,Dispositivos)
          else : 
               Dispositivo_fil=sub_container.multiselect('Dispositivo',Dispositivos)

     with filtro_objetivo:
          Objetivos = data['Objetivo'].unique()
          sub_container_objetivo = st.container()
          todos_objetivos = st.checkbox('Incluir todo', value=False)
          if todos_objetivos :
               Objetivo_fil = sub_container_objetivo.multiselect('Objetivo', Objetivos, Objetivos)
          else :
               Objetivo_fil = sub_container_objetivo.multiselect('Objetivo', Objetivos)

     with filtro_categoria:
          Categorias = data['Categoría'].unique()
          sub_container_categoria = st.container()
          todas_categorias = st.checkbox('Todas las categorías', value=False)
          if todas_categorias :
               Categoria_fil = sub_container_categoria.multiselect('Categoría', Categorias, Categorias)
          else :
               Categoria_fil = sub_container_categoria.multiselect('Categoría', Categorias)

data_filtrada = data[(data['Date'] > fecha_inicio.strftime("%Y-%m-%d")) 
                     & (data['Date'] <= fecha_final.strftime("%Y-%m-%d")) 
                     & (data['Objetivo'].isin(Objetivo_fil))
                     & (data['Categoría'].isin(Categoria_fil)) 
                     & (data['Device'].isin(Dispositivo_fil))]


    

with st.container():
     tarjeta_inversion, tarjeta_impresiones, tarjeta_clicks, tarjeta_cpc = st.columns(4)

     with tarjeta_inversion:
          st.metric(label='Inversión', value=f"${data_filtrada['Cost'].sum():,.0f}")
          
     with tarjeta_impresiones:
          st.metric(label='Impresiones', value=f"${data_filtrada['Impressions'].sum():,.0f}") 
     with tarjeta_clicks:
          st.metric(label='Clicks', value=f"${data_filtrada['Clicks'].sum():,.0f}")
     with tarjeta_cpc:
          st.metric(label='CPC', value=f"${data_filtrada['Cost'].sum()/data_filtrada['Clicks'].sum():,.0f}")

with st.container():
     comp_inv, share_disp = st.columns(2)

     with comp_inv:
          data_inv = data_filtrada.pivot_table(index='Date', values='Cost', aggfunc='sum')
          grafica_1= data_inv.iplot(kind='line', xTitle='Fecha', yTitle='Inversión', title='Comportamiento diario de inversión' ,color = '#004796', width=4, asFigure=True)
          st.plotly_chart(grafica_1)

     with share_disp:
          grafica_2= data_filtrada.iplot(kind='pie', labels="Device", values="Cost", title='Share por dispositivo', hole=.4, asFigure=True)
          st.plotly_chart(grafica_2)

with st.container():
    barra_apilada, grafico_area = st.columns(2)

    with barra_apilada:
        data_impcl = data_filtrada.pivot_table(index='Device', values=['Impressions','Cost'] , aggfunc='sum') 
        grafica_3= data_impcl.iplot(kind='bar', barmode='stack', yTitle='Device', title='Costo e Impresiones por dispositivo', asFigure=True) 
        st.plotly_chart(grafica_3)

    with grafico_area:
          data_area = data_filtrada.pivot_table(index='Date', columns='Device', values='Impressions', aggfunc='sum') 
          grafica_4= data_area.iplot(
               keys= list(np.unique(data_filtrada['Device'].to_numpy())),
               subplots=True,
               fill=True,
               xTitle="Date", yTitle="Impressions", title="Impresiones diarias por dispositivo", asFigure=True)
          st.plotly_chart(grafica_4)

st.write(data_filtrada)

st.button("Re-run")