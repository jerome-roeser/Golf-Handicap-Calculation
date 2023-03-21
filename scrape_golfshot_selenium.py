# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 15:34:34 2023

@author: Jerome Roeser
"""


# import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

import argparse
import pandas as pd


USER_NAME = 'jerome.roeser@gmail.com'

parser = argparse.ArgumentParser(description='Download GolfShot data')
parser.add_argument('username', type=str, nargs='?', help='Username for GolfShot account')
parser.add_argument('password', type=str, help='Password for GolfShot account')
args = parser.parse_args()

login = args.username if args.username else USER_NAME
password = args.password


# webdriver = r"C:\Users\roeser\Downloads\install_files\chromedriver_win32"
# webdriver = r"C:/Users/Jerome Roeser/Documents/chromedriver.exe"
webdriver = r"C:/temp/git_repos/chromedriver.exe"
# webdriver = r"W:/Documents/finxter/projects/chromedriver.exe" #change me!
# WebDriver = 'C:/temp/git_repos/chromedriver.exe'
#^Download from: https://chromedriver.chromium.org/

# service = Service(WebDriver)
# driver = webdriver.Chrome(service=service)
driver = Chrome(executable_path=webdriver)


driver.get("https://play.golfshot.com/signin")

# Find and fill in the username & password fields
username_field = driver.find_element('name','Email')
username_field.send_keys(login)
password_field = driver.find_element('name','Password')
password_field.send_keys(password)

password_field.send_keys(Keys.RETURN)


base_url = 'https://play.golfshot.com'
round_ids = driver.find_elements('tag name','tr')
suffixes = [i.get_attribute('data-href') for i in round_ids]
for i, suffix in enumerate(suffixes[2:7]):
    url_round_id = base_url + suffix
    driver.get(url_round_id)
    
    # lines = driver.find_elements('tag name', 'li')
    # info = [i.text for i in lines if i.text]
    profile = driver.find_elements('class name', 'profile')[0].text.split('\n')
    player_name = profile[1]
    player_handicap = float(profile[0])
    golf_course = profile[9]
    golf_course_tees = profile[10]
    round_date = profile[11]
    
    
    
    dfs = pd.read_html(driver.page_source, index_col=0)
    dfs[0].to_excel(f'data/scorecards/{player_name}_hcp-{player_handicap}_{golf_course}_{round_date}.xlsx')
    # if not tournament:()
    #     df[0].to_excel(
    #         f'{player_name}_hcp-{date}_{score}_{golf_course}_{tees}_{slope}_{sss}_casual.xlsx')
    # else:
    #     df[0].to_excel(
    #         f'{player_name}_{date}_{score}_{golf_course}_{tees}_{slope}_{sss}_tournament.xlsx')
    # print(dfs[0])


# driver.quit()
