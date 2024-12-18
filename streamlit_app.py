import streamlit as st
import pandas as pd
from streamlit_timeline import st_timeline
from datetime import date, timedelta
import plotly.express as px

# Función para cargar el archivo Excel y validar las hojas
def load_excel(file):
    try:
        xls = pd.ExcelFile(file)
        required_sheets = ['customer_data', 'timeline', 'change_request', 'work_at_risk', 'csat']
        if all(sheet in xls.sheet_names for sheet in required_sheets):
            return xls
        else:
            st.error("El archivo Excel debe contener las hojas: customer_data, timeline, change_request, work_at_risk, csat.")
            return None
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {e}")
        return None

# Función para obtener los datos del cliente
def get_customer_data(xls):
    df = pd.read_excel(xls, sheet_name='customer_data')
    customer_info = df.iloc[0]  # Asumiendo que la primera fila contiene los datos requeridos
    return df, customer_info



# Función para obtener los datos de CSAT histórico
def get_csat_data(xls):
    df = pd.read_excel(xls, sheet_name='csat')
    return df

# Función para cargar el archivo de solicitudes de servicio y validar las columnas requeridas
def load_service_requests(file):
    try:
        df = pd.read_excel(file)
        required_columns = ['customer', 'date', 'template', 'status']
        if all(column in df.columns for column in required_columns):
            # Convertir la columna 'date' a tipo datetime con formato día/mes/año
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
            return df
        else:
            st.error("El archivo Excel debe contener las columnas: customer, date, template, status.")
            return None
    except Exception as e:
        st.error(f"Error al cargar el archivo de solicitudes de servicio: {e}")
        return None

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="SAP Customer Dashboard", layout="wide")

# Barra lateral para la navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Status", "Service Requests"])

if page == "Status":
    st.title("SAP Customer Status")
    st.markdown("<h1 style='color: lightblue;'>Customer Status</h1>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/59/SAP_2011_logo.svg", width=200)

    # Cargador de archivos
    uploaded_file = st.file_uploader("Por favor, selecciona el archivo Excel de datos del cliente:", type=["xlsx"])

    if uploaded_file:
        xls = load_excel(uploaded_file)
        if xls:
            customer_data, customer_info = get_customer_data(xls)
            
            # Sección de Datos del Cliente
            st.subheader("Datos del Cliente")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(customer_info['Logotipo'], width=100)
            with col2:
                st.write(f"**Customer name:** {customer_info['Customer name']}")
                st.write(f"**Phase:** {customer_info['Phase']}")
                st.write(f"**Contract Type:** {customer_info['Contract Type']}")
                st.write(f"**ACV:** {customer_info['ACV']} euros")
                st.write(f"**Región:** {customer_info['Región']}")
                st.write(f"**Classification:** {customer_info['Classification']}")

            # Indicador de estado de la cuenta
            st.subheader("Account Status Indicator")
            status = customer_info['Account Status']
            if status == "Green":
                st.markdown("<div style='width: 20px; height: 20px; background-color: green; border-radius: 50%;'></div>", unsafe_allow_html=True)
            elif status == "Orange":
                st.markdown("<div style='width: 20px; height: 20px; background-color: orange; border-radius: 50%;'></div>", unsafe_allow_html=True)
            elif status == "Red":
                st.markdown("<div style='width: 20px; height: 20px; background-color: red; border-radius: 50%;'></div>", unsafe_allow_html=True)

            # Indicador de CSAT
            csat = customer_info['Last CSAT']
            csat_color = "red" if csat < 3 else "orange" if csat < 4 else "green"
            st.markdown(f"<p style='color: {csat_color};'>**Last CSAT:** {csat}</p>", unsafe_allow_html=True)
            
           # Timeline
            dfDatos = pd.DataFrame({"start":[None],"end":[None],'title':[None],"content":[None],"color":[None],"textcolor":[None],"type":[None]})    

            parAltoTimeline = 600
            parArchivo = load_excel(uploaded_file)
            if parArchivo is not None:           
                df = pd.read_excel(parArchivo, sheet_name='timeline', usecols=['start_date', 'finish_date', 'title', 'content'])
                if len(df) > 0:
                    df.rename(columns={'start_date': 'start', 'finish_date': 'end'}, inplace=True)
                    df['start'] = pd.to_datetime(df['start'])
                    df['end'] = pd.to_datetime(df['end'])
                    dfDatos = df        

                
                
            if len(dfDatos.dropna()) > 0: 
                items=[]
                if parArchivo:
                    dfDatos['start'] = dfDatos['start'].dt.strftime('%Y-%m-%d')
                    dfDatos['end'] = dfDatos['end'].dt.strftime('%Y-%m-%d')
                columns = dfDatos.columns
                item = {}
                
                for indice, fila in dfDatos.iterrows():      
                    item["style"] = ""
                    for col in columns: 
                        if fila[col]:
                            if col == "color":
                                color = fila["color"]
                                item["style"] = f"background-color:{color};" + item["style"]
                            elif col == "textcolor":
                                color = fila["textcolor"]
                                item["style"] = f"color:{color};" + item["style"]
                            elif col == "title":
                                item["title"] = fila["start"]
                            elif col == "content":
                                item["content"] = fila["title"]
                            else:
                                item[col] = fila[col]                    
                    item["id"] = indice
                    items.append(item)
                    item = {}
                FechaMin = (pd.to_datetime(dfDatos["start"]).min() + timedelta(days=-365)).strftime('%Y-%m-%d')
                FechaMax = (pd.to_datetime(dfDatos["start"]).max() + timedelta(days=365)).strftime('%Y-%m-%d')


                c1, c2 = st.columns([8,2])
                with c1:
                    timeline = st_timeline(items, groups=[], options={"min":FechaMin,"max":FechaMax,"align":"left"}, height=f"{parAltoTimeline}px", width="100%")            
                with c2:
                    if timeline:
                        dfEvento = dfDatos.iloc[timeline["id"]]
                        detalleEvento = f"""
                                        #### {dfEvento['title']}
                                        **Fecha**: {dfEvento['start']}\n\n
                                        {dfEvento['content']}
                        """
                        st.write(detalleEvento, unsafe_allow_html=True)
            


           
           # Sección del Mapa usando lat y long del customer info con zoom=2
            if 'lat' in customer_info and 'long' in customer_info:
                try:
                    lat = float(customer_info['lat'])
                    lon = float(customer_info['long'])
                    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                    st.subheader("Customer Location")
                    st.map(map_data, zoom=4)
                except ValueError:
                    st.error("Las coordenadas lat y long deben ser números válidos.")
                    
            # Sección del Equipo SAP
            st.subheader("SAP Team")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**TSM:** {customer_info['TSM']}")
            with col2:
                st.write(f"**CDM:** {customer_info['CDM']}")
            with col3:
                st.write(f"**CSP:** {customer_info['CSP']}")
            with col4:
                st.write(f"**PL:** {customer_info['PL']}")


            # Sección de CSAT Histórico usando Plotly
            csat_data = get_csat_data(xls)
            st.subheader("Historical CSAT")
            
            fig_csat = px.scatter(csat_data, x='date', y='value', title='Historical CSAT')
            fig_csat.update_layout(yaxis_range=[0, 5])
            
            st.plotly_chart(fig_csat)



elif page == "Service Requests":
    st.title("Service Requests")
    
    # Cargador de archivos de solicitudes de servicio
    uploaded_file = st.file_uploader("Por favor, selecciona el archivo Excel de solicitudes de servicio:", type=["xlsx"])

    if uploaded_file:
        service_requests_data = load_service_requests(uploaded_file)
        if service_requests_data is not None:
            
            # Mostrar tabla de solicitudes de servicio
            st.subheader("Tabla de Solicitudes de Servicio")
            st.dataframe(service_requests_data)

            # Gráfico comparativo entre clientes usando bar_chart
            service_requests_by_customer = service_requests_data.groupby('customer').size().reset_index(name='count')
            st.subheader("Comparativa entre Clientes")
            st.bar_chart(service_requests_by_customer.set_index('customer'))


            # Gráfico comparativo por estado usando gráfico de pastel
            service_requests_by_status = service_requests_data.groupby('status').size().reset_index(name='count')
            st.subheader("Comparativa por Estado")
            fig_status = px.pie(service_requests_by_status, names='status', values='count', title='Distribución por Estado')
            st.plotly_chart(fig_status)

            # Gráfico comparativo por plantilla usando gráfico de pastel
            service_requests_by_template = service_requests_data.groupby('template').size().reset_index(name='count')
            st.subheader("Comparativa por Plantilla")
            fig_template = px.pie(service_requests_by_template, names='template', values='count', title='Distribución por Plantilla')
            st.plotly_chart(fig_template)

            # Gráfico comparativo día a día y agrupado por clientes usando bar_chart
            service_requests_by_day_customer = service_requests_data.groupby([service_requests_data['date'].dt.date, 'customer']).size().unstack().fillna(0)
            st.subheader("Comparativa por Día y Cliente")
            st.bar_chart(service_requests_by_day_customer)
          
                      
