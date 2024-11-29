.PHONY: run clean

# Запуск игры
run:
	python src/main.py

# Очистка кэша Python и временных файлов
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

# Установка зависимостей
install:
	pip install -r requirements.txt
