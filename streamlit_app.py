import streamlit as st
import pandas as pd

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

elif page == "Customer Incidents":
    st.title("Customer Incidents")
    # Aquí puedes añadir el contenido para la página de incidentes del cliente
