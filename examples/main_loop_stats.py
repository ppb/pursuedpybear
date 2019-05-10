#!/usr/bin/env python3
from pathlib import Path

import numpy as np
import pandas as pd

COLUMNS = ('signal', 'events', 'gc')

def process(df):
    for start, end in zip(['start']+list(COLUMNS), COLUMNS):
        time_column = f"{end}_time"
        df[time_column] = df[end] - df[start]

    next_start = df['start'].shift(-1)
    df['delta_time'] = next_start - df['start']
    df['sleep_time'] = next_start - df[COLUMNS[-1]]
    df['fps'] = 1 / df['delta_time']


def plot(df, show=True):
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns

    ax = df.plot.area(
        stacked=True, alpha=0.5, title="Per-phase execution times",
        y=[f"{c}_time" for c in COLUMNS],
    )

    if show:
        plt.show()

def main(path=None):
    import sys

    if path is not None:
        path = Path(path)
    elif len(sys.argv) >= 2:
        path = Path(sys.argv[1])
    else:
        path = Path(__name__).parent / 'hugs_stats.feather'

    if path.suffix == '.csv':
        with open(path, 'r') as file:
            df = pd.read_csv(file)

    elif path.suffix == '.feather':
        with open(path, 'rb') as file:
            df = pd.read_feather(file)

    else:
        raise ValueError("Please provide a path to a CSV or Feather file.")


    process(df)
    for column in list(COLUMNS) + ['sleep']:
        col = df[f"{column}_time"]
        print(f"{column} for {col.mean()}s, std. dev. {col.std()}s")

    delta_time = df['delta_time']
    print(f"Output frame every {delta_time.mean()}s, std. dev. {delta_time.std()}s")

    return plot(df)


if __name__ == "__main__":
    main()
