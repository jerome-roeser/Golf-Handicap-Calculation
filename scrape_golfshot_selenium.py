# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 15:34:34 2023

@author: Jerome Roeser
"""


# import time
import pandas as pd

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

login = "jerome.roeser@gmail.com"
password = "123AZE"


# webdriver = r"C:\Users\roeser\Downloads\install_files\chromedriver_win32"
webdriver = r"C:/Users/Jerome Roeser/Documents/chromedriver.exe"
# webdriver = r"W:/Documents/finxter/projects/chromedriver.exe" #change me!
#^Download from: https://chromedriver.chromium.org/


driver = Chrome(executable_path=webdriver)


driver.get("https://play.golfshot.com/signin")

# Find and fill in the username & password fields
username_field = driver.find_element_by_name('Email')
username_field.send_keys(login)
password_field = driver.find_element_by_name('Password')
password_field.send_keys(password)

password_field.send_keys(Keys.RETURN)


base_url = 'https://play.golfshot.com'
round_ids = driver.find_elements_by_tag_name('tr')
suffixes = [i.get_attribute('data-href') for i in round_ids]
for i, suffix in enumerate(suffixes[2:7]):
    url_round_id = base_url + suffix
    driver.get(url_round_id)
    
    lines = driver.find_elements_by_tag_name('li')
    info = [i.text for i in lines if i.text]
    
    dfs = pd.read_html(driver.page_source, index_col=0)
    dfs[0].to_excel(f'scorecard_imports/scorecard_{i}.xlsx')
    # if not tournament:()
    #     df[0].to_excel(
    #         f'{player_name}_{date}_{score}_{golf_course}_{tees}_{slope}_{sss}_casual.xlsx')
    # else:
    #     df[0].to_excel(
    #         f'{player_name}_{date}_{score}_{golf_course}_{tees}_{slope}_{sss}_tournament.xlsx')
    # print(dfs[0])


# driver.quit()
