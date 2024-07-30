import pandas as pd
import numpy as np

from src.oop.data import Golfshot


class Rounds():
    '''
    DataFrames containing all roundId as index,
    and various properties of these rounds as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Golfshot().get_data()

    def get_round_details(self):
        """
        Returns a DataFrame with:
        roundId, Name, Date, NbH, Scoring Type, Golf, Teebox, Rating, Slope, course_hcp
        """
        mask_columns = ['roundId', 'playerId', 'start_date', 'facility_name',
                    'course_name', 'city', 'scoring_type', 'teebox',
                    'slope', 'rating', 'course_hcp']
        df = self.data.copy()
        df = df[mask_columns].groupby('roundId').first()
        return df.reset_index()

    def get_NbT(self):
        group = self.data.groupby('roundId')
        df = group.agg({'hole': 'first', 'strokes': 'count'}).reset_index()
        df['tuple'] = list(zip(df['hole'], df['strokes']))
        df['NbT'] = df['tuple'].map({
            ('1',9): '9A',
            ('10',9): '9B',
            ('1',18): '18'})
        return df[['roundId', 'NbT']]

    def get_scoring_data(self):
        """
        Returns a DataFrame with:
        roundId, Par, Strokes
        """
        df = self.data[['roundId', 'par', 'strokes']].copy()
        df = df.groupby('roundId').sum().reset_index()

        return df

    def get_sba_and_diff(self):
        """
        Returns a DataFrame with:
        roundId, SBA, Diff
        """
        mask_columns = ['roundId', 'hole', 'hcp', 'slope', 'rating', 'par', 'course_hcp',
                        'strokes']
        df = self.data[mask_columns].copy()
        group = df.groupby('roundId')

        df_diff = group.agg({
            'hole':'first',
            'slope': 'first',
            'rating': 'first',
            'course_hcp': 'first',
            'par': 'sum',
            'strokes': 'sum',
                })
        df_diff['holes_played'] = group.count()['strokes']
        df_diff['CR'] = \
            np.apply_along_axis(\
                lambda row: np.ceil(row[0] * (row[1] / 18)), \
                    axis=1, \
                    arr= df_diff[['course_hcp', 'holes_played']].values)
        df_diff['net_double_bogey'] = df_diff['par'] + df_diff['CR'] + 2
        df_diff['SBA_18_holes'] = \
            np.where(df_diff['strokes'] < df_diff['net_double_bogey'], \
                    df_diff['strokes'], \
                    df_diff['net_double_bogey'])
        df_diff['SBA'] = \
            np.apply_along_axis(\
                lambda row: row[0] + row[1] + row[2] + 1 if row[3] == 9 \
                    else row[2], \
                    axis=1, \
                    arr= df_diff[['par', 'CR', 'SBA_18_holes', 'holes_played']]\
                    .values)

        # calculate differential score
        df_diff['Diff'] = \
            np.apply_along_axis(\
                lambda x: round((113/x[0]) * (x[2]-x[1]), 1), \
                    axis= 1, \
                    arr= df_diff[['slope','rating','SBA']].values)

        # filter out incomplete rounds that can lead to menaningless differentials
        df_diff.query("holes_played == 18 or holes_played == 9", inplace=True)

        # return df, df_diff, group
        return df_diff[['holes_played', 'SBA', 'Diff']].reset_index()

    def get_rounds_data(self):
        rounds_data = self.get_round_details()\
            .merge(self.get_NbT(), on='roundId')\
            .merge(self.get_scoring_data(), on='roundId')\
            .merge(self.get_sba_and_diff(), on='roundId')
        rounds_data = rounds_data.sort_values(by='start_date', ascending=True)\
            .reset_index(drop=True)
        return rounds_data
