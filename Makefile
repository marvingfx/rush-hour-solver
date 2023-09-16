MAIN_DIR=src
TEST_DIR=tests

install:
	poetry install

update:
	poetry self update && \
	poetry update && \
	poetry up --latest
	
check_black:
	poetry run black --diff $(MAIN_DIR)
	
check_ruff:
	poetry run ruff --diff $(MAIN_DIR)

check_mypy:
	poetry run mypy $(MAIN_DIR)

check_deptry:
	poetry run deptry $(MAIN_DIR)

check: check_black check_ruff check_mypy check_deptry

fix_black:
	poetry run black $(MAIN_DIR)

fix_ruff:
	poetry run ruff --fix --show-source --show-fixes $(MAIN_DIR)

fix: fix_black fix_ruff
	
test:
	poetry run pytest -vv $(TEST_DIR) --cov $(MAIN_DIR)