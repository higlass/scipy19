import numpy as np
import pandas as pd


def parse_ncei_temperature_data(files, station: str = None):
    '''
    https://www.ncei.noaa.gov/access/search/data-search/global-hourly
    '''
    tables = [
        pd.read_csv(file, delimiter=',', quotechar='"', low_memory=False)
        for file in files
    ]

    if station is not None:
        tables = [t[t['STATION'] == station] for t in tables]

    df = pd.concat(tables).drop_duplicates()

    df['DATETIME'] = pd.to_datetime(df['DATE'])
    df['TEMP_C'] = [int(t.split(',')[0]) / 10. for t in df['TMP']]
    df = df[df['TEMP_C'] < 800]

    return df


def table_to_arrays(datetimes, temps):
    hours = datetimes.apply(lambda x: int(x.total_seconds() // 3600))
    arr = np.empty((max(hours)+1,))
    arr[:] = np.nan

    arr[hours] = temps

    not_nan_array = np.ones(arr.shape)
    not_nan_array[np.isnan(arr)] = 0

    return (arr, not_nan_array)


def get_ncei_temperature_data_as_array(definitions):
    temps = {}

    for city in definitions:
        temps[city] = parse_ncei_temperature_data(
            definitions[city]['files'],
            definitions[city]['station']
        )

    # Get the maximum-minimum and the minimum-maximum date time
    min_datetime = pd.to_datetime('1900-01-01T00:00:00')
    max_datetime = pd.to_datetime('2020-01-01T00:00:00')
    for city in definitions:
        min_datetime = max(min_datetime, min(temps[city]['DATETIME']))
        max_datetime = min(max_datetime, max(temps[city]['DATETIME']))

    # Convert the tables to numerical arrays
    temp_arrays = {}
    for city in temps:
        selection = (
            (temps[city]['DATETIME'] >= min_datetime) &
            (temps[city]['DATETIME'] <= max_datetime)
        )
        temp_arrays[city] = table_to_arrays(
            temps[city][selection]['DATETIME'] - min_datetime,
            temps[city][selection]['TEMP_C']
        )

    return temp_arrays, (min_datetime, max_datetime)
