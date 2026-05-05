import pandas as pd
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pprint
import streamlit as st


def country_finder(countr):
    country = pycountry.countries.get(alpha_2=countr)
    return country.name if country else "NA"


def load_enviro():
    load_dotenv()
    password = os.getenv('API_KEY')
    return password


password = load_enviro()
city = "Kingston"

geo_response = requests.get(
    f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={password}")
geo_data = geo_response.json()


country = country_finder(geo_data[0].get("country"))

state = geo_data[0].get("state", "")

city = geo_data[0].get("local_names", "").get("en")

print(f"{country} {state} {city}")
