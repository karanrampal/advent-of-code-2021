VENV := ./.venv

install: requirements.txt
	python -m venv $(VENV)
	source $(VENV)/Scripts/activate
	$(VENV)/Scripts/pip install --upgrade pip
	$(VENV)/Scripts/pip install -r requirements.txt

lint:
	pylint --disable=R -j 6 ./day*/*.py

format:
	black ./day*/
	isort ./day*/
	# Run mypy from each subdirectory, i don't know how to use it from parent

clean:
	rm -rf *.log .coverage .mypy_cache\
	 ./day*/*.log ./day*/.mypy_cache ./day*/__pycache__

.PHONY: lint format clean