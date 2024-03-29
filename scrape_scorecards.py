from getpass import getpass
from pathlib import Path
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import os

import argparse
import pandas as pd


USER_NAME = os.getenv('USER_NAME')
USER_ID = os.getenv('USER_ID')
NUMBER_OF_ROUNDS = 1

# webdriver = r"C:\Users\roeser\Downloads\install_files\chromedriver_win32"
webdriver = r"C:/Users/Jerome Roeser/Documents/chromedriver.exe"
# webdriver = r"C:/temp/git_repos/chromedriver.exe"  # change me!
# ^Download from: https://chromedriver.chromium.org/


def scrape_golfshot(login, password, profile_id, number=1):
    """
    This function logs into a golf score tracking website, scrapes data from a specified number of
    rounds, and saves the data as Excel files.
    
    :param login: The email or username used to log in to the Golfshot account
    :param password: The password is the login password for the Golfshot account
    :param number: The number parameter is an optional integer that specifies the number of golf rounds
    to scrape. If not provided, it defaults to 1, defaults to 1 (optional)
    """
    driver = Chrome(executable_path=webdriver)
    driver.get("https://play.golfshot.com/signin")

    # Find and fill in the username & password fields
    username_field = driver.find_element('name', 'Email')
    username_field.send_keys(login)
    password_field = driver.find_element('name', 'Password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    base_url = 'https://play.golfshot.com'
    profile_url = base_url + f"/profiles/{profile_id}/rounds?sb=Date&sd=Descending&p=1"
    driver.get(profile_url)
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
        dfs[0].iloc[-3:] = dfs[0].iloc[-3:].apply(
            pd.to_numeric, errors='coerce')
        if not Path(f'data/scorecards/{player_name}').exists():
            Path(f'data/scorecards/{player_name}').mkdir()
        dfs[0].to_excel(
            f'data/scorecards/{player_name}/{player_name}_{round_date[0]}_{golf_course}_{golf_course_tees[0]}_{course_handicap}.xlsx')
    driver.quit()


def get_args():
    """
    This function defines and parses command line arguments for downloading GolfShot data.
    :return: The function `get_args()` is returning the parsed arguments from the command line using the
    `argparse` module.
    """
    parser = argparse.ArgumentParser(description='Download GolfShot data')
    parser.add_argument('-n', '--number', type=int,
                        help='number of scorecards to import (Default = 1 -- the last round)')
    parser.add_argument('-u', '--username', type=str,
                        help='Username for login in GolfShot account')
    parser.add_argument('-i', '--profile_id', type=str,
                        help='the profile id to be screened, if not the data of the user has to be scraped')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    number_of_rounds = args.number if args.number else NUMBER_OF_ROUNDS
    login = args.username if args.username else USER_NAME
    profile_id = args.profile_id if args.profile_id else USER_ID
    password = getpass('Enter your password: ')
    path = Path()
    if not path.joinpath('data/scorecards').exists():
        path.joinpath('data/scorecards').mkdir()

    print(
        f'collecting last {number_of_rounds} (type = {type(number_of_rounds)}) scorecards....')

    scrape_golfshot(login, password, profile_id, number_of_rounds)
