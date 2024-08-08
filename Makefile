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
	python -m src.golf_handicap_calculation.main

sql_database:
	python -m src.database.make_database

scrape_golfshot:
	python -m src.database.scrape_rounds

streamlit:
	@streamlit run ui/app.py

reinstall_package:
	@pip uninstall -y whs-calculator || :
	@pip install -e .

########## Testing ##########

pytest:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes
