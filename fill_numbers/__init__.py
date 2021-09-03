# вызов обработок таблицы
#??? вопрос НУЖЕН-ЛИ ???
from fill_numbers.client import Client

# обработка таблицы локальными методами
from fill_numbers.local_handler import Local

# обработка таблицы методами баз даных
from fill_numbers.dbase_handler import DBase

# обработчик задачи
from fill_numbers.service import Service
