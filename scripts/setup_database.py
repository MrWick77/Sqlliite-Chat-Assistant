import sqlite3
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import DB_PATH, DATA_DIR, EMPLOYEES_CSV, DEPARTMENTS_CSV

class DatabaseSetup:
    def __init__(self):
        self.db_path = DB_PATH
        self.data_dir = DATA_DIR
        self.employees_csv = EMPLOYEES_CSV
        self.departments_csv = DEPARTMENTS_CSV

    def generate_sample_data(self):
        """Generate sample data for departments and employees"""
        
        departments = [
            "Sales", "Engineering", "Marketing", "Human Resources", 
            "Finance", "Operations", "Customer Support", "Research", 
            "Legal", "Product Management"
        ]

        first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", 
            "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", 
            "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", 
            "Charles", "Margaret", "Christopher", "Lisa", "Daniel", "Nancy"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", 
            "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", 
            "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor"
        ]

        self.data_dir.mkdir(parents=True, exist_ok=True)

        department_data = []
        managers = []
        for i, dept in enumerate(departments, 1):
            manager_first = random.choice(first_names)
            manager_last = random.choice(last_names)
            manager_full = f"{manager_first} {manager_last}"
            managers.append((manager_first, manager_last, dept))
            department_data.append([i, dept, manager_full])

        with open(self.departments_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'manager'])
            writer.writerows(department_data)

        employee_data = []
        employee_id = 1

        for first_name, last_name, dept in managers:
            salary = random.randint(90000, 150000)  # Higher salary for managers
            start_date = datetime(2019, 1, 1) + timedelta(days=random.randint(0, 365*3))
            employee_data.append([
                employee_id,
                first_name,
                last_name,
                dept,
                salary,
                start_date.strftime('%Y-%m-%d'),
                'Yes'  # is_manager
            ])
            employee_id += 1

        for dept in departments:
            num_employees = random.randint(5, 15)  # Random number of employees per department
            base_salary = {
                "Sales": (50000, 80000),
                "Engineering": (70000, 120000),
                "Marketing": (45000, 90000),
                "Human Resources": (45000, 85000),
                "Finance": (55000, 100000),
                "Operations": (40000, 80000),
                "Customer Support": (35000, 70000),
                "Research": (60000, 110000),
                "Legal": (65000, 120000),
                "Product Management": (60000, 110000)
            }

            for _ in range(num_employees):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                salary = random.randint(*base_salary[dept])
                start_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 365*3))
                
                employee_data.append([
                    employee_id,
                    first_name,
                    last_name,
                    dept,
                    salary,
                    start_date.strftime('%Y-%m-%d'),
                    'No'  # is_manager
                ])
                employee_id += 1

        with open(self.employees_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'first_name', 'last_name', 'department', 'salary', 'hire_date', 'is_manager'])
            writer.writerows(employee_data)

        return len(employee_data), len(department_data)

    def create_database(self):
        """Create the SQLite database and tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            hire_date DATE NOT NULL,
            is_manager TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manager TEXT NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    def load_data_to_database(self):
        """Load data from CSV files into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM employees")
        cursor.execute("DELETE FROM departments")

        # Load employees data
        with open(self.employees_csv, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                INSERT INTO employees (id, first_name, last_name, department, salary, hire_date, is_manager)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(row['id']), row['first_name'], row['last_name'], 
                    row['department'], int(row['salary']), row['hire_date'], 
                    row['is_manager']
                ))

        # Load departments data
        with open(self.departments_csv, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                INSERT INTO departments (id, name, manager)
                VALUES (?, ?, ?)
                ''', (int(row['id']), row['name'], row['manager']))

        conn.commit()
        conn.close()

    def verify_setup(self):
        """Verify that the database was set up correctly"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM employees")
        employee_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM departments")
        department_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT department) FROM employees")
        unique_departments = cursor.fetchone()[0]

        conn.close()

        return {
            'employees': employee_count,
            'departments': department_count,
            'unique_departments': unique_departments
        }

def main():
    print("Starting database setup...")
    
    setup = DatabaseSetup()
    
    print("Generating sample data...")
    num_employees, num_departments = setup.generate_sample_data()
    print(f"Generated {num_employees} employees and {num_departments} departments")
    
    print("\nCreating database tables...")
    setup.create_database()
    print("Database tables created successfully")
    
    print("\nLoading data into database...")
    setup.load_data_to_database()
    print("Data loaded successfully")
    
    print("\nVerifying setup...")
    stats = setup.verify_setup()
    print(f"Database verification complete:")
    print(f"- Total employees: {stats['employees']}")
    print(f"- Total departments: {stats['departments']}")
    print(f"- Unique departments: {stats['unique_departments']}")
    
    print("\nDatabase setup completed successfully!")

if __name__ == "__main__":
    main()