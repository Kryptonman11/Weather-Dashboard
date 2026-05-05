import pandas as pd
import requests
from dotenv import load_dotenv
import os
import streamlit as st
import matplotlib.pyplot as plt
import pycountry
st.set_page_config(layout="wide")


def load_enviro():
    load_dotenv()
    password = os.getenv('API_KEY')
    return password


def country_finder(countr):
    country = pycountry.countries.get(alpha_2=countr)
    return country.name if country else "NA"


def get_lat_long(city, password):
    geo_response = requests.get(
        f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={password}")
    get_lat_long.geo_data = geo_response.json()
    try:
        lat = get_lat_long.geo_data[0].get('lat')
        long = get_lat_long.geo_data[0].get('lon')
    except IndexError:
        return None
    else:
        return lat, long


def turn_to_data_frame(lat, long, password):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={password}&units=imperial")
    weather_response = response.json()
    df = pd.DataFrame(weather_response['list'])

    return df


def new_dataframe(df, *args):
    flatten_dataframe = pd.concat(
        [df[arg].apply(pd.Series) for arg in args], axis=1)
    flatten_dataframe['dt_text'] = df['dt_txt'].apply(lambda x: x[:10])
    conv_to_dict = {'Humidity': flatten_dataframe['humidity'],
                    'Temperature': flatten_dataframe['temp'], 'Windspeed': flatten_dataframe['speed'], 'date': flatten_dataframe['dt_text']}
    new_df = pd.DataFrame(conv_to_dict)
    return new_df


def average_df(dataframe, group):
    average = dataframe.groupby(group).mean()
    return average


def plot_data(dataframe, data):
    fig, ax = plt.subplots()
    ax.plot(dataframe[data])
    ax.set_xlabel("Date")
    ax.set_ylabel(data)
    return fig


def stream_lit_ui(country, state, cit, average, temp, humid, wind):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write(f"# Weather 5 day average {country} {state} {cit}")
        st.write(average)
        st.pyplot(temp)
    with col1:
        st.markdown("<br>" * 20, unsafe_allow_html=True)
        st.pyplot(humid)
    with col3:
        st.markdown("<br>" * 20, unsafe_allow_html=True)
        st.pyplot(wind)


password = load_enviro()
st.write(f"# Welcome to Weather Dashboard \n")


city = st.text_input("Enter a city")


if st.button("Search"):
    place = get_lat_long(city, password)
    if place:
        country = country_finder(get_lat_long.geo_data[0].get("country"))
        state = get_lat_long.geo_data[0].get("state", "")
        cit = get_lat_long.geo_data[0].get("local_names", "").get("en")
        print(f"{country} {state} {city}")
        lat, long = place
        df = turn_to_data_frame(lat, long, password)
        new_df = new_dataframe(df, 'main', 'wind')
        average = average_df(new_df, 'date')
        temp_chart = plot_data(average, "Temperature")
        humid_chart = plot_data(average, "Humidity")
        wind_chart = plot_data(average, "Windspeed")
        user_interface = stream_lit_ui(
            country, state, cit, average, temp_chart, humid_chart, wind_chart)
    else:
        st.error("City is not found")
