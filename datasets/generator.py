import os
import csv
import random
import string

from datetime import date
from operator import attrgetter
from typing import Iterable, Dict

from .models import SchemaColumn, Dataset


class CsvGenerator:
    NAMES = ['Oliver', 'George', 'Noah', 'Arthur', 'Harry', 'Leo', 'Muhammad', 'Jack', 'Charlie', 'Oscar',
             'Olivia', 'Amelia', 'Isla', 'Ava', 'Mia', 'Isabella', 'Sophia', 'Grace', 'Lily', 'Freya']
    SURNAMES = ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Robinson', 'Wright',
                'Thompson', 'Evans', 'Walker', 'White', 'Roberts', 'Green', 'Hall', 'Wood', 'Jackson', 'Clark']
    JOBS = ['Dentist', 'Registered Nurse', 'Pharmacist', 'Computer Systems Analyst', 'Physician',
            'Database Administrator', 'Software Developer', 'Physical Therapist', 'Web Developer', 'Dental Hygienist',
            'Occupational Therapist', 'Veterinarian', 'Computer Programmer', 'School Psychologist',
            'Physical Therapist Assistant', 'Interpreter & Translator', 'Mechanical Engineer',
            'Veterinary Technologist & Technician', 'Epidemiologist', 'IT Manager']
    DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'hotmail.co.uk']

    def __init__(self, columns: Iterable[SchemaColumn]):
        self._columns = sorted(columns, key=attrgetter('order'))

    @classmethod
    def _generate_column_value(cls, col: SchemaColumn) -> str:
        if col.data_type == SchemaColumn.FULL_NAME:
            return random.choice(cls.NAMES) + ' ' + random.choice(cls.SURNAMES)
        if col.data_type == SchemaColumn.JOB:
            return random.choice(cls.JOBS)
        if col.data_type == SchemaColumn.EMAIL:
            name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 10)))
            domain = random.choice(cls.DOMAINS)
            return f"{name}@{domain}"
        if col.data_type == SchemaColumn.PHONE_NUMBER:
            return str(random.randint(1, 100000000)).zfill(8)
        if col.data_type == SchemaColumn.DATE:
            return date.today().isoformat()

        return ''

    def _generate_row(self) -> Dict[str, str]:
        row = {}
        for col in self._columns:
            row[col.name] = self._generate_column_value(col)

        return row

    def generate(self, dataset: Dataset):
        path = os.path.join(dataset.TEMP_DIRECTORY, f"dataset_{dataset.id}.csv")
        with open(path, 'w') as file:
            csv_writer = csv.DictWriter(file, delimiter=dataset.delimiter, quotechar=dataset.quote_char,
                                        fieldnames=[c.name for c in self._columns])
            csv_writer.writeheader()

            for _ in range(dataset.count):
                csv_writer.writerow(self._generate_row())
        return path
