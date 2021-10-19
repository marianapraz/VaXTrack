import streamlit as st
import plotly_express as px
from dataloaders import load_vacc_data, load_miss_data


def about_page():
    st.title('About')

    col1, col2, col3 = st.columns(3)
    col1.image('data/mariana.jpeg')
    col1.markdown('### Mariana Prazeres')
    col1.markdown(' Data Visualization | [LinkedIn](https://www.linkedin.com/in/mprazeres/)')
    col2.image('https://icons-for-free.com/iconfiles/png/512/person'
           '-1324760545186718018.png')
    col3.image('https://icons-for-free.com/iconfiles/png/512/person'
           '-1324760545186718018.png')

    col1, col2, col3 = st.columns(3)
    col1.image(
        'https://icons-for-free.com/iconfiles/png/512/person-1324760545186718018.png')
    col2.image('https://icons-for-free.com/iconfiles/png/512/person'
               '-1324760545186718018.png')
    col3.image('https://icons-for-free.com/iconfiles/png/512/person'
               '-1324760545186718018.png')




def main_page():
    st.title('Misinformation versus Vaccine Uptake')

    st.header('Introduction')
    st.write('Misinformation on the Covid vaccine has been circulating on the '
             'internet and especially on social media since the start of its '
             'rollout in December 2020. Although by now vaccines have been offered '
             'to entire populations in many countries, uptake has stagnated in '
             'different regions and among different demographics across various '
             'countries.')

    st.header('Hotspots of Misinformation')
    st.write('blablabla')
    # DOCS: https://plotly.com/python/bubble-maps/
    _, df_miss_weekly = load_miss_data()

    color_schema = px.colors.diverging.curl#px.colors.sequential.Viridis
    # ['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786',
    #                 '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921']

    fig_miss = px.scatter_geo(
        df_miss_weekly,
        locations="iso",
        color="rating",
        color_continuous_scale=color_schema,
        animation_frame="week",
        hover_name="iso",
        size="rating",
        labels={'rating': 'Misinformation'},
        scope='world',
        title='<b>Misinformation around the world</b>',
        hover_data={
            'iso': True,
            'week': False
        },
        range_color=(0, 15),
        height=500,
        width=700,
        projection="equirectangular",  #orthographic"
    )
    # fit to area of interest
    fig_miss.update_geos(fitbounds=False, visible=True)
    fig_miss.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_miss["layout"].pop("updatemenus")
    fig_miss.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_miss)

    st.header('Topics of Misinformation')
    st.write('blablabla')
    st.image('data/wordcloud.png')

    st.header('Vaccination Uptake Map')
    st.write('blablabla')
    # DOCS: https://plotly.com/python/choropleth-maps/
    _, df_vacc_weekly = load_vacc_data()
    color_schema = px.colors.diverging.curl#px.colors.sequential.Viridis
    # #px.colors.sequential.RdPu
    # color_schema = ["#f197e1", "#ed77d8", "#e958cf", "#e538c6", "#dd1cba",
    #               "#bd18a0", "#9d1485", "#7e106a", "#5e0c50", "#3f0835"]

    fig_vacc = px.choropleth(
        df_vacc_weekly,
        locations="iso_code",
        color="new_vaccinations_smoothed_per_million",
        color_continuous_scale=color_schema,
        animation_frame="week",
        scope='world',
        labels={'new_vaccinations_smoothed_per_million': 'Vaccines'},
        title='<b>Vaccines around the world</b>',
        range_color=(0, 50000),
        # hover_name='province',
        # hover_data={
        #     'cases' : True,
        #     'cartodb_id' : False
        # },
        height=500,
        width=700,
        projection="equirectangular")

    # fit to area of interest
    fig_vacc.update_geos(fitbounds="geojson", visible=False)
    fig_vacc.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, )
    fig_vacc["layout"].pop("updatemenus")
    fig_vacc.update_layout(coloraxis_colorbar=dict(
        thicknessmode="pixels",
        thickness=50,
        lenmode="pixels",
        len=200,
        # yanchor="top", y=1,
        # ticks="outside",
        # dtick=5
    ))

    col1, col2 = st.columns(2)
    with col2:
        selected = st.checkbox('Overlay misinformation data.')

    if selected:
        fig_vacc.add_trace(fig_miss.data[0])
        for i, frame in enumerate(fig_vacc.frames):
            try:
                fig_vacc.frames[i].data += (fig_miss.frames[i].data[0], )
            except:
                pass
        fig_vacc.update_layout(hovermode='x')
    st.plotly_chart(fig_vacc)

    st.header('Misinformation over time by country')
    df_vacc, _ = load_vacc_data()
    df_miss, _ = load_miss_data()

    countries = list(df_vacc['location'].drop_duplicates().values)
    locs = st.multiselect("Choose countries", list(countries),
                          ['United Kingdom', 'Portugal'])
    color_schema = px.colors.diverging.curl# px.colors.sequential.Viridis#px
    # .colors.qualitative.Pastel
    # ['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786',
    #                 '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921']

    df_loc = df_vacc_weekly[df_vacc_weekly['location'].isin(locs)]
    # st.write(df_loc.sort_values(['location','week']))
    fig_line = px.line(
        df_loc.sort_values(['location', 'week']),
        x="week",
        y="new_vaccinations_smoothed_per_million",
        color='location',
        color_discrete_sequence=color_schema,
        title='Vaccine uptake and misinformation over time in selected '
        'countries',
        labels={
            'new_vaccinations_smoothed_per_million': 'Daily '
            'vaccinations per million',
            'location': 'Country'
        })
    # st.plotly_chart(fig_line)

    df_miss_loc = df_miss[df_miss['location'].isin(locs)]
    df_miss_loc_count = df_miss_loc.groupby(['date', 'location']).count()

    # st.write(df_vacc_weekly.set_index(['week','iso','location']))
    # st.write(df_miss_weekly.set_index(['week','iso', 'countries']))

    df_joined = df_miss_weekly.set_index(['week', 'iso', 'countries']).join(
        df_vacc_weekly.set_index(['week', 'iso', 'location']), ).reset_index()
    df_joined = df_joined[df_joined['location'].isin(locs)]

    # Create quiver plot
    # st.write(df_joined.sort_values(['location','week']))
    fig_quiver = px.scatter(df_joined.sort_values(['location', 'week']),
                            x="week",
                            y="new_vaccinations_smoothed_per_million",
                            size="rating",
                            color="location",
                            color_discrete_sequence=color_schema)
    fig_quiver.update_traces(marker=dict(symbol='x'))
    fig_quiver.update_layout(showlegend=False)
    # st.plotly_chart(fig_quiver)

    for i in range(len(locs)):
        fig_line.add_trace(fig_quiver.data[i])
    fig_line.update_layout(showlegend=False, hovermode='x')
    st.plotly_chart(fig_line)

    st.header('Time Series Analysis')
