def parse_scorecard_from_shotzoom(link=SHOTZOOM_URL, number_of_rounds=4, tournament=False):
    """
    takes as argument a shotzoom id link
    takes as argument the number of scorecareds that should be imported (default=1)
    creates scorecards as excel files
    name format: player-name_player-hcp_date_score_golf-course_color-of-tees_slope_sss.xlsx
    if competition: add: "tournament" in the name of the file 
    """
    base_url = 'https://shotzoom.com'
    entries = requests.get(link)
    s = BeautifulSoup(entries.content, 'html.parser')
    round_ids = s.find_all('td', {'class': 'score'})

    player_name = s.find('span', {'class': 'name'}).text
    for round_id in round_ids[:number_of_rounds]:
        suffix = round_id.a['href']
        url_round_id = base_url + suffix
        data_round_id = s.find_all('a', {'href': suffix})
        golf_course = data_round_id[1].text.strip()
        score = int(data_round_id[2].text)
        res = requests.get(url_round_id)
        soup = BeautifulSoup(res.content, 'html.parser')
        rating_and_slope = soup.find(
            'span', {'class': 'ratingAnadSlope'}).text.split()
        summary = soup.find('small').text.split()
        date = '-'.join(summary[-3:])
        tees = '-'.join(rating_and_slope[1:3])
        slope = int(rating_and_slope[-1])
        sss = float(rating_and_slope[-3])
        df = pd.read_html(res.text, index_col=0)
        df[0].iloc[:6] = df[0].iloc[:6].apply(pd.to_numeric, errors='coerce')
        df[0].iloc[-3:] = df[0].iloc[-3:].apply(pd.to_numeric, errors='coerce')
        if not tournament:
            df[0].to_excel(
                f'{player_name}_{date}_{score}_{golf_course}_{tees}_{slope}_{sss}_casual.xlsx')
        else:
            df[0].to_excel(
                f'{player_name}_{date}_{score}_{golf_course}_{tees}_{slope}_{sss}_tournament.xlsx')
    return

def get_current_index(player, file=FFG_STYLE_FILE):
    """
    checks the data in ffg style table stored in an excel file
    returns the player's current index
    """
    df = pd.read_excel(file)
    return df.Idx[0]

def get_course_handicap(hcp_player, slope):
    """
    takes a palyer handicap and a course slope (int) as arguments
    returns course handicap (int)
    """
    return round(hcp_player*slope/113)

def get_round_info(scorecard, hcp_player):
    df = process_scorecard_for_index_calculation(scorecard, hcp_player)  
    l = [x for x in scorecard.split('_')]
    coup_supp = 0
    if df.loc['Score'].isna().any():
        coup_supp += 1
        slope = slope * 2
        sss = sss * 2
    
    date_dt = l[1] #pd.to_datetime(l[6])#.strftime('%a %d-%m-%Y')
    sba = df.loc["SBA"].sum() + coup_supp
    score_diff = round((113/slope) * (sba-sss), 1)
        
    return [dict({'date': date_dt, 'score brut ajusté': sba, 
                  'score différentiel': score_diff, 'nouvel index': hcp_player}), df]


def get_scorecard_metadata(scorecard):
    df = get_scorecard_dataframe(scorecard)
    data = [x for x in scorecard.split('_')]
    player = data[0]
    hcp_player = get_current_index(player)
    slope, sss = float(data[-3]), float(data[-2])
    coup_supp = 0
    if df.loc['Score'].isna().any():
        coup_supp += 1
        slope = slope * 2
        sss = sss * 2
    return dict({'player_name':data[0],
                    'hcp_player': hcp_player,
                    'slope': slope,
                    'sss': sss})

    # index_calc()
    # export_tableau_index()
    # create tableau index with last x rounds 
    
    
    # # calculate index for each row
    # for i in range(len(df_scores)):
    #     df_scores.iloc[i, 3] = index_calc(df_scores.iloc[0:i+1, 2])
    
    # current_index = ''
       
    # # export file
    # df.to_excel('')
    
    # scorecards = []
    # for p in path.iterdir():
    #     if p.is_file() and p.match('Jerome*'):
    #         scorecards.append(p.name)
    # print('On dénombre', len(scorecards), 'carte(s) de scores')
    # # # print(f'{player} a initialement un handicap de {hcp_player}...\n')
    # # # print(f'{player} a {hcp_course} coups rendus\n')
    # #scorecard_list = []
    # for scorecard in scorecards[-20:]:
    #     scorecard_list.append(sba_calc(scorecard))
    
    # df_scores = pd.DataFrame(scorecard_list).sort_values('date')
   
    
    
    # df_scores.to_excel('tableau_index.xlsx')
    
    # # print(f'{player} a désormais un handicap de', df_scores.iloc[-1,-1])    
    # print('Ci-joint le tableau d\'index:\n\n', df_scores)

# print('On dénombre', len(scorecards), 'carte(s) de scores')
    # # print(f'{player} a initialement un handicap de {hcp_player}...\n')
    # # print(f'{player} a {hcp_course} coups rendus\n')
    
    # scorecard_list = []
    
    # for scorecard in scorecards:
    #     scorecard_list.append(sba_calc(scorecard))
    
    # df_scores = pd.DataFrame(scorecard_list).sort_values('date')
    
    # for i in range(len(df_scores)):
    #     df_scores.iloc[i, 3] = index_calc(df_scores.iloc[0:i+1, 2])
    
    # df_scores.to_excel('tableau_index.xlsx')
    
    # # print(f'{player} a désormais un handicap de', df_scores.iloc[-1,-1])    
    # print('Ci-joint le tableau d\'index:\n\n', df_scores)

# if __name__ == '__main__':
#     print('Checking scorecards...')

#     parser = argparse.ArgumentParser(description='Filter email addresses by disposable domains.')
#     parser.add_argument('-i', type=str, nargs='?', help='Path of input file with the email addresses.')
#     parser.add_argument('-o', type=str, nargs='?', help='Path where the output will be put.')
#     parser.add_argument('-r', action='store_true', help='Refresh local copy of the disposable domains file.')
    
#      args = parser.parse_args()

#     path_input = args.i if args.i else DEFAULT_INPUT
#     path_output = args.o if args.o else DEFAULT_OUTPUT
#     refresh = args.r
   
#     try:
#         mails_count = check_mails(path_input, path_output, refresh)
#         print(f'Copied {mails_count} email addresses to the output file.')
#         print('Done.')
#     except:
#         print(f'Sorry, an unexpected error ({sys.exc_info()[1]}) occurred!\nCall filtermails.py -h for help.')
    
#%% classes: 
    
# class Player():
#     """
#     A player
#     """
#     def __init__(self, name, index=54):
#         self.name = name
#         self.index = index
        
#     def __repr__(self):
#         return f"<{self.name} ; {self.index} >"
    
#     def __str__(self):
#         return f"{self.name}, hcp:{self.index}, coups_rendus:{self.coups_rendus}"
    
#     def course_handicap(self, slope):
#         """
#         course handicap depends on plyer index and course slope
#         """
#         return round(self.index * slope / 113)
        
        
# class Course():
#     """
#     A golf course
#     """
#     def __init__(self, name, tee, SSS, slope, par, scorecard):
#         self.name = name
#         self.par = par
#         self.slope = slope
        
#     def __repr__(self):
#         return f"<{self.name} ; {self.par} >"
    
#     def __str__(self):
#         return f"{self.name}, hcp:{self.par}, coups_rendus:{self.coups_rendus}"
        
# class Round():
#     """
#     A golf round. Has a date.
#     """
#     def __init__(self, date, score, course):
#         self.date = date
#         self.score = score
        
#     def __repr__(self):
#         return f"<{self.name} ; {self.index} >"
    
#     def __str__(self):
#         return f"{self.name}, hcp:{self.index}, coups_rendus:{self.coups_rendus}"


#%% inputs: scorecard, player
#TODO: clean import from golfshot
#TODO: web scraping Golfshot
#TODO: scorecard 
#TODO: sba_calc with adjusted hcp_course
#TODO: sba_calc for 9 holes rounds 
#TODO: export to excel
#TODO: needed data: hcp, slope, sss, date, name, competition

# with open('saved_dictionary.pkl', 'wb') as f:
#     pickle.dump(dfs, f)
    
# with open('saved_dictionary.pkl', 'rb') as f:
#     dfs_loaded = pickle.load(f)

    
