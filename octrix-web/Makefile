VENV = %USERPROFILE%\octrix-venv
BIN = $(VENV)\Scripts
PYTHON = $(BIN)\python
PIP = $(BIN)\pip

.PHONY: install run

install:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	cd src && $(BIN)\waitress-serve --port=5000 app:app
