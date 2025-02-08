import csv
from config import EMPLOYEES_CSV, DEPARTMENTS_CSV
from .db_manager import DatabaseManager

class DataLoader:
    def __init__(self):
        self.db = DatabaseManager()

    def load_csv_data(self):
        # Load employees
        with open(EMPLOYEES_CSV, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.db.execute_query(
                    '''INSERT INTO employees 
                       (id, first_name, last_name, department, salary, hire_date, is_manager)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (int(row['id']), row['first_name'], row['last_name'], 
                     row['department'], int(row['salary']), row['hire_date'], 
                     row['is_manager'])
                )

        # Load departments
        with open(DEPARTMENTS_CSV, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.db.execute_query(
                    'INSERT INTO departments (id, name, manager) VALUES (?, ?, ?)',
                    (int(row['id']), row['name'], row['manager'])
                )