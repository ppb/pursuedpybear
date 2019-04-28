#!/usr/bin/env python3
from pathlib import Path

import numpy as np
import pandas as pd

import holoviews as hv
hv.extension('bokeh')


NS_PER_SECONDS = 1e9


def process(df):
    columns = ['signal', 'events', 'scene']
    for start, end in zip(['start']+columns, columns):
        time_column = f"{end}_time"
        df[time_column] = (df[end] - df[start]) / NS_PER_SECONDS

    next_start = df['start'].shift(-1)
    df['delta_time'] = (next_start - df['start']) / NS_PER_SECONDS
    df['sleep_time'] = (next_start - df['scene']) / NS_PER_SECONDS
    df['fps'] = 1 / df['delta_time']


def plot(df):
    dims = {'kdims': 'time', 'vdims': 'time'}
    hv.opts.defaults(hv.opts.Area(fill_alpha=0.5))

    signal_time = hv.Area(df['signal_time'], label='signal', **dims)
    events_time = hv.Area(df['events_time'], label='events', **dims)
    scene_time  = hv.Area(df['scene_time'],  label='scene',  **dims)

    overlay = (signal_time * events_time * scene_time)
    hv.renderer('matplotlib').show(overlay)
    return overlay


def main(path=None):
    import sys
    path = Path(path or sys.argv[1])

    if path.suffix == '.csv':
        with open(path, 'r') as file:
            df = pd.read_csv(file)

    elif path.suffix == '.feather':
        with open(path, 'rb') as file:
            df = pd.read_feather(file)

    else:
        raise ValueError("Please provide a path to a CSV or Feather file.")


    process(df)
#    plot(df)
    for column in ['signal', 'events', 'scene', 'sleep']:
        col = df[f"{column}_time"]
        print(f"{column} for {col.mean()}s, std. dev. {col.std()}s")

    delta_time = df['delta_time']
    print(f"Output frame every {delta_time.mean()}s, std. dev. {delta_time.std()}s")

    return df


if __name__ == "__main__":
    main()
