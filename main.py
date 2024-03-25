import pandas as pd
import joblib

import streamlit as st

def transform_in_float(value):
    try:
        value = float(value)
    except:
        value = 0
    return value


st.title('Modelo Passos Mágicos - Ponto de Virada & Evasão')

tab_0, tab_1 = st.tabs(['Input Manual', 'Input Planilha'])

colunas_obrigatorias = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']

colunas_df = [f'{coluna}_ultimo_{ano}_ano' for ano in [1, 2, 3] for coluna in colunas_obrigatorias]

map_colunas = {}
map_ano = {
    'ULTIMO': 1,
    'PENULTIMO': 2,
    'ANTEPENULTIMO': 3
}

for coluna in colunas_obrigatorias:
    for ano in ['ULTIMO', 'PENULTIMO', 'ANTEPENULTIMO']:
        map_colunas[f'{coluna}_{ano}'] = f'{coluna}_ultimo_{map_ano.get(ano)}_ano'

model_evasao = joblib.load('model_evasao.joblib')
model_ponto_virada = joblib.load('model_ponto_virada.joblib')

with tab_0:
    """
    **Último ano**
    """

    col_1, col_2, col_3, col_4 = st.columns(4)

    with col_1:
        INDE_1 = st.number_input("INDE (último)", step=1.0, format="%.2f")
        IDA_1 = st.number_input("IDA (último)", step=1.0, format="%.2f")

    with col_2:
        IAA_1 = st.number_input("IAA (último)", step=1.0, format="%.2f")
        IPP_1 = st.number_input("IPP (último)", step=1.0, format="%.2f")

    with col_3:
        IEG_1 = st.number_input("IEG (último)", step=1.0, format="%.2f")
        IPV_1 = st.number_input("IPV (último)", step=1.0, format="%.2f")

    with col_4:
        IPS_1 = st.number_input("IPS (último)", step=1.0, format="%.2f")
        IAN_1 = st.number_input("IAN (último)", step=1.0, format="%.2f")

    """
    **Penúltimo ano**
    """

    col_1, col_2, col_3, col_4 = st.columns(4)

    with col_1:
        INDE_2 = st.number_input("INDE (penúltimo)", step=1.0, format="%.2f")
        IDA_2 = st.number_input("IDA (penúltimo)", step=1.0, format="%.2f")

    with col_2:
        IAA_2 = st.number_input("IAA (penúltimo)", step=1.0, format="%.2f")
        IPP_2 = st.number_input("IPP (penúltimo)", step=1.0, format="%.2f")

    with col_3:
        IEG_2 = st.number_input("IEG (penúltimo)", step=1.0, format="%.2f")
        IPV_2 = st.number_input("IPV (penúltimo)", step=1.0, format="%.2f")

    with col_4:
        IPS_2 = st.number_input("IPS (penúltimo)", step=1.0, format="%.2f")
        IAN_2 = st.number_input("IAN (penúltimo)", step=1.0, format="%.2f")

    """
    **Antepenúltimo ano**
    """

    col_1, col_2, col_3, col_4 = st.columns(4)

    with col_1:
        INDE_3 = st.number_input("INDE (antepenúltimo)", step=1.0, format="%.2f")
        IDA_3 = st.number_input("IDA (antepenúltimo)", step=1.0, format="%.2f")

    with col_2:
        IAA_3 = st.number_input("IAA (antepenúltimo)", step=1.0, format="%.2f")
        IPP_3 = st.number_input("IPP (antepenúltimo)", step=1.0, format="%.2f")

    with col_3:
        IEG_3 = st.number_input("IEG (antepenúltimo)", step=1.0, format="%.2f")
        IPV_3 = st.number_input("IPV (antepenúltimo)", step=1.0, format="%.2f")

    with col_4:
        IPS_3 = st.number_input("IPS (antepenúltimo)", step=1.0, format="%.2f")
        IAN_3 = st.number_input("IAN (antepenúltimo)", step=1.0, format="%.2f")

    valores = [eval(f'{coluna}_{ano}') for ano in [1, 2, 3] for coluna in colunas_obrigatorias]
    df_input = pd.DataFrame([valores], columns=colunas_df)

    if st.button('Gerar Predição'):
        result_ponto_virada = model_ponto_virada.predict(df_input.values)
        result_evasao = model_evasao.predict(df_input.values)

        st.success(f"Provável Ponto de Virada: {'Sim' if result_ponto_virada[0] == 1 else 'Não'}")
        st.success(f"Provável Evasão: {'Sim' if result_evasao[0] else 'Não'}")


with tab_1:
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])
    if uploaded_file is not None:
        df_input = pd.read_csv(uploaded_file, sep=';')
        nomes = df_input['NOME']
        df_input = df_input.drop(['NOME'], axis=1).fillna(0)
        df_input.columns = [map_colunas.get(coluna) for coluna in df_input.columns]
        for coluna in colunas_df:
            df_input[coluna] = df_input[coluna].apply(transform_in_float)

        result_ponto_virada = model_ponto_virada.predict(df_input.values)
        result_evasao = model_evasao.predict(df_input.values)

        df_result = pd.DataFrame({
            "Nome do Aluno": nomes,
            "Possível Ponto de Virada": ['Sim' if result == 1 else 'Não' for result in result_ponto_virada],
            "Possível Evasão": ['Sim' if result else 'Não' for result in result_evasao]

        })

        """
        **Resultado:**
        """

        st.dataframe(df_result, use_container_width=True)
