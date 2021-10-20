import streamlit as st
import plotly_express as px
from dataloaders import load_vacc_data, load_miss_data


def about_page():
    st.title('About')

    col1, col2, col3 = st.columns(3)
    col1.image('data/aizaan.jpg')
    col1.markdown('### Aizaan Anwar')
    col1.markdown('Data Wrangling, EDA and Statistics | '
                  '[LinkedIn](https://www.linkedin.com/in/aizaan)')
    col2.image('data/Wullenweber_Anne_Foto_Original.jpg')
    col2.markdown('### Anne Wullenweber')
    col2.markdown(
        ' EDA and Time Series Modeling & Forecasting'
        ' | [LinkedIn](https://www.linkedin.com/in/annewullenweber/)')

    col3.image('data/cori.JPG')
    col3.markdown('### Cori Campbell')
    col3.markdown(
        'Data Wrangling and EDA | '
        '[LinkedIn](https://uk.linkedin.com/in/cori-campbell-550bb7222)')

    col1, col2, col3 = st.columns(3)
    col1.image('data/mariana.jpeg')
    col1.markdown('### Mariana Prazeres')
    col1.markdown(
        'EDA and Data Visualization | [LinkedIn]('
        'https://www.linkedin.com/in/mprazeres/)')
    col2.image('data/saran.jpeg')
    col2.markdown('### Saran Davies')
    col2.markdown(
        'Data Visualisation and Graphics | [LinkedIn]('
        'https://www.linkedin.com/in/saran-davies/)')
    col3.image('data/Yifan_Zhang.jpg')
    col3.markdown('### Yifan Zhang')
    col3.markdown(
        'Data Preparation, EDA and Time Series Modeling | [LinkedIn]('
        'https://www.linkedin.com/in/yifan-zhang-in)')


def main_page():
    st.title('Exploring the impact of misinformation on global vaccine uptake')
    st.markdown("""
          
             
                <h4> <i>[an] overabundance 
             of information - some accurate and some not - [...] occurs 
             during an epidemic. It can lead to confusion and ultimately 
             mistrust in governments and public health response.</i>
                <div style="text-align: right">  WHO 2021 </div></h4>
                
                
           

                """, unsafe_allow_html=True)
    st.markdown(""" Understanding the factors that lead to different rates of vaccine 
            uptake is crucial to improve vaccination programmes not only for 
            the COVID vaccine, but also for future vaccine rollouts. 
            Overcoming vaccine hesitancy and misinformation is of paramount 
            importance for successful vaccination programmes. The 
            socio-economic impact of effective vaccination coverage cannot 
            be overstated. For example, in the absence of vaccine hesitancy, 
            236-305 covid-related deaths per million population can be prevented 
            (Mesa et al. 2021).""")

    # SECTION 1
    st.header('Hotspots of Misinformation')

    st.write('blablabla')

    # map plot for misinformation
    _, df_miss_weekly = load_miss_data()
    # st.write(df_miss_weekly) # Uncomment to see dataset

    # DOCS: https://plotly.com/python/bubble-maps/
    color_schema = px.colors.diverging.curl
    fig_miss = px.scatter_geo(
        df_miss_weekly,
        locations="iso",
        color="rating",
        color_continuous_scale=color_schema,
        animation_frame="week",
        hover_name="countries",
        size="rating",
        labels={'rating': 'Fake news discovered'},
        scope='world',
        title='<b>Misinformation around the world</b>',
        hover_data={
            'iso': False,
            'week': True,
            'rating': True
        },
        range_color=(0, 15),
        height=500,
        width=700,
        projection="equirectangular",  #orthographic"
    )
    # customizations
    fig_miss.update_geos(fitbounds=False, visible=True)
    fig_miss.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig_miss["layout"].pop("updatemenus")
    fig_miss.update_layout(coloraxis_showscale=False)
    # plot it
    st.plotly_chart(fig_miss)

    # SECTION 2
    st.header('Topics of Misinformation')

    st.write('blablabla')

    st.image('data/wordcloud.png')

    # SECTION 3
    st.header('Vaccination Uptake Map')

    st.write('blablabla')

    # map plot for vaccine uptake than can be overlayed with the previous
    # misinformation map plot
    _, df_vacc_weekly = load_vacc_data()
    # st.write(df_vacc_weekly) # uncomment to see data

    # DOCS: https://plotly.com/python/choropleth-maps/
    color_schema = px.colors.diverging.curl[:6] # pick only the greens
    color_schema.reverse()
    fig_vacc = px.choropleth(
        df_vacc_weekly,
        locations="iso_code",
        color="new_vaccinations_smoothed_per_million",
        color_continuous_scale=color_schema,
        animation_frame="week",
        scope='world',
        labels={'new_vaccinations_smoothed_per_million': ''
                                                         'New vaccinations '
                                                         '<br> '
                                              'per million'},
        range_color=(0, 50000),
        hover_name='location',
        hover_data={
            'week': True,
            'iso_code': False,
            'iso': False,
            'new_vaccinations_smoothed_per_million': True
        },

        height=500,
        width=900,
        projection="equirectangular")
    # customizations
    # customizations
    fig_vacc.update_geos(fitbounds=False, visible=False)
    fig_vacc.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, )
    fig_vacc["layout"].pop("updatemenus")
    fig_vacc.update_layout(coloraxis_colorbar=dict(
        thicknessmode="pixels",
        thickness=10,
        lenmode="pixels",
        len=400,
    ))

    # overlay
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
    # plot it
    st.plotly_chart(fig_vacc)

    # SECTION 4
    st.header('Misinformation over time by country')

    # Timeseries plot for vaccines versus misinformation
    df_vacc, _ = load_vacc_data()
    df_miss, _ = load_miss_data()

    # Country selector
    countries = list(df_vacc['location'].drop_duplicates().values)
    locs = st.multiselect("Choose countries", list(countries),
                          ['United Kingdom', 'Portugal'])
    df_loc = df_vacc_weekly[df_vacc_weekly['location'].isin(locs)]
    # st.write(df_loc.sort_values(['location','week'])) # uncomment to see
    df_joined = df_miss_weekly.set_index(['week', 'iso', 'countries']).join(
        df_vacc_weekly.set_index(['week', 'iso', 'location']), ).reset_index()
    df_joined = df_joined[df_joined['location'].isin(locs)]
    # st.write(df_joined.sort_values(['location','week'])) # uncomment to see

    # line plot of vaccination time series
    color_schema = ['#1C485D', '#3F9C81', '#E0A089', '#A43660']
    # this is a partial selection of px.colors.diverging.curl
    fig_line = px.line(
        df_loc.sort_values(['location', 'week']),
        x="week",
        y="new_vaccinations_smoothed_per_million",
        color='location',
        color_discrete_sequence=color_schema,
        labels={'new_vaccinations_smoothed_per_million': ''
                                                         'New vaccinations '
                                                         'per million'},
        hover_data={
            'week': False,
            'iso_code': False,
            'iso': False,
            'location': False,
            'new_vaccinations_smoothed_per_million': True
        },
        hover_name='location')
    # customizations
    fig_line.update_traces(hovertemplate="""
        <b>%{hovertext}</b>:  %{y} vaccines per million<extra></extra>"""
                           )
    # st.plotly_chart(fig_line) # uncomment to see just line plot

    # Create scatter plot with fake news information
    fig_scatter = px.scatter(df_joined.sort_values(['location', 'week']),
                            x="week",
                            y="new_vaccinations_smoothed_per_million",
                            size="rating",
                            color="location",
                            color_discrete_sequence=color_schema,
                            # hover_name='location',
                            hover_data={
                                'week': True,
                                'iso_code': False,
                                'iso': False,
                                'countries': False,
                                'new_vaccinations_smoothed_per_million': False,
                                'rating': True,
                                'location': False
                            },
                            labels={'rating': 'Fake news discovered'}
                            )
    # customizations
    fig_scatter.update_traces(marker=dict(symbol='x'))
    fig_scatter.update_layout(showlegend=False)
    fig_scatter.update_traces(hovertemplate="""
            %{customdata[3]} fake news spotted on %{x}"""
                           )
    # st.plotly_chart(fig_scatter) # uncomment to see just scatter plot

    # Combine the two plots and plot it
    for i in range(len(locs)):
        fig_line.add_trace(fig_scatter.data[i])
    fig_line.update_layout(showlegend=False, hovermode='x unified')
    st.plotly_chart(fig_line)

    # SECTION 4
    st.header('Time Series Analysis')
