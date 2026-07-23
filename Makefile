PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt
OUTPUT = maze.txt

.PHONY: install run debug clean lint lint-strict fclean re all package

all: run

install:
	pip install flake8 mypy build

package:
	$(PYTHON) -m build
	cp dist/*.whl dist/*.tar.gz .
	@rm -rf build/ dist/ *.egg-info

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@rm -rf build/ dist/ *.egg-info

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .

fclean: clean
	@rm -f $(OUTPUT)

re: fclean all