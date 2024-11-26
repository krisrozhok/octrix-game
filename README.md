# Octrix Game

Это реализация классической игры Octrix на Python. Игра основана на оригинальной версии из BASIC, но адаптирована для современных систем.

## Описание игры

Octrix - это карточная игра, где каждому игроку раздается по 8 карт (от туза до восьмерки). Карты ранжируются по мастям бриджа, где туз треф является самой низкой картой, а восьмерка пик - самой высокой. Цель игры - выиграть как можно больше взяток из восьми возможных.

## Особенности

* Поддержка от 1 до 4 игроков
* Возможность игры против компьютера
* Система подсчета очков с бонусами за последовательные выигрыши
* Точное воспроизведение механики оригинальной игры

## Требования

* Python 3.x

## Установка и запуск

### Windows

1. Убедитесь, что у вас установлен Python 3.x
    ```bash
    python --version
    ```

2. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/krisrozhok/octrix-game.git
    cd octrix-game
    ```

3. Запустите игру одним из способов:
    * Через Python напрямую:
        ```bash
        python main.py
        ```
    * Через make (если установлен):
        ```bash
        make run
        ```

## Как играть

1. При запуске игры вам будет предложено ознакомиться с правилами (ответьте Y на вопрос "TEACH GAME?")
2. Укажите количество игроков (1-4)
3. Введите имена игроков
4. Решите, будет ли компьютер участвовать в игре
5. Установите количество очков для победы (по умолчанию 88)

### Формат ввода карт

* Используйте двухсимвольный формат: значение + масть
* Значения: A (туз), 2-8
* Масти: C (трефы), D (бубны), H (червы), S (пики)
* Пример: "AC" для туза треф, "8S" для восьмерки пик
* Введите 'P' чтобы посмотреть свои карты

## Очистка временных файлов

Для очистки кэша и временных файлов Python:
```bash
make clean
```


## Автор

krisrozhok
