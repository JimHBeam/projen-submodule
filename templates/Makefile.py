def Makefile(options):
    return """
.PHONY: clean lint checktypes checkstyle fixstyle test test-all

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {{}} +
	find . -name '*.egg' -exec rm -f {{}} +
	find . -name '*.pyc' -exec rm -f {{}} +
	find . -name '*.pyo' -exec rm -f {{}} +
	find . -name '*~' -exec rm -f {{}} +
	find . -name '__pycache__' -exec rm -fr {{}} +
	rm -fr .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .venv/

lint: checktypes checkstyle ## run all checks

liccheck:
	poetry export -f requirements.txt -o requirements.txt
	poetry run liccheck || true
	rm -f requirements.txt

checktypes: .venv ## check types with mypy
	poetry run mypy --ignore-missing-imports {name} tests

checkstyle: .venv ## check style with flake8, black and isort
	poetry run flake8 {name}
	poetry run isort --check-only --profile black {name} tests
	poetry run black -l 99 --check --diff {name} tests

fixstyle: .venv ## fix black and isort style violations
	poetry run isort --profile black {name} tests
	poetry run black -l 99 {name} tests

test: .venv ## quick run of unit tests
	poetry run pytest --verbose --capture=no --cov={name} --cov-fail-under={coverage}
	
test-all: lint test

.venv: poetry.lock
	poetry install
	@touch -c .venv

poetry.lock:
	poetry lock -vvv
	@touch -c poetry.lock

-include Makefile_aux
-include Makefile_override
  """.format(
        name=options["name"].replace("-", "_"),
        coverage=options.get("coverage", 25)
    )
