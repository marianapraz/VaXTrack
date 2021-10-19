"""Dataloading functions"""

import pandas as pd
import streamlit as st

@st.cache
def load_vacc_data():
    """ Returns clean vaccination dataset."""
    df = pd.read_csv('data/owid-covid-data.csv')
    df = df[[
        'iso_code', 'location', 'date', 'new_vaccinations_smoothed_per_million'
    ]].rename({
        'new_vaccinations_smoothed_per_million': 'vaccines'
    }).fillna(0)
    # df_vacc['date'] = pd.to_datetime(df_vacc['date'])
    df['week'] = pd.to_datetime(df['date']).dt.week
    df['year'] = pd.to_datetime(df['date']).dt.year
    df = df[pd.to_datetime(df['date']).isin(
        pd.date_range(start='1/1/2021', end='10/10/2021'))]
    df['week'] = (pd.to_datetime(df.year.astype(str), format='%Y') +
                  pd.to_timedelta(df.week.mul(7).astype(str) +
                                  ' days')).dt.strftime('%Y-%m-%d')
    df = df[pd.to_datetime(df['week']).isin(
        pd.date_range(start='1/1/2021', end='10/10/2021'))]

    df_weekly = df[[
        'week', 'iso_code', 'location', 'new_vaccinations_smoothed_per_million'
    ]].groupby(['week', 'location', 'iso_code']).sum().reset_index()
    df_weekly['iso'] = df_weekly['iso_code']
    return df, df_weekly


@st.cache
def load_miss_data():
    """ Returns clean missinformation dataset."""
    df = pd.read_csv('data/fake_news_list.csv')
    df['location'] = df['location'].str.split(',')
    # df_miss['date'] = pd.to_datetime(df_miss['date'])
    df = df.explode('location')
    df['location'] = df['location'].str.strip()

    df_iso = pd.read_csv('data/wikipedia-iso-country-codes.csv').set_index(
        'English short name lower case')

    # clean names that don't have iso
    df = df[~df['location'].isin([
        'Europe', 'Asia', 'Middle East', 'North Africa', 'Africa',
        'North America', '', 'West Africa', 'East Africa',
        'Turkish Republic of Northern Cyprus', 'Sir Lanka', 'Ivory Coast',
        'Tanzania'
    ])]

    df['iso'] = df_iso.loc[df['location'].values]['Alpha-3 code'].values

    df['countries'] = df['location']
    df_miss_countries = df.groupby(['date', 'iso',
                                    'countries']).count().reset_index()

    df_miss_countries['week'] = pd.to_datetime(
        df_miss_countries['date']).dt.week
    df_miss_countries['year'] = pd.to_datetime(
        df_miss_countries['date']).dt.year
    df_miss_countries = df_miss_countries[df_miss_countries['year'] == 2021]
    df_miss_countries = df_miss_countries[pd.to_datetime(
        df_miss_countries['date']).isin(
            pd.date_range(start='1/1/2021', end='10/10/2021'))]
    df_miss_countries['week'] = (
                pd.to_datetime(df_miss_countries.year.astype(str),
                               format='%Y') + \
                pd.to_timedelta(
                    df_miss_countries.week.mul(7).astype(str) + ' days')
                ).dt.strftime('%Y-%m-%d')
    df_miss_countries = df_miss_countries[pd.to_datetime(
        df_miss_countries['week']).isin(
            pd.date_range(start='1/1/2021', end='10/10/2021'))]

    df_weekly = df_miss_countries[['week', 'iso', 'countries', 'rating'
                                   ]].groupby(['week', 'iso', 'countries'
                                               ]).sum().reset_index()
    return df, df_weekly
