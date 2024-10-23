import numpy as np
import pandas as pd

from golf_handicap_calculation.params import *
from golf_handicap_calculation.oop.differential_scores import Rounds


def index_from_diff(entries):
    """
    calculates the index from a liste of differential scores
    """
    length = len(entries)
    sorted_entries = sorted(entries)
    if length <= 3:
        return sorted_entries[0] - 2.0
    elif length == 4:
        return sorted_entries[0] - 1.0
    elif length == 5:
        return sorted_entries[0]
    elif length == 6:
        return round(np.mean(sorted_entries[:2])) - 1.0
    elif length <= 8:
        return round(np.mean(sorted_entries[:2]))
    elif length <= 11:
        return round(np.mean(sorted_entries[:3]))
    elif length <= 14:
        return round(np.mean(sorted_entries[:4]))
    elif length <= 16:
        return round(np.mean(sorted_entries[:5]))
    elif length <= 18:
        return round(np.mean(sorted_entries[:6]), 1)
    elif length == 19:
        return round(np.mean(sorted_entries[:7]))
    else:
        return round(np.mean(sorted(entries[-20:])[:8]), 1)

def calculate_index() -> pd.DataFrame:
    rounds_data = Rounds().get_rounds_data()

    # calculate index based on last 20 differential scores
    rounds_data['Idx'] = rounds_data['Diff']. \
            rolling(window=20, min_periods=1).apply(index_from_diff)

    # my preference: sort by date in descending order
    rounds_data.sort_values(by='start_date', ascending=False, inplace=True)
    rounds_data.to_csv(Path(LOCAL_DATA_PATH).joinpath('rounds_data.csv'), index=True)

    return rounds_data


if __name__ == '__main__':
    print(calculate_index())
