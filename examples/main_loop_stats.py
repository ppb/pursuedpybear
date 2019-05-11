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


def frames(df):
    return df.plot.area(
        stacked=False, alpha=0.5, title="Interframe times",
        y=['delta_time', 'sleep_time'],
    )


def phases(df):
    return df.plot.area(
        stacked=True, alpha=0.5, title="Per-phase execution times",
        y=[f"{c}_time" for c in COLUMNS],
    )



def plot(df, plotgen, *, show=False, save=None):
    import matplotlib
    import matplotlib.pyplot as plt
    import seaborn as sns

    if show:
        plotgen(df)
        plt.show()

    if save is not None:
        plotgen(df)
        plt.savefig(save)


def print_stats(df):
    for column in list(COLUMNS) + ['sleep']:
        col = df[f"{column}_time"]
        print(f"{column} for {col.mean()}s, std. dev. {col.std()}s")

    delta_time = df['delta_time']
    print(f"Output frame every {1000 * delta_time.mean()}ms ({1/delta_time.mean()} fps), "
          f"std. dev. {1000 * delta_time.std()}ms")


def cli(args=None):
    from pathlib import Path
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument('--phase-out', '-p', dest='phase',
                        type=Path,
                        help="Save the phase timing chart.")

    parser.add_argument('--frame-out', '-f', dest='frame',
                        type=Path,
                        help="Save the phase timing chart.")

    parser.add_argument('--show', '-s',
                        action="store_true",
                        help="Display the charts before saving.")

    parser.add_argument('data', type=Path,
                        default=Path(__name__).parent / 'hugs_stats.feather')

    return parser.parse_args(args)


def main(args=None):
    opts = cli(args)

    if opts.data.suffix == '.csv':
        with open(opts.data, 'r') as file:
            df = pd.read_csv(file)

    elif opts.data.suffix == '.feather':
        with open(opts.data, 'rb') as file:
            df = pd.read_feather(file)

    else:
        raise ValueError("Please provide a path to a CSV or Feather file.")


    process(df)

    print_stats(df)

    plot(df, phases, show=opts.show, save=opts.phase)
    plot(df, frames, show=opts.show, save=opts.frame)


if __name__ == "__main__":
    main()
