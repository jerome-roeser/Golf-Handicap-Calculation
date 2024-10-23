
import click
import json
import pandas as pd
import re
import requests

from bs4 import BeautifulSoup
from html.parser import HTMLParser
from lxml import etree
from pathlib import Path
from golf_handicap_calculation.params import *


class RoundParser(HTMLParser):
  def handle_data(self, data):
    # the golfshot model is available in a script block
    if 'Golfshot.Applications.Scorecard' in data:
      model = re.search(
          r"(?<=ReactDOM.hydrate\(React.createElement\(Golfshot.Applications.Scorecard, )(.*)(?=\), document.getElementById)", data).group()
      self.results = json.loads(model)


class CourseParser(HTMLParser):
  def handle_data(self, data):
    if 'Golfshot.Applications.CourseScorecard' in data:
      model = re.search(
          r'(?<=ReactDOM.hydrate\(React.createElement\(Golfshot.Applications.CourseScorecard, )(.*)(?=\), document.getElementById)', data).group()
      self.results = json.loads(model)


def download_course(session, course_id):
  COURSE_URL = f'{GOLFSHOT_URL}/courses/{course_id}'

  res = session.get(COURSE_URL)
  p = CourseParser()
  p.feed(res.text)

  course_uuid = p.results['source'].split('/')[-2]
  scorecard = session.get(p.results['source']).json()[
      'scorecard']  # remove unused siblings

  if not COURSES_DIRECTORY.exists():
      Path(COURSES_DIRECTORY).mkdir(parents=True)
  with open(COURSES_DIRECTORY.joinpath(f'{course_id}.json'), 'w') as f:
    ret = {'courseId': course_id,
           'courseUuid': course_uuid,
           'scorecard': scorecard}
    json.dump(ret, f)

dfs = []
def download_round(session, profile_id, round_id):
  ROUND_URL = f'{GOLFSHOT_URL}/profiles/{profile_id}/rounds/{round_id}'

  res = session.get(ROUND_URL)
  p = RoundParser()
  p.feed(res.text)
  dfs. append(pd.read_html(res.content, index_col=0))

  if not ROUNDS_DIRECTORY.exists():
      Path(ROUNDS_DIRECTORY).mkdir(parents=True)
  round_id = p.results['roundGroupId']
  round_date = p.results['model']['detail']['startTime'].split('T')[0]
  with open(ROUNDS_DIRECTORY.joinpath(f"{round_date}_{round_id}.json"), 'w') as f:
#   with open(f"data/rounds/{round_date}_{round_id}.json", 'w') as f:
    json.dump(p.results, f)

  download_course(session, p.results['model']['detail']['golfCourseWebId'])


def download_rounds(session, profile_id, last_round=None):
  ROUNDS_URL = f'{GOLFSHOT_URL}/profiles/{profile_id}/rounds'
  params = {'sb': 'Date', 'sd': 'Descending', 'p': 1}

  download_rounds = True
  while download_rounds:
    rounds_html = session.get(ROUNDS_URL, data=params).text
    soup = BeautifulSoup(rounds_html, 'html.parser')
    round_table = soup.find('table', {'class': 'search-results'})

    if not round_table:
      download_rounds = False
      break

    for row in round_table.tbody.findAll('tr'):
      round_id = row.attrs['data-href'].split('/')[-1]
      if round_id == last_round:
        download_rounds = False
        break
      print(f'Downloading {round_id}...')
      download_round(session, profile_id, round_id)

    params['p'] += 1

@click.command()
@click.option('--username', '-u', help='Username for GolfShot account')
@click.option('--password_', '-p', help='Password for GolfShot account')
@click.option('--profile_id', '-i', help='Profile ID for GolfShot account')
@click.option('--until_', is_flag=True, help='Download rounds until specified round (by descending date)')
def scrape_rounds(username, password_, profile_id, until_):

    login = username if username else USER_NAME
    password = password_ if password_ else PASSWORD
    golfshot_id = profile_id if profile_id else USER_ID
    until = until_ if until_ else USER_UNTIL

    with requests.Session() as session:
        tokenRequest = session.get(f'{GOLFSHOT_URL}/signin')
        parser = etree.HTMLParser()
        tree = etree.fromstring(tokenRequest.text, parser)
        verificationToken = tree.xpath(
            '//form//input[@name="__RequestVerificationToken"]/@value')[0]
        signin = session.post(f'{GOLFSHOT_URL}/signin',
                                data={'Email': login,
                                    'Password': password,
                                    '__RequestVerificationToken': verificationToken,
                                    })

        download_rounds(session, golfshot_id, until)

if __name__ == '__main__':
    scrape_rounds()
