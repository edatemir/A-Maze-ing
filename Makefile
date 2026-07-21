PYTHON = python
MAIN = a_maze_ing.py
CONFIG = config.txt
OUTPUT = maze.txt

all: run

run:
	$(PYTHON) $(MAIN) $(CONFIG)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete

fclean: clean
	@rm -f $(OUTPUT)

re: fclean all
.PHONY: all run clean fclean re