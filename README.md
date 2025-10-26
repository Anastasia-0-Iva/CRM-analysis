# Проект — CRM_analysis

CRM_analysis — это проект, который представляет собой обобщение информации о существующих базовых алгоритмах и абстрактных
структур данных с их реализацией на Python.
В коде используются библиотеки: `collections`, `random`.

# Дополнительная информация

- Пакет `algorithms` содержит следующие базовые алгоритмы с реализацией: </br>
  - `Breadth First Search` или `Поиск в ширину`; </br>
  - `Depth First Search` или `Поиск в глубину`; </br>
  - `Dijkstra algorithms` или `Алгоритм дейкстры`; </br>
  - Поисковые алгоритмы: </br>
    - `binary search` или `бинарный поиск`; </br>
  - Алгоритмы сортировки: </br>
    - `Merge sort` или `сортировка слиянием`; </br>
    - `Bubble sort` или `пузырьковая сортировка`; </br>
    - `Quick sort` или `быстрая сортировка`. </br>
- Пакет `data_structures` содержит следующие абстрактные структуры данных с реализацией: </br>
  - `Binary tree` или `Бинарное дерево`; </br>
  - `Graph` или `Граф`; </br>
  - `Linked List` или `Односвязный список`; </br>
  - `Queue` или `Очередь`; </br>
  - `Stack_first` или `Стек через список`; </br>
  - `Stack_second` или `Стек через односвязный список`; </br>
- Пакет `parallel_programming` содержит материалы по параллельному программированию: </br>
  - `asynchronous.py` - пример асинхронного программирования с использованием asyncio / aiohttp; </br>
  - `multithreading_example.py` - пример использования многопоточной обработки; </br>
  - `multiprocessing_example.py` - пример использования многопроцессорной обработки; </br>
  - `token_bucket.py` - применение дросселирования; </br>


# Клонирование репозитория

Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/learning_materials.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/learning_materials.git
cd learning_materials
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
```