import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def custom_format(x):
    if pd.api.types.is_numeric_dtype(x):
        return str(x).replace('.', '@').replace(',', '.').replace('@', ',')
    else:
        return x

def custom_number_input(label):
    text_input = st.text_input(label, placeholder="Capital a amortitzar en €...")
    try:
        # Convert input to numeric value
        numeric_value = float(text_input.replace(',', '.'))
        # Ensure the value is within the specified range
        return numeric_value
    except ValueError:
        # st.warning("Invalid input. Please enter a valid number.")
        return None

def calcular_porcentajes_desde_pagado(capital_total, capital_pagado_intereses, capital_pagado_intereses_reales):
    # Calcular porcentajes en función de los capitales pagados
    porcentaje_intereses_reales_desde_pagado = (capital_pagado_intereses_reales / capital_pagado_intereses) * 100
    porcentaje_pagado_desde_pagado = (capital_pagado_intereses / capital_total) * 100

    return porcentaje_intereses_reales_desde_pagado, porcentaje_pagado_desde_pagado

@st.cache_data(experimental_allow_widgets=True) 
def descarregar(r: bool, df):
    if r:
        excel_data = BytesIO()
        df.to_excel(excel_data, index=False, engine='openpyxl')
        st.download_button(label="Descarregar taula real", data=excel_data, file_name="taula_real.xlsx", key='download_button1')
        
    else:
        excel_data = BytesIO()
        df.to_excel(excel_data, index=False, engine='openpyxl')
        st.download_button(label="Descarregar taula arrodonida", data=excel_data, file_name="taula_arrodonida.xlsx", key='download_button2')


def generar_df(r: bool) -> pd.DataFrame:

    if r:
        col_interes = "INTERES_REAL"
    else:
        col_interes = "INTERES_ARRODONIT"


    #Crear DF
    dades_inicials = {
            'DATA': np.nan,
            'CAPITAL_PENDENT': CAPITAL,
            'CAPITAL_AMORTITZAT': 0,
            'AMORTITZAT' : 0,
            'INTERES' : 0,
            'APORTACIO' : 0,
            'QUOTA' : 0,
        }
    DF = pd.DataFrame(dades_inicials, index=[0])
    DF['APORTACIO'] = DF['APORTACIO'].astype(float)

    # Primera entrada
    data = pd.to_datetime(INTERESSOS["DATA"][0], format='%m/%Y')
    data = data.strftime('%m/%Y')
    aportacio = 0
    aa_idx = 0
    try:
        if(APORTACIONS["DATA"][aa_idx] == data):
            aa_idx += 1
            aportacio = APORTACIONS["APORTACIÓ"][aa_idx]
    except:
        pass
    interes_mensual = (INTERESSOS[col_interes][0]/100) / FREQUENCIA_PAGAMENT
    quota =  (CAPITAL-aportacio) / ((1-(1/(1+interes_mensual))**PLAÇ)/interes_mensual)
    interes = (CAPITAL-aportacio) * interes_mensual
    amortitzat = quota - interes
    total_amortitzat = 0 + amortitzat
    capital_pendent = (CAPITAL-aportacio) - amortitzat
    DF.loc[len(DF)] = {
            'DATA': data,
            'CAPITAL_PENDENT': capital_pendent,
            'CAPITAL_AMORTITZAT': total_amortitzat,
            'AMORTITZAT' : amortitzat,
            'INTERES' : interes,
            'APORTACIO' : aportacio,
            'QUOTA' : quota
    }

    # Resta d'entrades
    for periode in range(2, PLAÇ+1):
        data = pd.to_datetime(data, format='%m/%Y')
        data += pd.DateOffset(months=1)
        data = data.strftime('%m/%Y')
        try:
            if(APORTACIONS["DATA"][aa_idx] == data):
                aportacio = APORTACIONS["APORTACIÓ"][aa_idx] 
                aa_idx += 1
            else:
                aportacio = 0
        except:
            aportacio = 0
        quota = DF["QUOTA"][periode-1] + aportacio - DF["APORTACIO"][periode-1]
        interes = DF["CAPITAL_PENDENT"][periode-1] * interes_mensual
        amortitzat = quota - interes
        total_amortitzat = DF["CAPITAL_AMORTITZAT"][periode-1] + amortitzat
        capital_pendent = DF["CAPITAL_PENDENT"][periode-1] - amortitzat
        if(periode % 12 == 1 or DF["APORTACIO"][periode-1] != 0):
            interes_mensual = (INTERESSOS[col_interes][periode // FREQUENCIA_PAGAMENT]/100) / FREQUENCIA_PAGAMENT
            quota =  DF["CAPITAL_PENDENT"][periode-1] / ((1-(1/(1+interes_mensual))**(PLAÇ-periode+1))/interes_mensual) + aportacio
            interes = DF["CAPITAL_PENDENT"][periode-1] * interes_mensual
            amortitzat = quota - interes
            total_amortitzat = DF["CAPITAL_AMORTITZAT"][periode-1] + amortitzat
            capital_pendent = DF["CAPITAL_PENDENT"][periode-1] - amortitzat
        DF.loc[len(DF)] = {
            'DATA': data,
            'CAPITAL_PENDENT': capital_pendent,
            'CAPITAL_AMORTITZAT': total_amortitzat,
            'AMORTITZAT' : amortitzat,
            'INTERES' : interes,
            'APORTACIO' : aportacio,
            'QUOTA' : quota
        }
    return DF




st.title("Analitzador d'hipoteca :chart_with_upwards_trend:")

st.header("Com funciona?", divider="orange")
video_file = open('video.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

st.header("Penja els fitxers necesaris", divider="orange")

st.subheader("Fitxer dels interessos")
interessos_fitxer = st.file_uploader("Tria el fitxer", type="xlsx", key=1)
if interessos_fitxer:
    INTERESSOS = pd.read_excel(interessos_fitxer, names=["DATA", "INTERES_REAL", "INTERES_ARRODONIT"], header=None, decimal=",")
    INTERESSOS_styled = INTERESSOS.style.format({
        "INTERES_REAL" : "{:.2f}",
        "INTERES_ARRODONIT" : "{:.2f}"
    }, thousands=".", decimal=",")


st.subheader("Fitxer de les aportacions")
aportacions_fitxer = st.file_uploader("Tria el fitxer", type="xlsx", key=2)
if aportacions_fitxer:
    APORTACIONS = pd.read_excel(aportacions_fitxer, names=["DATA", "APORTACIÓ"], header=None, decimal=",")
    APORTACIONS_styled = APORTACIONS.style.format({
        "APORTACIÓ" : "{:.2f}"
    }, thousands=".", decimal=",")

if interessos_fitxer and aportacions_fitxer:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("INTERESSOS")
        st.dataframe(INTERESSOS_styled, hide_index=True, width=10000)
    with col2:
        st.subheader("APORTACIONS")
        ap_plot = pd.read_excel(aportacions_fitxer, names=["DATA", "APORTACIÓ"])
        st.dataframe(APORTACIONS_styled, hide_index=True, width=100000)

st.header("Entra les variables", divider='orange')
# CAPITAL = st.number_input("Capital a amortitzar", value=None, placeholder="Capital a amortitzar en €...")
CAPITAL = custom_number_input("Capital")
DURACIO = st.number_input("Duració", value=None, placeholder="Entrar el plaç en anys...", step=1, format="%d")
FREQUENCIA_PAGAMENT = st.number_input("Freqüència de revisió", value=None, placeholder="Entrar la freqüència amb la que es fan les revisions. (anual=12)..", step=1, format="%d")

if(CAPITAL and DURACIO and FREQUENCIA_PAGAMENT):
    PLAÇ = 12 * DURACIO
    st.subheader("Genial :thumbsup:")
    st.write(f'Segons les dades entrades, tens una hipoteca amb interès variable que canvia cada {FREQUENCIA_PAGAMENT} mesos. El capital a amortitzar és de {locale.currency(CAPITAL, grouping=True)}  en un plaç de {DURACIO} anys, és a dir, amb un total de {PLAÇ} quotes.')

    st.header("Ja està tot a punt!", divider='orange')

    if(interessos_fitxer and aportacions_fitxer):
        arrodonit = generar_df(False) 
        real = generar_df(True) 
        st.subheader("TAULA D'AMORTITZACIÓ ARRODONIDA")

        arrodonit_style = arrodonit.style.format(decimal=",", thousands=".", precision=2)

        st.dataframe(arrodonit_style)
        #descarregar(False, arrodonit)
        st.subheader("TAULA D'AMORTITZACIÓ REAL")
        real_style = real.style.format(decimal=",", thousands=".", precision=2)
        st.dataframe(real_style)
        #descarregar(True, real)

        st.header("Resultats",divider="orange")
        total_int_real = round(real["INTERES"].sum(), 2)
        total_int_arrodonit = round(arrodonit["INTERES"].sum(), 2)
        st.write(f"En total, s'han pagat {locale.currency(total_int_arrodonit, grouping=True)} en interessos amb l'interès arrodonit i {locale.currency(total_int_real, grouping=True)} amb l'interès real. És a dir, s'han pagat {locale.currency(round(total_int_arrodonit-total_int_real, 2), grouping=True)} de més")

        col1, col2, col3 = st.columns(3)
        col1.metric("Interessos reals", f"{locale.currency(total_int_real, grouping=True)}")
        col2.metric("Interessos pagats", f"{locale.currency(total_int_arrodonit, grouping=True)}")
        col3.metric("Diferència", f"{locale.currency(round(total_int_arrodonit-total_int_real, 2), grouping=True)}", f"-{round(((total_int_arrodonit - total_int_real)/ CAPITAL) * 100, 2)}% sobre el capital")


        plot = pd.merge(arrodonit, real, on="DATA")
        plot["DATA"] = pd.to_datetime(plot["DATA"])
        plot.rename(columns={'DATA': 'MES', 'INTERES_x': 'INTERES ARRODONIT', "INTERES_y": "INTERES REAL", }, inplace=True)


        st.line_chart(
        plot, x="MES", y=["INTERES ARRODONIT", "INTERES REAL"], color=["#FF0000","#008000"]  # Optional
        )



    else:
        st.warning("No has pujat tots els arxius necesaris.")
