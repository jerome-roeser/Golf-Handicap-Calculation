# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:03:38 2022

@author: roeser

update WHS for a player
input should be a scorecard.
course data include: slope, course handicap (derived from player handicap)
départ
PAR

"""

import argparse
from datetime import datetime
from getpass import getpass
from pathlib import Path
from scrape_scorecards import scrape_golfshot
import pandas as pd
import numpy as np


SHOTZOOM_URL = 'https://shotzoom.com/92836531767/golf'
FFG_STYLE_FILE = 'fiche_historique_index_JR.xlsx'
USER_NAME = 'jerome.roeser@gmail.com'
NUMBER_OF_ROUNDS = 1
player = 'Jerome Roeser'


def get_scorecard_list_from_folder(player, last_round=5):
    """
    This function searches for Excel scorecards in a specified folder for a given player and returns a
    list of their filenames.
    
    :param player: The name of the player whose scorecards are being searched for
    :param last_round: The parameter `last_round` is an optional integer parameter with a default value
    of 5. It is used to specify the maximum number of scorecards to be returned for the given player. If
    not specified, the function will return a maximum of 5 scorecards, defaults to 5 (optional)
    :return: a list of file names (strings) that match the input player name and are located in the
    specified folder path.
    """
    path = Path('./data/scorecards/')
    scorecard_list = []
    for p in path.iterdir():
        if p.is_file() and p.match(f'{player}*'):
            scorecard_list.append(p.name)
    return scorecard_list


def get_scorecard_dataframe(scorecard):
    """
    The function takes an excel file as an argument and returns a dataframe.
    
    :param scorecard: The parameter "scorecard" is a string that represents the name of an Excel file
    that contains a scorecard
    :return: A pandas dataframe is being returned.
    """
    path_to_scorecard = f'data/scorecards/{scorecard}'
    return pd.read_excel(path_to_scorecard, index_col=0)


def process_scorecard(scorecard):
    """
    The function processes a golf scorecard by converting certain columns to numeric values, calculating
    course rating and slope, and returning a dataframe with the relevant information.
    
    :param scorecard: The scorecard parameter is a string containing information about a golf course's
    holes, including par, handicap, and score information
    :return: a pandas DataFrame that has been processed and modified based on the input scorecard.
    """
    df = get_scorecard_dataframe(scorecard)
    df.iloc[:6] = df.iloc[:6].apply(pd.to_numeric, errors='coerce')
    df.iloc[-3:] = df.iloc[-3:].apply(pd.to_numeric, errors='coerce')
    l = [x for x in scorecard.split('_')]
    hcp_course = float(l[4][-9:-6])

    # sort out columns and calculate CR and SBA from course handicap
    df = df.iloc[1:4].drop(columns=['Out', 'In', 'Total'])
    df.loc['CR'] = [hcp_course // 18 + 1
                    if df.loc['Handicap'][i] <= hcp_course % 18
                    else hcp_course // 18
                    for i in range(0, 18)]
    df.fillna(df.loc['Par'] + df.loc['CR'], inplace=True)
    df.loc['ndb'] = df.loc['Par'] + df.loc['CR'] + 2
    df.loc["SBA"] = [df.iloc[2][i]
                     if df.iloc[2][i] < df.loc['ndb'][i]
                     else df.loc['ndb'][i]
                     for i in range(0, 18)]
    return df


def process_scorecard_9_holes(scorecard):
    """

    """
    df = get_scorecard_dataframe(scorecard)
    df.iloc[:6] = df.iloc[:6].apply(pd.to_numeric, errors='coerce')
    df.iloc[-3:] = df.iloc[-3:].apply(pd.to_numeric, errors='coerce')
    l = [x for x in scorecard.split('_')]
    hcp_course = float(l[4][-9:-6])

    # sort out columns and calculate CR and SBA from course handicap
    df = pd.concat([df, df], axis=1)
    df = df.iloc[1:4].drop(columns=['Out', 'Total'])

    df.loc['CR'] = [hcp_course // 18 + 1
                    if df.loc['Handicap'][i] <= hcp_course % 18
                    else hcp_course // 18
                    for i in range(0, 18)]
    df.fillna(df.loc['Par'] + df.loc['CR'], inplace=True)
    df.loc['ndb'] = df.loc['Par'] + df.loc['CR'] + 2
    df.loc["SBA"] = [df.iloc[2][i]
                     if df.iloc[2][i] < df.loc['ndb'][i]
                     else df.loc['ndb'][i]
                     for i in range(0, 18)]
    return df


def is_full_round(scorecard):
    """
    The function checks if a scorecard is a full round by verifying if it has 21 columns and no missing
    values in the fifth row.
    
    :param scorecard: The scorecard parameter is a data structure that contains information about a
    round of golf, such as the scores for each hole and the player's name. It could be a dictionary, a
    list, or any other data structure that can hold this information
    :return: a boolean value (True or False) depending on whether the input scorecard is a full round or
    not.
    """
    df = get_scorecard_dataframe(scorecard)
    if df.iloc[4].isna().any() or len(df.columns) < 21:
        return False
    else:
        return True


def starting_tee(scorecard):
    """
    The function returns the starting tee for a golf round based on the scorecard provided.
    
    :param scorecard: The scorecard parameter is a data structure that contains information about a
    round of golf, such as the player's name, the course being played, and the scores for each hole. It
    could be a dictionary, a list, or any other data structure that can hold this information
    :return: The function `starting_tee` returns an integer value, either 10 or 1, depending on the
    conditions specified in the code.
    """
    df = get_scorecard_dataframe(scorecard).fillna(0)
    if not is_full_round(scorecard) and df.iloc[3, 0] == 0:
        return 10
    else:
        return 1


def Nbt_entry(scorecard):
    """
    The function returns the appropriate next tee box entry for a golf scorecard based on whether it is
    a full round or not and which tee box the player started on.
    
    :param scorecard: It is a data structure that represents the scores of a golfer for each hole in a
    round of golf. It could be a list, dictionary, or any other data structure that allows for storing
    and accessing scores for each hole
    :return: The function `Nbt_entry` returns either the integer `18`, the string `'9A'`, or the string
    `'9R'`. The specific value returned depends on the input `scorecard` and the results of the
    `is_full_round` and `starting_tee` functions.
    """
    if is_full_round(scorecard):
        return 18
    elif not is_full_round(scorecard) and starting_tee(scorecard) == 1:
        return '9A'
    else:
        return '9R'


def score_brut_ajuste(scorecard):
    "calculate SBA for 18 and 9 holes scorecards."
    l = [x for x in scorecard.split('_')]
    df = get_scorecard_dataframe(scorecard)
    coup_supp = 0
    sss = float(l[3].split()[-2])
    slope = int(l[3].split()[-1])
    # for 9 holes scorecards (front or back) of a 18 holes course
    if df.iloc[4].isna().any():
        processed_df = process_scorecard(scorecard)
        coup_supp += 1
    # for 9 holes scorecards of a 9 holes course 
    elif len(df.columns) < 21:
        processed_df = process_scorecard_9_holes(scorecard)
        coup_supp += 1
        # slope = slope * 2
        sss = sss * 2
    else:
        processed_df = process_scorecard(scorecard)
    sba = int(sum(processed_df.loc['SBA'])) + coup_supp
    return sba


def score_differentiel(sba, slope, sss):
    """
    The function calculates the differential score between a player's score average and the course
    rating based on the slope rating.
    
    :param sba: Stands for "Starch Breakdown Ability". It is a measure of the ability of flour to break
    down starch into simple sugars during baking
    :param slope: The slope is a measure of the steepness of a line. In this context, it is likely
    referring to the slope of a golf course, which is a measure of the difficulty of the course. A
    higher slope indicates a more difficult course
    :param sss: The sss parameter is likely an abbreviation for "standard scratch score," which is a
    measure of the difficulty of a golf course. It is used to calculate a golfer's handicap
    :return: the score differential calculated using the formula: (113/slope) * (sba-sss), rounded to
    one decimal place.
    """
    return round((113/slope) * (sba-sss), 1)


def table_row(scorecard):
    """returns a dictionary from a scorecard which can be used as
      a row for the final excel file"""
    l = [x for x in scorecard.split('_')]
    df = get_scorecard_dataframe(scorecard)
    sss = float(l[3].split()[-2])
    slope = int(l[3].split()[-1])
    sba = score_brut_ajuste(scorecard)
    return dict({'N°': '',  # set as index?
                 'Nom': l[0],  # ?? Profile
                 'T': starting_tee(scorecard),  # 1 or 10
                #  'Date': datetime.strptime(l[1], '%b %d %Y'), #profile
                 'Date': l[1],
                 'NbT': Nbt_entry(scorecard),  # 9A, 9R or 18
                 'Fml': '',  # Strokeplay or Stableford Profile
                 'Golf': l[2],  # Profile
                 'Terrain': l[3].split()[0],  # tees? Profile
                 'Rep.': '',  # ??
                 'Par': int(df.Total.loc['Par']),
                 'SSS': sss,
                 'Slope': slope,
                 'Course Handicap': float(l[4][-9:-6]),
                 'Stat.': '',
                 'Score': int(df.Total.iloc[3]),
                 'SBA': sba,
                 'PCC': '',  # ?
                 'Diff': score_differentiel(sba, slope, sss),
                 'Ajst': '',  # ?
                 'Idx': ''
                 })


def fill_index_table(new_rows):
    df = pd.read_excel('templates/_fiche_historique_index.xlsx')
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df = df.drop_duplicates(subset=['Date', 'Score'])
    
    # sort table by descending date 
    df.Date = pd.to_datetime(df.Date)
    df = df.sort_values(by='Date', ascending=False)
    df.Date = df.Date.dt.strftime('%d %B %Y')

    # calculate index on rolling 20 scores 
    df.Idx = index_series_calc(df)
    df.to_excel(f'data/fiche_historique_index_{player}.xlsx', index=False)


def index_calc(entries):
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


def index_series_calc(df):
    "calculate index on rolling 20 scores"
    length = len(df.Diff)
    for i in range(length):
        if i + 20 <= length:
            l = [df.Diff.iloc[i] for i in range(i, i+20)]
        else:
            l = [df.Diff.iloc[i] for i in range(i, length)]
        df.Idx.iloc[i] = index_calc(l)
    return df.Idx


def get_args():
    parser = argparse.ArgumentParser(
        description='Upadte WHS for a player.',
        epilog="""should probably cite examples here instead 
        of writing this silly text"""
    )
    parser.add_argument('-n', '--number', type=int,
                        help='number of scorecards to import (Default = 1 i.e. the last round')
    parser.add_argument('-u', '--username', type=str,
                        help='Username for GolfShot account')
    parser.add_argument('-r', '--refresh', action='store_true',
                        help='Refresh local copy of the disposable domains file.')
    return parser.parse_args()


def main(refresh=False):
    """
    We assume the correct index is updated and used for each round of golf.
    For a scorecard the correct player index is used and thus the correct 
    course handicap is used. As such score brut ajusté and score différentiel
    should be accurate. 
    Main function should update the historique d'index file. 
    Import the local file and add a row entry for every round.
    For each row the index is calculated by taking into account only earlier rounds. 
    Export the historique d'index file
    """
    # parse scorecards in shotzoom and save as excel, create scorecard list
    if refresh:
        # if necessary last 5 or last 20 rounds
        scrape_golfshot(login, password, number_of_rounds)
    scorecard_list = get_scorecard_list_from_folder(
        player)  # if necessary last 5 or last 20 rounds
    entries = [table_row(i) for i in scorecard_list]
    fill_index_table(entries)


if __name__ == '__main__':
    args = get_args()
    number_of_rounds = args.number if args.number else NUMBER_OF_ROUNDS
    login = args.username if args.username else USER_NAME
    refresh = args.refresh
    if refresh:
        password = getpass('Enter your password: ')

    main(refresh)
