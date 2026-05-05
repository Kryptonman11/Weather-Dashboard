from datetime import datetime, timedelta
import streamlit as st

st.set_page_config(layout="wide")


col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios as needed
with col2:
    st.write(f"# Weather 5 day average")

    st.markdown("<br>" * 5, unsafe_allow_html=True)

    st.text_input("Enter a city ")
    st.markdown("<br>" * 5, unsafe_allow_html=True)
    st.write(f"Humidity:")
    st.button("Humidity graph")
with col1:
    st.markdown("<br>" * 17, unsafe_allow_html=True)
    st.write(f"Tempature:")

    st.button("Tempature graph")
with col3:
    st.markdown("<br>" * 17, unsafe_allow_html=True)
    st.write(f"Tempature:")

    st.button(" Windspeed graph")
