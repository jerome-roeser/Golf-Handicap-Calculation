default: pytest

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# clean:
# 	@rm -f */version.txt
# 	@rm -f .coverage
# 	@rm -f */.ipynb_checkpoints

run_main:
	python -m golf_handicap_calculation.main

sql_database:
	python -m golf_handicap_calculation.database.make_database

scrape_golfshot:
	python -m golf_handicap_calculation.database.scrape_rounds

streamlit:
	@streamlit run ui/app.py

install:
	poetry install

########## Testing ##########

pytest:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes
