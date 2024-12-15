import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_timeline import st_timeline

items = [
    {"id": 1, "content": "2022-10-20", "start": "2022-10-20"},
    {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
    {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
    {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
    {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
    {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
]

timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)

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
    return customer_info

# Función para obtener los datos de la línea de tiempo
def get_timeline_data(xls):
    df = pd.read_excel(xls, sheet_name='timeline')
    return df

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
            # Convertir la columna 'date' a tipo datetime
            df['date'] = pd.to_datetime(df['date'])
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
            customer_info = get_customer_data(xls)
            
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

            # Sección de la Línea de Tiempo
            timeline_data = get_timeline_data(xls)
            st.subheader("Timeline")
            fig, ax = plt.subplots()
            ax.plot(timeline_data['Date'], timeline_data['Event'], marker='o')
            ax.set_xlabel('Date')
            ax.set_ylabel('Event')
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Sección de CSAT Histórico
            csat_data = get_csat_data(xls)
            st.subheader("Historical CSAT")
            
            # Crear gráfico de dispersión usando st.scatter_chart
            csat_chart_data = csat_data.set_index('date')[['value']]
            
            # Mostrar gráfico en Streamlit con escala entre 0 y 5 en el eje y
            st.scatter_chart(csat_chart_data)

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

            # Crear gráfico de solicitudes por mes
            service_requests_by_month = service_requests_data.groupby(service_requests_data['date'].dt.to_period('M')).size().reset_index(name='count')
            
            fig, ax = plt.subplots()
            ax.bar(service_requests_by_month['date'].astype(str), service_requests_by_month['count'], color='skyblue')
            
            ax.set_xlabel('Mes')
            ax.set_ylabel('Número de Solicitudes')
            
            plt.xticks(rotation=45)
            
            # Mostrar gráfico en Streamlit
            st.pyplot(fig)
