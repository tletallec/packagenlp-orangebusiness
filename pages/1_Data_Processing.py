import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import importlib.resources as resources

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from collections import Counter
from packagenlp.nlp import NLP

import streamlit as st
import pandas as pd
from io import StringIO

dataframe = None
nlp = NLP()

tab_titles = ['Import Data', 'Treatment Data', 'Visualization Data']
tab1, tab2, tab3 = st.tabs(tab_titles)

with tab1:
    st.header("📂 Import Data")
    st.divider()
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        try:
            delimiter = st.text_input("Enter the delimiter:", ';')
            dataframe = pd.read_csv(uploaded_file, delimiter=delimiter)
            st.write("Data extract:")

            show_all_data = st.toggle("Show all data")
            if show_all_data:
                st.write(dataframe)
            else:
                st.write(dataframe.head())

            st.write(f"DataFrame Dimensions: {dataframe.shape}")

            language = st.radio("Select the language of your data",
                             ["**French**", "**English**"],
                             horizontal=True,
                             index=None)
            
            if language == "French":
                language = "fr"
            elif language == "English":
                language = "en"
  
        except Exception as e:
            st.error(f"Error parsing CSV file: {str(e)}")
    


# Initialize session state
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None

with tab2:
    st.header("⚙️ Treatment Data")
    st.divider()

    if dataframe is not None:
        selected_column = st.selectbox("Select a column to apply the treatment", dataframe.columns)

        choices_treatment = st.multiselect('Select the treatments to apply to your column',
                                           ['Clean Text', 'StopWords', 'Lematization'])

        st.divider()

        if 'Clean Text' in choices_treatment:
            st.subheader("Clean Text")

            st.caption("##### Paramètres")
            keep_numbers = st.checkbox("Garder les chiffres", value=True)
            exception = st.text_input("Exceptions", "")
            remove_accent = st.checkbox("Supprimer les accents", value=True)
            lowercase = st.checkbox("Texte en minuscule", value=True)

            apply_clean_text = st.toggle("Apply Clean Text")
            if apply_clean_text:
                # Appliquer le nettoyage du texte à la colonne sélectionnée
                if selected_column is not None and selected_column in dataframe.columns and dataframe[selected_column].apply(lambda x: isinstance(x, str)).all():
                    with st.spinner("Clean Text in progress"):
                        cleaned_data = dataframe[selected_column].apply(lambda text: nlp.cleanText(text, keep_numbers, exception, remove_accent, lowercase))
                        st.session_state.cleaned_data = cleaned_data  # Save the cleaned data to session state
                    st.success('Done!')
                else:
                    st.warning("La colonne sélectionnée ne contient pas de texte (chaînes de caractères). Veuillez sélectionner une colonne valide.")

        show_processed_data = st.toggle("Show processed data")   
        if show_processed_data:
            if st.session_state.cleaned_data is not None:
                st.write("Processed Data extract:")
                st.table(st.session_state.cleaned_data.head())
            else:
                st.warning("Please apply Clean Text first.")

    else:
        st.warning("No DataFrame uploaded yet. Please upload a file in the 'Import Data' tab.")