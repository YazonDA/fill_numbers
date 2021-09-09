# task`s intrface
from etl_platform.service import Service

# df with settings & hadlers
from etl_platform.client import Client

# обработка таблицы локальными методами
from etl_platform.local_handler import Local

# обработка таблицы методами баз даных
from etl_platform.dbase_handler import DBase

# обработка таблицы методами баз даных
from etl_platform.settings import set_client, set_local, set_dbase