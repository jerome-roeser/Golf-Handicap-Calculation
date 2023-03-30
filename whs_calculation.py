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

import requests
import argparse, sys
from bs4 import BeautifulSoup
from getpass import getpass
from pathlib import Path
from scrape_golfshot_selenium import scrape_golfshot
import pandas as pd
import numpy as np


SHOTZOOM_URL = 'https://shotzoom.com/92836531767/golf'
FFG_STYLE_FILE = 'fiche_historique_index_JR.xlsx'
player = 'Jerome Roeser'



def get_scorecard_list_from_folder(player, last_round=5):
    """
    looks for .xlxs scorecards
    Input a player name
    returns a list (dict?) of scorecard dataframes (max 20)
    """
    path = Path('./data/scorecards/')
    scorecard_list = []
    for p in path.iterdir():
        if p.is_file() and p.match(f'{player}*'):
            scorecard_list.append(p.name)
    return scorecard_list


def get_scorecard_dataframe(scorecard):
    """
    takes an excel file as an argument
    returns a dataframe
    """
    path_to_scorecard = f'data/scorecards/{scorecard}'
    return pd.read_excel(path_to_scorecard, index_col=0)

def process_scorecard_for_index_calculation(scorecard):
    """
   
    """
    df = get_scorecard_dataframe(scorecard)
    df.iloc[:6] = df.iloc[:6].apply(pd.to_numeric, errors='coerce')
    df.iloc[-3:] = df.iloc[-3:].apply(pd.to_numeric, errors='coerce')
    l = [x for x in scorecard.split('_')]
    
    
    slope, sss = float(l[3].split()[-1]), float(l[3].split()[-2])
    coup_supp = 0
    if df.iloc[4].isna().any():
        coup_supp += 1
        # slope = slope * 2
        # sss = sss * 2
    hcp_course = float(l[4][-9:-6])
       
    # sort out columns and calculate CR and SBA from course handicap
    df = df.iloc[1:4].drop(columns=['Out','In','Total'])
    df.loc['CR'] = [hcp_course // 18 + 1 
                    if df.loc['Handicap'][i] <= hcp_course % 18 
                    else hcp_course // 18 
                    for i in range(0,18)]
    df.fillna(df.loc['Par']+ df.loc['CR'], inplace=True)
    df.loc['ndb'] = df.loc['Par'] + df.loc['CR'] + 2
    df.loc["SBA"] = [df.iloc[2][i] 
                    if df.iloc[2][i] < df.loc['ndb'][i] 
                    else df.loc['ndb'][i]
                    for i in range(0,18)]
    return df

def is_full_round(scorecard):
    df = get_scorecard_dataframe(scorecard)
    if df.iloc[4].isna().any():
        return False

def starting_tee(scorecard):
    if not is_full_round(scorecard) and df.iloc[4].isna():
        return 10
    else:
        return 1

def fill_index_table(scorecard):
    """returns a dictionary from a scorecard which can be used as
      a row for the final excel file"""
    l = [x for x in scorecard.split('_')]
    df = get_scorecard_dataframe(scorecard)
    processed_df = process_scorecard_for_index_calculation(scorecard)
    return dict({'N°': '', # set as index? 
                 'Nom': l[0], #?? Profile
                 'T': 1, # 1 or 10
                 'Date': l[1], #profile
                 'NbT': 18, # 9A, 9R or 18
                 'Fml': '', # Strokeplay or Stableford Profile
                 'Golf': l[2], # Profile
                 'Terrain': l[3].split()[0], #tees? Profile
                 'Rep.': '', # ??         
                 'Par': int(df.Total.loc['Par']), 
                 'SSS': float(l[3].split()[-2]),
                 'Slope': int(l[3].split()[-1]),
                 'Stat.': '', 
                 'Score': int(df.Total.iloc[3]),
                 'SBA': int(sum(processed_df.loc['SBA'])),
                 'PCC': '', # ?
                 'Diff': '',
                 'Ajst': '', #?
                 'Idx': ''
                 })


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
        return np.mean(sorted_entries[:2]) - 1.0
    elif length <=8:
        return np.mean(sorted_entries[:2])
    elif length <= 11:
        return np.mean(sorted_entries[:3])
    elif length <= 14:
        return np.mean(sorted_entries[:4])
    elif length <= 16:
        return np.mean(sorted_entries[:5])
    elif length <= 18:
        return np.mean(sorted_entries[:6])
    elif length == 19:
        return np.mean(sorted_entries[:7])
    else:
        return np.mean(sorted(entries[-20:])[:8])


def get_args():
    parser = argparse.ArgumentParser(
        description='Upadte WHS for a player.',
        epilog="""should probably cite examples here instead 
        of writing this silly text"""
    )
    parser.add_argument('-r', '--rounds', type=int, help='number of scorecards to import (Default = 1 i.e. the last round')
    parser.add_argument('-u', '--username', type=str, help='Username for GolfShot account')
    return parser.parse_args()
    

def main():
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
    #parse scorecards in shotzoom and save as excel, create scorecard list
    scrape_golfshot(player, password) # if necessary last 5 or last 20 rounds
    scorecard_list = get_scorecard_list_from_folder(player) # if necessary last 5 or last 20 rounds
    entries = [fill_index_table(i) for i in scorecard_list]
    return entries
    

if __name__ == '__main__':
    args = get_args()
    password = getpass('Enter your password: ')

    main()
