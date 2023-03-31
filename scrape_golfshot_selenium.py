# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 15:34:34 2023

@author: Jerome Roeser
"""


# import time
from getpass import getpass
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

import argparse
import pandas as pd


USER_NAME = 'jerome.roeser@gmail.com'
NUMBER_OF_ROUNDS = 20

# webdriver = r"C:\Users\roeser\Downloads\install_files\chromedriver_win32"
# webdriver = r"C:/Users/Jerome Roeser/Documents/chromedriver.exe"
webdriver = r"C:/temp/git_repos/chromedriver.exe"  # change me!
#^Download from: https://chromedriver.chromium.org/


def scrape_golfshot(login, password, number=1):
    driver = Chrome(executable_path=webdriver)
    driver.get("https://play.golfshot.com/signin")

    # Find and fill in the username & password fields
    username_field = driver.find_element('name', 'Email')
    username_field.send_keys(login)
    password_field = driver.find_element('name', 'Password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    base_url = 'https://play.golfshot.com'
    round_ids = driver.find_elements('tag name', 'tr')
    suffixes = [i.get_attribute('data-href') for i in round_ids[2:]]
    for i, suffix in enumerate(suffixes[:number]):
        url_round_id = base_url + suffix
        driver.get(url_round_id)
        profile = driver.find_elements('class name', 'profile')[
            0].text.split('\n')
        player_name = profile[1]
        golf_course = profile[9]
        golf_course_tees = profile[10].replace('/ ', ' ', 1).split(', ')
        course_handicap = golf_course_tees[1]
        round_date = profile[11].replace(', ', ' ', 1).split(',')
        print(f"[+++] {golf_course} on {round_date[0]}...")
        dfs = pd.read_html(driver.page_source, index_col=0)
        dfs[0].iloc[:6] = dfs[0].iloc[:6].apply(pd.to_numeric, errors='coerce')
        dfs[0].iloc[-3:] = dfs[0].iloc[-3:].apply(pd.to_numeric, errors='coerce')
        dfs[0].to_excel(
            f'data/scorecards/{player_name}_{round_date[0]}_{golf_course}_{golf_course_tees[0]}_{course_handicap}.xlsx')
    driver.quit()

def get_args():
    parser = argparse.ArgumentParser(description='Download GolfShot data')
    parser.add_argument('-r', '--rounds', type=int, help='number of scorecards to import (Default = 1 i.e. the last round')
    parser.add_argument('-u', '--username', type=str, help='Username for GolfShot account')
    return parser.parse_args()
    

if __name__ == '__main__':
    args = get_args()
    number_of_rounds = args.rounds if args.rounds else NUMBER_OF_ROUNDS
    login = args.username if args.username else USER_NAME
    password = getpass('Enter your password: ')
    
    print(f'collecting last {number_of_rounds} (type = {type(number_of_rounds)}) scorecards....')

    scrape_golfshot(login, password, number_of_rounds)
