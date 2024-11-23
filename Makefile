# Makefile для сборки проекта Octrix

PYTHON = python3
SRC = src/main.py

run:
	$(PYTHON) $(SRC)

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
