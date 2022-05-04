from abc import ABC, abstractmethod
import sqlite3
import json
from typing import List
from database import ConcreteDatabase
from users import ConcreteUsers
from orders import ConcreteOrders, TimeRange


class OrdersService(ABC):
    @abstractmethod
    def db_population_from_file(self, file_path: str) -> None:
        """Method to populate database from file"""

    @abstractmethod
    def get_orders_by_date(self, timerange: List[str]) -> str:
        """Method to get orders by timerange"""

    @abstractmethod
    def get_users_by_products(self, user_num: int) -> str:
        """Method to get number of users by highest amount of ordered products"""


class ConcreteOrdersService(OrdersService):
    def db_population_from_file(self, file_path: str) -> None:
        ConcreteDatabase.db_population(self, file_path)


    def get_orders_by_date(self, timerange: List[str]) -> str:
        ConcreteOrders.orders_query(self, timerange)
                

    def get_users_by_products(self, user_num: int) -> str:
       ConcreteUsers.users_query(self, user_num)


def client_code(factory: ConcreteOrdersService) -> None:
    factory.db_population_from_file(file_path)
    #factory.get_orders_by_date(t.set_date('1973-07-08','1973-07-09'))
    #factory.get_users_by_products(4)


if __name__ == "__main__":
    t = TimeRange()
    file_path = 'data.ndjson'
    client_code(ConcreteOrdersService())