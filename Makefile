default: pytest

run_main:
	python -m world_handicap_calculator.main.main

sql_database:
	python -m world_handicap_calculator.database.make_database

scrape_golfshot:
	python -m world_handicap_calculator.database.scrape_rounds

streamlit:
	@streamlit run ui/app.py

reinstall_package:
	@pip uninstall -y world_handicap || :
	@pip install -e .

########## Testing ##########

pytest:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes
