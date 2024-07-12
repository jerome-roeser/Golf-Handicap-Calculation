run_main:
	python -m world_handicap_calculator.interface.main

database:
	python -m world_handicap_calculator.database.make_database

scrape:
	python -m world_handicap_calculator.database.scrape_rounds

streamlit:
	@streamlit run ui/app.py

reinstall_package:
	@pip uninstall -y world_handicap || :
	@pip install -e .
