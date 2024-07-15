import pandas as pd
import numpy as np

from world_handicap_calculator.oop.data import Golfshot


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

        # calculate initial SBA
        df['CR'] = np.apply_along_axis(lambda row: \
            row[0] // 18 + 1 if row[1] <= row[0] // 18 else row[0] // 18, \
                axis= 1, \
                arr= df[['course_hcp', 'hcp']].values)
        df['net_double_bogey'] = df['par'] + df['CR'] + 2
        df['SBA'] = np.where(df['strokes'] < df['net_double_bogey'], \
                            df['strokes'], \
                            df['net_double_bogey'])

        # fix issue with rating of 9 holes courses
        df['rating'] = df['rating'].apply(lambda x: x * 2 if x < 60 else x)

        # if 9 holes played then an additional stroke should be added to the SBA
        group = df.groupby('roundId')
        df_sum = group.sum()

        df_sum['holes_played'] = df.groupby(['roundId', 'hole']).count() \
                                    .groupby('roundId').sum()['strokes']
        df_sum['additional_stroke'] = \
            df_sum['holes_played'].map(lambda x: 1 if x == 9 else 0)

        df_sum['adjusted_SBA'] = df_sum['SBA'] + df_sum['additional_stroke']

        # calculate gross differential score from adjsusted SBA, slope and rating
        df_diff = pd.concat(
            [df.groupby('roundId').first()[['slope', 'rating']],
            df_sum['adjusted_SBA']], axis=1)
        df_diff['Diff'] = \
            np.apply_along_axis(lambda x: round((113/x[0]) * (x[2]-x[1]), 1), \
                1, df_diff.values)
        df_diff.rename(columns={'adjusted_SBA': 'SBA'}, inplace=True)

        return df_diff[['SBA', 'Diff']].reset_index()

    def get_rounds_data(self):
        rounds_data = self.get_round_details()\
            .merge(self.get_scoring_data(), on='roundId')\
            .merge(self.get_sba_and_diff(), on='roundId')
        rounds_data.sort_values(by='start_date', ascending=False ,inplace=True)
        return rounds_data
