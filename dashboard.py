import os
import json

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import pandas as pd
# from pandas_profiling import ProfileReport
import seaborn as sns
import plotly.figure_factory as ff
import plotly_express as px
import datetime


import streamlit as st
import streamlit.components.v1 as components


# Load data
@st.cache
def load_data():
    df_vacc = pd.read_csv('data/owid-covid-data.csv')
    df_vacc = df_vacc[['iso_code', 'location', 'date',
                       'new_vaccinations_smoothed_per_million']
    ].rename({'new_vaccinations_smoothed_per_million': 'vaccines'}).fillna(0)

    df_miss = pd.read_csv('data/fake_news_list.csv')
    df_miss['location'] = df_miss['location'].str.split(
        ',')
    # df_miss['date'] = pd.to_datetime(df_miss['date'])
    df_miss = df_miss.explode('location')
    df_miss['location'] = df_miss['location'].str.strip()
    return df_vacc, df_miss


st.title('Misinformation versus Vaccine Uptake - V1')
df_vacc, df_miss = load_data()

# st.subheader('Misinformation hotspots')
df_miss_countries = df_miss.groupby(['date','location']).count(
    ).reset_index()

# st.write('Dataset')
# if st.checkbox('show data for misinformation'):
#     st.table(df_miss_countries.sample(10))
# if st.checkbox('show data for vaccines'):
#     st.table(df_vacc.sample(10))

st.subheader('Map - Vaccination rates')
st.write('Too see further: https://plotly.com/python/choropleth-maps/')
# assign mp to the geojson data
# with open("data/countries.json", "r") as geo:
#     mp = json.load(geo)

# st.write(df_miss_countries["location"])
# st.write(mp["features"][0]["properties"])
df_vaccdf_vacc_no_date = df_vacc.groupby('iso_code').sum().reset_index()
fig = px.choropleth(df_vacc,
                    locations="iso_code",
                    # geojson=mp,
                    # featureidkey="properties.ADMIN",
                    color="new_vaccinations_smoothed_per_million",
                    color_continuous_scale="Viridis",
                    animation_frame="date",
                    scope='world',
                    labels={'new_vaccinations_smoothed_per_million': 'Vaccines'},
                    title='<b>Vaccines around the world</b>',
                    # hover_name='province',
                    # hover_data={
                    #     'cases' : True,
                    #     'cartodb_id' : False
                    # },
                    # height=900,
                    # locationmode='geojson-id',
                    )
# fit to area of interest
# fig.update_geos(fitbounds="locations", visible=True)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig)

st.subheader('Map - Misinformation hotspots')
st.write('Too see further: https://plotly.com/python/bubble-maps/')

df_iso = pd.read_csv('data/wikipedia-iso-country-codes.csv'
                     ).set_index('English short name lower case')

# clean names that don't have iso
df_miss = df_miss[~df_miss['location'].isin(
    [ 'Europe', 'Asia', 'Middle East', 'North Africa', 'Africa',
     'North America', '', 'West Africa', 'East Africa',
      'Turkish Republic of Northern Cyprus', 'Sir Lanka',
      'Ivory Coast', 'Tanzania']
)]

df_miss['iso'] = df_iso.loc[df_miss['location'].values]['Alpha-3 code'].values

df_miss_countries = df_miss.groupby(['date','iso']).count(
    ).reset_index()

df_miss_countries_no_date = df_miss_countries.groupby('iso').sum().reset_index()
# st.write(df_miss_countries)
# st.write(df_miss_countries.shape)
fig = px.scatter_geo(df_miss_countries,
                    locations="iso",
                    # geojson=mp,
                    # featureidkey="properties.ADMIN",
                    color="rating",
                    color_continuous_scale="Viridis",
                    animation_frame="date",
                    hover_name="iso", size="rating",
                    labels={'rating': 'Misinformation'},
                    title='<b>Misinformation around the world</b>',
                    # hover_data={
                    #     'cases' : True,
                    #     'cartodb_id' : False
                    # },
                    # height=900,
                    # locationmode='geojson-id',
                    )
# fit to area of interest
# fig.update_geos(fitbounds="locations", visible=True)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)




#
st.subheader('Misinformation over time in select countries')
countries = list(df_vacc['location'].drop_duplicates().values)
locs = st.multiselect(
        "Choose countries", list(countries), ['United Kingdom', 'United '
                                                                'States',
                                              'Portugal']
    )

fig, ax = plt.subplots()
# st.write(plt.style.available)

plt.style.use('seaborn-whitegrid')

for loc in locs:
    df_loc = df_vacc[df_vacc['location']==loc]
    df_loc['date'] = pd.to_datetime(df_loc['date'])

    p = ax.plot(df_loc['date'], df_loc[
        'new_vaccinations_smoothed_per_million'], label=loc,
             linewidth=4)

    df_miss_loc = df_miss[df_miss['location'] == loc]
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


#     # Create quiver plot
#     # fig = ff.create_quiver(date2num(list(df_joined['date'].values)),
#     #           list(df_joined['new_vaccinations_smoothed_per_million'].values),
#     #           [0 for _ in list(df_joined['date'].values)],
#     #         list(1000*df_joined['location_x'].values), arrow_scale=0.03, \
#     #                                                             scale=0.2,
#     #                        angle=np.pi/30, fill=p[0].get_color())#,
#
#
ax.legend()
ax.set_xlim([datetime.date(2021,1,1),datetime.date(2021,10,10) ])

fig.autofmt_xdate()
# ax.  xticks(rotation=90)
st.pyplot(fig)
