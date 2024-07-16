import numpy as np
import pandas as pd

from world_handicap_calculator.params import *
from world_handicap_calculator.oop.index_table import Rounds


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

    rounds_data['Idx'] = rounds_data['Diff']. \
            rolling(window=20, min_periods=1).apply(index_from_diff)

    return rounds_data


if __name__ == '__main__':
    print(calculate_index())
