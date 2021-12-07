VENV := ./.venv

install: requirements.txt
	python3 -m venv  $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements/requirements.txt

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