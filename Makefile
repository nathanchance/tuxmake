.PHONY: test

test:
	python3 -m pytest --cov=tuxmake
	black --check --diff .
	flake8 .
