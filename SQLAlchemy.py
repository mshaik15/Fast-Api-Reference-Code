from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
import sqlite3

print(sqlite3.sqlite_version) # Cheeck if SQLite is in project

# An engine is used to connect to a database
engine = create_engine("sqlite:///mydatabase.db", echo=True) # Connection script AKA database URL

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

