import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent

# Data directory
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Database settings
DB_NAME = 'company.db'
DB_PATH = BASE_DIR / DB_NAME

# CSV file paths
EMPLOYEES_CSV = DATA_DIR / 'employees.csv'
DEPARTMENTS_CSV = DATA_DIR / 'departments.csv'