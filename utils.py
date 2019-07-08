import numpy as np
import os
import pandas as pd
import pathlib
import requests


def download_file(
    url: str,
    filename: str,
    base: str = ".",
    dir: str = "data",
    overwrite: bool = False,
):
    """Method for downloading data

    Arguments:
        filename {str} -- File access of the ENCODE data file

    Keyword Arguments:
        base {str} -- Base directory (default: {"."})
        dir {str} -- Download directory (default: {"data"})
        overwrite {bool} -- If {True} existing files with be overwritten (default: {False})

    Returns:
        {str} -- Returns a pointer to `filename`.
    """
    filepath = os.path.join(base, dir, filename)

    if pathlib.Path(filepath).is_file() and not overwrite:
        print("File already exist. To overwrite pass `overwrite=True`")
        return

    chunkSize = 1024
    name, _ = os.path.splitext(filename)
    r = requests.get(url, stream=True)

    print("Download {}...".format(filename), end='')

    with open(filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunkSize):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    print(" done!")

    return filename


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

    return arr


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


def bed2ddb(filepath, name):
    """Factory function for bed2ddb tilesets"""
    
    from higlass.tilesets import Tileset
    from clodius.tiles import bed2ddb
    from clodius.tiles.utils import tiles_wrapper_2d
    
    return Tileset( 
        tileset_info=lambda: bed2ddb.get_2d_tileset_info(filepath),
        tiles=lambda tile_ids: tiles_wrapper_2d(tile_ids, lambda z,x,y: bed2ddb.get_2D_tiles(filepath,z,x,y)[x,y]),
        name=name
    )