from abc import ABC, abstractmethod
import sqlite3


class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Products(ABC):
    @abstractmethod
    def products_query(self):
        """Method to run concrete products query from database"""

class ConcreteProducts(Products, Singleton):
    def products_query(self):
        pass