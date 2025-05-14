# Showing simple statments for single tables
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, ForeignKey
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv("secrets.env")

print("SQLite3 Version")
print(sqlite3.sqlite_version) # Cheeck if SQLite is in project

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# An engine is used to connect to a database
# SQLite3
# engine = create_engine("sqlite:///mydatabase.db", echo=True) # Connection script AKA database URL

# Postgres - I already created the database inside of psql
engine = create_engine(
    f'postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/sqltutorial',
    echo=False
)

"""
Connections just send raw SQL to the database, it doesnt track python objects
Sessions
    - Utilized with ORM, lets you work with Python classes mapped into tables 
    - Tracks objects  and stores SQL quries in python classes
"""

meta = MetaData() 
    # Container object definined by SQLAlchemy that holds the blueprint registry for database schema
    # Lets us define multiple tables in one place
    # Required for create_all() and drop_all()

people = Table(
    "people", # Name of table
    meta, # Meta data
    Column('id', Integer, primary_key=True), # Column in table
    Column('name', String, nullable=False),
    Column('age', Integer),
)
meta.create_all(engine) # Create this table in our connected database

# Working with tables
conn = engine.connect()


# Insert data
insert_statement = people.insert().values(name='Mike', age=30)
result = conn.execute(insert_statement)

insert2_statement = people.insert().values(name='Jane', age=26)
result = conn.execute(insert2_statement)
conn.commit()  # IMPORTANT for Postgres (not needed for SQLite)

# Find/ Select Data
def select():
   select_statement = people.select().where(people.c.age >= 20)
   result = conn.execute(select_statement)

   for row in result.fetchall():
       print(row)

# Update Data
update_statement = people.update().where(people.c.name == 'Mike').values(age=50)
result = conn.execute(update_statement)
conn.commit()
select()

# Delete Data

# <table_name>.delete() <--- Delete all rows in <table_name>
# <table_name>.delete().where(<table)

delete_statment = people.delete()
result = conn.execute(delete_statment)
conn.commit()
select()




