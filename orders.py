from abc import ABC, abstractmethod
from typing import List
import sqlite3
import datetime


class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class TimeRange:
    def __init__(self):
        self.range_list = []
        
    def set_date(self, start: str, end: str) -> List[str]:
        if start >= end:
            raise Exception("First argument must be bigger than second argument")
        try:
            datetime.datetime.strptime(start, '%Y-%m-%d')
            datetime.datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD string")
        self.range_list = self.range_list + [start, end]
        return self.range_list


class Orders(ABC):
    @abstractmethod
    def orders_query(self) -> None:
        """Method to run concrete orders query from database"""


class ConcreteOrders(Orders, Singleton):
    def orders_query(self, timerange: List[str]) -> str:
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("SELECT * FROM orders WHERE created BETWEEN (?) AND (?) ORDER BY created", (timerange[0], timerange[1]))
            records = self.cur.fetchall()
            for r in records:
                print(f" id: {r[0]} \n created: {r[1]} \n user_id: {r[2]} \n")
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
        finally:
            if self.conn:
                self.conn.close()