import pandas as pd


def get_covid_data():
    
    url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/'
           'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df = pd.read_csv(url)
    # rename countries
    df['Country/Region'] = df['Country/Region'].replace({'Korea, South': 'South Korea'})
    df = df[~df['Country/Region'].isin(['Cruise Ship'])]   # Remove Ships

    return df

def get_growth_rate_data(df, countries):
    MIN_CASES = 50
    SINCE_CASES_NUM = 50
    dt_cols = df.columns[~df.columns.isin(['Province/State', 'Country/Region', 'Lat', 'Long'])]
    LAST_DATE = dt_cols[-1]
    dff = (df.groupby('Country/Region')[dt_cols].sum()
       .stack().reset_index(name='Confirmed Cases')
       .rename(columns={'level_1': 'Date', 'Country/Region': 'Country'}))
    dff['Date'] = pd.to_datetime(dff['Date'], format='%m/%d/%y')
    for c in dt_cols[::-1]:
        if not df[c].fillna(0).eq(0).all():
            LAST_DATE = c
            break
#     countries = dff[dff['Date'].eq(LAST_DATE) & dff['Confirmed Cases'].ge(MIN_CASES) & 
#             dff['Country'].ne('China')
#            ].sort_values(by='Confirmed Cases', ascending=False)
    dff2 = dff[dff['Country'].isin(countries)].copy()
    days_since = (dff2.assign(F=dff2['Confirmed Cases'].ge(SINCE_CASES_NUM))
                  .set_index('Date')
                  .groupby('Country')['F'].transform('idxmax'))
    dff2['Days since 100 cases'] = (dff2['Date'] - days_since.values).dt.days.values
    dff2 = dff2[dff2['Days since 100 cases'].ge(0)]
    
    return dff2