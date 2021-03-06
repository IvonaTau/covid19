import altair as alt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def get_country_colors(x):
    mapping = {
        'Italy': 'black',
        'Lithuania': '#E45756',
        'South Korea':  '#A1BA59',
        'Spain':'#9467bd',
        'Germany': '#9D755D',
        'France': '#F58518',
        'Poland': '#2495D3',
        'China': 'yellow',
        'United Kingdom': 'brown',
        'Latvia': '#F58518',
        'Estonia': '#9467bd',
        'Japan': '#C1B7AD',
        'US': 'orange',
        'Ukraine' : 'orange',
        'Russia': 'red'}
    return mapping.get(x, '#C1B7AD')


def plot_confirmed_cases_barplot(df, country, cutoff=60, logarithmic_scale=False):
    
    
    
    data_f = df[df['Country/Region'] == country]
    nb_cases = data_f.values[0][cutoff:].astype(float)
    dates = data_f.columns[cutoff:]
    df_ = pd.DataFrame({'Dates': dates,
                     'Confirmed_cases': nb_cases})

    plt.figure(figsize=(20, 6))

    g = sns.barplot(x="Dates", y="Confirmed_cases", data=df_)
    if logarithmic_scale:
        g.set(yscale="log")
        g.set_title('Confirmed cases in ' + country + ' (Logarithmic scale)')
    else:
        g.set_title('Confirmed cases in ' + country)
    var = g.set_xticklabels(g.get_xticklabels(), rotation=90)
    
    
def plot_confirmed_cases_per100(df, country, total_population, cutoff=60):
    divider = total_population // 100000
    data_f = df[df['Country/Region'] == country]
    nb_cases = data_f.values[0][cutoff:].astype(float)/divider
    dates = data_f.columns[cutoff:]
    y_pos = np.arange(len(dates))
    df_ = pd.DataFrame({'Dates': dates,
                     'Confirmed_cases': nb_cases})

    plt.figure(figsize=(20, 6))
    plt.plot(df_['Dates'],df_['Confirmed_cases'],'-')
    plt.plot(range(len(df_['Confirmed_cases'])), [25]*len(df_['Confirmed_cases']), ':')
    plt.xticks(y_pos,dates, rotation=90)
    plt.title('Total confirmed cases per 10 000 habitants in '+country)
    

def plot_new_cases_barplot(df, country, cutoff=60, window=7):
    data_f = df[df['Country/Region'] == country]
    
#     dt_cols = df.columns[~df.columns.isin(['Province/State', 'Country/Region', 'Lat', 'Long'])]
#     dff = (df.groupby('Country/Region')[dt_cols].sum()
#        .stack().reset_index(name='Confirmed Cases')
#        .rename(columns={'level_1': 'Date', 'Country/Region': 'Country'}))
#     data_f = dff[dff['Country'] == country]

    
    nb_cases = data_f.values[0][cutoff:].astype(float)
    dates = data_f.columns[cutoff:]
    df_ = pd.DataFrame({'Dates': dates,
                     'Confirmed_cases': nb_cases})
    df_['MA'] = df_.iloc[:,1].rolling(window=window).mean()

    y_pos = np.arange(len(dates))
    plt.figure(figsize=(20, 6))
    df_['Confirmed_cases'].diff()
    plt.bar(range(len(df_['Confirmed_cases'].diff())), df_['Confirmed_cases'].diff().clip(0,99999999))
    plt.plot(range(len(df_['MA'].diff())), df_['MA'].diff(), '--')
    plt.xticks(y_pos,dates, rotation=90)
    plt.title('New daily cases in '+country)
#     return df_
    
    
def plot_new_cases_per100(df, country, total_population, cutoff=60, window=14):
    divider =  total_population / 100000 
    data_f = df[df['Country/Region'] == country]
    nb_cases = data_f.values[0][cutoff:].astype(float)
    dates = data_f.columns[cutoff:]
    y_pos = np.arange(len(dates))
    df_ = pd.DataFrame({'Dates': dates,
                     'Confirmed_cases': nb_cases})
    df_['MA'] = df_.iloc[:,1].rolling(window=window).sum().diff()/divider

    plt.figure(figsize=(20, 6))
    plt.plot(df_['Dates'],df_['MA'],'-')
    plt.plot(range(len(df_['Confirmed_cases'])), [16]*len(df_['Confirmed_cases']), ':')
    plt.plot(range(len(df_['Confirmed_cases'])), [25]*len(df_['Confirmed_cases']), 'r:')
    plt.xticks(y_pos,dates, rotation=90)
    plt.title('14-day mean of new cases per 100 000 habitants in '+country)

    
def make_since_chart(dff2, highlight_countries, baseline_countries):
    
    max_date = dff2['Date'].max()
    color_domain = list(dff2['Country'].unique())
    color_range = list(map(get_country_colors, color_domain))
    
    selection = alt.selection_multi(fields=['Country'], bind='legend', 
                                    init=[{'Country': x} for x in highlight_countries + baseline_countries])

    base = alt.Chart(dff2, width=550).encode(
        x='Days since 100 cases:Q',
        y=alt.Y('Confirmed Cases:Q', scale=alt.Scale(type='log')),
        color=alt.Color(
            'Country:N',
            scale=alt.Scale(domain=color_domain, range=color_range),
            legend=alt.Legend(columns=2)),
        tooltip=list(dff2),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.05))
    )
#     max_day = dff2['Days since 100 cases'].max()
    max_day=35
    ref = pd.DataFrame([[x, 100*1.3**x] for x in range(max_day+1)], columns=['Days since 100 cases', 'Confirmed Cases'])
    base_ref = alt.Chart(ref).encode(x='Days since 100 cases:Q', y='Confirmed Cases:Q')
    return (
        base_ref.mark_line(color='black', opacity=.5, strokeDash=[3,3]) +
#         base_ref.transform_filter(
#             alt.datum['Days since 100 cases'] >= max_day
#         ).mark_text(dy=-6, align='right', fontSize=10, text='33% Daily Growth') +
        base.mark_line(point=True).add_selection(selection) + 
        base.transform_filter(
            alt.datum['Date'] >= int(max_date.timestamp() * 1000)
        ).mark_text(dy=-8, align='right', fontWeight='bold').encode(text='Country:N')
    ).properties(
        title=f"Compare {', '.join(highlight_countries)} trajectory with {', '.join(baseline_countries)}"
    )