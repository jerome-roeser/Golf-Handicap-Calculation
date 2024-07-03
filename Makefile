run_main:
	python -m world_handicap_calculator.interface.main

streamlit:
	@streamlit run ui/app.py

reinstall_package:
	@pip uninstall -y world_handicap || :
	@pip install -e .
