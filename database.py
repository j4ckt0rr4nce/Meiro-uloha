from abc import ABC, abstractmethod
import sqlite3
import json
import datetime
from load_input import ConcreteInputData


class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Database(ABC):
    @abstractmethod
    def db_population(self, file_path: str) -> None:
        """Method to populate database from file"""


class ConcreteDatabase(Database, Singleton):
    def db_population(self, file_path: str) -> None:
        if type(file_path) is not str:
            raise Exception("'file_path' paramater must be 'str'.")
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        records = ConcreteInputData.get_data_from_file(self, file_path)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id INT NOT NULL,
                                    name VARCHAR(50) NOT NULL,
                                    city VARCHAR(50) NOT NULL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ordered_products(
                                    id INT NOT NULL,
                                    name VARCHAR(50) NOT NULL,
                                    price VARCHAR(50) NOT NULL,
                                    user_id INT NOT NULL,
                                    order_id INT NOT NULL,
                                    FOREIGN KEY(user_id) REFERENCES users(id),
                                    FOREIGN KEY(order_id) REFERENCES orders(id))""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS orders(
                                    id INT NOT NULL,
                                    created DATETIME NOT NULL, 
                                    user_id INT NOT NULL,
                                    FOREIGN KEY(user_id) REFERENCES users(id))""")

        for r in records:
            date = datetime.datetime.now()-datetime.timedelta(seconds=r.get('created'))
            self.cur.execute("""INSERT INTO users(
                                    id,
                                    name,
                                    city
                            ) VALUES(?, ?, ?);""", (r.get('user')['id'], r.get('user')['name'], r.get('user')['city']))
            self.cur.execute("""INSERT INTO orders(
                                    id,
                                    created,
                                    user_id
                            ) VALUES(?, ?, ?);""", (r.get('id'), date.date(), r.get('user')['id']))
            for p in r.get('products'):
                self.cur.execute("""INSERT INTO ordered_products(
                                    id,
                                    name,
                                    price,
                                    user_id,
                                    order_id
                            ) VALUES(?, ?, ?, ?, ?);""", (p['id'], p['name'], p['price'], r.get('user')['id'], r.get('id')))
        self.conn.commit()
        self.conn.close()