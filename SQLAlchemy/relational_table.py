from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, select
import sqlite3
from dotenv import load_dotenv
import os

# Load secret
load_dotenv("secrets.env")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Show SQLite version (for fun)
print("SQLite3 Version:", sqlite3.sqlite_version)

# Create engine
engine = create_engine(
    f'postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/sqltutorial',
    echo=False
)

# Define schema
meta = MetaData()

people = Table(
    "people", meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('age', Integer)
)

things = Table(
    "things", meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id'))
)

# Create tables if not exist
meta.create_all(engine)

# Connect
conn = engine.connect()

# Clear old data
conn.execute(things.delete())
conn.execute(people.delete())
conn.commit()

# Insert people
people_data = [
    {'name': 'Gurt', 'age': 30},
    {'name': 'Kyle', 'age': 18},
    {'name': 'Daniel', 'age': 35},
    {'name': 'Steve', 'age': 30},
    {'name': 'Carl', 'age': 42}
]
conn.execute(people.insert(), people_data)
conn.commit()

# Get actual IDs
rows = conn.execute(select(people)).fetchall()
name_to_id = {row.name: row.id for row in rows}

things_data = [
    {'owner': name_to_id['Gurt'], 'description': 'Laptop', 'value': 1000.00},
    {'owner': name_to_id['Kyle'], 'description': 'Mouse', 'value': 10.00},
    {'owner': name_to_id['Daniel'], 'description': 'Speaker', 'value': 100.00},
    {'owner': name_to_id['Steve'], 'description': 'Banana', 'value': 0.80},
    {'owner': name_to_id['Carl'], 'description': 'Iphone', 'value': 800.00}
]
conn.execute(things.insert(), things_data)
conn.commit()

# View output
print("\nPeople:")
for row in conn.execute(select(people)).fetchall():
    print(row)

print("\nThings:")
for row in conn.execute(select(things)).fetchall():
    print(row)

conn.execute(things.delete())
conn.execute(people.delete())
conn.commit()

# View output
print()
print("People:")
for row in conn.execute(select(people)).fetchall():
    print(row)

print()
print("Things:")
for row in conn.execute(select(things)).fetchall():
    print(row)

