import os
from dotenv import load_dotenv

from turtle import pd

import pandas as pd
from pandas import DataFrame
import psycopg2


class DatabaseManager:
    """Manages cloud PostgreSQL schema setup, data insertion, and querying."""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes connection to the cloud database."""
        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Initializes raw schema for employees and departments."""
        create_query = """
        DROP TABLE IF EXISTS employees CASCADE;
        DROP TABLE IF EXISTS departments CASCADE;

        CREATE TABLE departments (
            dept_id INT PRIMARY KEY,
            dept_name VARCHAR(100) NOT NULL,
            location VARCHAR(100) NOT NULL,
            budget INT NOT NULL
        );

        CREATE TABLE employees (
            employee_id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(100) NOT NULL,
            start_date DATE NOT NULL,
            salary INT NOT NULL,
            dept_id INT REFERENCES departments(dept_id)
        );
        """
        self.cursor.execute(create_query)
        self.conn.commit()

    def insert_departments(self, department_records: list):
        """Populates the departments table."""
        insert_query = """
        INSERT INTO departments (dept_id, dept_name, location, budget)
        VALUES (%s, %s, %s, %s);
        """
        self.cursor.executemany(insert_query, department_records)
        self.conn.commit()

    def insert_employees(self, employee_records: list):
        """Populates the employees table."""
        insert_query = """
        INSERT INTO employees (employee_id, name, position, start_date, salary, dept_id)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        self.cursor.executemany(insert_query, employee_records)
        self.conn.commit()

    def load_employees_data(self) -> DataFrame:
        """Queries employee records into a Pandas DataFrame."""
        query = "SELECT * FROM employees ORDER BY employee_id ASC;"
        return pd.read_sql_query(query, self.conn)

    def load_joined_data(self) -> DataFrame:
        """Queries merged employee and department records into a DataFrame."""
        query = """
        SELECT 
            e.employee_id,
            e.name,
            e.position,
            e.start_date,
            e.salary,
            d.dept_name,
            d.location,
            d.budget
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id;
        """
        return pd.read_sql_query(query, self.conn)

    def close(self):
        """Closes active cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()