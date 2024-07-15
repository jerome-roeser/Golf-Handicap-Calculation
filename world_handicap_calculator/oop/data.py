import pandas as pd
import sqlite3
from world_handicap_calculator.params import *

class Golfshot():

    def get_data(self) -> pd.DataFrame:
        database = Path(LOCAL_DATA_PATH).joinpath('golf.sqlite')
        conn = sqlite3.connect(database= database)
        c = conn.cursor()

        query = """
                SELECT
                    s.roundId,
                    s.playerId,
                    h.courseId,
                    s.facility_name,
                    s.course_name,
                    s.city,
                    s.scoring_type,
                    h.teebox,
                    h.slope,
                    h.rating,
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
        df.drop_duplicates(inplace=True)
        conn.close()

        return df
