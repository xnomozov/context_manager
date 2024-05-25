import time
from typing import List
import psycopg2
from contextlib import contextmanager


# 1st - Way. by classgit 
class Timer:
    def __init__(self, n: int) -> None:
        self.n = n
        self.number_list: List[int] = []

    def __enter__(self) -> 'Timer':
        self.time_start: float = time.perf_counter()
        return self

    def __exit__(self, type, value, traceback) -> None:
        for number in range(self.n):
            number *= number
            self.number_list.append(number)
        time_end: float = time.perf_counter()
        spend_time: float = time_end - self.time_start
        print(f'Time spent in context manager: {spend_time} seconds')


with Timer(1000000) as timer:
    pass


# ---------------------------------------------------------------------------------------------------------------------

# 2nd Way with decorators


@contextmanager
def timer(n: int) -> None:
    """Calculates elapsed time"""
    t_start: float = time.perf_counter()
    yield
    my_list: List[int] = [number ** 2 for number in range(n)]
    t_end: float = time.perf_counter()
    print(f'Time taken: {t_end - t_start}')


with timer(1000) as t:
    pass


# =====================================================================================================================


# Database context manager
db = {'port': 5432,
      'host': 'localhost',
      'user': 'postgres',
      'password': 2508,
      'database': 'postgres'
      }


class DatabaseContextManager:
    def __enter__(self):
        self.conn = psycopg2.connect(**db)
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT  * FROM service""")
        print(self.cur.fetchall())
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cur.execute("UPDATE service SET name = %s WHERE id = %s", ('Najot Ta\'lim', 1))
            self.conn.commit()
            self.cur.execute("SELECT * FROM service")
            print(self.cur.fetchall())
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
        finally:
            self.cur.close()
            self.conn.close()


with DatabaseContextManager() as conn:
    pass  # We can add any additional database operations here

# =====================================================================================================================
