import random
import datetime

from faker import Faker
import numpy as np


class DataGenerator:
    """Generates synthetic domain records for employees and departments."""
    
    def __init__(self, seed: int = 42):
        self.fake = Faker()
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)
        
        self.positions_dept_map = {
            "Software Engineer": 101,
            "DevOps Engineer": 101,
            "Data Analyst": 102,
            "Data Engineer": 102,
            "Cloud Architect": 103,
            "Systems Administrator": 103,
            "Database Administrator": 103,
            "Cybersecurity Analyst": 104
        }

    def generate_departments(self) -> list:
        """Returns predefined organizational department tuples."""
        return [
            (101, "Engineering", "New York", 2500000),
            (102, "Data & AI", "San Francisco", 1800000),
            (103, "Cloud & Infrastructure", "Austin", 2000000),
            (104, "Cybersecurity", "Washington D.C.", 1500000)
        ]

    def generate_employees(self, count: int = 60) -> list:
        """Generates synthetic employee records with matching department foreign keys."""
        employees = []
        positions = list(self.positions_dept_map.keys())
        
        for emp_id in range(1, count + 1):
            name = self.fake.name()
            position = random.choice(positions)
            start_date = self.fake.date_between(
                start_date=datetime.date(2015, 1, 1),
                end_date=datetime.date(2024, 12, 31)
            )
            salary = random.randint(60000, 200000)
            dept_id = self.positions_dept_map[position]
            
            employees.append((emp_id, name, position, start_date, salary, dept_id))
            
        return employees