install:
	poetry install

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl

selfcheck:
	poetry check

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml -vv

lint:
	poetry run flake8 gendiff

check: selfcheck lint

build: check
	poetry build

gendiff:
	poetry run gendiff

.PHONY: install test lint selfcheck check build