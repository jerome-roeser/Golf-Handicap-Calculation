import datetime as dt
import json
import sqlite3

from pathlib import Path
from world_handicap_calculator.params import *


def create_courses_table(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # re-initilize the table
    try:
        c.execute("""DROP TABLE courses""")
        conn.commit()
    except:
        pass

    query = """
            CREATE TABLE courses(
                courseId VARCHAR(20) PRIMARY KEY,
                courseName VARCHAR(100),
                courseUuid VARCHAR(100))
            """
    c.execute(query)
    conn.commit()

    courses = [doc for doc in Path(COURSES_DIRECTORY).iterdir()]
    for i in range(len(courses)):
        with open(courses[i]) as f:
            data = json.load(f)
        id = data['courseId'].split('-')[0]
        name = ' '.join(courses[i].stem.split('-')[1:])
        uuid = data['courseUuid']
        course_data = (id, name, uuid)

        c.execute("""
                INSERT INTO courses
                    (courseId, courseName, courseUuid)
                VALUES(?, ?, ?)
                """, course_data)
        conn.commit()

def create_holes_table(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # re-initilize the table
    try:
        c.execute("""DROP TABLE holes""")
        conn.commit()
    except:
        pass

    query = """
            CREATE TABLE holes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                courseId VARCHAR(20),
                hole VARCHAR(20),
                teebox VARCHAR(20),
                slope INTEGER,
                rating INTEGER,
                distance_yards INTEGER,
                par INTEGER,
                hcp INTEGER,
                FOREIGN KEY(courseId) REFERENCES courses(courseId)
            )"""
    c.execute(query)
    conn.commit()

    courses = [doc for doc in Path(COURSES_DIRECTORY).iterdir()]
    for i in range(len(courses)):
        with open(courses[i]) as f:
            data = json.load(f)
        hole_data = []
        cell_lengths = data['scorecard']['holes']['cellCount']
        number_of_backTeeboxes = len(data['scorecard']['backTeeboxes']['teeboxes'])
        number_of_forwardTteeboxes = len(data['scorecard']['forwardTeeboxes']['teeboxes'])

        for teebox in range(number_of_backTeeboxes):
            for cell in range(cell_lengths):
                cell_data = {}
                cell_data['courseId'] = data['courseId'].split('-')[0]
                cell_data['hole'] = data['scorecard']['holes']['cells'][cell]['value']
                cell_data['par'] = int(data['scorecard']['backTeeboxes']['par']['cells'][cell]['value'])
                cell_data['hcp'] = data['scorecard']['backTeeboxes']['handicaps']['cells'][cell]['value']

                teebox_data = data['scorecard']['backTeeboxes']['teeboxes'][teebox]
                cell_data['teebox'] = teebox_data['color']
                cell_data['slope'] = teebox_data['slope']
                cell_data['rating'] = teebox_data['rating']
                cell_data['distance_yards'] = teebox_data['cells'][cell]['yards']
                hole_data.append(cell_data)

        cells = tuple(hole_data)
        c.executemany("""
                    INSERT INTO holes(
                            courseId,
                            hole,
                            par,
                            hcp,
                            teebox,
                            slope,
                            rating,
                            distance_yards
                        )
                    VALUES(
                        :courseId,
                        :hole,
                        :par,
                        :hcp,
                        :teebox,
                        :slope,
                        :rating,
                        :distance_yards
                        )""", cells)
        conn.commit()

def create_scores_table(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    try:
        c.execute("""DROP TABLE scores""")
        conn.commit()
    except:
        pass

    query = """
            CREATE TABLE scores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                courseId VARCHAR(20),
                city VARCHAR(100),
                course_name VARCHAR(100),
                facility_name VARCHAR(100),
                roundId VARCHAR(20),
                playerId VARCHAR(20),
                player_name VARCHAR(100),
                start_date DATETIME,
                scoring_type VARCHAR(20),
                pace_of_play FLOAT,
                course_hcp FLOAT,
                holes INTEGER,
                strokes INTEGER,
                FOREIGN KEY(courseId) REFERENCES courses(courseId)
            )
            """
    c.execute(query)
    conn.commit()

    rounds = [doc for doc in Path(ROUNDS_DIRECTORY).iterdir()]
    for i in range(len(rounds)):
        with open(rounds[i]) as f:
            data = json.load(f)
        round_data = []
        number_of_teams = len(data['model']['game']['teams'])

        for team in range(number_of_teams):
            number_of_players = len(data['model']['game'] \
                                        ['teams'][team]['players'])
            for player in range(number_of_players):
                number_of_holes = len(data['model']['game'] \
                                        ['teams'][team]['players'][0]['scores'])
                for hole in range(number_of_holes):
                    cell_data = {}
                    cell_data['courseId'] = data['model']['detail'] \
                                        ['golfCourseWebId'].split('-')[0]
                    cell_data['roundId'] = data['roundGroupId']
                    cell_data['playerId'] = data['userAccountId']
                    cell_data['player_name'] = data['model']['game'] \
                                        ['teams'][team] \
                                        ['players'][player]['name']
                    cell_data['start_date'] = dt.datetime.strptime(\
                                                data['model']['detail'] \
                                                    ['formattedStartTime'], \
                                                    '%b %d, %Y')
                    pace_of_play_formatted = data['model']['detail'] \
                                            ['formattedPaceOfPlay'].split(':')
                    cell_data['pace_of_play'] = dt.timedelta( \
                                        hours=int(pace_of_play_formatted[0]), \
                                        minutes=int(pace_of_play_formatted[1])) \
                                        .total_seconds() // 60
                    cell_data['course_hcp'] = float(data['model']['detail'] \
                                            ['formattedCourseHandicap'])
                    cell_data['holes'] = data['model']['header']['holes'][hole]
                    cell_data['strokes'] = data['model']['game']['teams'][team] \
                                    ['players'][player]['scores'][hole]['score']
                    cell_data['city'] = data['model']['detail']['city']
                    cell_data['course_name'] = data['model']['detail'] \
                                                ['courseName']
                    cell_data['facility_name'] = data['model']['detail'] \
                                                ['facilityName'].split('-')[0]
                    cell_data['scoring_type'] = data['model']['detail']['scoringType']

                    round_data.append(cell_data)

        cells = tuple(round_data)
        c.executemany("""
                      INSERT INTO scores(
                          courseId,
                          roundId,
                          city,
                          course_name,
                          facility_name,
                          playerId,
                          player_name,
                          scoring_type,
                          course_hcp,
                          holes,
                          strokes,
                          start_date,
                          pace_of_play
                        )
                    VALUES(
                        :courseId,
                        :roundId,
                        :city,
                        :course_name,
                        :facility_name,
                        :playerId,
                        :player_name,
                        :scoring_type,
                        :course_hcp,
                        :holes,
                        :strokes,
                        :start_date,
                        :pace_of_play
                    )""", cells)
        conn.commit()

if __name__ == '__main__':
    database = Path(LOCAL_DATA_PATH).joinpath('golf.sqlite')
    create_courses_table(database)
    create_holes_table(database)
    create_scores_table(database)
