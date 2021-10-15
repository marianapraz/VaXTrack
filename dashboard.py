import os

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
import seaborn as sns
import plotly.figure_factory as ff
import plotly_express as px
import numpy as np
import datetime
import folium
from streamlit_folium import folium_static


import streamlit as st
import streamlit.components.v1 as components

# Load data
@st.cache
def load_data():
    DATA_PATH = 'data/owid-covid-data.csv'
    data_load_state = st.text('Loading data...')
    data_load_state.text('Loading data from CSV path %s...' % DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    return df

@st.cache
def profiling(df):
    profile = ProfileReport(df, title="Pandas Profiling Report").to_html()
    return profile

df = load_data()
df_miss = pd.read_csv('data/fake_news_list.csv')

st.title('Misinformation versus Vaccine Uptake - V1')

st.subheader('Misinformation hotspots')
st.write('Need to fix country names manually :(')
countries_geo = "data/countries.json"
df_miss_countries = df_miss['location'].str.split(
    ',').explode().str.strip().value_counts().reset_index()

center = [40.738, 0] # lat, long
folium_map = folium.Map(location=center,
                        zoom_start=2, title='World Map')


folium.Choropleth(
    geo_data=countries_geo,
    name="choropleth",
    data=df_miss_countries,
    columns=["index", "location"],
    key_on="feature.properties.ADMIN",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(folium_map)

folium.LayerControl().add_to(folium_map)

folium_static(folium_map)










st.subheader('Misinformation over time in select countries')
df_vaccines = df[['location', 'date', 'new_vaccinations_smoothed_per_million']]
countries = list(df_vaccines['location'].drop_duplicates().values)
locs = st.multiselect(
        "Choose countries", list(countries), ['United Kingdom', 'United '
                                                                'States',
                                              'Portugal']
    )

df_miss_clean = df_miss[['location', 'date']].dropna()
fig, ax = plt.subplots()
# st.write(plt.style.available)

plt.style.use('seaborn-whitegrid')

for loc in locs:
    df_loc = df_vaccines[df_vaccines['location']==loc]
    df_loc['date'] = pd.to_datetime(df_loc['date'])

    p = ax.plot(pd.to_datetime(df_loc['date']), df_loc[
        'new_vaccinations_smoothed_per_million'], label=loc,
             linewidth=4)

    df_miss_loc = df_miss_clean[df_miss_clean['location'].str.contains(loc)]
    df_miss_loc_count = df_miss_loc.groupby('date').count()
    df_miss_loc_count.index = pd.to_datetime(df_miss_loc_count.index)

    df_joined = df_miss_loc_count.merge(df_loc, on='date', how='inner')[
                    ['date', 'location_x',
                     'new_vaccinations_smoothed_per_million']].fillna(0)
    ax.quiver(date2num(list(df_joined['date'].values)),
              list(df_joined['new_vaccinations_smoothed_per_million'].values),
              0, list(df_joined['location_x'].values), width=0.005,
              color=p[0].get_color(), alpha=0.8)

    # ax.bar(df_joined['date'],
    #        df_joined['location_x'],
    #        color=p[0].get_color(), alpha=0.8)


    # Create quiver plot
    # fig = ff.create_quiver(date2num(list(df_joined['date'].values)),
    #           list(df_joined['new_vaccinations_smoothed_per_million'].values),
    #           [0 for _ in list(df_joined['date'].values)],
    #         list(1000*df_joined['location_x'].values), arrow_scale=0.03, \
    #                                                             scale=0.2,
    #                        angle=np.pi/30, fill=p[0].get_color())#,


ax.legend()
ax.set_xlim([datetime.date(2021,1,1),datetime.date(2021,10,10) ])

fig.autofmt_xdate()
# ax.  xticks(rotation=90)
st.pyplot(fig)
