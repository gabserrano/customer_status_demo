import streamlit as st
import pandas as pd

# Título del dashboard
st.title('SAP Customer status')

# Encabezado
st.header('Customer status')

# Logotipo de SAP
st.image('https://upload.wikimedia.org/wikipedia/commons/5/59/SAP_2011_logo.svg', width=200)

# Solicitar la ruta al fichero Excel de datos del cliente
uploaded_file = st.file_uploader('Por favor, sube el fichero Excel de datos del cliente:', type=['xlsx', 'xls'])

# Validar si se ha proporcionado un fichero
if uploaded_file:
    try:
        # Leer el fichero Excel
        df = pd.read_excel(uploaded_file)

        # Mostrar los datos del cliente
        customer_name = df['Customer name'][0]
        logo_url = df['Logotipo'][0]
        acv = df['ACV'][0]
        tsm = df['TSM'][0]
        cdm = df['CDM'][0]
        csp = df['CSP'][0]
        region = df['Region'][0]
        classification = df['Clasification'][0]
        last_csat = df['Last CSAT'][0]

        st.subheader(f'Customer name: {customer_name}')
        st.image(logo_url, width=200)
        st.write(f'ACV: {acv} euros')
        st.write(f'TSM: {tsm}')
        st.write(f'CDM: {cdm}')
        st.write(f'CSP: {csp}')
        st.write(f'Region: {region}')
        st.write(f'Clasification: {classification}')

        # Mostrar el Last CSAT con el color correspondiente
        if last_csat >= 0 and last_csat < 3:
            csat_color = 'red'
        elif last_csat >= 3 and last_csat < 4:
            csat_color = 'orange'
        elif last_csat >= 4 and last_csat <= 5:
            csat_color = 'green'
        else:
            csat_color = 'black'

        st.markdown(f'<p style="color:{csat_color};">Last CSAT: {last_csat}</p>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f'Error al leer el fichero Excel: {e}')
else:
    st.warning('Por favor, sube el fichero Excel de datos del cliente.')
