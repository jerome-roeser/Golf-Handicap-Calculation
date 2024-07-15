"""
pseudo-code:
create an table like on the ffg website
for this: create a class for the table
for this: create a class for the player
for this create a class for the round
for this create a class for the course


calculate a round's handicap
calculate a player's handicap
"""

import numpy as np
import pandas as pd
import sqlite3

from pathlib import Path
from world_handicap_calculator.params import *
from world_handicap_calculator.oop.index_table import Rounds

def calculate_index() -> pd.DataFrame:
    rounds_data = Rounds().get_rounds_data()

    return rounds_data


if __name__ == '__main__':
    print(calculate_index())
    df = calculate_index()
    df.SBA.plot(kind='hist', bins= 50)
