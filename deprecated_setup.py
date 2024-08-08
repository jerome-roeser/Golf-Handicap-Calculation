from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='world_handicap_stats',
      version="0.0.1",
      description="Calculates actual golf handicap from last scorecards",
      license="MIT",
      author="Jerome Roeser",
      author_email="jerome.roeser@gmail.com",
      url="https://github.com/jerome-roeser/Golf-Handicap-Calculation",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
