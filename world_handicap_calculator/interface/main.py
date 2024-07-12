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

def process_rounds(database: Path) -> pd.DataFrame:
    conn = sqlite3.connect(database=database)
    c = conn.cursor()

    query = """
            SELECT
                roundId,
                s.playerId,
                h.courseId,
                s.start_date,
                s.pace_of_play,
                s.course_hcp,
                h.hole,
                h.par,
                h.hcp,
                s.strokes
            FROM holes h
            JOIN scores s
                ON s.courseId = h.courseId
                    AND s.holes = h.hole
            JOIN courses c
                ON c.courseId = h.courseId
            """
    c.execute(query)
    columns = [i[0] for i in c.description]
    data = c.fetchall()

    df = pd.DataFrame(data, columns=columns).sort_values(by= \
                                ['start_date', 'roundId', 'hole'])
    conn.close()

    df['CR'] = np.apply_along_axis(lambda row: \
        row[0] // 18 + 1 if row[1] <= row[0] // 18 else row[0] // 18, \
            axis= 1, \
            arr= df[['course_hcp', 'hcp']].values)
    df['net_double_bogey'] = df['par'] + df['CR'] + 2
    df['SBA'] = np.where(df['strokes'] < df['net_double_bogey'], \
                        df['strokes'], \
                        df['net_double_bogey'])

    return df


if __name__ == '__main__':
    database = Path(LOCAL_DATA_PATH).joinpath('golf.sqlite')
    print(process_rounds(database))
