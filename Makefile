.PHONY: test

test:
	python3 -m pytest --cov=tuxmake --cov-report=term-missing
	black --check --diff .
	flake8 .
