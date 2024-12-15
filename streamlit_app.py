import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar el archivo Excel y validar las hojas
def load_excel(file):
    try:
        xls = pd.ExcelFile(file)
        required_sheets = ['customer_data', 'timeline', 'change_request', 'work_at_risk']
        if all(sheet in xls.sheet_names for sheet in required_sheets):
            return xls
        else:
            st.error("El archivo Excel debe contener las hojas: customer_data, timeline, change_request, work_at_risk.")
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

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="SAP Customer Dashboard", layout="wide")

# Barra lateral para la navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Status", "Customer Incidents"])

if page == "Status":
    st.title("SAP Customer status")
    st.markdown("<h1 style='color: lightblue;'>Customer status</h1>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/59/SAP_2011_logo.svg", width=200)

    # Cargador de archivos
    uploaded_file = st.file_uploader("Por favor, selecciona el archivo Excel de datos del cliente:", type=["xlsx"])

    if uploaded_file:
        xls = load_excel(uploaded_file)
        if xls:
            customer_info = get_customer_data(xls)
            
            st.subheader("Datos del Cliente")
            st.write(f"Customer name: {customer_info['Customer name']}")
            st.write(f"Account Status: {customer_info['Account Status']}")
            st.write(f"Phase: {customer_info['Phase']}")
            st.write(f"Contract Type: {customer_info['Contract Type']}")
            st.image(customer_info['Logotipo'], width=100)
            st.write(f"ACV: {customer_info['ACV']} euros")
            st.write(f"Región: {customer_info['Región']}")
            st.write(f"Clasification: {customer_info['Clasification']}")

            csat = customer_info['Last CSAT']
            csat_color = "red" if csat < 3 else "orange" if csat < 4 else "green"
            st.markdown(f"<p style='color: {csat_color};'>Last CSAT: {csat}</p>", unsafe_allow_html=True)

            st.subheader("SAP Team")
            st.write(f"TSM: {customer_info['TSM']}")
            st.write(f"CDM: {customer_info['CDM']}")
            st.write(f"CSP: {customer_info['CSP']}")
            st.write(f"PL: {customer_info['PL']}")

            # Sección de la línea de tiempo
            timeline_data = get_timeline_data(xls)
            st.subheader("Timeline")
            fig, ax = plt.subplots()
            ax.plot(timeline_data['Date'], timeline_data['Event'], marker='o')
            ax.set_xlabel('Date')
            ax.set_ylabel('Event')
            plt.xticks(rotation=45)
            st.pyplot(fig)

elif page == "Customer Incidents":
    st.title("Customer Incidents")
    # Aquí puedes añadir el contenido para la página de incidentes del cliente

# Configuración de las páginas
st.set_page_config(page_title="Dashboard de Service Delivery", layout="wide")

# Función para cargar datos desde un archivo TXT
def cargar_datos(archivo):
    try:
        datos = pd.read_csv(archivo, header=None, names=["Mes", "Incidencias"])
        return datos
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Configuración de las páginas del dashboard
menu = ["Inicio", "Cliente 1", "Cliente 2", "Cliente 3"]
opcion = st.sidebar.selectbox("Navega entre las páginas", menu)

if opcion == "Inicio":
    st.title("Dashboard de Service Delivery")
    st.write("Este dashboard permite visualizar y comparar las incidencias por mes de hasta tres clientes.")
    st.write("Navega por las diferentes páginas en el menú lateral para ver los datos de cada cliente.")

elif opcion == "Cliente 1":
    st.title("Cliente 1")
    nombre_cliente1 = st.text_input("Nombre del Cliente 1:", value="Cliente 1")
    archivo_cliente1 = st.file_uploader(f"Sube un archivo .txt para {nombre_cliente1} (Mes,Incidencias):", type="txt", key="cliente1")

    if archivo_cliente1 is not None:
        datos_cliente1 = cargar_datos(archivo_cliente1)
        if datos_cliente1 is not None:
            st.subheader(f"Datos de {nombre_cliente1}")
            st.dataframe(datos_cliente1)

            fig, ax = plt.subplots()
            ax.bar(datos_cliente1["Mes"], datos_cliente1["Incidencias"], color='skyblue')
            ax.set_title(f"Incidencias por Mes - {nombre_cliente1}")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Número de Incidencias")
            plt.xticks(rotation=45)

            st.pyplot(fig)

elif opcion == "Cliente 2":
    st.title("Cliente 2")
    nombre_cliente2 = st.text_input("Nombre del Cliente 2:", value="Cliente 2")
    archivo_cliente2 = st.file_uploader(f"Sube un archivo .txt para {nombre_cliente2} (Mes,Incidencias):", type="txt", key="cliente2")

    if archivo_cliente2 is not None:
        datos_cliente2 = cargar_datos(archivo_cliente2)
        if datos_cliente2 is not None:
            st.subheader(f"Datos de {nombre_cliente2}")
            st.dataframe(datos_cliente2)

            fig, ax = plt.subplots()
            ax.bar(datos_cliente2["Mes"], datos_cliente2["Incidencias"], color='lightgreen')
            ax.set_title(f"Incidencias por Mes - {nombre_cliente2}")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Número de Incidencias")
            plt.xticks(rotation=45)

            st.pyplot(fig)

elif opcion == "Cliente 3":
    st.title("Cliente 3")
    nombre_cliente3 = st.text_input("Nombre del Cliente 3:", value="Cliente 3")
    archivo_cliente3 = st.file_uploader(f"Sube un archivo .txt para {nombre_cliente3} (Mes,Incidencias):", type="txt", key="cliente3")

    if archivo_cliente3 is not None:
        datos_cliente3 = cargar_datos(archivo_cliente3)
        if datos_cliente3 is not None:
            st.subheader(f"Datos de {nombre_cliente3}")
            st.dataframe(datos_cliente3)

            fig, ax = plt.subplots()
            ax.bar(datos_cliente3["Mes"], datos_cliente3["Incidencias"], color='salmon')
            ax.set_title(f"Incidencias por Mes - {nombre_cliente3}")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Número de Incidencias")
            plt.xticks(rotation=45)

            st.pyplot(fig)
