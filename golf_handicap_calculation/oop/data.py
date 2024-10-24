import pandas as pd
import sqlite3
from golf_handicap_calculation.params import *

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
                    s.teebox,
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
                        AND s.teebox = h.teebox
                        AND s.holes = h.hole
                JOIN courses c
                    ON c.courseId = h.courseId
                WHERE s.strokes IS NOT NULL
                """
        c.execute(query)
        columns = [i[0] for i in c.description]
        data = c.fetchall()

        df = pd.DataFrame(data, columns=columns).sort_values(by= \
                                    ['start_date', 'roundId', 'hole'])
        df.drop_duplicates(inplace=True)
        conn.close()

        return df
