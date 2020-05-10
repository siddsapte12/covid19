import pandas as pd
import numpy as np

from datetime import datetime


def store_relational_JH_data(data_path, value='confirmed'):
    ''' Transformes the COVID data in a relational data set

    '''

    pd_raw = pd.read_csv(data_path)

    pd_data_base = pd_raw.rename(columns={'Country/Region': 'country',
                                          'Province/State': 'state'})
    pd_data_base['country'] = pd_data_base['country'].str.replace(
        'US', 'United States')
    pd_data_base['state'] = pd_data_base['state'].str.replace(
        'US', 'United States')

    pd_data_base['state'] = pd_data_base['state'].fillna('no')

    pd_data_base = pd_data_base.drop(['Lat', 'Long'], axis=1)

    pd_relational_model = pd_data_base.set_index(['state', 'country']) \
        .T \
        .stack(level=[0, 1]) \
        .reset_index() \
        .rename(columns={'level_0': 'date',
                         0: value},
                )

    pd_relational_model['date'] = pd_relational_model.date.astype(
        'datetime64[ns]')
    pd_relational_model[value] = pd_relational_model[value]/1000000
    #save_path = 'COVID_relational_' + value + '.csv'
    # print(save_path)

    #pd_relational_model.to_csv(save_path, index=False)
    print(' Number of rows stored: ' + str(pd_relational_model.shape[0]))
    return pd_relational_model


# if __name__ == '__main__':
#     confirmed = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
#     store_relational_JH_data(confirmed, 'confirmed')
#     deaths = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
#     store_relational_JH_data(deaths, 'deaths')
#     recovered = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
#     store_relational_JH_data(recovered, 'recovered')
